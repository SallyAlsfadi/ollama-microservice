import { useState } from "react";
import "./MessageSender.css"; // Optional styling

const MessageSender = () => {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  const sendMessage = async () => {
    if (!message.trim()) return alert("Enter a message!");

    setStatus("Sending...");

    try {
      const response = await fetch("http://172.21.80.1:8000/forward", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from_service: "device_a_client",
          to_service: "device_b_service",
          message: message.trim(),
        }),
      });

      const result = await response.json();

      if (result.status === "sent") {
        setStatus(`✅ Message sent: "${message}"`);
        setMessage(""); // Clear input field
      } else {
        setStatus(`❌ Error: ${result.error}`);
      }
    } catch (error) {
      setStatus("❌ Network error: Could not send message");
    }
  };

  return (
    <div className="message-container">
      <h2>Send Message to Device B</h2>
      
      <div className="input-area">
        <input
          type="text"
          value={message}
          placeholder="Type message..."
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>

      {status && <p className="status">{status}</p>}
    </div>
  );
};

export default MessageSender;
