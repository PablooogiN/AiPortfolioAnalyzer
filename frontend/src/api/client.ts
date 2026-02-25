import axios from "axios";
import type {
  AnalysisData,
  CashPositions,
  Holding,
  PortfolioSummary,
} from "../types";

const api = axios.create({ baseURL: "/api" });

export async function getHoldings(): Promise<Holding[]> {
  const { data } = await api.get<Holding[]>("/holdings");
  return data;
}

export async function createHolding(
  holding: Omit<Holding, "id">
): Promise<Holding> {
  const { data } = await api.post<Holding>("/holdings", holding);
  return data;
}

export async function updateHolding(
  id: number,
  holding: Partial<Omit<Holding, "id">>
): Promise<Holding> {
  const { data } = await api.put<Holding>(`/holdings/${id}`, holding);
  return data;
}

export async function deleteHolding(id: number): Promise<void> {
  await api.delete(`/holdings/${id}`);
}

export async function getPortfolio(): Promise<PortfolioSummary> {
  const { data } = await api.get<PortfolioSummary>("/portfolio");
  return data;
}

export async function getCash(): Promise<CashPositions> {
  const { data } = await api.get<CashPositions>("/cash");
  return data;
}

export async function updateCash(
  cash: CashPositions
): Promise<CashPositions> {
  const { data } = await api.put<CashPositions>("/cash", cash);
  return data;
}

export async function analyzePortfolio(
  strategy: string
): Promise<AnalysisData> {
  const { data } = await api.post<AnalysisData>("/analyze", { strategy });
  return data;
}
