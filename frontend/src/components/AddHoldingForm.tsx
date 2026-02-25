import { useState } from "react";
import { createHolding } from "../api/client";

interface Props {
  onAdded: () => void;
}

export default function AddHoldingForm({ onAdded }: Props) {
  const [ticker, setTicker] = useState("");
  const [shares, setShares] = useState("");
  const [accountType, setAccountType] = useState<"pre-tax" | "post-tax">(
    "post-tax"
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await createHolding({
        ticker: ticker.toUpperCase().trim(),
        shares: parseFloat(shares),
        account_type: accountType,
      });
      setTicker("");
      setShares("");
      onAdded();
    } catch {
      setError("Failed to add holding. Check your inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-3 items-end">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Ticker
        </label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="AAPL"
          required
          className="w-28 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Shares
        </label>
        <input
          type="number"
          value={shares}
          onChange={(e) => setShares(e.target.value)}
          placeholder="100"
          required
          min="0.001"
          step="any"
          className="w-28 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Account Type
        </label>
        <select
          value={accountType}
          onChange={(e) =>
            setAccountType(e.target.value as "pre-tax" | "post-tax")
          }
          className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="post-tax">Post-Tax</option>
          <option value="pre-tax">Pre-Tax</option>
        </select>
      </div>
      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Adding..." : "Add Holding"}
      </button>
      {error && <p className="text-red-600 text-sm w-full">{error}</p>}
    </form>
  );
}
