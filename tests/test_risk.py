
""" To run this file as a check: 
python -m pytest tests/test_risk.py -v
"""
import pytest
import pandas as pd
import numpy as np
from metrics.risk import sharpe_ratio, max_drawdown, win_loss_ratio, compute_all_metrics

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