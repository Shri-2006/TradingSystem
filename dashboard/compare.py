import os
import pandas as pd
from core.logger import get_trades
from metrics.risk import compute_all_metrics

def get_strategy_returns(strategy):
    """
    This will pull the trade history from SQlite file and compute daily returns for each strategy
    """
    trades=get_trades(strategy)
    if not trades:
        return None
    df=pd.DataFrame(trades,columns= ['id','timestamp','strategy','asset','action','price','quantity','pnl','reason'])
    df['pnl']=pd.to_numeric(df['pnl'],errors='coerce').fillna(0)
    return df['pnl']


def print_comparision():
    """
    Prints a side by side comparision for all strategies
    """
    strategies=["stable","risky1","risky2"]
    rows=[]
    for strategy in strategies:
        returns = get_strategy_returns(strategy)
        if returns is None or len(returns)==0:
            rows.append({"strategy":strategy,"sharpe_ratio":"N/A","max_drawdown":"N/A","win_loss":"N/A","total_trades":0,"status":"No data"})
        else:
            metrics = compute_all_metrics(returns)
            rows.append({"strategy": strategy,
                         "sharpe_ratio":f"{metrics['sharpe_ratio']:.2f}",
                         "max_drawdown": f"{metrics['max_drawdown']:.2%}"
                         ,"win_loss": f"{metrics['win_loss_ratio']:.2%}",
                         "total_trades": len(returns),
                         "status": "RUNNING"})
            
    df=pd.DataFrame(rows).set_index("strategy")
    print("\n======TRADING SYSTEM STRATEGY COMPARISION TABLE======\n")
    print(df.to_string())
    print()

if __name__=="__main__":
    print_comparision()