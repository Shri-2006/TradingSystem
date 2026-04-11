import os
import time
import threading #i want the bots to run side by side so that the run_stable and run_risky1 both start (since they run infintely)
from models.retrain import start_scheduler
from strategies.stable import run as run_stable
from strategies.risky1 import run as run_risky1
from strategies.risky2 import run as run_risky2
from paper_trading.alpaca_paper import is_market_open
from core.config import FEATURE_FLAGS

def main():
    """
    This will be the main function. it starts the tradingsystem through these steps
    In the background it starts retraining scheduler
    Launches stable and risky1 in separte threads
    keeps main process alive
    """
    print("="*50)
    print(" Trading System Starting....")
    print("="*50)

    #retraining scheduler start background
    scheduler=start_scheduler()

    #separate threads per bbot
    stable_thread=threading.Thread(target=run_stable,daemon=True, name="stable")
    risky1_thread=threading.Thread(target=run_risky1,daemon=True,name="risky1")
    risky2_thread=threading.Thread(target=run_risky2,daemon=True,name="risky2")
    
    stable_thread.start()
    print("Stable strat bot thread has started")
    risky1_thread.start()
    print("Risky1 strat bot threat started")
    if FEATURE_FLAGS["risky2_enabled"]==True:
        risky2_thread.start()
        print("Risky2 RL bot for crypto thread is started")
        #Keeping the main procecss alive
    else:
        print("risky2 rl bot is currently disabled in config.py, enable it when model is trained")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nShutting down TradingSystem due to user input...")
        scheduler.shutdown()
        print("Scheduler has stopped. Goodbye for now!")

if __name__ == "__main__":
    main()