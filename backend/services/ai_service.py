import os
from collections.abc import AsyncGenerator

import anthropic

from services.strategies import get_strategy_prompt


def _build_portfolio_table(holdings: list[dict]) -> str:
    lines = [
        "| Ticker | Shares | Avg Cost | Current Price | Value | Weight | Gain/Loss | Sector |",
        "|--------|--------|----------|---------------|-------|--------|-----------|--------|",
    ]
    for h in holdings:
        sign = "+" if h["gain_loss"] >= 0 else ""
        lines.append(
            f"| {h['ticker']} | {h['shares']} | ${h['avg_cost']:.2f} | "
            f"${h['current_price']:.2f} | ${h['current_value']:,.2f} | "
            f"{h['weight']:.1f}% | {sign}{h['gain_loss_pct']:.1f}% | "
            f"{h['sector']} |"
        )
    return "\n".join(lines)


def _build_market_data(holdings: list[dict]) -> str:
    lines = []
    for h in holdings:
        pe = f"{h['pe_ratio']:.1f}" if h["pe_ratio"] else "N/A"
        fwd_pe = f"{h['forward_pe']:.1f}" if h["forward_pe"] else "N/A"
        div_yield = (
            f"{h['dividend_yield'] * 100:.2f}%" if h["dividend_yield"] else "N/A"
        )
        beta = f"{h['beta']:.2f}" if h["beta"] else "N/A"
        mc = f"${h['market_cap'] / 1e9:.1f}B" if h["market_cap"] else "N/A"
        high = f"${h['fifty_two_week_high']:.2f}" if h["fifty_two_week_high"] else "N/A"
        low = f"${h['fifty_two_week_low']:.2f}" if h["fifty_two_week_low"] else "N/A"

        lines.append(
            f"- **{h['ticker']}** ({h['industry']}): P/E {pe}, Fwd P/E {fwd_pe}, "
            f"Div Yield {div_yield}, Beta {beta}, Market Cap {mc}, "
            f"52w Range {low}–{high}"
        )
    return "\n".join(lines)


async def stream_analysis(
    holdings: list[dict], strategy_key: str
) -> AsyncGenerator[dict, None]:
    system_prompt = get_strategy_prompt(strategy_key)

    total_value = sum(h["current_value"] for h in holdings)
    total_cost = sum(h["shares"] * h["avg_cost"] for h in holdings)
    total_gl = total_value - total_cost
    total_gl_pct = (total_gl / total_cost * 100) if total_cost else 0

    user_message = (
        f"## My Portfolio (Total Value: ${total_value:,.2f}, "
        f"Overall Gain/Loss: {'+' if total_gl >= 0 else ''}{total_gl_pct:.1f}%)\n\n"
        f"{_build_portfolio_table(holdings)}\n\n"
        f"## Key Market Data\n\n"
        f"{_build_market_data(holdings)}\n\n"
        f"Please analyze this portfolio and provide 3-5 specific, actionable "
        f"recommendations. Be concrete — mention specific tickers to buy, sell, "
        f"or adjust. Format your response in well-structured markdown."
    )

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    model = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-6")

    with client.messages.stream(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield {"event": "message", "data": text}

    yield {"event": "done", "data": "[DONE]"}
