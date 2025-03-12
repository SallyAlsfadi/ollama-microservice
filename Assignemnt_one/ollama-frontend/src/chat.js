import React, { useState } from "react";
import axios from "axios";
import "./chat.css";

const Chat = () => {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    const newMessages = [...messages, { role: "user", text: prompt }];
    setMessages(newMessages);

    try {
      const response = await axios.post("http://localhost:8080/ask", {
        prompt,
      });
      setMessages([
        ...newMessages,
        { role: "bot", text: response.data.response },
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { role: "bot", text: "Error: Could not connect to the server." },
      ]);
    }

    setPrompt("");
    setLoading(false);
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-content">
            <img src="./" alt="Support" />
            <div>
              <div>How can we help?</div>
              <div className="status">Ollama microservice!</div>
            </div>
          </div>
        </div>

        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={msg.role === "user" ? "user-message" : "bot-message"}
            >
              <strong>{msg.role === "user" ? "You: " : "Ollama: "}</strong>
              {msg.text}
            </div>
          ))}
          {loading && (
            <p className="loading-text">Ollama is thinking...</p>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message here..."
          />
          <button onClick={handleSend} disabled={loading}>
            {loading ? "Sending..." : "➤"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
