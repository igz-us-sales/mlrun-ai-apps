def heart_disease():
    import pathlib

    import streamlit as st
    import yaml
    from PIL import Image
    from .utils import get_mock_server, format_selectbox

    #########
    # Setup #
    #########
    # Get config and set constants
    with open("pages/heart_disease/config.yaml") as f:
        config = yaml.safe_load(f)

    HEART_CLASSES = config["heart_classes"]
    RESTECG_CLASSES = config["restecg_classes"]
    DEPLOYMENT_CODE_1 = pathlib.Path(
        config["snippets"]["deployment_code_1"]
    ).read_text()
    DEPLOYMENT_CODE_2 = pathlib.Path(
        config["snippets"]["deployment_code_2"]
    ).read_text()
    DEPLOYMENT_CODE_3 = pathlib.Path(
        config["snippets"]["deployment_code_3"]
    ).read_text()
    DEPLOYMENT_LOGS = pathlib.Path(config["snippets"]["deployment_logs"]).read_text()
    INFERENCING_CODE = pathlib.Path(config["snippets"]["inferencing_code"]).read_text()

    # Initialize mock_server and get model
    mock_server = get_mock_server(key="heart", config=config)
    print("SERVER", mock_server, type(mock_server))

    ###########################
    # Interactive application #
    ###########################

    st.title("Heart Disease Inference Graph")
    st.write(
        """
        AI application for predicting heart disease. Predictions delivered via a [model server](https://docs.mlrun.org/en/latest/serving/model-serving-get-started.html) with user selected input. Note that the first prediction may take slightly longer than later predictions.

        This application utilizes MLRun inference graphs - these allow you to define complex real-time behavior including feature engineering, enrichment, API calls, ML models, and more. The inference graph for this application looks like the following:
        """
    )
    st.image(image=Image.open("pages/heart_disease/img/inference-graph.png"))
    st.write(
        """
        This allows us to perform the required feature engineering for the model to make a prediction. While this graph is relatively simple, you can get as complex as you'd like. See more on advanced inference graphs [here](https://docs.mlrun.org/en/latest/serving/graph-example.html).
        """
    )

    # Display columns
    controls_display, image_display = st.columns([2, 1])
    with controls_display:
        st.subheader("Select Values")

    with image_display:
        st.subheader("Prediction")

    # Sliders for prediction
    with st.form(key="heart-input"):
        controls_col_1, controls_col_2, image_col = st.columns(3)

        with controls_col_1:
            age = st.slider(label="Age", min_value=1, max_value=120, step=1, value=62)
            sex = st.selectbox(
                label="Sex",
                options=["female", "male"],
                format_func=format_selectbox,
                index=0,
            )
            cp = st.selectbox(
                label="Chest Pain",
                options=[
                    "typical_angina",
                    "atypical_angina",
                    "non_anginal_pain",
                    "asymtomatic",
                ],
                format_func=format_selectbox,
                index=0,
            )
            exang = st.selectbox(
                label="Exercise Induced Angina",
                options=[
                    "no",
                    "yes",
                ],
                format_func=format_selectbox,
                index=0,
            )
            fbs = st.selectbox(
                label="Fasting Blood Sugar > 120 mg/dl",
                options=[
                    True,
                    False,
                ],
                index=0,
            )
            slope = st.selectbox(
                label="Slope of Peak Exercise ST Segment",
                options=["flat", "downsloping", "upsloping"],
                format_func=format_selectbox,
                index=0,
            )

            thal = st.selectbox(
                label="Thalassemia (Blood Disorder)",
                options=["reversable_defect", "normal", "fixed_defect"],
                format_func=format_selectbox,
                index=0,
            )

        with controls_col_2:
            trestbps = st.slider(
                label="Resting Blood Pressure (mm/Hg)",
                min_value=90,
                max_value=170,
                step=1,
                value=138,
            )
            chol = st.slider(
                label="Cholesterol (mg/dl)",
                min_value=120,
                max_value=360,
                step=1,
                value=294,
            )
            restecg = st.selectbox(
                label="Resting ECG",
                options=RESTECG_CLASSES.keys(),
                format_func=lambda x: RESTECG_CLASSES[x],
                index=1,
            )
            thalach = st.slider(
                label="Maximum Heart Rate (BPS)",
                min_value=88,
                max_value=202,
                step=1,
                value=106,
            )
            oldpeak = st.slider(
                label="ST Depression Induced by Exercise Relative to Rest",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                value=1.9,
            )
            ca = st.slider(
                label="Number of Major Vessels",
                min_value=0,
                max_value=3,
                step=1,
                value=3,
            )

        submit_button = st.form_submit_button(label="Predict")

        if submit_button or "heart_prediction" in st.session_state:
            # Make prediction via mock_server and save in streamlit state
            resp = mock_server.test(
                path="/",
                body={
                    "age": age,
                    "sex": sex,
                    "cp": cp,
                    "exang": exang,
                    "fbs": fbs,
                    "slope": slope,
                    "thal": thal,
                    "trestbps": trestbps,
                    "chol": chol,
                    "restecg": restecg,
                    "thalach": thalach,
                    "oldpeak": oldpeak,
                    "ca": ca,
                },
            )
            pred = resp["prediction"]["outputs"][0]
            st.session_state.heart_prediction = pred

    # Image of predicted iris
    with image_col:
        if "heart_prediction" in st.session_state:
            with st.spinner("Predicting..."):
                st.image(
                    image=Image.open(HEART_CLASSES[pred]["image"]),
                    caption=HEART_CLASSES[pred]["name"],
                )
                st.json(resp["prediction"])

        else:
            st.info("Please Make Prediction")

    #####################
    # Behind the scenes #
    #####################

    # Replace inference display placeholder with model and input data
    st.subheader("Behind the Scenes - Inferencing")
    record = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "exang": exang,
        "fbs": fbs,
        "slope": slope,
        "thal": thal,
        "trestbps": trestbps,
        "chol": chol,
        "restecg": restecg,
        "thalach": thalach,
        "oldpeak": oldpeak,
        "ca": ca,
    }
    inference_display = INFERENCING_CODE.replace("RECORD", f"{record}")
    st.code(inference_display, language="python")

    st.subheader("Behind the Scenes - Deployment")
    st.code(DEPLOYMENT_CODE_1, language="python")
    with st.expander("Configuration and Helper Functions"):
        st.code(DEPLOYMENT_CODE_2, language="python")
    st.code(DEPLOYMENT_CODE_3, language="python")
    # st.code(DEPLOYMENT_LOGS, language="bash")

    # Raw JSON from model
    st.subheader("Behind the Scenes - Raw Model Output")
    if "heart_prediction" in st.session_state:
        with st.spinner("Predicting..."):
            st.write(
                "Try expanding the JSON output to see what the record looks like at each point in the graph. You can see the original, one hot encoded, formatted, prediction, etc. This shows how the event is transformed in real-time based on the defined inference graph."
            )
            st.json(resp, expanded=False)
    else:
        st.info("Please Make Prediction")
