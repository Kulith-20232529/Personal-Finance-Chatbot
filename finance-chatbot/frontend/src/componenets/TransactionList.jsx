import { useEffect, useState } from "react";
import axios from "axios";

export default function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = async () => {
    const res = await axios.get("http://127.0.0.1:8000/transactions");
    setTransactions(res.data);
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const deleteTransaction = async (id) => {
    await axios.delete(`http://127.0.0.1:8000/transactions/${id}`);
    fetchTransactions();
  };

  const editTransaction = async (id) => {
    const newAmount = prompt("Enter new amount:");
    const newCategory = prompt("Enter new category:");

    await axios.put(`http://127.0.0.1:8000/transactions/${id}`, {
      amount: Number(newAmount),
      category: newCategory,
    });

    fetchTransactions();
  };

  return (
    <div>
      <h2>Transaction History</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t) => (
            <tr key={t.id}>
              <td>{t.amount}</td>
              <td>{t.category}</td>
              <td>
                <button onClick={() => editTransaction(t.id)}>✏️ Edit</button>
                <button onClick={() => deleteTransaction(t.id)}>🗑️ Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}