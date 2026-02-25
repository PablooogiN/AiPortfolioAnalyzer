"""One-shot example input and per-strategy example outputs.

The shared EXAMPLE_INPUT and strategy-specific EXAMPLE_OUTPUTS are injected
into the ChatPromptTemplate as a human/AI message pair so the model follows
a consistent four-section format.
"""

EXAMPLE_INPUT = """\
## My Portfolio (Total Invested Value: $17,793.00, Total Including Cash: $27,793.00)

| Ticker | Shares | Account Type | Current Price | Value | Weight | Sector |
|--------|--------|--------------|---------------|-------|--------|--------|
| AAPL | 50 | post-tax | $178.50 | $8,925.00 | 50.2% | Technology |
| JNJ | 30 | pre-tax | $155.20 | $4,656.00 | 26.2% | Healthcare |
| XOM | 40 | post-tax | $105.30 | $4,212.00 | 23.7% | Energy |

## Cash Positions

- Pre-tax (e.g. 401k/IRA): $5,000.00
- Post-tax (taxable brokerage): $5,000.00
- Total cash: $10,000.00

## Key Market Data

- **AAPL** (Consumer Electronics): P/E 28.5, Fwd P/E 26.1, Div Yield 0.55%, Beta 1.21, Market Cap $2800.0B, 52w Range $140.00\u2013$182.00
- **JNJ** (Pharmaceuticals): P/E 15.2, Fwd P/E 14.8, Div Yield 3.10%, Beta 0.55, Market Cap $375.0B, 52w Range $148.00\u2013$175.00
- **XOM** (Oil & Gas): P/E 12.1, Fwd P/E 11.5, Div Yield 3.40%, Beta 0.90, Market Cap $430.0B, 52w Range $80.00\u2013$112.00

Please analyze this portfolio and provide 3-5 specific, actionable recommendations. Be concrete -- mention specific tickers to buy, sell, or adjust. Consider the tax implications of each account type when making recommendations (e.g., tax-efficient placement of assets). Format your response in well-structured markdown. Do not add any additional filler or additional information, respond simply with the recommendation. Do not use any emojis."""


