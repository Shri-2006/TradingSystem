import pandas as pd
from textblob import TextBlob
from polygon import RESTClient
from core.config import POLYGON_API_KEY

client = RESTClient(api_key=POLYGON_API_KEY)
def get_sentiment(ticker, limit=10):
    """
    Fetches the most recent news headlines for the given ticker and scores a sentiment for it.
    Tickers are things like AAPL or SPY
    limit: how many articles to analyze
    returns: average sentiment scores will be between -1.0 and 1.0, with -1 being very negative sentiment, 0 neutral, and 1 as very positive

    """

    news= client.list_ticker_news(ticker,limit=limit)
    scores=[]#will be filled later
    for article in news:
        headline=article.title
        score=TextBlob(headline).sentiment.polarity
        scores.append(score)
    if not scores:
        return 0.0 #should no news be found, consider it as neutral
    return sum(scores)/len(scores)#return the average score
def get_sentiment_label(score):
    """
    Basically converts the numeric score to a readable label

    """
    positive="POSITIVE"
    neutral="NEUTRAL"
    negative="NEGATIVE"
    if score>.1:return positive
    elif score<-.1:return negative
    else: return neutral

def add_sentiment_to_df(df,ticker):
    """
    adds sentiment score col to any dataframe with the OHLCV stuff. Its called from inside build_features before ML training
    """

    score=get_sentiment(ticker)
    df['sentiment']=score#all rows will have same score
    return df
