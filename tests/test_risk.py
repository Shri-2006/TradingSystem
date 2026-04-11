
""" To run this file as a check: 
python -m pytest tests/test_risk.py -v
"""
import pytest
import pandas as pd
import numpy as np
from metrics.risk import sharpe_ratio, max_drawdown, win_loss_ratio, compute_all_metrics, sortino_ratio

def make_returns(positive=True, rows=252):
    """
    Creates fake daily returns for testing
    positive=True means generally upward returns
    positive=False means generally downward returns
    """
    np.random.seed(42)
    if positive:
        return pd.Series(np.random.normal(0.001, 0.01, rows))
    else:
        return pd.Series(np.random.normal(-0.001, 0.01, rows))

def test_sharpe_ratio_positive_returns():
    """Positive returns should produce positive Sharpe ratio"""
    returns = make_returns(positive=True)
    result  = sharpe_ratio(returns, risk_free_rate=0.04)
    assert result > 0

def test_sharpe_ratio_negative_returns():
    """Negative returns should produce negative Sharpe ratio"""
    returns = make_returns(positive=False)
    result  = sharpe_ratio(returns, risk_free_rate=0.04)
    assert result < 0

def test_sharpe_ratio_flat_returns():
    """Flat returns (no std) should return 0.0 without crashing"""
    returns = pd.Series([0.0] * 100)
    result  = sharpe_ratio(returns, risk_free_rate=0.04)
    assert result == 0.0

def test_max_drawdown_is_negative():
    """Max drawdown should always be negative or zero"""
    returns = make_returns()
    result  = max_drawdown(returns)
    assert result <= 0

def test_max_drawdown_range():
    """Max drawdown should be between -1 and 0 since its basically the worst thing"""
    returns = make_returns()
    result  = max_drawdown(returns)
    assert -1 <= result <= 0

def test_win_loss_ratio_range():
    """Win/loss ratio should be between 0 and 1 since it is a ratio"""
    returns = make_returns()
    result  = win_loss_ratio(returns)
    assert 0 <= result <= 1

def test_win_loss_empty_returns():
    """Empty returns should return 0.0 without crashing"""
    result = win_loss_ratio(pd.Series([]))
    assert result == 0.0

def test_compute_all_metrics_keys():
    """compute_all_metrics() should return all three keys"""
    returns = make_returns()
    result  = compute_all_metrics(returns)
    assert "sharpe_ratio"  in result
    assert "max_drawdown"  in result
    assert "win_loss_ratio" in result




# ── Sortino Ratio Tests ──────────────────────────────────────
def test_sortino_positive_returns():
    """Sortino should be positive when returns are consistently positive"""
    returns = pd.Series([0.01, 0.02, 0.01, 0.03, 0.02])
    result = sortino_ratio(returns)
    assert result > 0

def test_sortino_negative_returns():
    """Sortino should be negative when returns are consistently negative"""
    returns = pd.Series([-0.01, -0.02, -0.01, -0.03, -0.02])
    result = sortino_ratio(returns)
    assert result < 0

def test_sortino_flat_returns():
    """Sortino should return 0 for flat returns"""
    returns = pd.Series([0.0] * 10)
    result = sortino_ratio(returns)
    assert result == 0.0

def test_sortino_no_downside():
    """Sortino should return 0 when no downside exists"""
    returns = pd.Series([0.01, 0.02, 0.03])
    result = sortino_ratio(returns)
    assert result == 0.0

# ── Risk Manager Tests ───────────────────────────────────────
import os
os.environ['POLYGON_API_KEY'] = 'test_key'
os.environ['ALPACA_API_KEY'] = 'test_key'
os.environ['ALPACA_SECRET_KEY'] = 'test_key'

from metrics.risk_manager import get_portfolio_risk_level, get_position_size, check_stop_loss

def test_risk_level_safe():
    """Should return safe when equity is above warning threshold"""
    result = get_portfolio_risk_level("stable", 1000.0)
    assert result == "safe"

def test_risk_level_warning():
    """Should return warning when equity drops past warning threshold"""
    # stable warning at -7%, start = 1000, so 930 triggers warning
    result = get_portfolio_risk_level("stable", 920.0)
    assert result == "warning"

def test_risk_level_critical():
    """Should return critical when equity drops past kill switch"""
    # stable kill switch at -15%, so 840 triggers critical
    result = get_portfolio_risk_level("stable", 840.0)
    assert result == "critical"

def test_position_size_safe():
    """Full position size when safe"""
    base = 200.0
    result = get_position_size("stable", 1000.0, base)
    assert result == base

def test_position_size_warning():
    """Half position size when warning"""
    base = 200.0
    result = get_position_size("stable", 920.0, base)
    assert result == base * 0.5

def test_position_size_critical():
    """Zero position size when critical"""
    base = 200.0
    result = get_position_size("stable", 840.0, base)
    assert result == 0.0

def test_stop_loss_triggered():
    """Stop loss should trigger when price drops enough"""
    result = check_stop_loss("stable", entry_price=100.0, current_price=94.0)
    assert result == True  # 6% drop > 5% threshold

def test_stop_loss_not_triggered():
    """Stop loss should not trigger on small dip"""
    result = check_stop_loss("stable", entry_price=100.0, current_price=97.0)
    assert result == False  # 3% drop < 5% threshold