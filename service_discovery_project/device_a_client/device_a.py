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

# Call get_services to display the available services
get_services()

# Get user input for the message
user_message = input("Enter the message to send: ")

# Send the message to another service
send_message("Shubhangi's Microservice", user_message)
