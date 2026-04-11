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

def get_sleep_duration(strategy):
    """
    To save compute credits, this will return how long to sleep based on time until the opening of the market. It saves by making making it sleep longer when theres longer time till market opens
    24 hours: Sleep 12
    12 hours: Sleep 8
    8 hours: Sleep 3
    1 hour: sleep 30 min
    0 hours: Sleep 1 min
    market open: return 0 (trade now)
    """
    api=get_api(strategy)
    clock=api.get_clock()
    if (clock.is_open==True):
        #market is open
        return 0
    #calculation of time till open market
    currentTime=clock.timestamp
    next_opening=clock.next_open
    seconds_left=(next_opening-currentTime).total_seconds()
    x=3600

    #if statements on how to sleep
    if seconds_left>24*x:
        return 12*x
    elif seconds_left>12*x:
        return x*8
    elif seconds_left>8*x:
        return x*3;
    elif seconds_left>1*x:
        return (1/2)*x;
    else:
        return 60




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