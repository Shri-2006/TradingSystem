import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone
from core.config import (CAPITAL, STRATEGY_COLORS, HEARTBEAT_STALE_SECONDS,MAX_DRAWDOWN, WARNING_DRAWDOWN)
from core.logger import get_trades, get_heartbeat
from metrics.risk import compute_all_metrics
from paper_trading.alpaca_paper import get_api

