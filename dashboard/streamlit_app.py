import streamlit as st
import pandas as pd
import os
from core.logger import get_trades
from metrics.risk import compute_all_metrics
from dashboard.compare import get_strategy_returns

#configuring the streamlit page
#emoji from https://emojiterra.com/trading/
st.set_page_config(page_title="Trading System Dashboard", page_icon="📊",layout="wide")

st.title("Trading System -A Live Strategy Dashboard")
st.caption("Comparing Grid Trading, Momentum Breakout, and RL strategies across stocks and crypto")

#Table creation
st.header("Strategy Comparision")
strategies=["stable","risky1","risky2"]
rows=[]
for strategy in strategies:
    returns = get_strategy_returns(strategy)
    if returns is None or (len(returns)==0):
        rows.append({
            "Strategy"    : strategy.upper(),
            "Sharpe Ratio": "N/A",
            "Max Drawdown": "N/A",
            "Win Rate"    : "N/A",
            "Total Trades": 0,
            "Status"      : "No data available yet"
        })
    else:
        metrics = compute_all_metrics(returns)
        rows.append({
            "Strategy"    : strategy.upper(),
            "Sharpe Ratio": f"{metrics['sharpe_ratio']:.2f}",
            "Max Drawdown": f"{metrics['max_drawdown']:.2%}",
            "Win Rate"    : f"{metrics['win_loss_ratio']:.2%}",
            "Total Trades": len(returns),
            "Status"      : "Running Live"
        })

df=pd.DataFrame(rows).set_index("Strategy")
st.dataframe(df,use_container_width=True)


#Most recent trades is being put here now
st.header("Recent Trades")
all_trades=[]
