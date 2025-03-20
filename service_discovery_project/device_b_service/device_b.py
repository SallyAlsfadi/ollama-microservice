from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Store registered services and undelivered messages
services = {}

class Service(BaseModel):
    name: str
    address: str

# Register device (only needed when Device B connects to the registrar)
@app.post("/register")
def register_service(service: Service):
    if service.name in services:
        raise HTTPException(status_code=400, detail="Service already registered.")
    
    services[service.name] = service.address
    return {"message": f"Service '{service.name}' registered successfully", "service": service}

# Heartbeat for Device B (to ensure it's still active and connected)
@app.post("/heartbeat")
def heartbeat(name: str):
    if name in services:
        return {"message": f"Heartbeat received from {name}"}
    raise HTTPException(status_code=404, detail="Service not registered")

# Forward the message from Device B to another service
@app.post("/forward")
def forward_message(from_service: str, to_service: str, message: str):
    if to_service not in services:
        raise HTTPException(status_code=404, detail="Target service not found")

    target_address = services[to_service]
    
    try:
        # Forward message directly to the target device
        response = requests.post(f"{target_address}/receive", json={"from_service": from_service, "message": message})
        response.raise_for_status()  # If the response is not OK, this will raise an error
        return response.json()  # Return response from target service

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to forward message: {str(e)}"}

# Receive messages (for testing forwarded messages)
@app.post("/receive")
def receive_message(from_service: str, message: str):
    """
    This endpoint is used to receive forwarded messages from other devices.
    """
    print(f"Received message from {from_service}: {message}")
    return {"status": "success", "message": f"Message received from {from_service}: {message}"}