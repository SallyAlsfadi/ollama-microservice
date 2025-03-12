from fastapi import FastAPI, HTTPException
import time
import threading
import requests

app = FastAPI()
services = {}

@app.post("/register")
def register_service(name: str, address: str):
    services[name] = {"address": address, "last_heartbeat": time.time()}
    return {"message": f"Service '{name}' registered at {address}"}

@app.post("/heartbeat")
def receive_heartbeat(name: str):
    if name in services:
        services[name]["last_heartbeat"] = time.time()
        return {"message": f"Heartbeat received from {name}"}
    raise HTTPException(status_code=404, detail="Service not registered")

@app.get("/services")
def get_services():
    return [{"name": name, "address": info["address"]} for name, info in services.items()]

@app.post("/forward")
def forward_message(from_service: str, to_service: str, message: str):
    if to_service not in services:
        raise HTTPException(status_code=404, detail="Target service not found")

    target_address = services[to_service]["address"]
    try:
        response = requests.post(f"{target_address}/receive", json={"from": from_service, "message": message})
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": f"Failed to reach {to_service} at {target_address}"}

def cleanup_services():
    while True:
        time.sleep(60)
        current_time = time.time()
        to_remove = [name for name, info in services.items() if current_time - info["last_heartbeat"] > 300]
        for name in to_remove:
            del services[name]
            print(f"Removed '{name}' due to inactivity")

threading.Thread(target=cleanup_services, daemon=True).start()
