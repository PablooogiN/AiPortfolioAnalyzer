import type { AnalysisData } from "../types";

const ACTION_STYLES: Record<string, string> = {
  BUY: "bg-green-100 text-green-800",
  ADD: "bg-blue-100 text-blue-800",
  HOLD: "bg-gray-100 text-gray-800",
  TRIM: "bg-yellow-100 text-yellow-800",
  SELL: "bg-red-100 text-red-800",
};

interface Props {
  data: AnalysisData | null;
  loading: boolean;
  error: string;
}

export default function AnalysisResult({ data, loading, error }: Props) {
  if (error) {
    return (
      <div className="rounded-md bg-red-50 border border-red-200 p-4 text-red-700">
        {error}
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 gap-3">
        <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
        <p className="text-sm text-gray-500">Analyzing your portfolio...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <p className="text-gray-400 italic text-center py-8">
        Select a strategy and click &quot;Analyze Portfolio&quot; to get AI
        suggestions.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 uppercase tracking-wide mb-2">
          Portfolio Summary
        </h3>
        <p className="text-sm text-blue-800 leading-relaxed">{data.summary}</p>
      </div>

      {/* Key Findings */}
      {data.key_findings.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">
            Key Findings
          </h3>
          <ul className="space-y-2">
            {data.key_findings.map((finding, i) => (
              <li
                key={i}
                className="flex gap-2 text-sm text-gray-700 leading-relaxed"
              >
                <span className="text-blue-500 mt-0.5 shrink-0">&#9679;</span>
                <span dangerouslySetInnerHTML={{ __html: boldTickers(finding) }} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {data.recommendations.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">
            Recommendations
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                  <th className="px-4 py-3 w-20">Action</th>
                  <th className="px-4 py-3 w-24">Ticker</th>
                  <th className="px-4 py-3">Rationale</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {data.recommendations.map((rec, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          ACTION_STYLES[rec.action] ?? "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {rec.action}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-semibold text-gray-900">
                      {rec.ticker}
                    </td>
                    <td className="px-4 py-3 text-gray-700">{rec.rationale}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Risk Warnings */}
      {data.risk_warnings.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-amber-900 uppercase tracking-wide mb-2">
            Risk Warnings
          </h3>
          <ul className="space-y-1.5">
            {data.risk_warnings.map((warning, i) => (
              <li key={i} className="flex gap-2 text-sm text-amber-800">
                <span className="shrink-0">&#9888;</span>
                <span>{warning}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

/** Replace **text** with <strong>text</strong> for inline bold rendering. */
function boldTickers(text: string): string {
  return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}
