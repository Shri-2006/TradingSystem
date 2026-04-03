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

#loading model only once to keep same model for each trade in single session, save memory (analysis of algorithms thank you) and to improve speed to avoid reinitializing model from disk each trade

model=load_model("stable_model.pkl")
#Alpaca connection (paper vs live)
if PAPER_MODE["stable"]:
    BASE_URL=ALPACA_PAPER_URL
else:
    BASE_URL=ALPACA_LIVE_URL

def get_api():
    """
    will confirm and return the alpaca api conenctions.
    """
    from core.config import ALPACA_API_KEY, ALPACA_SECRET_KEY
    return tradeapi.REST(ALPACA_API_KEY,ALPACA_SECRET_KEY,BASE_URL)

def check_kill_switch(api):
    """
    This will checkk if the loss has exceeded 15% overall. if it has, it closes alll positions and stops trading immediately. It will also return true if kill switchh is fired, else false if safe
    """
    account=api.get_account()
    equity=float(account.equity)
    start_cash=CAPITAL["stable"]
    drawdown=(equity-start_cash)/(start_cash);

    if drawdown<= MAX_DRAWDOWN["stable"]:
        print(f"KILL SWITCH IS BEING FIRED STOP NOW - drawdown is {drawdown:.2%} and has exceeded the limit")
        api.close_all_positions()
        log_trade("stable","ALL","KILL_SWITCH",0,0,pnl=drawdown,reason=(f"Drawdown is {drawdown:.2%}"))
        return True
    return False

def get_current_position(api,ticker):
    """"
    this wil return the current posisition size in dollars for ticker, if doesn't have one, it will return 0
    """
    try:
        position=api.get_position(ticker)
        return float(position.market_value)
    except:
        return 0.0#no position held
    


#Main trading logic btw, take a look :D
def trade_ticker(api,ticker):
    """
    This will run a full trading cycle per ticker, and is called only once per ticker per trading cycle in the function run()
    
    """
    #get price data
    df=get_latest_bar(ticker)
    if df is None or df.empty:
        print(f"There is no data for {ticker}, will skip")
        return
    
    #now the features
    df=build_features(df)
    df=add_sentiment_to_df(df,ticker)

    #now checks regime
    if not get_regime_for_strategy(df,"stable"):
        print(f"{ticker}  regime is in a unfavorable spot, sitting out this time")
        return
    
    #now gets the ML prediction
    feature_cols=[c for c in df.columns if c not in ['open','high','low','close','volume']]
    X=df[feature_cols].values
    prediction=model.predict(X[-1].reshape(1,-1))[0]
    price=float(df['close'].iloc[-1])
    
    #now based on the predicition it will choose what trade to do
    current_pos=get_current_position(api,ticker)
    max_pos=MAX_POSITION_SIZE["stable"]
    if prediction==1 and current_pos<max_pos:
        #if predicition is 1 and pos is less than max, buy
        qty=round((max_pos-current_pos)/price,4)
        if qty>0:
            api.submit_order(symbol=ticker,qty=qty,side='buy',type='market',time_in_force='day')
            log_trade("stable",ticker,"BUY",price,qty,reason="ML signals to Buy and the regime is favorable")
            print(f"Buy {qty}{ticker} @ ${price}")

    elif prediction ==0 and current_pos>0:
        #if prediciton is 0 and pos is greater than 0, SELL NOW
        api.close_position(ticker)
        log_trade("stable",ticker,"SELL",price,current_pos,reason="ML signals to SELL now")
        print(f"SELL{ticker}  @  ${price}")
    else:
        #in other cases simply hold the pos
        print(f"HOLD{ticker}, no action needed rn")

        