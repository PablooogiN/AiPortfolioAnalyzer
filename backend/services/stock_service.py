import time

import yfinance as yf

from models import Holding

# Simple in-memory cache for full ticker info (used during analysis)
_info_cache: dict[str, dict] = {}
_info_cache_ts: dict[str, float] = {}
_CACHE_TTL = 300  # 5 minutes


def _get_cached_info(ticker: str) -> dict:
    now = time.time()
    if ticker in _info_cache and (now - _info_cache_ts.get(ticker, 0)) < _CACHE_TTL:
        return _info_cache[ticker]
    try:
        info = yf.Ticker(ticker).info
    except Exception:
        info = {}
    _info_cache[ticker] = info
    _info_cache_ts[ticker] = now
    return info


def get_prices(holdings: list[Holding]) -> list[dict]:
    """Lightweight price fetch using yf.download (single batch HTTP call).
    Used for the portfolio table — no heavy .info calls."""
    tickers = [h.ticker for h in holdings]

    prices: dict[str, float] = {}
    try:
        df = yf.download(tickers, period="1d", progress=False, threads=True)
        if not df.empty:
            close = df["Close"]
            for t in tickers:
                try:
                    val = close[t].iloc[-1] if t in close.columns else close.iloc[-1]
                    val = float(val.iloc[0]) if hasattr(val, "iloc") else float(val)
                    prices[t] = val if val == val else 0.0  # NaN check
                except (KeyError, IndexError):
                    pass
    except Exception:
        pass

    result = []
    for holding in holdings:
        current_price = prices.get(holding.ticker, 0.0)
        current_value = holding.shares * current_price

        result.append(
            {
                "id": holding.id,
                "ticker": holding.ticker,
                "shares": holding.shares,
                "account_type": holding.account_type,
                "current_price": round(current_price, 2),
                "current_value": round(current_value, 2),
                "weight": 0,
                "sector": "N/A",
                "industry": "N/A",
                "market_cap": None,
                "pe_ratio": None,
                "forward_pe": None,
                "dividend_yield": None,
                "beta": None,
                "fifty_two_week_high": None,
                "fifty_two_week_low": None,
            }
        )

    return result


def enrich_holdings(holdings: list[Holding]) -> list[dict]:
    """Full enrichment with fundamental data — uses cached .info calls.
    Used for AI analysis only."""
    # First get prices via the lightweight batch call
    priced = get_prices(holdings)

    # Then layer on fundamental data from cached .info
    for item in priced:
        info = _get_cached_info(item["ticker"])
        # Override price if .info has a more accurate one
        if info.get("currentPrice"):
            cp = info["currentPrice"]
            item["current_price"] = round(cp, 2)
            item["current_value"] = round(item["shares"] * cp, 2)

        item["market_cap"] = info.get("marketCap")
        item["pe_ratio"] = info.get("trailingPE")
        item["forward_pe"] = info.get("forwardPE")
        item["dividend_yield"] = info.get("dividendYield")
        item["beta"] = info.get("beta")
        item["sector"] = info.get("sector", "N/A")
        item["industry"] = info.get("industry", "N/A")
        item["fifty_two_week_high"] = info.get("fiftyTwoWeekHigh")
        item["fifty_two_week_low"] = info.get("fiftyTwoWeekLow")

    return priced
