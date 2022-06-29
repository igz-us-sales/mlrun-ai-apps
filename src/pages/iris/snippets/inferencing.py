import requests

# Data from user
data = {{"inputs": [RECORD]}}

# Development testing
resp = mock_server.test(path="/v2/models/MODEL/predict", body=data)

# Production request
resp = requests.post(url="http://PROD_ENDPOINT/v2/models/MODEL/predict", json=data)
