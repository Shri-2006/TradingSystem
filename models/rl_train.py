import os
import numpy as np
from datetime import datetime, timedelta
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from models.rl_environment import TradingEnvironment
from data.polygon_fetcher import get_historical_data
from core.features import build_features
from data.sentiment_fetcher import add_sentiment_to_df
from core.config import CAPITAL, MAX_POSITION_SIZE

#the path the model will save itself in
MODEL_PATH="models/risky2_model.zip"
strategy="risky2"
def prepare_rl_data(ticker,days_to_look_back=365): #look back one year
    """
    This will prepare historical data by building features for RL training. Its set up to use one year of data for default so that it can see multipke types of market regimes like trending, volaitle, ranging
    """
    end=datetime.today().strftime('%Y-%m-%d')
    start=(datetime.today()-timedelta(days=days_to_look_back)).strftime('%Y-%m-%d');
    print(f"Fetching data for {ticker} from these dates {start} to {end}............");
    df=get_historical_data(ticker,start,end)
    if df.empty:
        raise ValueError(f"There is no data returned for {ticker}");
    df=build_features(df);
    df=add_sentiment_to_df(df,ticker)
    df=df.dropna()
    print(f"There are {len(df)} rows prepared for training the RL model");
    return df;


def train_rl_model(ticker="Symbol/Base",days_to_look_back=365,timesteps=500000):#increased timesteps to 500000 to be mroe accurate
    
    """
    This will train Proximal policy optimization (PPO) model on historical crypto data. The ticker is crypto pair in alpaca format such as BTC/USD, and timesteps is how many steps the PPO trains for. 50000 is an amount that likely won't take hours to train but is still enough to do basic patterns    
    https://en.wikipedia.org/wiki/Proximal_policy_optimization
    """
    #call prepare data and create environment
    df=prepare_rl_data(ticker,days_to_look_back);
    env=TradingEnvironment(df=df, initial_capital=CAPITAL[strategy],max_position_pct=MAX_POSITION_SIZE[strategy]/CAPITAL[strategy]);

    #check environmetn to be safe, then start building ppo agent

    print("Environment being checked ............");
    check_env(env,warn=True)
    #Mlppolicy is multi layer perception, a standard in non image training https://stable-baselines.readthedocs.io/en/master/modules/policies.html
    print("PPO (Proximal policy optimization) agent being built....")
    model=PPO(policy="MlpPolicy",env=env,verbose=1,learning_rate=3e-4,n_steps=2048,batch_size=128,n_epochs=10, gamma=.99, seed=100)#verbose means to print training progress, learning rate standard is 3e-4, standard steps for ppo is 2048 per update, batch size is 128 because why not, epochs (one entire pass through the entire data set) is 10 per update, and the gamma is how much agent values rewards(0 means instant profit search while .99 means it tries to go for long term gain). Seed is to be able to reproduce it

    #train and save the model
    print(f"Training PPO on {ticker} for {timesteps} steps.....")
    model.learn(total_timesteps=timesteps)

    model.save(MODEL_PATH)
    print(f"Model saved in {MODEL_PATH}")
    return model;

def load_rl_model():
    """
    To load a trained PPO model from the hard disk. If the model doesnt exist it will return none.
    """
    if(os.path.exists(MODEL_PATH)):
        print("loading an existing RL model from disk.....")
        return PPO.load(MODEL_PATH)
    print("no RL model was found and it needs to be trained first")
    return None

if __name__=="__main__":
    train_rl_model();