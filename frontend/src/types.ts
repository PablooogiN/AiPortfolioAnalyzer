export interface Holding {
  id: number;
  ticker: string;
  shares: number;
  account_type: "pre-tax" | "post-tax";
}

export interface EnrichedHolding extends Holding {
  current_price: number;
  current_value: number;
  weight: number;
  sector: string;
  industry: string;
  pe_ratio: number | null;
  forward_pe: number | null;
  dividend_yield: number | null;
  beta: number | null;
  market_cap: number | null;
  fifty_two_week_high: number | null;
  fifty_two_week_low: number | null;
}

export interface CashPositions {
  pre_tax_cash: number;
  post_tax_cash: number;
}

export interface PortfolioSummary {
  holdings: EnrichedHolding[];
  total_value: number;
  pre_tax_cash: number;
  post_tax_cash: number;
  total_portfolio_value: number;
}

export interface Strategy {
  key: string;
  label: string;
  description: string;
}

export interface Recommendation {
  action: string;
  ticker: string;
  rationale: string;
}

export interface AnalysisData {
  summary: string;
  key_findings: string[];
  recommendations: Recommendation[];
  risk_warnings: string[];
}
