import { useState } from "react";
import {
  PieChart, Pie, Cell, Tooltip,
  ResponsiveContainer
} from "recharts";

export default function ProFinanceDashboard() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chartData, setChartData] = useState([]);

  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"];

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: "user", text: userMessage }]);
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await res.json();

      setMessages(prev => [...prev, { role: "bot", text: data.response }]);

      // 🔥 update chart with real data
      const formatted = Object.keys(data.data).map(key => ({
        name: key,
        value: data.data[key]
      }));

      setChartData(formatted);

    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Backend error ❌" }]);
    }
  };

  return (
    <div style={{ fontFamily: "Arial", padding: 20, background: "#f5f5f5", minHeight: "100vh" }}>
      
      <h1 style={{ textAlign: "center" }}>💰 Finance Chatbot</h1>

      <div style={{ display: "flex", gap: 20 }}>
        
        {/* Chat Section */}
        <div style={{
          flex: 1,
          background: "white",
          padding: 15,
          borderRadius: 10,
          boxShadow: "0 0 10px rgba(0,0,0,0.1)"
        }}>
          <h3>Chat</h3>

          <div style={{
            height: 300,
            overflowY: "auto",
            border: "1px solid #ddd",
            padding: 10,
            marginBottom: 10
          }}>
            {messages.map((m, i) => (
              <div key={i} style={{
                textAlign: m.role === "user" ? "right" : "left",
                marginBottom: 5
              }}>
                <span style={{
                  background: m.role === "user" ? "#3b82f6" : "#e5e7eb",
                  color: m.role === "user" ? "white" : "black",
                  padding: "6px 10px",
                  borderRadius: 8,
                  display: "inline-block"
                }}>
                  {m.text}
                </span>
              </div>
            ))}
          </div>

          <div style={{ display: "flex", gap: 10 }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type expense..."
              style={{ flex: 1, padding: 8 }}
            />
            <button onClick={sendMessage} style={{
              background: "#3b82f6",
              color: "white",
              border: "none",
              padding: "8px 12px",
              borderRadius: 5
            }}>
              Send
            </button>
          </div>
        </div>

        {/* Chart Section */}
        <div style={{
          flex: 1,
          background: "white",
          padding: 15,
          borderRadius: 10,
          boxShadow: "0 0 10px rgba(0,0,0,0.1)"
        }}>
          <h3>Spending Breakdown</h3>

          {chartData.length === 0 ? (
            <p>No data yet</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={chartData} dataKey="value" outerRadius={100}>
                  {chartData.map((_, i) => (
                    <Cell key={i} fill={colors[i % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

      </div>
    </div>
  );
}