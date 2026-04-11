import { useState } from "react";

function App() {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);

  const send = async () => {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();

    setChat([...chat, { user: msg, bot: data.response }]);
    setMsg("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>💰 Finance Chatbot</h2>

      {chat.map((c, i) => (
        <div key={i}>
          <p><b>You:</b> {c.user}</p>
          <p><b>Bot:</b> {c.bot}</p>
        </div>
      ))}

      <input value={msg} onChange={e => setMsg(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}

export default App;