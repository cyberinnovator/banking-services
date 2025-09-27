import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white px-6 py-3 flex justify-between">
      <h1 className="font-bold text-xl">🏦 Banking System</h1>
      <div className="space-x-4">
        <Link to="/" className="hover:underline">Dashboard</Link>
        <Link to="/accounts" className="hover:underline">Accounts</Link>
        <Link to="/loans" className="hover:underline">Loans</Link>
        <Link to="/transactions" className="hover:underline">Transactions</Link>
      </div>
    </nav>
  );
}
