import requests
import time
import socket
import asyncio
import httpx
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SERVICE_REGISTRAR_URL = "http://10.0.0.242:8000"
SERVICE_NAME = "Shubhangi's Microservice"

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store messages in memory
messages = []
active_connections = []

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error detecting local IP: {e}")
        return "127.0.0.1"

DEVICE_B_IP = get_local_ip()
SERVICE_ADDRESS = f"http://{DEVICE_B_IP}:8001"

async def register():
    retries = 5
    while retries > 0:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SERVICE_REGISTRAR_URL}/register",
                    params={"name": SERVICE_NAME, "address": SERVICE_ADDRESS},
                    timeout=10
                )
            if response.status_code == 200:
                print(f"Service registered successfully: {response.json()}")
                break
            else:
                print(f"Failed to register: {response.status_code}")
        except Exception as e:
            print(f"Error registering service: {e}. Retrying...")
            retries -= 1
            time.sleep(5)
    if retries == 0:
        print("Failed to register after multiple attempts.")

async def send_heartbeat():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"{SERVICE_REGISTRAR_URL}/heartbeat", params={"name": SERVICE_NAME}, timeout=10)
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
        await asyncio.sleep(120)

# WebSocket Connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_message(message):
    for connection in active_connections:
        await connection.send_json(message)

# Receive message and broadcast it via WebSocket
@app.post("/receive")
async def receive_message(request: Request):
    data = await request.json()
    messages.append({"from": data["from"], "message": data["message"]})
    await broadcast_message(data)  # Notify clients in real-time
    return {"status": "success", "received": data["message"]}

# Fetch stored messages
@app.get("/messages")
async def get_messages():
    return {"messages": messages}

@app.on_event("startup")
async def startup():
    print(f"Device B IP: {DEVICE_B_IP}")
    print(f"Service Address: {SERVICE_ADDRESS}")
    await register()
    asyncio.create_task(send_heartbeat())

@app.on_event("shutdown")
async def shutdown():
    try:
        requests.post(f"{SERVICE_REGISTRAR_URL}/deregister", params={"name": SERVICE_NAME})
        print("Service deregistered.")
    except Exception as e:
        print(f"Error deregistering service: {e}")
