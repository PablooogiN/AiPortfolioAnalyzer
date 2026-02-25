export interface Holding {
  id: number;
  ticker: string;
  shares: number;
  avg_cost: number;
  date_added: string;
}

export interface EnrichedHolding extends Holding {
  current_price: number;
  current_value: number;
  cost_basis: number;
  gain_loss: number;
  gain_loss_pct: number;
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

export interface PortfolioSummary {
  holdings: EnrichedHolding[];
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_pct: number;
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
