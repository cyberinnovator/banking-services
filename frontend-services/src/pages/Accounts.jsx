import { useState, useEffect } from "react";

export default function Accounts() {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";
  const API_URL = `${API_BASE}/api/accounts`;
  const [accounts, setAccounts] = useState([]);
  const [form, setForm] = useState({
    cust_name: "",
    cust_street: "",
    cust_city: "",
    branch_name: "",
    initial_balance: "",
  });

  const fetchAccounts = async () => {
    const res = await fetch(API_URL);
    const data = await res.json();
    setAccounts(data.accounts || []);
  };

  useEffect(() => { fetchAccounts(); }, []);

  const createAccount = async (e) => {
    e.preventDefault();
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, initial_balance: parseFloat(form.initial_balance) }),
    });
    setForm({ cust_name: "", cust_street: "", cust_city: "", branch_name: "", initial_balance: "" });
    fetchAccounts();
  };

  const deleteAccount = async (acc_no) => {
    await fetch(`${API_URL}/${acc_no}`, { method: "DELETE" });
    fetchAccounts();
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Accounts</h2>

      {/* Create Account Form */}
      <form onSubmit={createAccount} className="space-y-2 max-w-md">
        {Object.keys(form).map((key) => (
          <input
            key={key}
            className="border p-2 w-full"
            placeholder={key.replace("_", " ")}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        <button className="bg-green-500 text-white px-4 py-2 rounded">Create Account</button>
      </form>

      {/* List Accounts */}
      <h3 className="text-xl font-semibold mt-6">All Accounts</h3>
      <ul className="mt-2">
        {accounts.map((acc) => (
          <li key={acc.acc_no} className="border p-2 my-1 flex justify-between">
            <span>
              {acc.customer.cust_name} – {acc.branch_name} – ₹{acc.balance}
            </span>
            <button
              onClick={() => deleteAccount(acc.acc_no)}
              className="bg-red-500 text-white px-3 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
