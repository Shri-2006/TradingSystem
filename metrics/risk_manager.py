from core.config import MAX_DRAWDOWN, WARNING_DRAWDOWN, STOP_LOSS_PER_TRADE, CAPITAL

def get_portfolio_risk_level(strategy,current_equity):
    """
    This will return the current risk level of a portfolio.
    Safe means normal trading and no issues. Warning means that drawdown has exceeded halfway mark and to reduce position size. Critical means to stop buying immediately, the kill switch has been exceeded by drawdown.
    Peak equity is the factor instead of starting capital to protect profits.
    """
    start =CAPITAL[strategy]
    drawdown=(current_equity-start)/start
    
    #return statements
    if drawdown<=MAX_DRAWDOWN[strategy]:
        return "critical"
    elif drawdown <=WARNING_DRAWDOWN[strategy]:
        return "warning"
    else:
        return "safe"
    


def get_position_size(strategy,current_equity,base_size):
    """
    Returns the adjusted position size based on the current level of risk. If safe, full position size. if warning, half position size (to reduce risk before kill switch is tripped), if critical 0 (stop buying immediately)
    base size is the normal max position size from config btw
    """
    risk_level=get_portfolio_risk_level(strategy,current_equity)


    if risk_level =="critical":#sell now
        return 0.0
    elif risk_level=="warning":
        return base_size*.5#half
    else:
        return base_size #safe
    


def check_stop_loss(strategy,entry_price,current_price):
    """
    if stop loss has been activated for a position it will hit true. It will compare current price to entry price using the stop_loss-per_trade limit
    """
    if entry_price<=0:
        return False
    loss_per_trade=((current_price-entry_price)/entry_price)
    return (loss_per_trade<=-STOP_LOSS_PER_TRADE[strategy])



def should_close_position(strategy,entry_price,current_price,current_equity):
    """
    This is a master check that determines if a position must be closed immediately. Combines both stop loss check and portfolio risk level.
    Returns trueif the position should be closed, false if safe to hold.
    """
    #close if stop loss hits
    if check_stop_loss(strategy,entry_price,current_price):
        print(f"Stop loss was triggered for {strategy} \n entry was ${entry_price:.2f} and current price is ${current_price:.2f}")
        return True
    

    #if portfolio has hit critical, close now
    risk_level=get_portfolio_risk_level(strategy,current_equity)
    if risk_level=="critical":
        print(f"Portfolio for {strategy} has hit critical, closing positions")
        return True;

    return False;