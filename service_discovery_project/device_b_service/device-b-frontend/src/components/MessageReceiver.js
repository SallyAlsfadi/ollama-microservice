import { useState, useEffect } from "react";
import "./MessageReceiver.css";

const DEVICE_B_URL = "http://localhost:8001";
const WS_URL = "ws://localhost:8001/ws"; // WebSocket connection

const MessageReceiver = () => {
  const [messages, setMessages] = useState([]);

  // Fetch messages from backend (fallback)
  const fetchMessages = async () => {
    try {
      const response = await fetch(`${DEVICE_B_URL}/messages`);
      const data = await response.json();
      setMessages(data.messages); // Fix: Access messages array properly
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  useEffect(() => {
    fetchMessages(); // Load initial messages

    // Open WebSocket connection
    const ws = new WebSocket(WS_URL);

    ws.onmessage = (event) => {
      const receivedMessage = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, receivedMessage]);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket closed. Reconnecting in 5 seconds...");
      setTimeout(() => {
        window.location.reload(); // Restart app to reconnect
      }, 5000);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="receiver-container">
      <h1>📩 Shubhangi's Microservice - Message Inbox</h1>
      {messages.length > 0 && (
        <div className="notification">New Message: "{messages[messages.length - 1].message}"</div>
      )}
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>📨 From {msg.from}: {msg.message}</li>
        ))}
      </ul>
    </div>
  );
};

export default MessageReceiver;
