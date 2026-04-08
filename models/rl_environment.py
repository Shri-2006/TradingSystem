import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces #defines shape and  and type of the input/output
from core.features import build_features
from data.sentiment_fetcher import add_sentiment_to_df

class TradingEnvironment(gym.Env): #Blueprint essentially of the environemet for rl
    """
    Custom Gymnasium trading environment for risky2 RL bot.
    
    State: price features + current position + unrealized PnL
    Actions: 0=HOLD, 1=BUY, 2=SELL
    Reward: realized PnL, penalty for overtrading and holding losses
    
    This is designed to support future risk hooks such as :
    - position size comes from config (not hardcoded)
    - drawdown tracked per step for future kill switch integration
    - trade log compatible with existing SQLite logger
    """

    def __init__(self, df, initial_capital=200.0, max_position_pct=0.25):
        super().__init__()
        # Price data — expects OHLCV DataFrame with features already built in df
        self.df = df.reset_index(drop=True)
        self.initial_capital = initial_capital
        self.max_position = initial_capital * max_position_pct  # hook for future position sizing
        # 3 potential actions: 0=HOLD, 1=BUY, 2=SELL
        self.action_space = spaces.Discrete(3)

        # Observation: all feature columns + 2 extra (position size, unrealized PnL)
        n_features = len(self._get_feature_cols())
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(n_features + 2,),
            dtype=np.float32
        )

        self.reset()

    def _get_feature_cols(self):
        """Returns feature columns — excludes raw OHLCV"""
        return [c for c in self.df.columns
                if c not in ['open', 'high', 'low', 'close', 'volume']]