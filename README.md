# SinghQuant: Multi-Strategy Trading System with ML and Risk Management

## Overview
A multiple strategy algorithmic trading system that compares grid trading, momentum breakout, and reinforcement learning across stocks and crypto with backtesting on historical data, keeping risk metrics, and having a live dashboard through Streamlit

## Strategies
**Stable:** Stable is intended to go for longer term gains and to be careful of going on short risks in stocks/etfs
**Risky1:** Risky1 is intended to go for short term gains in the stocks markets, going high risk high reward
**Risky2:** Risky2 is intended to go for short term gains in the cryptocurrency markets, going high risk high reward.


## Tech Stack
Alpaca - allows for paper trading and live execution for all bots
Polygon.io - Stock/ETF price data for stable and risky1, and crypto price data for risky2
SQLite- SQL database provider
scikit-learn - supervised ml for stable and risky1
XGBoost - supervised ml for stable and risky1 bots
Stable Baselines3 - reinforcement learning for risky2
VectorBT- Engine to test models on historical data
Streamlit - Live dashboard to see performance

## Project Structure
```
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
./data/polygon_fetcher.py
./data/sentiment_fetcher.py
./metrics
./metrics/risk.py
./metrics/risk_manager.py
./metrics/equity_curve_filter.py
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
- Oracle Cloud deployment — waiting on ARM capacity availability

### Completed Parts:
- core/config.py - This provides the configuration of the system and what are the providers
- core/logger.py - Creates database and provides functions to initialize the database tables, log each trade, and get past trades from database
- core/features.py- shared feature engineering for all 3 strategy bots. Computed rolling averages, RSI, momentum, Bollinger Bands, ATR, z-score, and volume indicators from raw data with open, high, low, close, volume data.
- data/polygon_fetcher.py - fetch historical and live data relating to stocks and etfs from polygon.io, adding crypto support
- data/sentiment_fetcher.py - fetch sentiment analysis from news articles using TextBlob and put into scores column in df
- models/regime_detector.py - detect whether market is trending or ranging
- models/train.py — XGBoost training pipeline for stable and risky1. It will fetches historical data, builds features, creates BUY/SELL labels, trains model, and saves the model as a .pkl file
- models/retrain.py — scheduled retraining every 14 days
- backtesting/engine.py — VectorBT backtesting engine, generates BUY/SELL signals from ML model, runs backtest with 0.1% fees and slippage, returns total return, Sharpe ratio, max drawdown
- backtesting/run_backtest.py — runs backtests across all strategies
- metrics/risk.py — Sharpe ratio (with live US Treasury rate fetch),max drawdown, win/loss ratio, compute_all_metric adn wrapper
- metrics/risk_manager.py — per-trade risk: stop loss, position sizing, peak equity kill switch, warning/critical thresholds, ATR-based dynamic threshold scaling- metrics/equity_curve_filter.py — macro trading state filter: reconstructs equity curve from closed trade history, computes moving average and drawdown, returns FULL/THROTTLE/HALT state with position size multiplier. Called once per cycle in stable.py and risky1.py before the per-ticker loop
- strategies/stable.py - Creating the strategy for the stable trading bot (one of the biggest files too actually)
- strategies/risky1.py - Creating the strategy for the risky trading bot (one of the second biggest files)
- paper_trading/alpaca_paper.py - centralized the Alpaca API wrapper for all strategies. Handles paper/live switching per bot, order submission, position checking, and kill switch execution
- dashboard/compare.py - terminal comparison table for all strategies
- dashboard/streamlit_app.py - live Streamlit web dashboard with strategy comparison table, recent trades, capital allocation pulled from config.py
- run.py - unified system launcher
- Dockerfile — containerizes the full system
- docker-compose.yml — runs bots + Streamlit dashboard together
- .github/workflows/test.yml — GitHub Actions CI, auto-runs 16 tests on every push to main
- models/rl_environment.py- Created a custom gymnasium trading env for risky2 rl bot. The state is price features +position+unrealized PnL. Actions 0=HOLD,1=Buy,2=SELL. There is small penatly for overtrading and nudges to exit loser positions. Drawdown traced per step is a hook for a future kill switch integration for this.
- models/rl_train.py - PPO training pipeline for risky2. It fetches a year's worth of historical crypto daya, builds features and trains agent using MlpPolicy for about 50000 timesteps. The model will be saved in risky2_model.zip
- strategies/risky2.py- Live RL trading strategy for crypto, it loads ppo model and builds live observation from the latest price data, and feeds it to the model for hold/buy/sell decisions. 
-
### nice sources to read up on:
https://www.investopedia.com/terms/b/bollingerbands.asp



