import pandas as pd# excel of python
import numpy as np #math operations of data
from ta.momentum import RSIIndicator #Checks overbought or oversold
from ta.trend import SMAIndicator, EMAIndicator #SMA= average price over n amount of days and EMA is the same but greater weight on recent data(better for price changes)
from ta.volatility import BollingerBands, AverageTrueRange #For grid tracking, it keeps measurement of where to overbuy vs oversold. ATR is how the measurement of price changes on average per day. higer atr=more volatility


def add_moving_averages(df):
    """
    Adds short and long-term moving averages to the dataframe
    df must have a 'close' column
    """

    df['sma_20'] = SMAIndicator(df['close'], window=20).sma_indicator() #looks at past 20 bars and average close price over 20 days
    df['sma_50'] = SMAIndicator(df['close'], window=50).sma_indicator()#looks at past 50 bars and average close price over 50 days
    df['ema_12']=EMAIndicator(df['close'],window=12).ema_indicator() #looks at past 12 bars and average close price over 12 days, with more emphasis based on how recent the data is
    df['ema_26']=EMAIndicator(df['close'],window=26).ema_indicator() #looks at past 26 bars and average close price over 26 days, with more emphasis based on how recent the data is

    return df;

def add_momentum(df):
    """
    Adds RSI and price momentum to the dataaframe
    RSI>70 = overbought while RSI <30 = oversold
    """
    df['rsi']=RSIIndicator(df['close'],window=14).rsi()
    # pct_change is how much price has changed over those bars as a percentage, positive=up, negative=trending down
    df['momentum_5']=df['close'].pct_change(periods=5)#momentum of 5 bars,
    df['momentum_15']=df['close'].pct_change(periods=15)#momentum of 15 bars
    return df


def add_volatility(df):
    """
    Adds Bollinger Bands and ATR to the dataframe. 
    Bollinger bands show overbought and oversold zone areas
    ATR will measure how volatile the asset is at the moment
    """
    bb=BollingerBands(df['close'],window=20,window_dev=2)
    df['bb_upper']=bb.bollinger_hband()#upper band
    df['bb_middle']=bb.bollinger_mavg()#middle band is sma20 btw
    df['bb_lower'] = bb.bollinger_lband()#lower band
    df['atr']=AverageTrueRange(
        df['high'],df['low'],df['close'],window=14
    ).average_true_range()
    return df

def add_zscore(df, window = 20):
    """
    Z-score will measure how far the price is from the mean
    Z>2 means unusally high price and will likely drop
    Z<-2 means price is extradonarily low and will likely rise
    Basically Key signal for the grid trading strategy
    """
    #rolling means the in the most recent time period
    rolling_mean=df['close'].rolling(window=window).mean()
    rolling_std=df['close'].rolling(window=window).std()
    df['zscore']=(df['close']-rolling_mean)/rolling_std
    return df

def add_volume_change(df):
    """
    Measures unusual volume activity, a big price move with a high volume is far more reliable than a big price move with low volume
    """
    df['volume_change']=df['volume'].pct_change(periods=1)#change from previous bar 
    df['volume_ma_20']=df['volume'].rolling(window=20).mean()#average over last 20 bars
    df['volume_ratio']=df['volume']/df['volume_ma_20'] #1 is average, 2.5 is very large change, .3 would be a very small amount of price moves, and shouldn't be trusted.
    return df

    
def build_features(df):
    """
    Main function that will run all feature engineerings in order. 
    This will be called on any raw dataframe before it is fed to ML model
    df must have columns: {open, high, low, close, volume} to store the data
    """
    df=df.copy()#copy original dataframe, original should not be affected
    df=add_moving_averages(df)
    df=add_momentum(df)
    df=add_volatility(df)
    df=add_zscore(df)
    df=add_volume_change(df)
    df.dropna(inplace=True)#remove rows that don't have values from the calculations that roll
    return df
