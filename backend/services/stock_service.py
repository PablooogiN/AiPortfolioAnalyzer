import yfinance as yf

from models import Holding


def enrich_holdings(holdings: list[Holding]) -> list[dict]:
    tickers = [h.ticker for h in holdings]
    data = yf.Tickers(" ".join(tickers))

    enriched = []
    for holding in holdings:
        ticker_obj = data.tickers.get(holding.ticker)
        info = {}
        current_price = 0.0

        if ticker_obj:
            try:
                info = ticker_obj.info
                current_price = info.get("currentPrice") or info.get(
                    "regularMarketPrice", 0.0
                )
            except Exception:
                current_price = 0.0

        current_value = holding.shares * current_price
        cost_basis = holding.shares * holding.avg_cost
        gain_loss = current_value - cost_basis
        gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis else 0

        enriched.append(
            {
                "id": holding.id,
                "ticker": holding.ticker,
                "shares": holding.shares,
                "avg_cost": holding.avg_cost,
                "date_added": holding.date_added,
                "current_price": round(current_price, 2),
                "current_value": round(current_value, 2),
                "cost_basis": round(cost_basis, 2),
                "gain_loss": round(gain_loss, 2),
                "gain_loss_pct": round(gain_loss_pct, 2),
                "weight": 0,  # computed by caller after totaling
                # Market data for AI context
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            }
        )

    return enriched
