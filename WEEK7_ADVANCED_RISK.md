# Week 7 — Advanced Risk Management

## Prerequisites
- RL bot (risky2) must be fully designed and integrated
- Week 6 risk management upgrade must be complete (see WEEK6_RISK_PLAN.md)

## Planned Improvements

### 1. ATR-Based Dynamic Kill Switch
Replace static 15%/30% drawdown thresholds with volatility-adjusted ones.
Current ATR is already computed in features.py — feed it into risk.py.
If market ATR doubles, the kill switch threshold widens to avoid triggering
on noise. If market is flat/low volatility, threshold tightens.
This prevents false positives during high volatility regimes.

### 2. Equity Curve Trading
Treat the bot's own performance as a tradeable signal.
Compute a rolling 10-day MA and 30-day MA of the bot's daily returns.
If 10-day MA crosses below 30-day MA, pause trading.
Resume when 10-day MA crosses back above 30-day MA.
Prevents the bot from bleeding out during regimes it wasn't trained for.
Data source: SQLite trade logs already being recorded.

### 3. Streamlit Dashboard Upgrade
Add two new graphs to streamlit_app.py:
- Equity curve over time (cumulative PnL)
- Drawdown curve over time
These two graphs together are the first thing a professional trader
looks at to decide if a bot is broken or just having a bad day.
Data source: SQLite trade logs.

## Implementation Order
1. ATR-based kill switch (metrics/risk.py upgrade)
2. Equity curve trading logic (new section in metrics/risk.py)
3. Dashboard graphs (dashboard/streamlit_app.py upgrade)

## Notes
- ATR already available in features.py — no new data needed
- Equity curve data already in SQLite — no new logging needed
- Dashboard upgrade is additive — existing tables stay as is

## Readme
Make sure to update readme to reflect newer updates