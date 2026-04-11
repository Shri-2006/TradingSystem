import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'trades.db')

def init_db():
    """Creates trades and heartbeat tables if they don't exist. Enables WAL mode."""
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()

    # Enable write ahead logging (WAL, a SQLite setting that has the bot write a trade to separate log file, have dashboard read, then merges the files which allows dashboard to read while bots write simultaneously)
    cursor.execute("PRAGMA journal_mode=WAL")

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

    # Heartbeat table - each bot writes here every 30 seconds to show state of strategy
    # Dashboard uses this to show RUNNING/PAUSED/DISCONNECTED
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heartbeat (
            strategy    TEXT    PRIMARY KEY,
            last_seen   TEXT    NOT NULL,
            status      TEXT    NOT NULL
        )
    ''')

    syst.commit()
    syst.close()

def log_trade(strategy, asset, action, price, quantity, pnl=None, reason=None):
    """
    Logs a single trade to the database.
    strategy: "stable" | "risky1" | "risky2"
    asset   : e.g. "SPY" or "BTC/USDT"
    action  : "BUY" | "SELL" | "HOLD"
    price   : price at time of trade
    quantity: how much was bought or sold
    pnl     : profit or loss (if not yet closed, None)
    reason  : why the trade fired
    """
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()
    cursor.execute('''
        INSERT INTO trades (timestamp, strategy, asset, action, price, quantity, pnl, reason)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (datetime.utcnow().isoformat(), strategy, asset, action, price, quantity, pnl, reason))
    syst.commit()
    syst.close()

def log_heartbeat(strategy, status="RUNNING"):
    """
    Each bot calls this every 30 seconds to signal it is alive.
    Dashboard checks last_seen — if stale shows DISCONNECTED.
    """
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()
    cursor.execute('''
        INSERT INTO heartbeat (strategy, last_seen, status)
        VALUES (?, ?, ?)
        ON CONFLICT(strategy) DO UPDATE SET
            last_seen = excluded.last_seen,
            status    = excluded.status
    ''', (strategy, datetime.utcnow().isoformat(), status))
    syst.commit()
    syst.close()

def get_heartbeat(strategy):
    """
    Returns last heartbeat for a strategy.
    Returns None if bot has never run.
    """
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()
    cursor.execute('SELECT last_seen, status FROM heartbeat WHERE strategy = ?', (strategy,))
    row = cursor.fetchone()
    syst.close()
    return row

def get_trades(strategy=None):
    """
    Retrieves trades from the database.
    Pass strategy name to filter or leave empty to get all trades.
    """
    syst = sqlite3.connect(DB_PATH)
    cursor = syst.cursor()
    if strategy:
        cursor.execute('SELECT * FROM trades WHERE strategy = ?', (strategy,))
    else:
        cursor.execute('SELECT * FROM trades')
    rows = cursor.fetchall()
    syst.close()
    return rows

# Initialize database on import
init_db()












































































































































#this is the old one, im just keeping it here to see what i did on my own
# import os
# import sqlite3
# from datetime import datetime

# #creating a database at the root of the project as trades.db
# DB_PATH=os.path.join(os.path.dirname(__file__),'..','trades.db')

# #creating database tables if it doesn't yet exist
# def init_db():
#     """CREATES THE TRADES TABLE IF IT DOES NOT EXIST"""
#     syst = sqlite3.connect(DB_PATH)
#     cursor = syst.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS trades (
#             id          INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp   TEXT    NOT NULL,
#             strategy    TEXT    NOT NULL,
#             asset       TEXT    NOT NULL,
#             action      TEXT    NOT NULL,
#             price       REAL    NOT NULL,
#             quantity    REAL    NOT NULL,
#             pnl         REAL,
#             reason      TEXT
#         )
#     ''')
#     syst.commit()
#     syst.close()

# #function to log each trade to database
# def log_trade(strategy,asset,action,price,quantity,pnl=None,reason=None):
#     """
#     Logs a single trade to the database
#     strategy: "stable" | "risky1" | "risky2"
#     asset   : e.g. "SPY" or "BTC/USDT"
#     action  : "BUY" | "SELL" | "HOLD"
#     price   : price at time of trade
#     quantity: how much was bought or sold
#     pnl     : profit or loss (if not yet closed, None)
#     reason  : why the trade fired e.g. "Signal of ML" or "Kill Switch"
#     """
#     syst=sqlite3.connect(DB_PATH)
#     cursor=syst.cursor();
#     cursor.execute('''
#                    INSERT INTO trades (timestamp, strategy, asset, action,price,quantity,pnl,reason)
#                    VALUES (?,?,?,?,?,?,?,?)
#                    ''',(
#                        datetime.utcnow().isoformat(), strategy, asset, action, price, quantity, pnl,  reason
#                    )
#                    )
#     syst.commit()
#     syst.close()

#     #get trades from database
# def get_trades(strategy=None):
#     """
#     Retrieves trades from the database
#     Pass the strategy name to the filter or leave empty to get all of the trades
#     """
#     syst=sqlite3.connect(DB_PATH)
#     cursor=syst.cursor()
#     if strategy:
#         cursor.execute('SELECT * FROM trades WHERE strategy = ?', (strategy,))
#     else:
#         cursor.execute('SELECT * FROM trades')
#     rows=cursor.fetchall()
#     syst.close()
#     return rows
    

# #when file gets imported the database gets initialized
# init_db()
    