#This file is meant to check features. run: 
"""
cd /workspaces/TradingSystem
python -m pytest tests/test_features.py -v
"""

import pytest
import pandas as pd
import numpy as np
from core.features import build_features

def make_sample_df(rows=100):
    """
    Creates a fake OHLCV dataframe for testing We need enough rows for rolling windows to work (min of at least 50)
    """
    np.random.seed(42)
    dates  = pd.date_range(start='2024-01-01', periods=rows, freq='D')
    closes = 100 + np.cumsum(np.random.randn(rows))  # random walk
    df = pd.DataFrame({'open': closes * 0.99,'high': closes * 1.01,'low': closes * 0.98, 'close': closes,'volume' : np.random.randint(1000000, 5000000, rows)}, index=dates)
    return df

def test_build_features_returns_dataframe():
    """build_features() should return a DataFrame"""
    df     = make_sample_df()
    result = build_features(df)
    assert isinstance(result, pd.DataFrame)

def test_build_features_has_expected_columns():
    """build_features() should add all indicator columns"""
    df= make_sample_df()
    result=build_features(df)
    expected = ['sma_20', 'sma_50', 'rsi', 'momentum_5',
                'bb_upper', 'bb_lower', 'atr', 'zscore', 'volume_ratio']
    for col in expected:
        assert col in result.columns, f"Missing column: {col}"

def test_build_features_drops_nan():
    """build_features() should have no NaN values after dropna"""
    df= make_sample_df()
    result =build_features(df)
    assert result.isnull().sum().sum() == 0


def test_build_features_reduces_rows():
    """Rolling windows need warmup and result should have fewer rows than input"""
    df= make_sample_df(rows=100)
    result =build_features(df)
    assert len(result) < 100