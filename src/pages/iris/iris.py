def iris():
    import pathlib

    import streamlit as st
    import yaml
    from PIL import Image
    from .utils import get_mock_server

    #########
    # Setup #
    #########
    # Get config and set constants
    with open("pages/iris/config.yaml") as f:
        config = yaml.safe_load(f)

    IRIS_CLASSES = config["iris_classes"]
    DEPLOYMENT_CODE = pathlib.Path(config["snippets"]["deployment_code"]).read_text()
    DEPLOYMENT_LOGS = pathlib.Path(config["snippets"]["deployment_logs"]).read_text()
    INFERENCING_CODE = pathlib.Path(config["snippets"]["inferencing_code"]).read_text()
    MODEL_PATH = config["model_path"]

    # Initialize mock_server and get model
    mock_server = get_mock_server(key="iris", model_path=MODEL_PATH)
    model = mock_server.test("/v2/models")["models"][0]

    ###########################
    # Interactive application #
    ###########################

    st.title("Iris UI")
    st.write(
        """
        AI application for predicting Iris species. Predictions delivered via a [model server](https://docs.mlrun.org/en/latest/serving/model-serving-get-started.html) with user selected input. Note that the first prediction may take slightly longer than later predictions.
        """
    )

    controls_col, image_col, json_col = st.columns(3)

    # Sliders for prediction
    with controls_col:
        st.subheader("Select Values")
        with st.form(key="iris-input"):
            sepal_length = st.slider(
                label="sepal length",
                min_value=4.0,
                max_value=8.0,
                step=0.1,
                value=5.1,
            )
            sepal_width = st.slider(
                label="sepal width",
                min_value=2.0,
                max_value=4.5,
                step=0.1,
                value=3.5,
            )
            petal_length = st.slider(
                label="petal length",
                min_value=1.0,
                max_value=7.0,
                step=0.1,
                value=1.4,
            )
            petal_width = st.slider(
                label="petal width",
                min_value=0.0,
                max_value=3.0,
                step=0.1,
                value=0.2,
            )
            submit_button = st.form_submit_button(label="Predict")

            if submit_button or "iris_prediction" in st.session_state:
                # Make prediction via mock_server and save in streamlit state
                url = f"/v2/models/{model}/predict"
                data = {
                    "inputs": [[sepal_length, sepal_width, petal_length, petal_width]]
                }
                resp = mock_server.test(path=url, body=data)
                pred = resp["outputs"][0]
                st.session_state.iris_prediction = pred

    # Image of predicted iris
    with image_col:
        st.subheader("Prediction")
        if "iris_prediction" in st.session_state:
            with st.spinner("Predicting..."):
                st.image(
                    image=Image.open(IRIS_CLASSES[pred]["image"]),
                    caption=IRIS_CLASSES[pred]["name"],
                )
        else:
            st.info("Please Make Prediction")

    # Raw JSON from model
    with json_col:
        st.subheader("Raw Model Output")
        if "iris_prediction" in st.session_state:
            with st.spinner("Predicting..."):
                st.json(resp)
        else:
            st.info("Please Make Prediction")

    #####################
    # Behind the scenes #
    #####################

    # Replace inference display placeholder with model and input data
    st.subheader("Behind the Scenes - Inferencing")
    record = f"[{sepal_length}, {sepal_width}, {petal_length}, {petal_width}]"
    inference_display = INFERENCING_CODE.replace("MODEL", model).replace(
        "RECORD", record
    )
    st.code(inference_display, language="python")

    st.subheader("Behind the Scenes - Deployment")
    st.code(DEPLOYMENT_CODE, language="python")
    # st.code(DEPLOYMENT_LOGS, language="bash")
