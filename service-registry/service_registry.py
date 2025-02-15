from flask import Flask, request, jsonify

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

    print(f" {service_name} registered at {service_address}")
    
    return jsonify({"message": f"{service_name} registered successfully"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)  
