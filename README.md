# Algo Trading Competition

IMC Prosperity 4 - Algorithmic trading competition. Round-by-round strategy development, backtesting, and iteration.

## Round 1 - "Trading Groundwork" (1st Iteration)

### Products
- **ASH_COATED_OSMIUM** - Position limit: 80
- - **INTARIAN_PEPPER_ROOT** - Position limit: 80
 
  - ### Targetgic on ASH_COATED_OSMIUM captured small spread profits
  - - Position limits respected
    - - Order book parsing and fair value calculation
     
      - ### Next Iteration Needed
      - - Trend-following for INTARIAN_PEPPER_ROOT (buy and hold)
        - - Maintain market-making for ASH_COATED_OSMIUM
          - - Adaptive spreads based on volatility
            - - End-of-round position management
             
              - ## Project Structure
             
              - ```
                algo-trading-comp/
                ├── datamodel.py                    # IMC Prosperity API reference
                ├── round1/
                │   ├── submissions/
                │   │   └── round1_naive_v1.py      # 1st iteration naive market maker
                │   ├── backtests/                  # Backtest result archives
                │   ├── logs/                       # Activity logs
                │   ├── data/                       # Market data capsules
                │   ├── ROUND1_ANALYSIS.md          # Naive v1 results analysis
                │   └── ROUND1_DATA_ANALYSIS.md     # Full data capsule + strategy brief
                ├── tools/
                │   └── log_parser.py               # Log parsing utility
                └── docs/                           # Round PDFs and reference material
                ```

                ## Status

                | Round | Iteration | Profit | Target | Status |
                |-------|-----------|--------|--------|--------|
                | 1 | Naive v1 | 865.59 | 200,000 | Baseline established |
                | 1 | v2 (pending) | -- | 200,000 | Strategy development  |
  - Earn a net profit of **200,000 XIRECs** before the beginning of day 3.
 
  - ### 1st Iteration: Naive Market Maker (v1)
 
  - **Strategy:** Symmetric market-making around mid-price for both products. Aggressive fills on mispriced orders, passive resting orders with tight spreads.
 
  - **Result:** 865.59 XIRECs (0.43% of target)
 
  - | Product | PnL | Notes |
  - |---------|-----|-------|
  - | ASH_COATED_OSMIUM | +928.78 | Market-making worked on flat product |
  - | INTARIAN_PEPPER_ROOT | -63.19 | Fought a massive uptrend |
 
  - ### Key Findings from Data Analysis
 
  - **INTARIAN_PEPPER_ROOT** trends +1,000 points per day (~8-10%) across all 3 historical days. This is the primary profit source.
 
  - **ASH_COATED_OSMIUM** is flat noise around 10,000. Spread capture only.
 
  - ### What Failed
  - - Symmetric orders on a trending product = selling into rising prices
    - - No directional bias detection
      - - No position management for trend exposure
       
        - ### What Worked
        - - Market-making lo
