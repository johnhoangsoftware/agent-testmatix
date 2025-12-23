from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from src.ingest.spec_parser import parse_endpoints
from src.agent.testcase_gen import generate_testcases
from src.agent.save_csv import save_csv

app = Flask(__name__)

def load_spec(url):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    os.makedirs("data", exist_ok=True)
    with open("data/spec.json", "w") as f:
        json.dump(data, f, indent=2)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_spec', methods=['POST'])
def load_spec_route():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    print(f"[LOG] Loading spec from {url}")
    try:
        spec = load_spec(url)
        endpoints = parse_endpoints(spec)
        endpoint_list = [{'method': ep['method'], 'path': ep['path'], 'params': ep['params']} for ep in endpoints]
        print(f"[LOG] Loaded {len(endpoints)} endpoints")
        return jsonify({'endpoints': endpoint_list})
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_route():
    data = request.json
    selected_indices = data.get('endpoints', [])
    model = data.get('model', 'gemini')
    if not selected_indices:
        return jsonify({'error': 'No endpoints selected'}), 400
    print(f"[LOG] Generating tests for {len(selected_indices)} endpoints using {model}")
    try:
        # Load endpoints from saved spec
        with open("data/spec.json", "r") as f:
            spec = json.load(f)
        all_endpoints = parse_endpoints(spec)
        selected_endpoints = [all_endpoints[int(i)] for i in selected_indices]
        print(f"[LOG] Selected endpoints: {[f'{ep['method']} {ep['path']}' for ep in selected_endpoints]}")
        csv_text = generate_testcases(selected_endpoints, llm=model)
        save_csv(csv_text)
        print("[LOG] Test cases generated and saved")
        return jsonify({'message': 'Test cases generated and saved to data/testcase_matrix.csv', 'csv': csv_text})
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)