import { useCallback, useEffect, useRef, useState } from "react";
import { getPortfolio, streamAnalysis } from "./api/client";
import type { PortfolioSummary } from "./types";
import AddHoldingForm from "./components/AddHoldingForm";
import HoldingsTable from "./components/HoldingsTable";
import StrategySelector from "./components/StrategySelector";
import AnalysisResult from "./components/AnalysisResult";

export default function App() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [loadingPortfolio, setLoadingPortfolio] = useState(true);
  const [strategy, setStrategy] = useState("value");
  const [analysisContent, setAnalysisContent] = useState("");
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  const fetchPortfolio = useCallback(async () => {
    setLoadingPortfolio(true);
    try {
      const data = await getPortfolio();
      setPortfolio(data);
    } catch {
      // portfolio fetch failed — table will show empty
    } finally {
      setLoadingPortfolio(false);
    }
  }, []);

  useEffect(() => {
    fetchPortfolio();
  }, [fetchPortfolio]);

  const handleAnalyze = () => {
    if (abortRef.current) abortRef.current.abort();
    setAnalysisContent("");
    setAnalysisError("");
    setAnalysisLoading(true);

    abortRef.current = streamAnalysis(
      strategy,
      (chunk) => setAnalysisContent((prev) => prev + chunk),
      () => setAnalysisLoading(false),
      (err) => {
        setAnalysisError(err);
        setAnalysisLoading(false);
      }
    );
  };

  const hasHoldings = (portfolio?.holdings.length ?? 0) > 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Portfolio Analyzer
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Add your holdings and get AI-powered analysis
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-8">
        {/* Add Holding */}
        <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Add Holding</h2>
          <AddHoldingForm onAdded={fetchPortfolio} />
        </section>

        {/* Portfolio Table */}
        <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Your Portfolio</h2>
          {loadingPortfolio ? (
            <p className="text-gray-400 text-center py-8">
              Loading portfolio...
            </p>
          ) : (
            <HoldingsTable
              holdings={portfolio?.holdings ?? []}
              totalValue={portfolio?.total_value ?? 0}
              totalCost={portfolio?.total_cost ?? 0}
              totalGainLoss={portfolio?.total_gain_loss ?? 0}
              totalGainLossPct={portfolio?.total_gain_loss_pct ?? 0}
              onRefresh={fetchPortfolio}
            />
          )}
        </section>

        {/* Strategy & Analysis */}
        <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">AI Analysis</h2>
          <StrategySelector
            selected={strategy}
            onSelect={setStrategy}
            onAnalyze={handleAnalyze}
            loading={analysisLoading}
            disabled={!hasHoldings}
          />
          <div className="mt-6 border-t border-gray-100 pt-6">
            <AnalysisResult
              content={analysisContent}
              loading={analysisLoading}
              error={analysisError}
            />
          </div>
        </section>
      </main>
    </div>
  );
}
