import mlrun
import streamlit as st

from pages import home, iris, heart_disease

if __name__ == "__main__":
    st.set_page_config(page_title="MLRun AI Apps", layout="wide")

    page_names_to_funcs = {
        "Home": home,
        "Iris Demo": iris,
        "Heart Disease": heart_disease,
    }
    demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()
