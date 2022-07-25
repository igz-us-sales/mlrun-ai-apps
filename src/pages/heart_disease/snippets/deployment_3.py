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