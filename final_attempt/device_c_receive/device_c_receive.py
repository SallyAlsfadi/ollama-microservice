from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    from_service: str
    message: str

@app.post("/receive")
async def receive_message(message: Message):
    print(f"Received message from {message.from_service}: {message.message}")
    return {"status": "success", "message": "Message received"}