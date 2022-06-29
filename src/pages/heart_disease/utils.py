import mlrun
import streamlit as st
from mlrun.feature_store.steps import MapValues, OneHotEncoder
from mlrun.serving.server import GraphServer


def format_selectbox(item):
    return " ".join([i.capitalize() for i in item.split("_")])


def format_model_inputs(event):
    return {"inputs": [list(event.values())]}


def save_original(event):
    return {"original": event}


@st.experimental_singleton
def get_mock_server(key: str, config: dict) -> GraphServer:
    """
    Loads and returns MLRun mock server for given model

    :param key:        Name of model
    :param config:     Configuration dictionary from YAML

    :returns: Mock server
    """
    # Import model server and get graph
    serve = mlrun.import_function("hub://v2_model_server")
    graph = serve.set_topology("flow", engine="async")

    graph.add_step(name="save_original", handler="save_original")
    graph.add_step(
        name="age_mapper",
        class_name="MapValues",
        input_path="original",
        result_path="mapped",
        mapping=config["age_mapping"],
        with_original_features=True,
        after="$prev",
    )
    graph.add_step(
        name="one_hot_encoder",
        class_name="OneHotEncoder",
        input_path="mapped",
        result_path="ohe",
        mapping=config["one_hot_encoder_mapping"],
        after="$prev",
    )
    graph.add_step(
        name="format_inputs",
        handler="format_model_inputs",
        input_path="ohe",
        result_path="formatted",
        after="$prev",
    )

    router = graph.add_step(
        class_name="*",
        name="router",
        after="$prev",
        input_path="formatted",
        result_path="prediction",
    ).respond()
    router.add_route(
        "heart", class_name="ClassifierModel", model_path=config["model_path"]
    )

    # Mock server will emulate K8s production deployment
    mock_server = serve.to_mock_server()
    return mock_server
