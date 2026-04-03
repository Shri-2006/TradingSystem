"""
python -m pytest tests/ -v
"""
import os
os.environ['POLYGON_API_KEY']='test_key' #dummy test key that will be used for testnig only.
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock#https://docs.python.org/3/library/unittest.mock.html,lets us test all tests without using an actual model or data or api keys yet. supposedly the business standard way (-_-)
from backtesting.engine import generate_signals, get_backtest_summary

def make_featured_df(rows=100):
    """
    Creates a fake featured df for backtesting tests
    """
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=rows, freq='D')
    closes = 100 + np.cumsum(np.random.randn(rows))
    df = pd.DataFrame({
        'open': closes * 0.99,
        'high':closes * 1.01,
        'low':closes * 0.98,
        'close' :closes,
        'volume': np.random.randint(1000000, 5000000, rows),
        'sma_20': closes * 0.99,
        'sma_50': closes * 0.98,
        'rsi' : np.random.uniform(30, 70, rows),
        'momentum_5':np.random.randn(rows) * 0.01,
        'zscore':np.random.randn(rows),
        'volume_ratio':np.random.uniform(0.5, 2.0, rows),
    }, index=dates)
    return df

def make_mock_model(prediction=1):
    """
    Creates a fake ML model that always predicts the same value. prediction: 1 = always BUY, 0 = always SELL
    """
    model = MagicMock()
    model.predict.return_value = np.array([prediction] * 100)
    return model

def test_generate_signals_returns_two_series():
    """generate_signals() should return entries and exits as boolean Series"""
    df      = make_featured_df()
    model   = make_mock_model(prediction=1)
    entries, exits = generate_signals(df, model)
    assert isinstance(entries, pd.Series)
    assert isinstance(exits, pd.Series)

def test_generate_signals_buy_model():
    """A model that always predicts buy should have all entries True"""
    df      = make_featured_df()
    model   = make_mock_model(prediction=1)
    entries, exits = generate_signals(df, model)
    assert entries.all()
    assert not exits.any()

def test_generate_signals_sell_model():
    """A model that always predicts sell should have all exits True"""
    df      = make_featured_df()
    model   = make_mock_model(prediction=0)
    entries, exits = generate_signals(df, model)
    assert exits.all()
    assert not entries.any()

def test_get_backtest_summary_structure():
    """get_backtest_summary() should return a df with expected columns"""
    mock_portfolio = MagicMock()
    mock_portfolio.total_return.return_value = 0.15
    mock_portfolio.sharpe_ratio.return_value = 1.2
    mock_portfolio.max_drawdown.return_value = -0.08
    mock_portfolio.trades.count.return_value = 42
    results = {"SPY": mock_portfolio}
    summary = get_backtest_summary(results)
    assert isinstance(summary, pd.DataFrame)
    assert "total_return" in summary.columns
    assert "sharpe_ratio" in summary.columns
    assert "max_drawdown" in summary.columns