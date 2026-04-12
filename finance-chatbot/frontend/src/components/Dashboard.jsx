import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";
import Charts from "./Charts";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getDashboard().then((res) => setData(res.data));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h1>📊 Dashboard</h1>
      <h2>Total: ₹{data.total}</h2>

      <Charts data={data} />

      <h3>Recent Transactions</h3>
      <ul>
        {data.recent.map((e, i) => (
          <li key={i}>
            {e.date} - ₹{e.amount} ({e.category})
          </li>
        ))}
      </ul>
    </div>
  );
}