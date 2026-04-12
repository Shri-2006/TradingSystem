import pandas as pd
import numpy as np
from core.features import build_features
from ta.trend import ADXIndicator
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

def get_regime_for_strategy(df, strategy):
    """
    Returns whether the current regime is suitable for a given strategy
    strategy: "stable" | "risky1" | "risky2"
    Returns : True if conditions are good, False if bot should sit out
    """
    regime = detect_regime(df)

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