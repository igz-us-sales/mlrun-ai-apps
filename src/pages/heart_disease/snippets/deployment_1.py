import mlrun
from mlrun.feature_store.steps import MapValues, OneHotEncoder

# Import model server from function marketplace
serve = mlrun.import_function("hub://v2_model_server")
graph = serve.set_topology("flow", engine="async")
