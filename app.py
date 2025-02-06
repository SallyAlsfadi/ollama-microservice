from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})  

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

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
    app.run(host="0.0.0.0", port=8080, debug=True)
