## This will fetch latest price data from polygon, build_features(), check regime (if volatile it will not do it), load the ml model to predict buy/sell/hold. If buy, check to avoid MAX_Position_size, place grid of buy orders around current price. If sell, it will close the position, and it will check the kill switch where if drawdown supersedes 15% it will stop everything to prevent extreme loss. It will also log every trade to SQLite.

import os
import time
import pandas as pd
from datetime import datetime
from core.config import (STABLE_ASSETS,MAX_POSITION_SIZE,MAX_DRAWDOWN,CAPITAL,PAPER_MODE,ALPACA_PAPER_URL,ALPACA_LIVE_URL )
from core.logger import log_trade
from core.features import build_features
from data.polygon_fetcher import get_latest_bar
from data.sentiment_fetcher import add_sentiment_to_df
from models.regime_detector import get_regime_for_strategy
from models.train import load_model
from metrics.risk import compute_all_metrics
import alpaca_trade_api as tradeapi