## This will fetch latest price data from polygon, build_features(), check regime (if volatile it will not do it), load the ml model to predict buy/sell/hold. If buy, check to avoid MAX_Position_size, place grid of buy orders around current price. If sell, it will close the position, and it will check the kill switch where if drawdown supersedes 15% it will stop everything to prevent extreme loss. It will also log every trade to SQLite.

import os
import time
import pandas as pd
from datetime import datetime
from core.config import (RISKY1_ASSETS,MAX_POSITION_SIZE,MAX_DRAWDOWN,CAPITAL,PAPER_MODE,ALPACA_PAPER_URL,ALPACA_LIVE_URL )
from core.logger import log_trade
from core.features import build_features
from data.polygon_fetcher import get_latest_bar
from data.sentiment_fetcher import add_sentiment_to_df
from models.regime_detector import get_regime_for_strategy
from models.train import load_model
from metrics.risk import compute_all_metrics
import alpaca_trade_api as tradeapi

#loading model only once to keep same model for each trade in single session, save memory (analysis of algorithms thank you) and to improve speed to avoid reinitializing model from disk each trade

model=load_model("risky1_model.pkl")
#Alpaca connection (paper vs live)
if PAPER_MODE["risky1"]:
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
    This will checkk if the loss has exceeded 30% overall. if it has, it closes alll positions and stops trading immediately. It will also return true if kill switchh is fired, else false if safe
    """
    account=api.get_account()
    equity=float(account.equity)
    start_cash=CAPITAL["risky1"]
    drawdown=(equity-start_cash)/(start_cash);

    if drawdown<= MAX_DRAWDOWN["risky1"]:
        print(f"KILL SWITCH IS BEING FIRED STOP NOW - drawdown is {drawdown:.2%} and has exceeded the limit")
        api.close_all_positions()
        log_trade("risky1","ALL","KILL_SWITCH",0,0,pnl=drawdown,reason=(f"Drawdown is {drawdown:.2%}"))
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
    if not get_regime_for_strategy(df,"risky1"):
        print(f"{ticker}  regime is in a unfavorable spot, sitting out this time")
        return
    
    #now gets the ML prediction
    feature_cols=[c for c in df.columns if c not in ['open','high','low','close','volume']]
    X=df[feature_cols].values
    prediction=model.predict(X[-1].reshape(1,-1))[0]
    price=float(df['close'].iloc[-1])
    
    #now based on the predicition it will choose what trade to do
    current_pos=get_current_position(api,ticker)
    max_pos=MAX_POSITION_SIZE["risky1"]
    # Momentum strategy exits faster than grid
    # Sell if momentum turns negative even without ML signal
    if df['momentum_5'].iloc[-1] < 0 and current_pos > 0:
        api.close_position(ticker)
        log_trade("risky1", ticker, "SELL", price, current_pos,
          reason="Momentum turned negative")
        return
    if prediction==1 and current_pos<max_pos:
        #if predicition is 1 and pos is less than max, buy
        qty=round((max_pos-current_pos)/price,4)

        if qty>0:
            api.submit_order(symbol=ticker,qty=qty,side='buy',type='market',time_in_force='day')
            log_trade("risky1",ticker,"BUY",price,qty,reason="ML signals to Buy and the regime is favorable")
            print(f"Buy {qty}{ticker} @ ${price}")

    elif prediction ==0 and current_pos>0:
        #if prediciton is 0 and pos is greater than 0, SELL NOW
        api.close_position(ticker)
        log_trade("risky1",ticker,"SELL",price,current_pos,reason="ML signals to SELL now")
        print(f"SELL{ticker}  @  ${price}")
    else:
        #in other cases simply hold the pos
        print(f"HOLD{ticker}, no action needed rn")




def run():
    """ 
    This is the main loop for the risky1 strategy, and it runs continusly. it will check each ticker every 60 seconds, and runs continuosly. It iwll be called from run.py when the system boots up
    """
    api=get_api()
    print("Risky1 bot started now...")
    while True:
        try:
            #check kill switch before anything else
            if check_kill_switch(api):
                print("Kill switch has stopped risky1 bot")
                break
            #running trading cycle per each ticker (assets)
            for ticker in RISKY1_ASSETS:
                try:
                    trade_ticker(api,ticker)
                except Exception as e:
                    print(f"error trading this asset: {ticker}: {e}")
                    continue
            print(f"cycle has complteded at {datetime.now()}-time to sleep for 1 min")
            time.sleep(60)
        except KeyboardInterrupt:
            print("Risky1 bot was manually stopped by user")
            break
        except Exception as e:
            print(f"there was an unexpected error : {e}, will restart cycle in 60 seconds")
            time.sleep(60)
    
if __name__=="__main__":
    run();