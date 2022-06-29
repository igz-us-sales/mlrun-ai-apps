import mlrun
import streamlit as st
from mlrun.serving.server import GraphServer


@st.experimental_singleton
def get_mock_server(key: str, model_path: str) -> GraphServer:
    """
    Loads and returns MLRun mock server for given model

    :param key:        Name of model
    :param model_path: Path to model

    :returns: Mock server
    """
    # Import model server and add model from S3
    serve = mlrun.import_function("hub://v2_model_server")
    serve.add_model(
        key=key,
        model_path=model_path,
    )

    # Mock server will emulate K8s production deployment
    mock_server = serve.to_mock_server()
    return mock_server
