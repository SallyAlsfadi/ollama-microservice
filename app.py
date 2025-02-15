from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
import time
import threading 
app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})  

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"
SERVICE_REGISTRY_URL = "http://localhost:5050"  
SERVICE_NAME = "ollama-service"
SERVICE_ADDRESS = "localhost:8080"

def register_service():
    """
    Register this service with the service registry.
    """
    try:
        response = requests.post(f"{SERVICE_REGISTRY_URL}/register", json={
            "service_name": SERVICE_NAME,
            "service_address": SERVICE_ADDRESS
        })
        if response.status_code == 200:
            print(f" {SERVICE_NAME} registered successfully.")
        else:
            print(f"⚠️ Failed to register {SERVICE_NAME}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f" Error registering service: {e}")

def send_heartbeat():
    """
    Send a heartbeat every 2 minutes to inform the registry that the service is alive.
    """
    while True:
        try:
            response = requests.post(f"{SERVICE_REGISTRY_URL}/heartbeat", json={
                "service_name": SERVICE_NAME
            })
            if response.status_code == 200:
                print(f" Heartbeat sent for {SERVICE_NAME}.")
            else:
                print(f"⚠️ Heartbeat failed: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f" Heartbeat error: {e}")

        time.sleep(120) 

@app.route('/ask', methods=['POST'])
def ask_ollama():
    """
    Receives a JSON request with a 'prompt', sends it to Ollama's LLM,
    and returns the response.
    """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    ollama_response = requests.post(OLLAMA_API_URL, json={
        "model": "mistral",
        "prompt": data['prompt'],
        "stream": False
    })

    if ollama_response.status_code == 200:
        result = ollama_response.json()
        return jsonify({"response": result.get("response", "No response received")})
    else:
        return jsonify({"error": "Failed to communicate with Ollama"}), 500


if __name__ == '__main__':
    register_service()
    threading.Thread(target=send_heartbeat, daemon=True).start() 
    app.run(host="0.0.0.0", port=8080, debug=True)
