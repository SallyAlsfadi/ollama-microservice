from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


registered_services = {}

@app.route('/register', methods=['POST'])
def register_service():
    """
    Endpoint for microservices to register themselves.
    They must send JSON: {"service_name": "name", "service_address": "IP:port"}
    """
    data = request.get_json()

    if not data or 'service_name' not in data or 'service_address' not in data:
        return jsonify({"error": "Missing service_name or service_address"}), 400

    service_name = data['service_name']
    service_address = data['service_address']

    registered_services[service_name] = {"address": service_address}

    print(f"✅ {service_name} registered at {service_address}")
    
    return jsonify({"message": f"{service_name} registered successfully"}), 200

@app.route('/services', methods=['GET'])
def list_services():
    """
    Endpoint to list all registered services.
    """
    return jsonify(registered_services), 200

@app.route('/send', methods=['POST'])
def forward_message():
    """
    Endpoint to forward messages from one service to another.
    Expected JSON: {"from_service": "serviceA", "to_service": "serviceB", "message": "Hello"}
    """
    data = request.get_json()

    if not data or 'from_service' not in data or 'to_service' not in data or 'message' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    from_service = data['from_service']
    to_service = data['to_service']
    message = data['message']

    if to_service not in registered_services:
        return jsonify({"error": f"Service '{to_service}' not found"}), 404

    recipient_address = registered_services[to_service]["address"]
    
    try:
     
        response = requests.post(f"http://{recipient_address}/receive", json={
            "from_service": from_service,
            "message": message
        })
        
        return jsonify({"status": "Message forwarded", "response": response.json()}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to deliver message to {to_service}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
