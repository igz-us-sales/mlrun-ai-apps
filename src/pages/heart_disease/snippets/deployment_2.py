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
