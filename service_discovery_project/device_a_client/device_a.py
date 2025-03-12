import requests


SERVICE_REGISTRAR_URL = "http://192.168.2.62:8000"

def get_services():

    response = requests.get(f"{SERVICE_REGISTRAR_URL}/services")
    print("Available services:", response.json())

def send_message(to_service, message):
    
    response = requests.post(f"{SERVICE_REGISTRAR_URL}/forward", 
                             params={"from_service": "device_a_client", 
                                     "to_service": to_service, 
                                     "message": message})
    print("Response:", response.json())

get_services()
send_message("device_b_service", "Hello from Device A!")
