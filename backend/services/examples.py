"""One-shot example input and per-strategy example outputs.

The shared EXAMPLE_INPUT and strategy-specific EXAMPLE_OUTPUTS are injected
into the ChatPromptTemplate as a human/AI message pair so the model follows
a consistent four-section format.
"""

EXAMPLE_INPUT = """\
## My Portfolio (Total Value: $52,340.00, Overall Gain/Loss: +12.3%)

| Ticker | Shares | Avg Cost | Current Price | Value | Weight | Gain/Loss | Sector |
|--------|--------|----------|---------------|-------|--------|-----------|--------|
| AAPL | 50 | $142.00 | $178.50 | $8,925.00 | 17.1% | +25.7% | Technology |
| JNJ | 30 | $165.00 | $155.20 | $4,656.00 | 8.9% | -5.9% | Healthcare |
| XOM | 40 | $85.00 | $105.30 | $4,212.00 | 8.0% | +23.9% | Energy |

## Key Market Data

- **AAPL** (Consumer Electronics): P/E 28.5, Fwd P/E 26.1, Div Yield 0.55%, Beta 1.21, Market Cap $2800.0B, 52w Range $140.00-$182.00
- **JNJ** (Pharmaceuticals): P/E 15.2, Fwd P/E 14.8, Div Yield 3.10%, Beta 0.55, Market Cap $375.0B, 52w Range $148.00-$175.00
- **XOM** (Oil & Gas): P/E 12.1, Fwd P/E 11.5, Div Yield 3.40%, Beta 0.90, Market Cap $430.0B, 52w Range $80.00-$112.00

Please analyze this portfolio and provide 3-5 specific, actionable recommendations. Be concrete -- mention specific tickers to buy, sell, or adjust. Format your response in well-structured markdown. Do not add any additional filler or additional information, respond simply with the recommendation. Do not use any emojis."""


