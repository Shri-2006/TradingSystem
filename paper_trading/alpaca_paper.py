import alpaca_trade_api as tradeapi
from core.config import(ALPACA_API_KEY,ALPACA_SECRET_KEY,ALPACA_PAPER_URL,ALPACA_LIVE_URL,PAPER_MODE)

def get_api(strategy):
    
    """
    returns the authenticated alpaca api for paper and live url based on paper_mode, for each strategy (stable,risky1,risky2)

    """
    if ((PAPER_MODE[strategy])==False):
        url=ALPACA_LIVE_URL
    else:
        url=ALPACA_PAPER_URL

    return tradeapi.REST(ALPACA_API_KEY,ALPACA_SECRET_KEY,url)

def is_market_open(strategy):
    """
    Checks if the us stock market is currently open (bots cannot and shouldnt trade when market is closed). Risky2 ignores this since crypto is 24/7
    """
    api=get_api(strategy)
    clock=api.get_clock()
    return clock.is_open

def get_account_info(strategy):
    """
    This will return the current equity and cash of the account, and will be used by kill switch to check the drawdown
    """
    api=get_api(strategy)
    account=api.get_account()
    return{
        "equity":float(account.equity),"cash":float(account.cash),"buying_power":float(account.buying_power)
    }

def get_position(strategy,ticker):
    """
    Returns the current position value of a ticker in dollars, and if no position held returns 0
    """
    api=get_api(strategy)
    try:
        pos=api.get_position(ticker)
        return float(pos.market_value)
    except:
        return 0.0
    

def submit_order(strategy,ticker,qty,side):
    """
    This will submit an order for buy or sell (side), how much (qty), which one (ticker), and which bot (strategy)

    """


    api=get_api(strategy)
    order=api.submit_order(symbol=ticker,qty=qty,side=side,type='market',time_in_force='day')
    print(f"Order has been submitted: {side} {qty} {ticker}")
    return order


def close_position(strategy,ticker):
    """this will close the entire position for a single ticker"""
    api=get_api(strategy)
    api.close_position(ticker)
    print(f"position has been closed for : {ticker}")

def close_all_positions(strategy):
    #this is an emergenncy close all pos by killswitch
    api=get_api(strategy)
    api.close_all_positions()
    print(f"all positions for {strategy} have been closed due to kill switch")