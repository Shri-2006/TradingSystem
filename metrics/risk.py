import numpy as np
import pandas as pd

def sharpe_ratio(returns,risk_free_rate=0.04):
    """
    Calculates the annualized sharpe ratio. Returns is pandas series of daily returnss, risk_free_rate is the annual risk free rate, default is 4%, the current US treasury (0.04). 
    The higher the ratio, the better. If above 1, it is good, above 2 is amazing, and above that is insanely good
    """
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

