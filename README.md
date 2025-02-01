# **Ollama Microservice**

This microservice is a Flask-based API that interacts with an **Ollama Large Language Model (LLM)**. It receives a prompt via a `POST` request and returns a generated response.

### **Prerequisites**

- **Ollama LLM Server** (running on `http://localhost:11434`)

### **Why Port 8080?**

By default, Flask runs on **port 5000**, but on macOS, **port 5000 is reserved (possibly for AirDrop)**, which may cause conflicts. To avoid this, the API runs on **port 8080**.

## ** Running the Microservice**

### \*\*Option 1: Using Docker

1. **Build the Docker Image**:
   ```bash
   docker build -t flask-ollama .
   ```

Run the Docker Container:
docker run -p 8080:8080 flask-ollama

using Postman :
Endpoint: POST /ask : Sends a prompt to the Ollama LLM and retrieves the response.
URL: http://localhost:8080/ask
Body: (raw JSON) : any prompt you want
