import axios from "axios";
import type { Holding, PortfolioSummary } from "../types";

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

export function streamAnalysis(
  strategy: string,
  onChunk: (text: string) => void,
  onDone: () => void,
  onError: (err: string) => void
): AbortController {
  const controller = new AbortController();

  fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ strategy }),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        const err = await response.json();
        onError(err.detail || "Analysis failed");
        return;
      }

      const reader = response.body?.getReader();
      if (!reader) {
        onError("No response body");
        return;
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") {
              onDone();
              return;
            }
            onChunk(data);
          }
        }
      }
      onDone();
    })
    .catch((err) => {
      if (err.name !== "AbortError") {
        onError(err.message);
      }
    });

  return controller;
}
