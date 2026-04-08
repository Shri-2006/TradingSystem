# Week 8 — Sentiment & Macro Upgrade

## Prerequisites
- Week 7 advanced risk must be complete
- RL bot must be running in paper trading

## Planned Improvements

### 1. SearXNG Macro Circuit Breaker
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

### 4. Reddit Sentiment (Optional)
Add r/wallstreetbets and r/stocks sentiment via PRAW library.
Aggregate with existing TextBlob Polygon news sentiment.
Weighted average: 70% news sentiment, 30% Reddit sentiment.
Only implement if TextBlob sentiment proves insufficient.

## Implementation Order
1. SearXNG circuit breaker (new file: data/macro_fetcher.py)
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

## Bot 4 & 5
- Implement a RL version of stable and risky1 for stocks and etfs