import requests
import time
import socket
from fastapi import FastAPI, Request

app = FastAPI()


SERVICE_REGISTRAR_URL = "http://192.168.2.62:8000"
SERVICE_NAME = "device_b_service"


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

def register():
   
    try:
        response = requests.post(f"{SERVICE_REGISTRAR_URL}/register", 
                                 params={"name": SERVICE_NAME, "address": SERVICE_ADDRESS})
        print(response.json())
    except Exception as e:
        print(f"Error registering service: {e}")

def send_heartbeat():
  
    while True:
        time.sleep(120)
        try:
            requests.post(f"{SERVICE_REGISTRAR_URL}/heartbeat", 
                          params={"name": SERVICE_NAME})
        except Exception as e:
            print(f"Error sending heartbeat: {e}")

@app.post("/receive")
async def receive_message(request: Request):
   
    data = await request.json()
    print(f"Received message from {data['from']}: {data['message']}")
    return {"status": "success", "received": data["message"]}


register()


import threading
threading.Thread(target=send_heartbeat, daemon=True).start()
