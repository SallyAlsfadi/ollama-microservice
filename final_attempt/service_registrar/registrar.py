from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import time
import threading

app = FastAPI()

services = {}

HEARTBEAT_TIMEOUT = 300  
undelivered_messages = {}

class Service(BaseModel):
    name: str
    address: str

@app.post("/register")
def register_service(service: Service):
    if service.name in services:
        raise HTTPException(status_code=400, detail="Service already registered.")
    
 
    services[service.name] = {"address": service.address, "last_heartbeat": time.time()}
    return {"message": f"Service '{service.name}' registered successfully", "service": service}

@app.post("/heartbeat")
def heartbeat(name: str):
    if name in services:
      
        services[name]["last_heartbeat"] = time.time()
        return {"message": f"Heartbeat received from {name}"}
    
    raise HTTPException(status_code=404, detail="Service not registered")

@app.get("/services")
def get_services():
    return {"services": services}

@app.post("/deregister")
def deregister_service(name: str):
    if name in services:
        del services[name]
        return {"message": f"Service '{name}' deregistered successfully"}
    raise HTTPException(status_code=404, detail="Service not found")

@app.post("/forward")
def forward_message(from_service: str, to_service: str, message: str):
   
    if to_service not in services:
        raise HTTPException(status_code=404, detail="Target service not found")

    target_address = services[to_service]["address"]
    
    try:
        
        response = requests.post(f"{target_address}/receive", json={"from_service": from_service, "message": message})
        response.raise_for_status() 
        return response.json()
    
    except requests.exceptions.RequestException as e:
       
        if to_service not in undelivered_messages:
            undelivered_messages[to_service] = []
        undelivered_messages[to_service].append({"from": from_service, "message": message})
        
        return {"status": "error", "message": f"Message stored temporarily. {str(e)}"}

@app.get("/undelivered")
def get_undelivered_messages(service_name: str):
  
    if service_name in undelivered_messages:
        return {"status": "success", "undelivered_messages": undelivered_messages[service_name]}
    return {"status": "success", "message": "No undelivered messages"}

def cleanup_inactive_services():
    while True:
        time.sleep(60) 
        current_time = time.time()
        inactive_services = [name for name, info in services.items() if current_time - info["last_heartbeat"] > HEARTBEAT_TIMEOUT]
        
     
        for name in inactive_services:
            del services[name]
            print(f"Service '{name}' removed due to inactivity.")


threading.Thread(target=cleanup_inactive_services, daemon=True).start()
