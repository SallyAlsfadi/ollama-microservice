from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)


services = {}


SERVICE_TIMEOUT = 300 


@app.route('/register', methods=['POST'])
def register_service():
  
    data = request.get_json()
    service_name = data.get("name")
    service_address = data.get("address")

    if not service_name or not service_address:
        return jsonify({"error": "Missing 'name' or 'address'"}), 400

    services[service_name] = {"address": service_address, "last_seen": time.time()}
    return jsonify({"message": f"Service {service_name} registered successfully"})


@app.route('/services', methods=['GET'])
def list_services():
   
    return jsonify(services)


@app.route('/forward/<target_service>', methods=['POST'])
def forward_message(target_service):
 
    if target_service not in services:
        return jsonify({"error": "Service not found"}), 404

    message = request.get_json().get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    
    target_address = services[target_service]["address"]
    return jsonify({"message": f"Forwarding to {target_address}: {message}"})


def cleanup_services():
    
    while True:
        current_time = time.time()
        for service in list(services.keys()):
            if current_time - services[service]["last_seen"] > SERVICE_TIMEOUT:
                del services[service]
        time.sleep(60)  



threading.Thread(target=cleanup_services, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
