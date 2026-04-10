import pytest
import numpy as np
import pandas as pd
import os
os.environ['POLYGON_API_KEY'] = 'test_key'
os.environ['ALPACA_API_KEY'] = 'test_key'
os.environ['ALPACA_SECRET_KEY'] = 'test_key'

from models.rl_environment import TradingEnvironment

def make_dummy_df(rows=100):
    """Creates a dummy OHLCV + feature dataframe for testing"""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=rows, freq='D')
    df = pd.DataFrame({
        'open'         : np.random.uniform(100, 200, rows),
        'high'         : np.random.uniform(200, 300, rows),
        'low'          : np.random.uniform(50, 100, rows),
        'close'        : np.random.uniform(100, 200, rows),
        'volume'       : np.random.uniform(1000, 5000, rows),
        'sma_20'       : np.random.uniform(100, 200, rows),
        'sma_50'       : np.random.uniform(100, 200, rows),
        'ema_12'       : np.random.uniform(100, 200, rows),
        'ema_26'       : np.random.uniform(100, 200, rows),
        'rsi'          : np.random.uniform(0, 100, rows),
        'momentum_5'   : np.random.uniform(-1, 1, rows),
        'momentum_15'  : np.random.uniform(-1, 1, rows),
        'bb_upper'     : np.random.uniform(200, 300, rows),
        'bb_middle'    : np.random.uniform(100, 200, rows),
        'bb_lower'     : np.random.uniform(50, 100, rows),
        'atr'          : np.random.uniform(1, 10, rows),
        'zscore'       : np.random.uniform(-3, 3, rows),
        'volume_change': np.random.uniform(-1, 1, rows),
        'volume_ma_20' : np.random.uniform(1000, 5000, rows),
        'volume_ratio' : np.random.uniform(0, 2, rows),
        'sentiment'    : np.random.uniform(-1, 1, rows),
    }, index=dates)
    return df



def test_environment_initializes():
    """Environment should initialize without errors"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    assert env.initial_capital == 200.0
    assert env.cash == 200.0
    assert env.position == 0.0

def test_observation_shape():
    """Observation shape should match observation_space"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    obs, _ = env.reset()
    assert obs.shape == env.observation_space.shape

def test_reset_clears_state():
    """Reset should return environment to clean starting state"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    assert env.current_step == 0
    assert env.cash == 200.0
    assert env.position == 0.0
    assert env.total_pnl == 0.0
    assert env.trade_count == 0

def test_buy_action():
    """Action 1 should open a position"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    obs, reward, done, _, info = env.step(1)  # BUY
    assert env.position > 0
    assert env.cash < 200.0
    assert env.trade_count == 1

def test_hold_action():
    """Action 0 should not change position"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    obs, reward, done, _, info = env.step(0)  # HOLD
    assert env.position == 0.0
    assert env.cash == 200.0

def test_sell_without_position():
    """Selling with no position should do nothing"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    obs, reward, done, _, info = env.step(2)  # SELL with no position
    assert env.position == 0.0
    assert env.cash == 200.0

def test_buy_then_sell():
    """Buy then sell should close position and update PnL"""
    df = make_dummy_df()
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    env.step(1)  # BUY
    assert env.position > 0
    env.step(2)  # SELL
    assert env.position == 0.0
    assert env.cash != 200.0  # cash changed after trade

def test_episode_ends():
    """Episode should end when all rows are consumed"""
    df = make_dummy_df(rows=10)
    env = TradingEnvironment(df=df, initial_capital=200.0)
    env.reset()
    done = False
    steps = 0
    while not done:
        obs, reward, done, _, info = env.step(0)
        steps += 1
    assert done is True