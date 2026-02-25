import type { EnrichedHolding } from "../types";
import { deleteHolding } from "../api/client";

interface Props {
  holdings: EnrichedHolding[];
  totalValue: number;
  onRefresh: () => void;
}

export default function HoldingsTable({
  holdings,
  totalValue,
  onRefresh,
}: Props) {
  const handleDelete = async (id: number, ticker: string) => {
    if (!confirm(`Delete ${ticker}?`)) return;
    await deleteHolding(id);
    onRefresh();
  };

  if (holdings.length === 0) {
    return (
      <p className="text-gray-500 italic py-8 text-center">
        No holdings yet. Add your first stock above.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
          <tr>
            <th className="px-4 py-3">Ticker</th>
            <th className="px-4 py-3 text-right">Shares</th>
            <th className="px-4 py-3">Account Type</th>
            <th className="px-4 py-3 text-right">Current Price</th>
            <th className="px-4 py-3 text-right">Value</th>
            <th className="px-4 py-3 text-right">Weight</th>
            <th className="px-4 py-3">Sector</th>
            <th className="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {holdings.map((h) => (
            <tr key={h.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-semibold">{h.ticker}</td>
              <td className="px-4 py-3 text-right">{h.shares}</td>
              <td className="px-4 py-3">
                <span
                  className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                    h.account_type === "pre-tax"
                      ? "bg-amber-100 text-amber-800"
                      : "bg-blue-100 text-blue-800"
                  }`}
                >
                  {h.account_type === "pre-tax" ? "Pre-Tax" : "Post-Tax"}
                </span>
              </td>
              <td className="px-4 py-3 text-right">
                ${h.current_price.toFixed(2)}
              </td>
              <td className="px-4 py-3 text-right">
                ${h.current_value.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </td>
              <td className="px-4 py-3 text-right">{h.weight.toFixed(1)}%</td>
              <td className="px-4 py-3 text-gray-500">{h.sector}</td>
              <td className="px-4 py-3">
                <button
                  onClick={() => handleDelete(h.id, h.ticker)}
                  className="text-red-400 hover:text-red-600 text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot className="bg-gray-50 font-semibold text-sm">
          <tr>
            <td className="px-4 py-3" colSpan={4}>
              Total
            </td>
            <td className="px-4 py-3 text-right">
              $
              {totalValue.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </td>
            <td className="px-4 py-3 text-right">100%</td>
            <td colSpan={2}></td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
