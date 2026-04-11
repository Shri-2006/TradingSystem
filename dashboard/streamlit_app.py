import streamlit as st
import pandas as pd
import os
from core.logger import get_trades
from metrics.risk import compute_all_metrics
from dashboard.compare import get_strategy_returns
from core.config import CAPITAL

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
            "Sortino Ratio": "N/A",
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
            "Sortino Ratio":f"{metrics['sortino_ratio']:.2f}",
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
for strategy in strategies:
    trades=get_trades(strategy)
    if trades:#==True doesn't work for some reason
        all_trades.extend(trades)
if all_trades:
    trades_df=pd.DataFrame(all_trades,columns=['id', 'timestamp', 'strategy', 'asset','action', 'price', 'quantity', 'pnl', 'reason'])
    trades_df=trades_df.sort_values('timestamp',ascending=False)#descending from most recent
    trades_df=trades_df.drop(columns=['id'])
    st.dataframe(trades_df.head(20),use_container_width=True)
else:
    st.info("Bots are being warmed up so no trades have been logged yet")

#Allocation of funds
st.header("Capital Allocation")

from paper_trading.alpaca_paper import get_api
try:
    api = get_api("stable")
    account = api.get_account()
    portfolio_value = float(account.portfolio_value)
    cash = float(account.cash)
    invested = portfolio_value - cash

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Portfolio Value", value=f"${portfolio_value:,.2f}")
    with col2:
        st.metric(label="Cash Available", value=f"${cash:,.2f}")
    with col3:
        st.metric(label="Invested", value=f"${invested:,.2f}")
except Exception as e:
    # Fallback to config values if Alpaca unavailable
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Stable Bot", value=f"${CAPITAL['stable']:,.2f}", delta="Grid Trading")
    with col2:
        st.metric(label="Risky Bot 1", value=f"${CAPITAL['risky1']:,.2f}", delta="Momentum")
    with col3:
        st.metric(label="Risky Bot 2", value=f"${CAPITAL['risky2']:,.2f}", delta="RL Agent")


#foolter of page
st.divider()
st.caption("Built By Shriyans Singh github.com/Shri-2006 | Uses Polygon.io, Alpaca, XGBoost, Stable Baselines3 | (p.s. you should hire me)")