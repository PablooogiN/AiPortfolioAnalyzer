import type { Strategy } from "../types";

const STRATEGIES: Strategy[] = [
  {
    key: "value",
    label: "Value Investing",
    description: "Graham & Buffett style — find undervalued stocks",
  },
  {
    key: "growth",
    label: "Growth Investing",
    description: "Focus on revenue growth and momentum",
  },
  {
    key: "dividend",
    label: "Dividend Income",
    description: "Maximize sustainable dividend yield",
  },
  {
    key: "risk",
    label: "Risk & Diversification",
    description: "Reduce concentration and manage downside",
  },
  {
    key: "index",
    label: "Index Comparison",
    description: "Compare against S&P 500 benchmarks",
  },
];

interface Props {
  selected: string;
  onSelect: (key: string) => void;
  onAnalyze: () => void;
  loading: boolean;
  disabled: boolean;
}

export default function StrategySelector({
  selected,
  onSelect,
  onAnalyze,
  loading,
  disabled,
}: Props) {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {STRATEGIES.map((s) => (
          <button
            key={s.key}
            onClick={() => onSelect(s.key)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
              selected === s.key
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>
      <p className="text-sm text-gray-500">
        {STRATEGIES.find((s) => s.key === selected)?.description}
      </p>
      <button
        onClick={onAnalyze}
        disabled={loading || disabled}
        className="rounded-md bg-green-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-green-700 disabled:opacity-50 transition-colors"
      >
        {loading ? "Analyzing..." : "Analyze Portfolio"}
      </button>
    </div>
  );
}
