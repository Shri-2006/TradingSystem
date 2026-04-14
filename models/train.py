import os 
import pickle #to save python objects to file and go back. XGBoost will use .pkl file type
import numpy as np #numpy is used by XGBoost and sklearn for math operations in arrays
import pandas as pd #DataFrames library
from xgboost import XGBClassifier #Xgboost is decision tree algo that is inddustry standard for table data, and will be the actual ml model i train.
from sklearn.model_selection import train_test_split #split data to training data and testnig data, to prevent overfitting of model on certain data. Learned this concept at Incture during Summer 2025 internship
from sklearn.metrics import accuracy_score #gives percentage of correct predictions : .25=25% correct accuracy
from core.features import build_features #OHLCV into indicators, i built this
from data.polygon_fetcher import get_historical_data, get_multiple_tickers #get historical data for training
from data.sentiment_fetcher import add_sentiment_to_df #include sentiment score in df
from core.config import STABLE_ASSETS, RETRAIN_INTERVAL_DAYS #Asset whitelist and retraining interval is brought from config to prevent too many repetitons

#Location of saved trained models
MODEL_DIR= os.path.join(os.path.dirname(__file__))

def create_labels(df):
    """
    Creates a buy and sell label from the price data.
    If tomorrows close > todays close -> 1 and buy. If tomorrows close < todays close -> sell or hold
    """
    df=df.copy() #make a copy and edit that dataframe
    df['label']= ((df['close'].shift(-1)>df['close']).astype(int))
    df.dropna(inplace=True)#removes the last row because there is no need to compare tomorrow
    return df

def prepare_data(df, ticker):
    """
    The data will go from:
    raw data-> features -> labels-> data for training
    Features and Labels will be returned in numpy arrays
    """
    df=build_features(df)
    df=add_sentiment_to_df(df,ticker)
    df=create_labels(df)

    #columns that arent label open high low close volume aren't features and should be droppped from the copy
    feature_cols=[c for c in df.columns if c not in ['label','open','high','low','close','volume']]

    X=df[feature_cols].values
    Y=df['label'].values
    return X,Y

#Now to actually train the model
def train_model(X,Y):
    """
    XGBoost classifer is trained and it will return the model and accuracy score
    """

    X_train, X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,shuffle=False)#false to prevent messing order of time
    model=XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,use_label_encoder=False,eval_metric='logloss')#n_estimator=number of trees, max_depth is how deep per tree, learning rate is the rate model learns

    model.fit(X_train,Y_train)
    accuracy=accuracy_score(Y_test,model.predict(X_test))
    print(f"Model Accuracy: {accuracy: .2%}")
    return model, accuracy
    
def save_model(model,filename):
    """
    Time to save the trained model in .pkl file. The filename is going to be something like "stable_model.pkl"
    """
    path=os.path.join(MODEL_DIR,filename)
    with open(path,'wb') as f:
        pickle.dump(model,f)
    print(f"Model saved to {path}")

def load_model(filename):
    """
    Load the saved model from file.  The filename is going to be something like "stable_model.pkl" again
    """
    path=os.path.join(MODEL_DIR,filename)
    with open(path,'rb')as f:
        model=pickle.load(f)
    return model

def train_and_save(strategy, start, end):
    """
    Basically this fetches data, prepares, traines model, and then saves the model. 
    The possible strategies are "stable" or "risky1" (risky2 is being done differently)
    start and end date strings are in "YYYY-MM-DD" format
    """

    print(f"Training {strategy} model...")
    if strategy== "stable": 
        tickers= STABLE_ASSETS
        filename="stable_model.pkl"
    elif strategy == "risky1":
        tickers= ["SPY"] #temporary placeholder until the ML picks new assets for risky1
        filename="risky1_model.pkl"
    else:
        print(f"unknown strategy, are you sure you have the right name? : {strategy}")
        return;
    all_X=[]
    all_Y=[]
    #fetching data and putting all data from all tickers together
    data=get_multiple_tickers(tickers,start,end)
    for t, df in data.items():
        X,Y=prepare_data(df,t)
        all_X.append(X)
        all_Y.append(Y)
    X_combined=np.vstack(all_X)
    Y_combined=np.concatenate(all_Y)

    model,accuracy=train_model(X_combined,Y_combined)
    save_model(model,filename)
    print(f"{strategy} model was trained with an accuracy of {accuracy: .2%}")


#if __name__ == "__main__"