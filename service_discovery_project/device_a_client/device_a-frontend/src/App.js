import React, { useState } from 'react';

function App() {
  // State to store the message input by the user
  const [message, setMessage] = useState('');  // This will hold the message entered by the user
  const [isLoading, setIsLoading] = useState(false);  // To track if the request is in progress
  const [responseMessage, setResponseMessage] = useState('');  // To display response from the server

  // Handle the change in the message input field
  const handleInputChange = (e) => {
    setMessage(e.target.value);  // Update the message state as the user types
  };

  // Handle sending the message to the backend
  const handleSendMessage = async () => {
    if (message.trim() === '') {
      alert('Please enter a message.');  // Alert if the message is empty
      return;
    }

    // Set loading state
    setIsLoading(true);

    try {
      // Sending the message to the Flask backend
      const response = await fetch('http://127.0.0.1:5000/send-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_service: "Shubhangi's Microservice",  // Target service where the message is being sent
          message: message,  // The message entered by the user, stored in the state
        }),
      });

      const data = await response.json();

      // Handle the response from the backend
      if (response.ok) {
        setResponseMessage('Message sent successfully!');  // Display success message
      } else {
        setResponseMessage(`Failed to send message: ${data.error || 'Unknown error'}`);  // Display failure message
      }
    } catch (error) {
      // Catch any errors in case of network issues or other errors
      setResponseMessage('Error sending message: ' + error.message);
    } finally {
      // Reset loading state
      setIsLoading(false);
    }

    // Clear the message input after sending
    setMessage('');
  };

  return (
    <div className="App">
      <h1>Send Message to Shubhangi's Microservice</h1>
      
      <textarea
        value={message}  // This binds the value of the textarea to the state variable `message`
        onChange={handleInputChange}  // This updates the state when the user types
        placeholder="Type your message"
        rows="4"
        cols="50"
      />
      <br />
      <button onClick={handleSendMessage} disabled={isLoading}>
        {isLoading ? 'Sending...' : 'Send Message'}  
      </button>

      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default App;
