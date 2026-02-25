import { useCallback, useEffect, useState } from "react";
import { analyzePortfolio, getPortfolio } from "./api/client";
import type { AnalysisData, PortfolioSummary } from "./types";
import AddHoldingForm from "./components/AddHoldingForm";
import CashPositions from "./components/CashPositions";
import HoldingsTable from "./components/HoldingsTable";
import StrategySelector from "./components/StrategySelector";
import AnalysisResult from "./components/AnalysisResult";

export default function App() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [loadingPortfolio, setLoadingPortfolio] = useState(true);
  const [strategy, setStrategy] = useState("value");
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");

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

  const handleAnalyze = async () => {
    setAnalysisData(null);
    setAnalysisError("");
    setAnalysisLoading(true);
    try {
      const result = await analyzePortfolio(strategy);
      setAnalysisData(result);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Analysis failed";
      setAnalysisError(message);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const hasHoldings = (portfolio?.holdings.length ?? 0) > 0;
  const totalPortfolioValue = portfolio?.total_portfolio_value ?? 0;
  const totalInvested = portfolio?.total_value ?? 0;
  const totalCash =
    (portfolio?.pre_tax_cash ?? 0) + (portfolio?.post_tax_cash ?? 0);

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

        {/* Cash Positions */}
        <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Cash Positions</h2>
          <CashPositions onUpdated={fetchPortfolio} />
        </section>

        {/* Portfolio Table */}
        <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Your Portfolio</h2>
            {totalPortfolioValue > 0 && (
              <div className="text-sm text-gray-600">
                Invested:{" "}
                <span className="font-semibold">
                  ${totalInvested.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </span>
                {totalCash > 0 && (
                  <>
                    {" "}| Cash:{" "}
                    <span className="font-semibold">
                      ${totalCash.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                    </span>
                    {" "}| Total:{" "}
                    <span className="font-semibold">
                      ${totalPortfolioValue.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                    </span>
                  </>
                )}
              </div>
            )}
          </div>
          {loadingPortfolio ? (
            <p className="text-gray-400 text-center py-8">
              Loading portfolio...
            </p>
          ) : (
            <HoldingsTable
              holdings={portfolio?.holdings ?? []}
              totalValue={portfolio?.total_value ?? 0}
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
              data={analysisData}
              loading={analysisLoading}
              error={analysisError}
            />
          </div>
        </section>
      </main>
    </div>
  );
}
