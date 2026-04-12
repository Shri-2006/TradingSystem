import pandas as pd
import numpy as np
from core.features import build_features
from ta.trend import ADXIndicator
import requests
# Regime labels
TRENDING  = "TRENDING"
RANGING   = "RANGING"
VOLATILE  = "VOLATILE"

def detect_regime(df):
    """
    Detects the current market regime from a featured DataFrame
    df must already have features built via build_features()
    Returns: "TRENDING", "RANGING", or "VOLATILE"

    How it works:
    - ADX > 25         = strong trend (TRENDING)
    - ATR spike        = high volatility (VOLATILE)
    - everything else  = ranging market (RANGING)
    """
    if df.empty or len(df) < 2:
        return RANGING  # default to ranging if not enough data

    latest = df.iloc[-1]  # most recent bar

    # Check for volatilty
    # If ATR is more than double the 20-bar average = volatile market
    atr_mean = df['atr'].rolling(window=20).mean().iloc[-1]
    if latest['atr'] > atr_mean * 2:
        return VOLATILE

    #Trend Check
    if len(df) >= 14:
        adx_value = ADXIndicator(df['high'], df['low'], df['close'], window=14).adx().iloc[-1]
        if adx_value > 25:
            return TRENDING
    else:
        # fall back to SMA crossover if not enough bars for ADX
        # # SMA 20 above SMA 50 = uptrend while SMA 20 below SMA 50 = downtrend and Either way = TRENDING

        if latest['sma_20'] > latest['sma_50'] * 1.01 or \
            latest['sma_20'] < latest['sma_50'] * 0.99:
            return TRENDING

 
    # Default
    return RANGING

def get_regime_for_strategy(df, strategy, vix=None):
    """
    This will return whether or not the current regime is suitable for the strategies currently avaialbe. If vix is above 30, risky bots sit out. its optional. <20 is low fear and normal trading. 20-30 is stable still trades risky sits out. greater than 30 means to stop now
    #     Returns whether the current regime is suitable for a given strategy
    #     strategy: "stable" | "risky1" | "risky2"
    #     Returns : True if conditions are good, False if bot should sit out
    """
    regime = detect_regime(df)
    if vix is not None:
        if vix > 30:
            if strategy in ["risky1", "risky2"]:
                print(f"VIX={vix:.1f} — high fear, {strategy} sitting out")
                return False
                    # 20-30 range: risky bots still trade, equity curve filter handles sizing to prevent too much loss
        
    if strategy == "stable":
        # Grid trading works best in ranging markets
        # Still okay in trending — just less optimal but it sits out when volatile
        return regime in [RANGING, TRENDING]

    elif strategy == "risky1":
        # Momentum works best when trending
        # Sit out when ranging or volatile
        return regime == TRENDING

    elif strategy == "risky2":
        # Crypto RL bot is trained to handle volatility and it only sits out when completely ranging with no movement
        return regime in [TRENDING, VOLATILE]

    return True  # default to allowing trade if unknown strategy


    



def regime_summary(df):
    """
    Returns a readable summary of current market conditions and is used by the dashboard to display regime status
    """
    regime = detect_regime(df)
    descriptions = {
        TRENDING : "Market is trending— momentum conditions favorable",
        RANGING  : "Market is ranging— grid trading conditions favorable",
        VOLATILE : "Market is volatile —reduced position sizing recommended",
    }
    return {
        "regime"      : regime,
        "description" : descriptions[regime]
    }



def get_vix():
    """"
    This will return the latest VIX value from FRED API. VIX is a measurement of market fear. The higher, the worse. If the fetch fails it returns None so it doesn't crash the whole system
    """

    try:
        url="https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS"
        response=requests.get(url,timeout=10)
        lines=response.text.strip().split("\n")
        #in csv format its DATE,VALUE, i want to skip header and find the last non NULL values in this
        for line in reversed(lines[1:]):
            date, value = line.split(",")
            if value.strip() != ".":  # FRED uses "." for missing data not null, that was annoying.
                return float(value.strip())
        return None
    except Exception:
        return None #dont crash entire system!
    




















#  def get_regime_for_strategy(df, strategy):
#     """
#     Returns whether the current regime is suitable for a given strategy
#     strategy: "stable" | "risky1" | "risky2"
#     Returns : True if conditions are good, False if bot should sit out
#     """
#     regime = detect_regime(df)

    # if strategy == "stable":
    #     # Grid trading works best in ranging markets
    #     # Still okay in trending — just less optimal but it sits out when volatile
    #     return regime in [RANGING, TRENDING]

    # elif strategy == "risky1":
    #     # Momentum works best when trending
    #     # Sit out when ranging or volatile
    #     return regime == TRENDING

    # elif strategy == "risky2":
    #     # Crypto RL bot is trained to handle volatility and it only sits out when completely ranging with no movement
    #     return regime in [TRENDING, VOLATILE]

    # return True  # default to allowing trade if unknown strategy

