from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

registered_services = {}  # Stores { "service_name": {"address": "IP:port", "last_seen": timestamp} }

@app.route('/register', methods=['POST'])
def register_service():
    """
    Endpoint for microservices to register themselves.
    """
    data = request.get_json()

    if not data or 'service_name' not in data or 'service_address' not in data:
        return jsonify({"error": "Missing service_name or service_address"}), 400

    service_name = data['service_name']
    service_address = data['service_address']

    registered_services[service_name] = {
        "address": service_address,
        "last_seen": time.time() 
    }

    print(f"✅ {service_name} registered at {service_address}")
    
    return jsonify({"message": f"{service_name} registered successfully"}), 200

@app.route('/heartbeat', methods=['POST'])
def receive_heartbeat():
    """
    Microservices call this every 2 minutes to indicate they are still alive.
    """
    data = request.get_json()
    if not data or 'service_name' not in data:
        return jsonify({"error": "Missing service_name"}), 400

    service_name = data['service_name']
    if service_name in registered_services:
        registered_services[service_name]["last_seen"] = time.time()
        print(f"💓 Heartbeat received from {service_name}")
        return jsonify({"message": f"Heartbeat received from {service_name}"}), 200
    else:
        return jsonify({"error": "Service not registered"}), 404

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

def remove_inactive_services():
    """
    Remove services that haven't sent a heartbeat in 5 minutes.
    """
    while True:
        current_time = time.time()
        to_remove = [name for name, info in registered_services.items() if current_time - info["last_seen"] > 300]

        for service in to_remove:
            print(f"Removing inactive service: {service}")
            del registered_services[service]

        time.sleep(60)


threading.Thread(target=remove_inactive_services, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
