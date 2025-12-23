import requests
from config.settings import OPENAPI_URL
import json
import os

def load_spec():
    resp = requests.get(OPENAPI_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    os.makedirs("data", exist_ok=True)
    with open("data/spec.json", "w") as f:
        json.dump(data, f, indent=2)

    return data