EXAMPLE_OUTPUTS: dict[str, str] = {
    # ── Value Investing ────────────────────────────────────────
    "value": """\
## Portfolio Summary

A concentrated 3-stock portfolio valued at $52,340 with a healthy +12.3% overall return. The portfolio leans toward large-cap established names with reasonable valuations, though sector diversification is limited to three sectors.

## Key Findings

- **AAPL** trades at a P/E of 28.5, well above the S&P 500 average of ~21. The +25.7% gain is attractive, but the current price sits near the top of its 52-week range ($140-$182), leaving limited margin of safety.
- **JNJ** at P/E 15.2 with a 3.10% dividend yield represents classic value territory. The -5.9% loss is modest and the forward P/E of 14.8 suggests slight earnings growth ahead.
- **XOM** offers the strongest value metrics: P/E 12.1, forward P/E 11.5, and a 3.40% yield. At $105.30, it is comfortably within its 52-week range and has delivered +23.9%.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Trim 20-30% of the position. At P/E 28.5 and near its 52-week high, AAPL is priced for perfection. Lock in some gains and redeploy capital to cheaper names. |
| 2 | HOLD | JNJ | Hold at current size. P/E 15.2 and Fwd P/E 14.8 suggest the market has priced in near-term headwinds. The 3.1% yield provides downside support while you wait for a recovery. |
| 3 | ADD | XOM | Add 10-15 shares. At P/E 12.1 and yielding 3.4%, XOM offers a margin of safety even if energy prices soften moderately. |
| 4 | BUY | BRK.B | Initiate a position in Berkshire Hathaway. P/E around 14, no dividend drag, massive cash reserves, and excellent capital allocation track record. |

## Risk Warnings

- Portfolio holds only 3 stocks, creating significant single-stock risk. Target at least 8-12 positions for adequate diversification.
- No exposure to financials, utilities, or real estate sectors.
- 100% US large-cap allocation with no international diversification.""",

    # ── Growth Investing ───────────────────────────────────────
    "growth": """\
## Portfolio Summary

A $52,340 portfolio with solid +12.3% returns but limited growth exposure. The three holdings are mature, large-cap companies. The portfolio is missing high-growth sectors like cloud computing, AI, and biotech.

## Key Findings

- **AAPL** has the strongest growth profile here with a forward P/E of 26.1, but its consumer electronics segment is mature. Revenue growth has slowed to single digits. The +25.7% gain has been driven more by buybacks and multiple expansion than top-line acceleration.
- **JNJ** is a defensive healthcare name, not a growth stock. Revenue growth is low single digits and the pharmaceutical pipeline, while deep, is not translating to earnings momentum. The -5.9% loss reflects this stagnation.
- **XOM** is a cyclical energy play. The +23.9% gain was driven by commodity prices, not structural growth. Forward P/E of 11.5 reflects the market's view that current earnings are near-peak.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | HOLD | AAPL | Hold the position. AAPL's services segment is growing at 15%+ and provides recurring revenue. The installed base of 2B+ devices is a growth platform, even if hardware growth has slowed. |
| 2 | TRIM | JNJ | Trim 50% of the position. JNJ's low-single-digit growth does not justify a 8.9% portfolio weight in a growth-oriented strategy. Redeploy into higher-growth names. |
| 3 | SELL | XOM | Sell the entire position. Energy is inherently cyclical and XOM's growth prospects are limited. The +23.9% gain is a good exit point. |
| 4 | BUY | NVDA | Initiate a position in NVIDIA. The AI infrastructure buildout is a multi-year growth driver with revenue growing 60%+ year over year. |
| 5 | BUY | AMZN | Initiate a position in Amazon. AWS cloud growth, advertising expansion, and margin improvement create a compelling multi-engine growth story. |

## Risk Warnings

- Shifting to growth stocks will increase portfolio volatility and beta significantly.
- Growth stocks are more sensitive to interest rate changes and multiple compression.
- The suggested sells (JNJ, XOM) would eliminate all dividend income from the portfolio.""",

    # ── Dividend Income ────────────────────────────────────────
    "dividend": """\
## Portfolio Summary

A $52,340 portfolio generating modest dividend income. JNJ (3.10% yield) and XOM (3.40% yield) are solid income producers, but AAPL's 0.55% yield drags the portfolio's blended yield down. The overall portfolio yield is approximately 1.9%, below the 2.5-3.0% target for an income-focused strategy.

## Key Findings

- **AAPL** yields just 0.55%, making it one of the lowest-yielding mega-caps. While AAPL has grown its dividend consistently, the payout ratio is low (~15%) and the yield is too thin for income purposes.
- **JNJ** is a Dividend King with 60+ consecutive years of dividend increases. The 3.10% yield at P/E 15.2 is well-covered by earnings, with a payout ratio around 47%.
- **XOM** yields 3.40% with a strong history of dividend maintenance even through oil price downturns. The payout ratio is approximately 41% at current earnings, leaving ample room for continued payments.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Trim 50-70% of the AAPL position. At 0.55% yield, it contributes almost nothing to income. Redeploy into higher-yielding names that still offer growth. |
| 2 | ADD | JNJ | Add 15-20 shares. At P/E 15.2 and yielding 3.10%, JNJ is attractively priced for income investors. The -5.9% dip is a buying opportunity for a Dividend King. |
| 3 | HOLD | XOM | Hold the full position. The 3.40% yield is well-covered and XOM has maintained or grown its dividend for 40+ years. |
| 4 | BUY | O | Initiate a position in Realty Income (O). Monthly dividend payer yielding approximately 5.5%, with 25+ years of consecutive increases. Adds real estate sector exposure. |
| 5 | BUY | PEP | Initiate a position in PepsiCo. Dividend Aristocrat yielding around 2.9% with 50+ years of consecutive increases and stable consumer staples cash flows. |

## Risk Warnings

- High-yield strategies can become yield traps if dividend cuts occur. Always verify payout ratios and free cash flow coverage.
- Concentrating in dividend stocks often means overweighting utilities, REITs, and consumer staples, which may underperform in growth-driven markets.
- Rising interest rates can make dividend stocks less attractive relative to bonds.""",

    # ── Risk & Diversification ─────────────────────────────────
    "risk": """\
## Portfolio Summary

A highly concentrated $52,340 portfolio with only 3 holdings across 3 sectors. While the +12.3% return is solid, the portfolio carries substantial single-stock risk and lacks diversification across geography, market cap, and asset class.

## Key Findings

- **Concentration risk is severe.** AAPL alone is 17.1% of the portfolio, and the top holding drives overall returns. A single negative earnings report could materially impact the portfolio.
- **Sector exposure is narrow.** Technology (17.1%), Healthcare (8.9%), and Energy (8.0%) cover only 34% of the portfolio's invested capital across just 3 of 11 GICS sectors. No exposure to financials, industrials, consumer discretionary, utilities, or real estate.
- **Beta profile is moderate.** AAPL (1.21) pulls the portfolio beta up, while JNJ (0.55) anchors it. XOM (0.90) is near market. The blended beta is approximately 0.92, close to market but driven by few data points.
- **Geographic risk:** 100% US equities with no international diversification.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | TRIM | AAPL | Reduce to a 10% max position weight. At 17.1%, a single stock has outsized impact on portfolio returns. Cap individual positions at 10%. |
| 2 | BUY | VTI | Add a broad US total market ETF. This instantly diversifies across 4,000+ stocks and all 11 sectors, reducing single-stock risk dramatically. |
| 3 | BUY | VXUS | Add an international equity ETF. Allocate 15-20% to non-US developed and emerging markets to reduce geographic concentration. |
| 4 | BUY | BND | Add a bond ETF for 10-15% of the portfolio. This reduces overall portfolio volatility and provides a buffer during equity drawdowns. |

## Risk Warnings

- With only 3 holdings, a 20% drop in any single stock reduces the portfolio by 1.6-3.4%. With 15+ holdings, the same drop costs less than 1.3%.
- The portfolio has zero fixed-income or alternative exposure, making it 100% correlated to equity markets.
- No small-cap or mid-cap exposure means missing a significant return driver over long time horizons.""",

    # ── Index Comparison ───────────────────────────────────────
    "index": """\
## Portfolio Summary

A $52,340 portfolio that bears little resemblance to the S&P 500 index. With only 3 holdings, the portfolio has extreme tracking error relative to any broad benchmark. The +12.3% return is competitive but carries far more idiosyncratic risk than an index approach.

## Key Findings

- **Technology underweight.** AAPL at 17.1% is the only tech holding. The S&P 500 has approximately 30% in technology. Missing entirely: MSFT, GOOGL, NVDA, META.
- **Healthcare underweight.** JNJ at 8.9% vs the S&P 500 healthcare weight of approximately 13%. Only one name in a sector with dozens of index constituents.
- **Energy overweight.** XOM at 8.0% vs the S&P 500 energy weight of approximately 4%. This is a meaningful sector bet.
- **Missing sectors entirely.** No exposure to financials (~13% of S&P), consumer discretionary (~10%), industrials (~9%), communication services (~9%), or five other sectors.

## Recommendations

| # | Action | Ticker | Rationale |
|---|--------|--------|-----------|
| 1 | BUY | VOO | Allocate 50-60% of the portfolio to an S&P 500 index fund. This provides instant broad-market exposure and eliminates the need to pick individual stocks for the core allocation. |
| 2 | HOLD | AAPL | Keep AAPL as a satellite holding (10% max) if you have conviction. It is already the largest S&P 500 constituent, so you are effectively overweighting it. |
| 3 | SELL | JNJ | Sell JNJ and let the index fund provide healthcare exposure across dozens of names instead of concentrating in one. |
| 4 | SELL | XOM | Sell XOM. At 8% of your portfolio vs 4% in the index, you are making a large energy sector bet. Let the index fund handle sector allocation. |

## Risk Warnings

- This portfolio currently has a tracking error of 15%+ vs the S&P 500, meaning annual returns will deviate wildly from the benchmark.
- With 3 stocks you are taking on substantial uncompensated idiosyncratic risk. The market does not reward you for single-stock risk.
- A core-satellite approach (60% index + 40% individual picks) would dramatically reduce risk while still allowing for active conviction bets.""",
}
