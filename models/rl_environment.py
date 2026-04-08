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

    def reset(self, seed=None, options=None):
        """Reset environment to starting state for new episode of model"""
        super().reset(seed=seed)
        self.current_step = 0
        self.cash         = self.initial_capital
        self.position     = 0.0   # dollars held in asset
        self.entry_price  = 0.0   # price we bought at
        self.total_pnl    = 0.0
        self.peak_value   = self.initial_capital  # for drawdown tracking
        self.trade_count  = 0     # penalty for overtrading
        return self._get_observation(), {}

    def _get_observation(self):
        """Build the state vector the model sees regarding price"""
        row          = self.df.iloc[self.current_step]
        feature_cols = self._get_feature_cols()
        features     = row[feature_cols].values.astype(np.float32)

        # Add position state — hook for future risk controls
        position_norm  = self.position / self.initial_capital
        unrealized_pnl = 0.0
        if self.position > 0 and self.entry_price > 0:
            current_price  = float(row['close'])
            unrealized_pnl = (current_price - self.entry_price) / self.entry_price

        return np.append(features, [position_norm, unrealized_pnl]).astype(np.float32)
    

    def step(self, action):
        """
        Execute one trading action and return new state, reward, done flag. This is called by the model every step during training.
        """
        row= self.df.iloc[self.current_step]
        price= float(row['close'])
        reward=  0.0
        #not needed any more
        #self.trade_count += 0  # reset per step

        #  Action 1: BUY 
        if action == 1 and self.position == 0:
            # Only buy if no position held — hook for future position sizing
            self.position= min(self.max_position, self.cash)
            self.cash-= self.position
            self.entry_price = price
            self.trade_count += 1
            reward= -0.001  # small cost for trading

        #  Action 2: SELL 
        elif action == 2 and self.position > 0:
            pnl= self.position * (price - self.entry_price) / self.entry_price
            self.cash+= self.position + pnl
            reward= pnl / self.initial_capital  # normalize reward
            self.total_pnl += pnl
            self.position = 0.0
            self.entry_price = 0.0
            self.trade_count += 1

        #  Action 0(neutral): HOLD 
        else:
            # Small penalty for holding a losing position to discourage model from keeping losing positions, but not so much of a penalty that it will sell to prevent any losses
            if self.position > 0 and self.entry_price > 0:
                unrealized = self.position * (price - self.entry_price) / self.entry_price
                if unrealized < 0:
                    reward = unrealized * 0.001  # tiny nudge to exit losers

        # Track peak value for drawdown — hook for future kill switch
        portfolio_value   = self.cash + self.position
        self.peak_value   = max(self.peak_value, portfolio_value)
        drawdown          = (portfolio_value - self.peak_value) / self.peak_value

        # Move to next step
        self.current_step += 1
        done = self.current_step >= len(self.df) - 1

        return self._get_observation(), reward, done, False, {
            "total_pnl" : self.total_pnl,
            "drawdown"  : drawdown,
            "trades"    : self.trade_count
        }
    

    def render(self):
        """Simple text render for debugging during training"""
        portfolio_value = self.cash + self.position
        print(f"Step {self.current_step} | " f"Portfolio: ${portfolio_value:.2f}| "f"Cash: ${self.cash:.2f}|"f"Position: ${self.position:.2f} | "f"Total PnL: ${self.total_pnl:.2f}")