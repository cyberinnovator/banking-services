import { useState, useEffect } from "react";

export default function Loans() {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";
  const API_URL = `${API_BASE}/api/loans`;
  const [loans, setLoans] = useState([]);
  const [form, setForm] = useState({
    cust_name: "",
    branch_name: "",
    amount: "",
  });

  const fetchLoans = async () => {
    const res = await fetch(API_URL);
    const data = await res.json();
    setLoans(data.loans || []);
  };

  useEffect(() => { fetchLoans(); }, []);

  const createLoan = async (e) => {
    e.preventDefault();
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, amount: parseFloat(form.amount) }),
    });
    setForm({ cust_name: "", branch_name: "", amount: "" });
    fetchLoans();
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Loans</h2>

      <form onSubmit={createLoan} className="space-y-2 max-w-md">
        {Object.keys(form).map((key) => (
          <input
            key={key}
            className="border p-2 w-full"
            placeholder={key.replace("_", " ")}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        <button className="bg-blue-500 text-white px-4 py-2 rounded">Apply Loan</button>
      </form>

      <h3 className="text-xl font-semibold mt-6">All Loans</h3>
      <ul className="mt-2">
        {loans.map((loan) => (
          <li key={loan.loan_no} className="border p-2 my-1">
            {loan.customer.cust_name} – {loan.branch_name} – ₹{loan.amount}
          </li>
        ))}
      </ul>
    </div>
  );
}
