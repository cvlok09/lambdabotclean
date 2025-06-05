import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { text: "Welcome! Type a message to update the roster.", sender: "bot" },
  ]);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { text: input, sender: "user" }]);

    fetch("https://cleanbackend-52u5.onrender.com/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: input }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setMessages((prev) => [...prev, { text: data.response, sender: "bot" }]);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        setMessages((prev) => [...prev, { text: "Error: Something went wrong", sender: "bot" }]);
      });

    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h2>Fraternity Roster Chatbot</h2>
      <div style={{ marginBottom: 10 }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              background: msg.sender === "bot" ? "#eee" : "#007bff",
              color: msg.sender === "bot" ? "#000" : "#fff",
              padding: "8px 12px",
              borderRadius: 12,
              margin: "5px 0",
              display: "inline-block",
              maxWidth: "80%",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div>
        <input
          style={{ padding: 10, width: "75%" }}
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={sendMessage} style={{ padding: 10 }}>Send</button>
      </div>
    </div>
  );
}

export default App;
