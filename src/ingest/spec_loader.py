import requests
import json
import os

def load_spec(url=None):
    if url is None:
        from config.settings import OPENAPI_URL
        url = OPENAPI_URL
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    os.makedirs("data", exist_ok=True)
    with open("data/spec.json", "w") as f:
        json.dump(data, f, indent=2)

    return data
