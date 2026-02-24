import type { EnrichedHolding } from "../types";
import { deleteHolding } from "../api/client";

interface Props {
  holdings: EnrichedHolding[];
  totalValue: number;
  totalCost: number;
  totalGainLoss: number;
  totalGainLossPct: number;
  onRefresh: () => void;
}

export default function HoldingsTable({
  holdings,
  totalValue,
  totalCost,
  totalGainLoss,
  totalGainLossPct,
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
            <th className="px-4 py-3 text-right">Avg Cost</th>
            <th className="px-4 py-3 text-right">Current Price</th>
            <th className="px-4 py-3 text-right">Value</th>
            <th className="px-4 py-3 text-right">Weight</th>
            <th className="px-4 py-3 text-right">Gain/Loss</th>
            <th className="px-4 py-3">Sector</th>
            <th className="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {holdings.map((h) => (
            <tr key={h.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-semibold">{h.ticker}</td>
              <td className="px-4 py-3 text-right">{h.shares}</td>
              <td className="px-4 py-3 text-right">${h.avg_cost.toFixed(2)}</td>
              <td className="px-4 py-3 text-right">
                ${h.current_price.toFixed(2)}
              </td>
              <td className="px-4 py-3 text-right">
                ${h.current_value.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </td>
              <td className="px-4 py-3 text-right">{h.weight.toFixed(1)}%</td>
              <td
                className={`px-4 py-3 text-right font-medium ${
                  h.gain_loss >= 0 ? "text-green-600" : "text-red-600"
                }`}
              >
                {h.gain_loss >= 0 ? "+" : ""}
                {h.gain_loss_pct.toFixed(1)}%
              </td>
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
            <td
              className={`px-4 py-3 text-right ${
                totalGainLoss >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              {totalGainLoss >= 0 ? "+" : ""}$
              {Math.abs(totalGainLoss).toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}{" "}
              ({totalGainLoss >= 0 ? "+" : ""}
              {totalGainLossPct.toFixed(1)}%)
            </td>
            <td colSpan={2}></td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
