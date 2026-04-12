# Week 8 — Sentiment & Macro Upgrade

## Prerequisites
- Week 7 advanced risk must be complete
- RL bot must be running in paper trading

## Planned Improvements

### 1. SearXNG Macro Circuit Breaker (Optional)
Use self-hosted SearXNG instance to search for high-impact macro keywords.
If search results contain high frequency of words like:
- "Federal Reserve interest rate"
- "SEC lawsuit"
- "exchange halt"
- "market circuit breaker"
- "bank failure"
Then automatically move all positions to cash before price action hits
the kill switch threshold.
This is External Alpha — price data alone is not enough in the age of
high-frequency news trading.
SearXNG is self-hosted, free, and private — no Tavily or Exa needed.

### 2. ADX Regime Detection Upgrade
Replace current simple SMA crossover regime detection with ADX indicator.
ADX measures trend strength — industry standard for regime detection.
If ADX > 25 → trending regime → momentum strategies perform better
If ADX < 20 → ranging regime → grid strategies perform better
Update regime_detector.py to use ADX alongside existing logic.

### 3. VIX Macro Signal
Pull VIX data from FRED API (free, no API key needed for basic access).
Use VIX as a macro regime signal:
- VIX < 20 → low fear → normal trading
- VIX 20-30 → elevated fear → reduce position sizes
- VIX > 30 → high fear → consider pausing risky bots
Integrate into regime_detector.py alongside ADX.

### 4. Reddit Sentiment (Optional, maybe skip)
Add r/wallstreetbets and r/stocks sentiment via PRAW library.
Aggregate with existing TextBlob Polygon news sentiment.
Weighted average: 70% news sentiment, 30% Reddit sentiment.
Only implement if TextBlob sentiment proves insufficient.

## Implementation Order
1. SearXNG circuit breaker (new file: data/macro_fetcher.py) (OPTIONAL)
2. ADX regime detection (upgrade models/regime_detector.py)
3. VIX signal (upgrade models/regime_detector.py)
4. Reddit sentiment (upgrade data/sentiment_fetcher.py) — optional

## Notes
- SearXNG API endpoint needs to be confirmed before implementation
- FRED API is free with no key required for VIX data
- Reddit PRAW requires Reddit API credentials (free)
- FinBERT skipped — too compute heavy for EliteBook/Oracle ARM

## Readme
- update readme again
- add supervised vs unsupervised vs reinforced learning chart that explains differences in methods

## Bot 4 & 5 (do this absolutely last, make sure the first 3 bots work)
- Implement a RL version of stable and risky1 for stocks and etfs

## Bot 6(do this absolutely last, make sure the first 3 bots work)
- Implement a supervised learning version of risky2 (for crypto)

## Bot 7,8,9(do this absolutely last, make sure the first 3 bots work)
-Implement a unsupervised learning version of stable,risky1, risky2



## Cloud SQL update
Have the model ping a cloud server (maybe your onedrive?) and upload the models that have been created. ONLY ON ORACLE CLOUD INSTANCE. This will prevent the bot from seeming like its inactive (so do it like once every 10 min). Doing this will also create a backup in case your instance crashes, so you dont have to train a brand new model for each strategy from scratch again. Now that we are on oracle, change the command in config.py to true in featureflags

## Rename entire project
This is fairly easy so do this first:rename the TradingSystem to
 SinghQuant: Multi-Strategy Trading System with ML and Risk Management
 (fix the name to be more professional and also to include details that were skipped out)