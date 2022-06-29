import requests

# Data from user
data = RECORD

# Development testing
resp = mock_server.test(path="/", body=data)

# Production request
resp = requests.post(url="http://PROD_ENDPOINT", json=data)
