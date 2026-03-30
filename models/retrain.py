import os
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler #this will schedule in the background for eveyr 14 days to retrain calls train_and_save() for stable and risky1 emthod
from models.train import train_and_save
from core.config import RETRAIN_INTERVAL_DAYS

def get_date_range():
    """
    Gets the start and end dates for retraining, and will train on the most recent 2 years of data

    """
    end=datetime.today().strftime('%Y-%m-%d')
    years_to_train=2
    days_to_train=years_to_train*365
    start=(datetime.today()-timedelta(days=(days_to_train))).strftime('%Y-%m-%d')
    return start,end
def retrain_all():
    """
    Retrains all supervised learning models on fresh data, and is called automatically every 14 days by APScheduler
    """
    print(f"Retraining all models at {datetime.now()}...")
    start,end=get_date_range()
    train_and_save("stable",start,end)
    train_and_save("risky1",start,end)
    print("Retraining has been completed. \n")
    return

def start_scheduler():
    """
    Starts the background scheduler to run retrain_all() every RETRAIN_INTERVAL_DAYS days. Its called from run.py at the system boot
    """
    scheduler=BackgroundScheduler()
    scheduler.add_job(
        retrain_all,trigger='interval',days=RETRAIN_INTERVAL_DAYS,next_run_time=None #Bascailly don't start retraining as soon as system boots
    )
    scheduler.start()
    print(f"Retraining scheduler has started and will run retrain every {RETRAIN_INTERVAL_DAYS} days")
    return scheduler