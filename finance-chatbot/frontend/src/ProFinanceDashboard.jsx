import { useState, useEffect } from "react";
import {
  PieChart, Pie, Cell, Tooltip,
  ResponsiveContainer
} from "recharts";

export default function ProFinanceDashboard() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chartData, setChartData] = useState([]);
  const [total, setTotal] = useState(0);
  const [transactions, setTransactions] = useState([]);

  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

  // Load initial data
  const loadData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "category breakdown" })
      });

      const data = await res.json();
      updateChart(data.data);
    } catch {}
  };

  useEffect(() => {
    loadData();
  }, []);

  const updateChart = (dataObj) => {
    if (!dataObj) return;

    const formatted = Object.keys(dataObj).map(key => ({
      name: key,
      value: dataObj[key]
    }));

    setChartData(formatted);

    const totalVal = Object.values(dataObj).reduce((a, b) => a + b, 0);
    setTotal(totalVal);
  };

  // Simple parser for UI transaction list
  const extractTransaction = (message) => {
    const words = message.toLowerCase().split(" ");
    let amount = 0;
    let category = "misc";

    if (words.includes("spent")) {
      const idx = words.indexOf("spent") + 1;
      amount = parseFloat(words[idx]) || 0;
    }

    if (words.includes("on")) {
      const idx = words.indexOf("on") + 1;
      category = words[idx] || "misc";
    }

    if (amount > 0) {
      return {
        id: Date.now(),
        amount,
        category
      };
    }

    return null;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: "user", text: userMessage }]);
    setInput("");

    // Add to transaction list (UI level)
    const tx = extractTransaction(userMessage);
    if (tx) {
      setTransactions(prev => [tx, ...prev]);
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await res.json();

      setMessages(prev => [...prev, { role: "bot", text: data.response }]);

      updateChart(data.data);

    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Server error ❌" }]);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial", background: "#f1f5f9" }}>

      {/* Sidebar */}
      <div style={{ width: 220, background: "#111827", color: "white", padding: 20 }}>
        <h2>💰 Finance AI</h2>
        <p style={{ opacity: 0.7 }}>Dashboard</p>
      </div>

      {/* Main */}
      <div style={{ flex: 1, padding: 20 }}>

        {/* Top Cards */}
        <div style={{ display: "flex", gap: 20, marginBottom: 20 }}>
          <div style={cardStyle}>
            <h4>Total Spent</h4>
            <h2>LKR {total}</h2>
          </div>
          <div style={cardStyle}>
            <h4>Transactions</h4>
            <h2>{transactions.length}</h2>
          </div>
          <div style={cardStyle}>
            <h4>Status</h4>
            <h2>Active</h2>
          </div>
        </div>

        <div style={{ display: "flex", gap: 20 }}>

          {/* Chat */}
          <div style={{ ...panelStyle, flex: 1 }}>
            <h3>💬 Chat</h3>

            <div style={{ height: 250, overflowY: "auto", border: "1px solid #ddd", padding: 10, marginBottom: 10 }}>
              {messages.map((m, i) => (
                <div key={i} style={{ textAlign: m.role === "user" ? "right" : "left", marginBottom: 6 }}>
                  <span style={{
                    background: m.role === "user" ? "#3b82f6" : "#e5e7eb",
                    color: m.role === "user" ? "white" : "black",
                    padding: "6px 10px",
                    borderRadius: 10
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
                placeholder="Add expense..."
                style={{ flex: 1, padding: 8 }}
              />
              <button onClick={sendMessage} style={btnStyle}>Send</button>
            </div>
          </div>

          {/* Charts */}
          <div style={{ ...panelStyle, flex: 1 }}>
            <h3>📊 Spending Breakdown</h3>

            {chartData.length === 0 ? (
              <p>No data yet</p>
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={chartData} dataKey="value" outerRadius={90}>
                    {chartData.map((_, i) => (
                      <Cell key={i} fill={colors[i % colors.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Transactions Panel */}
          <div style={{ ...panelStyle, flex: 1 }}>
            <h3>🧾 Transactions</h3>

            {transactions.length === 0 ? (
              <p>No transactions yet</p>
            ) : (
              <div style={{ maxHeight: 300, overflowY: "auto" }}>
                {transactions.map(t => (
                  <div key={t.id} style={{
                    display: "flex",
                    justifyContent: "space-between",
                    padding: "8px 0",
                    borderBottom: "1px solid #eee"
                  }}>
                    <span>{t.category}</span>
                    <span style={{ color: "#ef4444" }}>- LKR {t.amount}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

const cardStyle = {
  background: "white",
  padding: 15,
  borderRadius: 10,
  boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
  flex: 1
};

const panelStyle = {
  background: "white",
  padding: 15,
  borderRadius: 10,
  boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
};

const btnStyle = {
  background: "#3b82f6",
  color: "white",
  border: "none",
  padding: "8px 14px",
  borderRadius: 6,
  cursor: "pointer"
};