# Trading Bot

## Overview
A multiple strategy algorithmic trading system that compares grid trading, momentum breakout, and reinforcement learning across stocks and crypto with backtesting on historical data, keeping risk metrics, and having a live dashboard through Streamlit

## Strategies
**Stable:** Stable is intended to go for longer term gains and to be careful of going on short risks in stocks/etfs
**Risky1:** Risky1 is intended to go for short term gains in the stocks markets, going high risk high reward
**Risky2:** Risky2 is intended to go for short term gains in the cryptocurrency markets, going high risk high reward.


## Tech Stack
Alpaca - allows for paper trading
Polygon.io - Stock/ETF price data for stable and risky1
Kraken API- Crypto Price data provider for risky2
SQLite- SQL database provider
scikit-learn - supervised ml for stable and risky1
XGBoost - supervised ml for stable and risky1 bots
Stable Baselines3 - reinforcement learning for risky2
VectorBT- Engine to test models on historical data
Streamlit - Live dashboard to see performance

## Project Structure
```
.
./.env
./.git
./.gitignore
./DECISION_LOG.md
./README.md
./RESULTS.md
./backtesting
./backtesting/engine.py
./backtesting/results
./backtesting/run_backtest.py
./core
./core/config.py
./core/features.py
./core/logger.py
./dashboard
./dashboard/compare.py
./dashboard/streamlit_app.py
./data
./data/kraken_fetcher.py
./data/polygon_fetcher.py
./data/sentiment_fetcher.py
./metrics
./metrics/risk.py
./models
./models/regime_detector.py
./models/retrain.py
./models/rl_environment.py
./models/rl_train.py
./models/train.py
./paper_trading
./paper_trading/alpaca_paper.py
./requirements.txt
./run.py
./strategies
./strategies/risky1.py
./strategies/risky2.py
./strategies/stable.py
./tests
./tests/test_backtesting.py
./tests/test_features.py
./tests/test_risk.py

```

## Setup
Not ready for set up yet

## Progress

### In Progress:
- data/kraken_fetcher.py- fetch historical and live data relating to crypto from kraken
### Completed Parts:
- core/config.py - This provides the configuration of the system and what are the providers
- core/logger.py - Creates database and provides functions to initialize the database tables, log each trade, and get past trades from database
- core/features.py- shared feature engineering for all 3 strategy bots. Computed rolling averages, RSI, momentum, Bollinger Bands, ATR, z-score, and volume indicators from raw data with open, high, low, close, volume data.
- data/polygon_fetcher.py - fetch historical and live data relating to stocks and etfs from polygon.io


### nice sources to read up on:
https://www.investopedia.com/terms/b/bollingerbands.asp
