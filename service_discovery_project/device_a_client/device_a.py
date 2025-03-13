import requests


SERVICE_REGISTRAR_URL = "http://172.21.80.1:8000"

def get_services():

    response = requests.get(f"{SERVICE_REGISTRAR_URL}/services")
    print("Available services:", response.json())

def send_message(to_service, message):
    
    response = requests.post(f"{SERVICE_REGISTRAR_URL}/forward", 
                             params={"from_service": "Badal's Microservice", 
                                     "to_service": to_service, 
                                     "message": message})
    print("Response:", response.json())

get_services()
send_message("Shubhangi's Microservice", "Hello from Badal's Service !")
