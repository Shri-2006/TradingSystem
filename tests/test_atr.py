# tests/test_atr.py
import unittest
from unittest.mock import patch
import os

os.environ.setdefault("ALPACA_API_KEY", "dummy")
os.environ.setdefault("ALPACA_SECRET_KEY", "dummy")
os.environ.setdefault("POLYGON_API_KEY", "dummy")

from metrics.risk_manager import (
    get_atr_adjusted_thresholds,
    get_portfolio_risk_level,
    get_position_size,
    should_close_position,
)


class TestATRKillSwitch(unittest.TestCase):

    # ── get_atr_adjusted_thresholds ───────────────────────────────────────────

    def test_high_atr_widens_thresholds(self):
        """Double the baseline ATR should widen thresholds by 1.5x (clamped)."""
        warning, kill = get_atr_adjusted_thresholds("stable", 0.030)
        self.assertLess(warning, -0.07)   # wider than static -0.07
        self.assertLess(kill, -0.15)      # wider than static -0.15

    def test_low_atr_tightens_thresholds(self):
        """Below baseline ATR should tighten thresholds."""
        warning, kill = get_atr_adjusted_thresholds("stable", 0.008)
        self.assertGreater(warning, -0.07)  # tighter than static -0.07
        self.assertGreater(kill, -0.15)     # tighter than static -0.15

    def test_extreme_atr_is_clamped(self):
        """Extreme ATR should be clamped to 1.5x — thresholds shouldn't go infinite."""
        warning_extreme, kill_extreme = get_atr_adjusted_thresholds("stable", 0.100)
        warning_double,  kill_double  = get_atr_adjusted_thresholds("stable", 0.030)
        self.assertAlmostEqual(warning_extreme, warning_double, places=5)
        self.assertAlmostEqual(kill_extreme, kill_double, places=5)

    def test_low_atr_floor_is_clamped(self):
        """Extremely low ATR should be clamped to 0.5x — thresholds shouldn't over-tighten."""
        warning_tiny,  kill_tiny   = get_atr_adjusted_thresholds("stable", 0.001)
        warning_floor, kill_floor  = get_atr_adjusted_thresholds("stable", 0.0075)
        self.assertAlmostEqual(warning_tiny, warning_floor, places=5)
        self.assertAlmostEqual(kill_tiny, kill_floor, places=5)

    # ── get_portfolio_risk_level ──────────────────────────────────────────────

    def test_safe_no_atr(self):
        """Full capital with no ATR should return safe."""
        self.assertEqual(get_portfolio_risk_level("stable", 1000), "safe")

    def test_critical_no_atr(self):
        """15%+ drawdown with no ATR should return critical."""
        self.assertEqual(get_portfolio_risk_level("stable", 840), "critical")

    def test_warning_no_atr(self):
        """~8% drawdown with no ATR should return warning."""
        self.assertEqual(get_portfolio_risk_level("stable", 920), "warning")

    def test_high_atr_prevents_warning(self):
        """High ATR widens thresholds — a 7% drawdown should be safe in volatile market."""
        result = get_portfolio_risk_level("stable", 930, current_atr=0.030)
        self.assertEqual(result, "safe")

    def test_low_atr_triggers_warning_earlier(self):
        """Low ATR tightens thresholds — a 6% drawdown should warn in calm market."""
        result = get_portfolio_risk_level("stable", 940, current_atr=0.008)
        self.assertEqual(result, "warning")

    # ── get_position_size ─────────────────────────────────────────────────────

    def test_full_size_when_safe(self):
        """Safe portfolio should return full base position size."""
        self.assertEqual(get_position_size("stable", 1000, 200), 200)

    def test_half_size_when_warning(self):
        """Warning portfolio should return half position size."""
        self.assertEqual(get_position_size("stable", 920, 200), 100.0)

    def test_zero_size_when_critical(self):
        """Critical portfolio should return 0 — no new positions."""
        self.assertEqual(get_position_size("stable", 840, 200), 0.0)

    def test_atr_widens_keeps_full_size(self):
        """High ATR widens thresholds — mild drawdown should still get full size."""
        self.assertEqual(get_position_size("stable", 940, 200, current_atr=0.030), 200)

    # ── should_close_position ─────────────────────────────────────────────────

    def test_stop_loss_triggers_close(self):
        """6% drop from entry should trigger stop loss for stable (threshold 5%)."""
        self.assertTrue(should_close_position("stable", 100, 94, 1000))

    def test_no_close_when_safe(self):
        """Small price drop in healthy portfolio should not close position."""
        self.assertFalse(should_close_position("stable", 100, 99, 1000))

    def test_critical_portfolio_triggers_close(self):
        """Critical drawdown should close position even without stop loss."""
        self.assertTrue(should_close_position("stable", 100, 99, 840))

    def test_atr_affects_close_decision(self):
        """Low ATR tightens thresholds — borderline drawdown should close in calm market."""
        self.assertTrue(should_close_position("stable", 100, 94, 940, current_atr=0.008))


if __name__ == "__main__":
    unittest.main()