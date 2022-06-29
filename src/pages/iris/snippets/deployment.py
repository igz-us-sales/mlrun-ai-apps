import mlrun

# Create MLRun project
project = mlrun.get_or_create_project(name="iris-backend", context="./")

# Import model server from function marketplace
serve = mlrun.import_function('hub://v2_model_server')

# Add model to model server
serve.add_model(key="iris", model_path="https://s3.wasabisys.com/iguazio/models/iris/model.pkl")

# Deploy to local mock server (Development testing)
mock_server = serve.to_mock_server()

# Deploy to Nuclio serverless function (Production K8s deployment)
addr = serve.deploy()