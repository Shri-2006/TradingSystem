# tests/test_regime.py
import unittest
import os
import pandas as pd
import numpy as np

os.environ.setdefault("ALPACA_API_KEY", "dummy")
os.environ.setdefault("ALPACA_SECRET_KEY", "dummy")
os.environ.setdefault("POLYGON_API_KEY", "dummy")

from models.regime_detector import detect_regime, get_regime_for_strategy, TRENDING, RANGING, VOLATILE
from models.regime_detector import detect_regime, get_regime_for_strategy, get_vix, TRENDING, RANGING, VOLATILE

def make_df(trend_slope=1.5, atr_multiplier=1.0, n=100, seed=42):
    """
    Builds a pre-featured DataFrame for regime testing.
    trend_slope  : higher = stronger trend
    atr_multiplier: >2 triggers VOLATILE via ATR spike detection
    """
    np.random.seed(seed)
    close = pd.Series([100 + i * trend_slope + np.random.randn() * 0.5 for i in range(n)])
    high  = close + 2.0 * atr_multiplier + np.abs(np.random.randn(n))
    low   = close - 2.0 * atr_multiplier - np.abs(np.random.randn(n))

    df = pd.DataFrame({
        'open'         : close - 0.5,
        'high'         : high,
        'low'          : low,
        'close'        : close,
        'volume'       : 1000000,
        'sma_20'       : close.rolling(20).mean(),
        'sma_50'       : close.rolling(50).mean(),
        'atr'          : (high - low) * atr_multiplier,
        'rsi'          : 50.0,
        'momentum_5'   : close.pct_change(5),
        'momentum_15'  : close.pct_change(15),
        'bb_upper'     : close + 2,
        'bb_middle'    : close,
        'bb_lower'     : close - 2,
        'zscore'       : 0.0,
        'volume_change': 0.0,
        'volume_ma_20' : 1000000,
        'volume_ratio' : 1.0,
    }).dropna()

    return df


class TestRegimeDetector(unittest.TestCase):

    def test_strong_trend_returns_trending(self):
        """Strongly trending price series should return TRENDING."""
        df = make_df(trend_slope=1.5)
        self.assertEqual(detect_regime(df), TRENDING)

    def test_flat_market_returns_ranging(self):
        """Flat price with no movement should return RANGING."""
        df = make_df(trend_slope=0.0)
        self.assertEqual(detect_regime(df), RANGING)

    def test_volatile_market_returns_volatile(self):
        """ATR spike above 2x average should return VOLATILE."""
        np.random.seed(42)
        n = 100
        close = pd.Series([100.0 + np.random.randn() * 0.5 for _ in range(n)])
        base_atr = 1.0
        spike_atr = [base_atr] * (n - 1) + [base_atr * 10]  # spike on last bar

        high = close + 1.0
        low  = close - 1.0

        df = pd.DataFrame({
            'open'         : close - 0.5,
            'high'         : high,
            'low'          : low,
            'close'        : close,
            'volume'       : 1000000,
            'sma_20'       : close.rolling(20).mean(),
            'sma_50'       : close.rolling(50).mean(),
            'atr'          : pd.Series(spike_atr),
            'rsi'          : 50.0,
            'momentum_5'   : close.pct_change(5),
            'momentum_15'  : close.pct_change(15),
            'bb_upper'     : close + 2,
            'bb_middle'    : close,
            'bb_lower'     : close - 2,
            'zscore'       : 0.0,
            'volume_change': 0.0,
            'volume_ma_20' : 1000000,
            'volume_ratio' : 1.0,
        }).dropna()

        self.assertEqual(detect_regime(df), VOLATILE)

    def test_empty_df_returns_ranging(self):
        """Empty DataFrame should safely default to RANGING."""
        df = pd.DataFrame()
        self.assertEqual(detect_regime(df), RANGING)

    def test_insufficient_data_returns_ranging(self):
        """Single row DataFrame should safely default to RANGING."""
        df = make_df(n=100).iloc[:1]
        self.assertEqual(detect_regime(df), RANGING)

    # ── get_regime_for_strategy ───────────────────────────────────────────────

    def test_stable_allowed_in_trending(self):
        df = make_df(trend_slope=1.5)
        self.assertTrue(get_regime_for_strategy(df, "stable"))

    def test_stable_allowed_in_ranging(self):
        df = make_df(trend_slope=0.0)
        self.assertTrue(get_regime_for_strategy(df, "stable"))

    def test_risky1_allowed_in_trending(self):
        df = make_df(trend_slope=1.5)
        self.assertTrue(get_regime_for_strategy(df, "risky1"))

    def test_risky1_blocked_in_ranging(self):
        df = make_df(trend_slope=0.0)
        self.assertFalse(get_regime_for_strategy(df, "risky1"))
# ── VIX signal ────────────────────────────────────────────────────────────────

def make_trending_df():
    """Reusable trending df for VIX tests."""
    return make_df(trend_slope=1.5)

class TestVIXSignal(unittest.TestCase):

    def test_high_vix_blocks_risky1(self):
        """VIX > 30 should block risky1 regardless of regime."""
        df = make_trending_df()
        self.assertFalse(get_regime_for_strategy(df, "risky1", vix=35))

    def test_high_vix_blocks_risky2(self):
        """VIX > 30 should block risky2 regardless of regime."""
        df = make_trending_df()
        self.assertFalse(get_regime_for_strategy(df, "risky2", vix=35))

    def test_high_vix_does_not_block_stable(self):
        """VIX > 30 should not stop stable — it is designed for rough markets."""
        df = make_trending_df()
        self.assertTrue(get_regime_for_strategy(df, "stable", vix=35))

    def test_mid_vix_allows_risky1(self):
        """VIX 20-30 is elevated but risky1 still trades — equity curve filter handles sizing."""
        df = make_trending_df()
        self.assertTrue(get_regime_for_strategy(df, "risky1", vix=25))

    def test_no_vix_falls_back_to_regime(self):
        """None VIX should fall back to regime logic only."""
        df = make_trending_df()
        self.assertTrue(get_regime_for_strategy(df, "risky1", vix=None))

    def test_get_vix_returns_float_or_none(self):
        """get_vix should always return a float or None"""
        vix = get_vix()
        self.assertTrue(vix is None or isinstance(vix, float))

if __name__ == "__main__":
    unittest.main()