EXAMPLE_OUTPUTS: dict[str, str] = {
    # ── Value Investing ────────────────────────────────────────
    "value": """\
## Portfolio Summary

A concentrated 3-stock portfolio with $17,793 invested and $10,000 in cash reserves. The portfolio leans toward large-cap established names with reasonable valuations, though sector diversification is limited to three sectors. The substantial cash position provides flexibility for new value opportunities.

## Key Findings

- **AAPL** trades at a P/E of 28.5, well above the S&P 500 average of ~21. The current price sits near the top of its 52-week range ($140-$182), leaving limited margin of safety. Held in a post-tax account, any trim would trigger capital gains.
- **JNJ** at P/E 15.2 with a 3.10% dividend yield represents classic value territory. Held in a pre-tax account, the dividend income grows tax-deferred -- ideal placement.
- **XOM** offers the strongest value metrics: P/E 12.1, forward P/E 11.5, and a 3.40% yield. However, its 3.40% dividend in a post-tax account creates unnecessary tax drag.
- **$10,000 in cash** ($5K pre-tax, $5K post-tax) is available to deploy into undervalued opportunities.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Trim 20-30% of the position. At P/E 28.5 and near its 52-week high, AAPL is priced for perfection. Lock in some gains and redeploy capital to cheaper names. |
| 2 | HOLD | JNJ | Hold at current size. P/E 15.2 and Fwd P/E 14.8 suggest the market has priced in near-term headwinds. The 3.1% yield growing tax-deferred in the pre-tax account is ideal. |
| 3 | ADD | XOM | Add 10-15 shares in your pre-tax account using the $5K pre-tax cash. At P/E 12.1 and yielding 3.4%, XOM offers a margin of safety and the dividend would be better sheltered from taxes. |
| 4 | BUY | BRK.B | Initiate a position in Berkshire Hathaway in your post-tax account using post-tax cash. P/E around 14, no dividend (tax-efficient for taxable accounts), massive cash reserves, and excellent capital allocation. |

## Risk Warnings

- Portfolio holds only 3 stocks, creating significant single-stock risk. Target at least 8-12 positions for adequate diversification.
- No exposure to financials, utilities, or real estate sectors.
- 100% US large-cap allocation with no international diversification.""",

    # ── Growth Investing ───────────────────────────────────────
    "growth": """\
## Portfolio Summary

A $17,793 portfolio with $10,000 in cash but limited growth exposure. The three holdings are mature, large-cap companies. The portfolio is missing high-growth sectors like cloud computing, AI, and biotech. The cash reserves should be deployed into growth names, preferably in the post-tax account for long-term capital gains treatment.

## Key Findings

- **AAPL** has the strongest growth profile here with a forward P/E of 26.1, but its consumer electronics segment is mature. Revenue growth has slowed to single digits. Appropriately held in a post-tax account for long-term capital gains.
- **JNJ** is a defensive healthcare name, not a growth stock. Revenue growth is low single digits. Held in a pre-tax account, it occupies space that could be used for higher-growth, tax-inefficient names.
- **XOM** is a cyclical energy play. The forward P/E of 11.5 reflects the market's view that current earnings are near-peak. Not a growth investment.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | HOLD | AAPL | Hold the position. AAPL's services segment is growing at 15%+ and provides recurring revenue. Well-placed in the post-tax account for long-term gains. |
| 2 | TRIM | JNJ | Trim 50% of the position. JNJ's low-single-digit growth does not justify a 26.2% portfolio weight in a growth-oriented strategy. Keep some for stability. |
| 3 | SELL | XOM | Sell the entire position. Energy is inherently cyclical and XOM's growth prospects are limited. |
| 4 | BUY | NVDA | Initiate a position in NVIDIA in your post-tax account. The AI infrastructure buildout is a multi-year growth driver with revenue growing 60%+ year over year. Growth stocks benefit from long-term capital gains in taxable accounts. |
| 5 | BUY | AMZN | Initiate a position in Amazon in your post-tax account. AWS cloud growth, advertising expansion, and margin improvement create a compelling multi-engine growth story. |

## Risk Warnings

- Shifting to growth stocks will increase portfolio volatility and beta significantly.
- Growth stocks are more sensitive to interest rate changes and multiple compression.
- The suggested sells (JNJ, XOM) would eliminate all dividend income from the portfolio.""",

    # ── Dividend Income ────────────────────────────────────────
    "dividend": """\
## Portfolio Summary

A $17,793 portfolio with $10,000 in cash generating modest dividend income. JNJ (3.10% yield) and XOM (3.40% yield) are solid income producers, but AAPL's 0.55% yield drags the blended yield down. The cash reserves should be deployed into dividend payers, ideally in the pre-tax account to shelter dividend income from taxes.

## Key Findings

- **AAPL** yields just 0.55%, making it one of the lowest-yielding mega-caps. The payout ratio is low (~15%) and the yield is too thin for income purposes.
- **JNJ** is a Dividend King with 60+ consecutive years of dividend increases. The 3.10% yield at P/E 15.2 is well-covered. Ideally placed in the pre-tax account where dividends grow tax-deferred.
- **XOM** yields 3.40% with strong dividend history, but it is in a post-tax account where dividends are taxed annually -- not ideal for a high-yield holding.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Trim 50-70% of the AAPL position. At 0.55% yield, it contributes almost nothing to income. Redeploy into higher-yielding names. |
| 2 | ADD | JNJ | Add 15-20 shares in the pre-tax account using pre-tax cash. At P/E 15.2 and yielding 3.10%, JNJ is attractively priced. Keeping dividends in pre-tax maximizes tax-deferred compounding. |
| 3 | HOLD | XOM | Hold the full position. The 3.40% yield is well-covered. Consider moving future XOM purchases to the pre-tax account to shelter the high dividend. |
| 4 | BUY | O | Initiate a position in Realty Income (O) in your pre-tax account. Monthly dividend payer yielding approximately 5.5%. REIT dividends are taxed as ordinary income, so pre-tax placement is essential. |
| 5 | BUY | PEP | Initiate a position in PepsiCo in your post-tax account. Dividend Aristocrat yielding around 2.9% with qualified dividends that receive favorable tax treatment in taxable accounts. |

## Risk Warnings

- High-yield strategies can become yield traps if dividend cuts occur. Always verify payout ratios and free cash flow coverage.
- Concentrating in dividend stocks often means overweighting utilities, REITs, and consumer staples, which may underperform in growth-driven markets.
- REIT dividends (like O) are taxed as ordinary income -- place these in pre-tax accounts when possible.""",

    # ── Risk & Diversification ─────────────────────────────────
    "risk": """\
## Portfolio Summary

A highly concentrated $17,793 portfolio with only 3 holdings across 3 sectors, plus $10,000 in cash. While the cash provides a buffer, the invested portion carries substantial single-stock risk and lacks diversification across geography, market cap, and asset class.

## Key Findings

- **Concentration risk is severe.** AAPL alone is 50.2% of the invested portfolio. A single negative earnings report could materially impact overall value.
- **Sector exposure is narrow.** Technology (50.2%), Healthcare (26.2%), and Energy (23.7%) cover only 3 of 11 GICS sectors. No exposure to financials, industrials, consumer discretionary, utilities, or real estate.
- **Beta profile is moderate.** AAPL (1.21) pulls the portfolio beta up, while JNJ (0.55) anchors it. XOM (0.90) is near market. The blended beta is approximately 0.92.
- **Tax diversification is good.** Holdings span both pre-tax and post-tax accounts, providing flexibility for tax-efficient rebalancing.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Reduce to a max 25% position weight. At 50.2%, a single stock has outsized impact on portfolio returns. |
| 2 | BUY | VTI | Add a broad US total market ETF in your post-tax account. Low turnover makes it tax-efficient. This instantly diversifies across 4,000+ stocks and all 11 sectors. |
| 3 | BUY | VXUS | Add an international equity ETF in your post-tax account. Allocate 15-20% to non-US markets to reduce geographic concentration. Foreign tax credits benefit taxable accounts. |
| 4 | BUY | BND | Add a bond ETF in your pre-tax account. Bond interest is taxed as ordinary income, so pre-tax placement is ideal. This reduces overall portfolio volatility. |

## Risk Warnings

- With only 3 holdings, a 20% drop in AAPL alone reduces the portfolio by over 10%. With 15+ holdings, the impact would be under 1.3%.
- The portfolio has zero fixed-income or alternative exposure, making it 100% correlated to equity markets.
- No small-cap or mid-cap exposure means missing a significant return driver over long time horizons.""",

    # ── Index Comparison ───────────────────────────────────────
    "index": """\
## Portfolio Summary

A $17,793 portfolio that bears little resemblance to the S&P 500 index. With only 3 holdings, the portfolio has extreme tracking error relative to any broad benchmark. The $10,000 cash position could be efficiently deployed into index funds.

## Key Findings

- **Technology underweight.** AAPL at 50.2% of invested value is the only tech holding, but the portfolio is missing MSFT, GOOGL, NVDA, META which collectively make up ~20% of the S&P 500.
- **Healthcare underweight.** JNJ at 26.2% is high for one stock, but the S&P has ~13% across dozens of healthcare names.
- **Energy overweight.** XOM at 23.7% vs the S&P 500 energy weight of approximately 4%. This is a massive sector bet.
- **Missing sectors entirely.** No exposure to financials (~13% of S&P), consumer discretionary (~10%), industrials (~9%), or six other sectors.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | BUY | VOO | Deploy the $10,000 cash into an S&P 500 index fund. Place primarily in the post-tax account -- VOO's low turnover and qualified dividends are tax-efficient. This provides instant broad-market exposure. |
| 2 | HOLD | AAPL | Keep AAPL as a satellite holding but trim to 10% max of total portfolio. It is already the largest S&P 500 constituent. |
| 3 | SELL | JNJ | Sell JNJ and let the index fund provide healthcare exposure across dozens of names instead of concentrating in one. |
| 4 | SELL | XOM | Sell XOM. At 23.7% of your portfolio vs 4% in the index, you are making a large energy sector bet. Let the index fund handle sector allocation. |

## Risk Warnings

- This portfolio currently has extreme tracking error vs the S&P 500, meaning annual returns will deviate wildly from the benchmark.
- With 3 stocks you are taking on substantial uncompensated idiosyncratic risk.
- A core-satellite approach (60% index + 40% individual picks) would dramatically reduce risk while still allowing for active conviction bets.""",
}
