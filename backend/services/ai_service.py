import re

from services.chain_factory import build_chain


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
            f"52w Range {low}\u2013{high}"
        )
    return "\n".join(lines)


def _build_user_message(holdings: list[dict]) -> str:
    total_value = sum(h["current_value"] for h in holdings)
    total_cost = sum(h["shares"] * h["avg_cost"] for h in holdings)
    total_gl = total_value - total_cost
    total_gl_pct = (total_gl / total_cost * 100) if total_cost else 0

    return (
        f"## My Portfolio (Total Value: ${total_value:,.2f}, "
        f"Overall Gain/Loss: {'+' if total_gl >= 0 else ''}{total_gl_pct:.1f}%)\n\n"
        f"{_build_portfolio_table(holdings)}\n\n"
        f"## Key Market Data\n\n"
        f"{_build_market_data(holdings)}\n\n"
        f"Please analyze this portfolio and provide 3-5 specific, actionable "
        f"recommendations. Be concrete \u2014 mention specific tickers to buy, sell, "
        f"or adjust. Format your response in well-structured markdown. "
        f"Do not add any additional filler or additional information, "
        f"respond simply with the recommendation. Do not use any emojis."
    )


def _parse_response(text: str) -> dict:
    """Parse the AI markdown response into structured sections."""
    # Split on ## headings
    sections: dict[str, str] = {}
    current_key = ""
    current_lines: list[str] = []

    for line in text.split("\n"):
        if line.startswith("## "):
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            heading = line[3:].strip().lower()
            if "summary" in heading:
                current_key = "summary"
            elif "finding" in heading:
                current_key = "key_findings"
            elif "recommendation" in heading:
                current_key = "recommendations"
            elif "risk" in heading or "warning" in heading:
                current_key = "risk_warnings"
            else:
                current_key = heading
            current_lines = []
        else:
            current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    # Parse summary
    summary = sections.get("summary", "")

    # Parse key findings (bullet points)
    key_findings = []
    for line in sections.get("key_findings", "").split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            key_findings.append(line[2:].strip())
        elif line and not line.startswith("|") and not line.startswith("#"):
            key_findings.append(line)

    # Parse recommendations table
    recommendations = []
    rec_text = sections.get("recommendations", "")
    # Match table rows: | # | ACTION | TICKER | rationale |
    row_pattern = re.compile(
        r"\|\s*\d+\s*\|\s*(\w+)\s*\|\s*([A-Z.]+(?:\s*[A-Z.]*)?)\s*\|\s*(.*?)\s*\|"
    )
    for match in row_pattern.finditer(rec_text):
        recommendations.append(
            {
                "action": match.group(1).strip().upper(),
                "ticker": match.group(2).strip(),
                "rationale": match.group(3).strip(),
            }
        )

    # Parse risk warnings (bullet points)
    risk_warnings = []
    for line in sections.get("risk_warnings", "").split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            risk_warnings.append(line[2:].strip())
        elif line and not line.startswith("|") and not line.startswith("#"):
            risk_warnings.append(line)

    return {
        "summary": summary,
        "key_findings": key_findings,
        "recommendations": recommendations,
        "risk_warnings": risk_warnings,
    }


async def analyze(holdings: list[dict], strategy_key: str) -> dict:
    """Run the AI analysis and return parsed structured JSON."""
    chain = build_chain(strategy_key)
    user_input = _build_user_message(holdings)

    result = await chain.ainvoke({"user_input": user_input})
    raw_text = result.content if hasattr(result, "content") else str(result)

    return _parse_response(raw_text)
