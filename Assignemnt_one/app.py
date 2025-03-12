from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests

app = Flask(__name__)
CORS(app)

# Update the URL to connect directly to the locally installed Ollama LLM
#OLLAMA_API_URL = "http://localhost:11434/api/generate" # only without docker
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate" #with docker
 

@app.route('/ask', methods=['POST'])
def ask_ollama():
    """
    Receives a JSON request with a 'prompt', sends it to Ollama's LLM,
    and returns the response.
    """
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    try:
        ollama_response = requests.post(OLLAMA_API_URL, json={
            "model": "mistral",  # Change this to another model if needed
            "prompt": data['prompt'],
            "stream": False
        }, timeout=50)

        if ollama_response.status_code == 200:
            result = ollama_response.json()
            return jsonify({"response": result.get("response", "No response received")})
        else:
            return jsonify({"error": "Failed to communicate with Ollama"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to Ollama: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
