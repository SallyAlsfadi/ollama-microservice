# Ollama Microservice

This project is a Flask-based microservice that interacts with a locally installed **Ollama LLM**. It is fully containerized using **Docker**.

---

## ** How to Run This Project**

Follow these steps to set up and run the microservice.

### **1️⃣ Prerequisites**

- Install **Ollama**: [Download Ollama](https://ollama.ai/download)
- Install **Docker**: [Download Docker](https://www.docker.com/products/docker-desktop)

---

### ** Running Ollama Locally**

Ensure that **Ollama is installed and running** before starting the Flask app.

Check if Ollama is installed:

```bash
ollama list


Start with ollama : ollama run mistral to make sure it's running


docker build -t ollama-microservice .
docker run -p 8080:8080 ollama-microservice

in the posman to test it use : curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{
  "prompt": "Tell me a joke."
}'



Ensure Flask is using host.docker.internal inside app.py: OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"
```
