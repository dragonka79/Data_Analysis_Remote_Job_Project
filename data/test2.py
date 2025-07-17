import requests
import json

# Fetch the product list
url = "https://fakestoreapi.com/products"
response = requests.get(url)
data = response.json()

# Preview one product to inspect keys
print(json.dumps(data[0], indent=4))
