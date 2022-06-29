import mlrun
from mlrun.feature_store.steps import MapValues, OneHotEncoder

# Import model server from function marketplace
serve = mlrun.import_function('hub://v2_model_server')
graph = serve.set_topology("flow", engine="async")

# Mappings for feature engineering
AGE_MAPPING = {
    "age": {
        "ranges": {
            "toddler": [0, 3],
            "child": [3, 18],
            "adult": [18, 65],
            "elder": [65, 120],
        }
    }
}

ONE_HOT_ENCODER_MAPPING = {
    "age_mapped": ["toddler", "child", "adult", "elder"],
    "sex": ["male", "female"],
    "cp": ["typical_angina", "atypical_angina", "non_anginal_pain", "asymtomatic"],
    "fbs": [False, True],
    "exang": ["no", "yes"],
    "slope": ["downsloping", "upsloping", "flat"],
    "thal": ["normal", "reversable_defect", "fixed_defect"],
}

# Helper function
def format_model_inputs(event):
    return {"inputs": [list(event.values())]}

# Feature engineering
graph.add_step(name="age_mapper", class_name="MapValues", mapping=AGE_MAPPING, with_original_features=True)
graph.add_step(name="one_hot_encoder", class_name="OneHotEncoder", mapping=ONE_HOT_ENCODER_MAPPING, after="$prev")
graph.add_step(name="format_inputs", handler="format_model_inputs", after="$prev")

# Add model
router = graph.add_step(class_name="*", name="router", after="$prev").respond()
router.add_route("heart", class_name="ClassifierModel", model_path="heart_classifier.pkl")

# Deploy to local mock server (Development testing)
mock_server = serve.to_mock_server()

# Deploy to Nuclio serverless function (Production K8s deployment)
addr = serve.deploy()