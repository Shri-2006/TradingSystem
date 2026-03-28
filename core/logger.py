import os
import sqlite3
from datetime import datetime

#creating a database at the root of the project as trades.db
DB_PATH=os.path.join(os.path.dirname(__file__),'..','trades.db')

#creating database tables if it doesn't yet exist
def init_db():
    """CREATES THE TRADES TABLE IF IT DOES NOT EXIST"""
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            strategy    TEXT    NOT NULL,
            asset       TEXT    NOT NULL,
            action      TEXT    NOT NULL,
            price       REAL    NOT NULL,
            quantity    REAL    NOT NULL,
            pnl         REAL,
            reason      TEXT
        )
    ''')
    syst.commit()
    syst.close()

#function to log each trade to database
def log_trade(strategy,asset,action,price,quantity,pnl=None,reason=None):
    """
    Logs a single trade to the database
    strategy: "stable" | "risky1" | "risky2"
    asset   : e.g. "SPY" or "BTC/USDT"
    action  : "BUY" | "SELL" | "HOLD"
    price   : price at time of trade
    quantity: how much was bought or sold
    pnl     : profit or loss (if not yet closed, None)
    reason  : why the trade fired e.g. "Signal of ML" or "Kill Switch"
    """
    syst=sqlite3.connect(DB_PATH)
    cursor=syst.cursor();
    cursor.execute('''
                   INSERT INTO trades (timestamp, strategy, asset, action,price,quantity,pnl,reason)
                   VALUES (?,?,?,?,?,?,?,?)
                   ''',(
                       datetime.utcnow().isoformat(), strategy, asset, action, price, quantity, pnl,  reason
                   )
                   )
    syst.commit()
    syst.close()

    #get trades from database
def get_trades(strategy=None):
    """
    Retrieves trades from the database
    Pass the strategy name to the filter or leave empty to get all of the trades
    """
    syst=sqlite3.connect(DB_PATH)
    cursor=syst.cursor()
    if strategy:
        cursor.execute('SELECT * FROM trades WHERE strategy = ?', (strategy,))
    else:
        cursor.execute('SELECT * FROM trades')
    rows=cursor.fetchall()
    syst.close()
    return rows
    

#when file gets imported the database gets initialized
init_db()
    