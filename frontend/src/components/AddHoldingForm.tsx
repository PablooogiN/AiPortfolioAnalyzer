import { useState } from "react";
import { createHolding } from "../api/client";

interface Props {
  onAdded: () => void;
}

export default function AddHoldingForm({ onAdded }: Props) {
  const [ticker, setTicker] = useState("");
  const [shares, setShares] = useState("");
  const [avgCost, setAvgCost] = useState("");
  const [dateAdded, setDateAdded] = useState(
    new Date().toISOString().slice(0, 10)
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
        avg_cost: parseFloat(avgCost),
        date_added: dateAdded,
      });
      setTicker("");
      setShares("");
      setAvgCost("");
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
          Avg Cost ($)
        </label>
        <input
          type="number"
          value={avgCost}
          onChange={(e) => setAvgCost(e.target.value)}
          placeholder="150.00"
          required
          min="0.01"
          step="any"
          className="w-32 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Date Added
        </label>
        <input
          type="date"
          value={dateAdded}
          onChange={(e) => setDateAdded(e.target.value)}
          required
          className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
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
