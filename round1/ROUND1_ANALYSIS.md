# Round 1 - Full Data Capsule + Naive v1 Results Analysis

**For:** Opus strategy development  
**Source Files:** ROUND_1.zip (3 days historical), 179465.zip (naive v1 backtest)

---

## TL;DR for Opus

INTARIAN_PEPPER_ROOT goes up ~1,000 points every single day (+8-10% per day). This is not noise, it is a relentless uptrend across all 3 historical days. The naive market-maker fought this trend and barely broke even. ASH_COATED_OSMIUM is flat noise around 10,000 with a 16-point spread, perfect for market-making. The winning strategy is: go long INTARIAN_PEPPER_ROOT aggressively and market-make ASH_COATED_OSMIUM.

---

## Historical Data (3 Days from Data Capsule)

### INTARIAN_PEPPER_ROOT - THE TREND MACHINE

| Day | Open | Close | Change | Change % |
|-----|------|-------|--------|----------|
| -2 | 9,998.5 | 11,001.5 | +1,003.0 | +10.032% |
| -1 | 10,998.5 | 11,998.0 | +999.5 | +9.088% |
| 0 | 11,998.5 | 13,000.0 | +1,001.5 | +8.347% |
| **3-Day Total** | 9,998.5 | 13,000.0 | +3,001.5 | **+30.020%** |

Key characteristics:
- Gains ~1,000 points per day (nearly linear)
- Low per-tick volatility (0.027% std dev) -- smooth trend, not choppy
- Spread: 2-21 points (avg ~13)
- ~335 trades per day, avg size 5.2 units
- Price range per day: ~1,010 points
- Opens near prior close each day (no gaps)

### ASH_COATED_OSMIUM - THE MEAN REVERTER

| Day | Open | Close | Change | Change % |
|-----|------|-------|--------|----------|
| -2 | 10,010.0 | 9,993.5 | -16.5 | -0.165% |
| -1 | 10,003.0 | 10,002.0 | -1.0 | -0.010% |
| 0 | 10,013.0 | 10,007.0 | -6.0 | -0.060% |
| **3-Day Total** | 10,010.0 | 10,007.0 | -3.0 | **-0.030%** |

Key characteristics:
- Essentially flat over 3 days (< 0.1% total move)
- Per-tick volatility: 0.037% std dev -- noisy but range-bound
- Spread: 5-22 points (avg ~16)
- ~420 trades per day, avg size 5.2 units
- Price range per day: ~40 points (tight)
- Mean-reverts around ~10,000

---

## Naive v1 Backtest Results (179465)

### Overall
- **Final Profit: 865.59 XIRECs** (target: 200,000)
- Achievement: 0.43%

### Per Product
- ASH_COATED_OSMIUM: +928.78 XIRECs (market-making worked)
- INTARIAN_PEPPER_ROOT: -63.19 XIRECs (fought the trend, lost)

### What the Naive Strategy Did
- Symmetric market-making: equal buy and sell orders around mid-price
- Tight spreads: 1 point for INTARIAN_PEPPER_ROOT, 2 points for ASH_COATED_OSMIUM
- Aggressive fill on mispriced orders (buy below mid, sell above mid)
- EMA tracking for ASH_COATED_OSMIUM (unused for bias)
- Position limit: 80 units per product respected

### Why It Failed
The strategy treated both products identically as mean-reverting. INTARIAN_PEPPER_ROOT is NOT mean-reverting -- it trends +1,000 points per day. The symmetric asks (sell orders) were filled constantly as price rose, building short exposure on a rising asset. The strategy was underwater by end of round.

---

## Position Limits and Constraints

| Product | Position Limit |
|---------|---------------|
| ASH_COATED_OSMIUM | 80 |
| INTARIAN_PEPPER_ROOT | 80 |

---

## Profit Potential Estimates

### INTARIAN_PEPPER_ROOT (Trend Following)
- Daily move: ~1,000 points
- Position limit: 80 units
- If max long at open, hold to close: 80 x 1,000 = **80,000 XIRECs per day**
- Over 2 trading days to hit target: **160,000 XIRECs**
- Challenge: can't buy 80 units instantly, need to accumulate

### ASH_COATED_OSMIUM (Market Making)
- Avg spread: ~16 points
- If capturing half-spread per trade: ~8 points
- ~420 trades/day at avg 5 units: ~2,100 units traded
- Potential: 2,100 x 8 = **16,800 XIRECs per day**
- More realistically with competition: **5,000-10,000 per day**

### Combined Realistic Target
- INTARIAN_PEPPER_ROOT trend: 40,000-80,000/day
- ASH_COATED_OSMIUM MM: 5,000-10,000/day
- **Estimated achievable: 100,000-150,000 over 2 days**
- Target is 200,000 so need to be aggressive

---

## Trade Flow Patterns (for strategy timing)

### INTARIAN_PEPPER_ROOT
- ~335 trades per day
- Avg trade size: 5.2 units
- One trade roughly every 300 timestamps (30 seconds if 100ms ticks)
- Price increments are small but consistent (smooth ramp up)

### ASH_COATED_OSMIUM
- ~420 trades per day
- Avg trade size: 5.2 units
- More frequent trading (every ~240 timestamps)
- Prices oscillate in tight band, good for capturing bid-ask

---

## Critical Insights for Opus

1. **INTARIAN_PEPPER_ROOT is free money if you go long early.** The trend is unambiguous across all 3 historical days. Buy at open, accumulate to position limit, hold. The only risk is if the pattern breaks on the live round.

2. **ASH_COATED_OSMIUM is a spread-capture product.** Don't try to predict direction. Place resting orders at best bid -1 and best ask +1 and collect the spread when they fill.

3. **The naive strategy's main error was symmetry.** It placed equal buy/sell orders for INTARIAN_PEPPER_ROOT when it should have been buy-only (or heavily buy-biased).

4. **Position management matters.** With a limit of 80, you need to buy INTARIAN_PEPPER_ROOT early in the day and hold. Don't sell it back -- every unit sold is a unit of missed trend profit.

5. **The backtest only ran Day 0 with 1000 snapshots (not 10,000).** The data capsule shows ~10,000 snapshots per day per product. The naive strategy's low profit is partly from running a shorter test, but primarily from fighting the trend.

6. **No fees detected.** The sum of product PnLs exactly matched the reported final profit (865.59). No hidden fees on these products.

---

## Files in This Analysis

| File | Purpose |
|------|---------|
| `round1/submissions/round1_naive_v1.py` | The naive market-maker (1st submission) |
| `round1/data/179465.zip` | Backtest results from naive v1 |
| `round1/data/ROUND_1.zip` | Historical data capsule (3 days) |
| `round1/ROUND1_ANALYSIS.md` | Quick analysis of naive results |
| `round1/ROUND1_DATA_ANALYSIS.md` | This file -- full data + strategy brief |
| `tools/log_parser.py` | Log parsing utility |
| `datamodel.py` | IMC Prosperity API reference |
