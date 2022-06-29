import streamlit as st


def home():
    st.title("MLRun AI Apps")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        ### Welcome
        MLRun is an open source framework to orchestrate MLOps
        from the research stage to production-ready AI applications.
        
        Our goal is to showcase different capabilities of the MLRun
        framework and how it can be embedded into ML applications.
        
        ### Get Started
        If you would like get started with MLRun, check out the official
        website [here](https://www.mlrun.org/).

        ### Select a Demo
        To see MLRun in action within the context of an application, select
        one of the demos in the sidebar.
        
        You will find fully functional ML
        applications as well as a __Behind the Scenes__ peek on how the
        app was developed and deployed.
        """
    )
