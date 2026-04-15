# Week 20+ — Financial Health Analyzer

## Overview
A standalone tool that analyzes a company's public financial data 
and returns a structured health report. Built as a separate repo 
by request, with planned integration into SinghQuant as a 
fundamental signal layer.

## Standalone Repo Purpose
Given a stock ticker, the tool will:
- Scrape the publicly available balance sheet (SEC EDGAR or similar)
- Calculate likelihood of survival (debt ratios, cash runway, etc.)
- Produce a financial health score (0-100)
- Recommend a credit limit based on financial strength
- Summarize key fundamentals in plain language

## SinghQuant Integration (Phase 2)
Once the standalone tool is stable, integrate its output as a 
signal into SinghQuant's trading decisions:

Current signals: ADX + VIX + SearXNG macro + XGBoost technical
New signal:      Financial health score → filter weak companies

Practical effect:
- Stable bot skips any ticker with health score below threshold
- Risky1 bot avoids momentum trading companies with deteriorating 
  balance sheets even if technicals look favorable
- Score refreshes weekly (balance sheets don't change daily)

## Metrics to Calculate
- **Survival Likelihood** — based on debt-to-equity, current ratio, 
  cash runway, interest coverage
- **Financial Health Score** — weighted composite of key ratios
- **Recommended Credit Limit** — based on revenue stability and 
  debt capacity
- **Altman Z-Score** — classic bankruptcy prediction model
- **Quick Ratio** — liquidity check (cash + receivables / liabilities)
- **Revenue Trend** — growing, flat, or declining over 3 years

## Data Sources (candidates)
- SEC EDGAR — free, official, US companies
- Polygon.io financials endpoint — already have API key
- Yahoo Finance scraping — fallback, less reliable
- Macrotrends — public balance sheet data

## Architecture (planned)
ticker input
↓
fetch balance sheet (SEC EDGAR or Polygon financials)
↓
parse key line items (assets, liabilities, revenue, debt, cash)
↓
calculate ratios and scores
↓
return structured report + health score
↓
(Phase 2) feed score into SinghQuant regime filter
## Repo Plan
- Separate GitHub repo (name TBD)
- Python, pandas, requests
- CLI tool first: `python analyze.py AAPL`
- Simple JSON output for easy SinghQuant integration later
- No ML needed initially — pure fundamental math

## Why This Matters for SinghQuant
Technical signals (RSI, momentum, XGBoost) tell you what the 
price is doing. Fundamental signals tell you if the company 
behind the price is healthy. Combining both reduces the risk of 
trading into a company that looks good on a chart but is 
financially deteriorating.

## Timeline
- Week 20+: Build standalone version
- Week 22+: Test on known cases (healthy vs distressed companies)
- Week 24+: Integrate health score as SinghQuant filter
- Week 26+: Add to dashboard Tab 3 (Risk & Positions)

## Notes
- Balance sheets update quarterly — no need for real-time data
- Start with US stocks only (SEC EDGAR coverage)
- Dad's standalone use case is the primary deliverable
- SinghQuant integration is Phase 2 and optional
