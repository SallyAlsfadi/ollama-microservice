from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

services = {}

class Service(BaseModel):
    name: str
    address: str


@app.post("/register")
def register_service(service: Service):

    if service.name in services:
        raise HTTPException(status_code=400, detail="Service already registered.")
    
    services[service.name] = service.address
    return {"message": f"Service '{service.name}' registered successfully", "service": service}

@app.post("/heartbeat")
def heartbeat(name: str):
    if name in services:
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
