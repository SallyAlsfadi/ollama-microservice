import React, { useState } from "react";
import axios from "axios";

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
    <div style={styles.container}>
      <h2>Ollama Chat</h2>
      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={msg.role === "user" ? styles.userMessage : styles.botMessage}
          >
            <strong>{msg.role === "user" ? "You:" : "Ollama:"}</strong>{" "}
            {msg.text}
          </div>
        ))}
        {loading && <p style={styles.loading}>Ollama is thinking...</p>}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your message..."
          style={styles.input}
        />
        <button onClick={handleSend} style={styles.button} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: "20px",
    textAlign: "center",
    maxWidth: "500px",
    margin: "auto",
  },
  chatBox: {
    height: "300px",
    overflowY: "auto",
    border: "1px solid #ddd",
    padding: "10px",
    borderRadius: "8px",
    backgroundColor: "#f9f9f9",
    marginBottom: "10px",
  },
  userMessage: {
    textAlign: "right",
    backgroundColor: "#d1e7dd",
    padding: "8px",
    borderRadius: "5px",
    margin: "5px 0",
  },
  botMessage: {
    textAlign: "left",
    backgroundColor: "#f8d7da",
    padding: "8px",
    borderRadius: "5px",
    margin: "5px 0",
  },
  inputContainer: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ddd",
  },
  button: {
    padding: "10px 20px",
    border: "none",
    borderRadius: "5px",
    backgroundColor: "#007bff",
    color: "white",
    cursor: "pointer",
  },
  loading: {
    fontStyle: "italic",
    color: "#777",
  },
};

export default Chat;
