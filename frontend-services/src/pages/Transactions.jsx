import { useState, useEffect } from "react";

export default function Transactions() {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";
  const LIST_URL = `${API_BASE}/api/transactions`;
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    acc_no: "",
    type: "deposit",
    amount: "",
  });

  const fetchTransactions = async () => {
    const res = await fetch(LIST_URL);
    const data = await res.json();
    setTransactions(data.transactions || []);
  };

  useEffect(() => { fetchTransactions(); }, []);

  const createTransaction = async (e) => {
    e.preventDefault();
    const endpoint = form.type === "deposit"
      ? `${API_BASE}/api/transactions/deposit`
      : `${API_BASE}/api/transactions/withdraw`;

    await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ acc_no: form.acc_no, amount: parseFloat(form.amount) }),
    });
    setForm({ acc_no: "", type: "deposit", amount: "" });
    fetchTransactions();
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Transactions</h2>

      <form onSubmit={createTransaction} className="space-y-2 max-w-md">
        <input
          className="border p-2 w-full"
          placeholder="Account No"
          value={form.acc_no}
          onChange={(e) => setForm({ ...form, acc_no: e.target.value })}
        />
        <select
          className="border p-2 w-full"
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
        >
          <option value="deposit">Deposit</option>
          <option value="withdraw">Withdraw</option>
        </select>
        <input
          className="border p-2 w-full"
          placeholder="Amount"
          type="number"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
        />
        <button className="bg-purple-500 text-white px-4 py-2 rounded">
          Submit
        </button>
      </form>

      <h3 className="text-xl font-semibold mt-6">All Transactions</h3>
      <ul className="mt-2">
        {transactions.map((tx) => (
          <li key={tx.txn_id} className="border p-2 my-1">
            {tx.acc_no} – {tx.type} – ₹{tx.amount}
          </li>
        ))}
      </ul>
    </div>
  );
}
