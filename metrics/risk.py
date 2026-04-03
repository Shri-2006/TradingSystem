import numpy as np
import pandas as pd


def get_risk_free_rate():
    """
    this will give the current us 10 year treasury yield from polygon.io. If the fetch fails it falls back to 4% as a default. 10 year industry is chosen becaause it is the industry standard of risk-free rates
    """
    try:
        from polygon import RESTClient
        from core.config import POLYGON_API_KEY
        client=RESTClient(api_key=POLYGON_API_KEY)
        #The ticker is I:TNX for polygon 10 year treasury yield
        data=client.get_last_trade("I:TNX")
        rate=data.price/100
        print(f"Current risk-free rate that is fetched is : {data.price:.2f}%")
        return rate
    except Exception as e:
        print(f"WARNING AND ERROR, falling back to default rate of 4% since treasury rate could not be fetched \n\n error code is: {e}")
        return 0.04
    





def sharpe_ratio(returns,risk_free_rate=None):
    """
    Calculates the annualized sharpe ratio. Returns is pandas series of daily returnss, risk_free_rate is the annual risk free rate, default is 4%, will change to live us treasury if working right. 
    The higher the ratio, the better. If above 1, it is good, above 2 is amazing, and above that is insanely good
    """
    if (risk_free_rate is None):
        risk_free_rate=get_risk_free_rate()
    
    daily_return_free=risk_free_rate/252 #divided by 252 business days per year
    excess=returns-daily_return_free
    if(excess.std()==0):
        return 0.00000000000000000#muscle spasm hehe
    return(excess.mean()/excess.std())*np.sqrt(252)#annualize sharpe ratio through sqrt(252)* mean/std of excess returns

def max_drawdown(returns):
    """
    Calculates max drawdown (worst peak to trough loss). returns is pandas series of daily returns
    result is negative (-.23=23%)
    """

    combined=(1+returns).cumprod()#for every 1 dollar invested what is growth
    peak = combined.cummax()#running max
    drawdown=(combined-peak)/peak
    return drawdown.min()#worst point in this

def win_loss_ratio(returns):
    """
    Percentage of days with positive returns out of total days. .55=55% profitable days
    """
    if (len(returns)==0):
        return 0.0;
    wins=(returns>0).sum();
    return wins/len(returns)



def compute_all_metrics(returns):
    """
    It runs all three functions to get the 3 metrics and return in a clean dictioonary. The dashboard will use it to display the comparision of strategies
    returns is the pandas series of daily returns
    """

    return {

        "sharpe_ratio":sharpe_ratio(returns),
        "max_drawdown":max_drawdown(returns),
        "win_loss_ratio":win_loss_ratio(returns)
    }

