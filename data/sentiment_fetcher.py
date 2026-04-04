import pandas as pd
from textblob import TextBlob
from polygon import RESTClient
from core.config import POLYGON_API_KEY

client = RESTClient(api_key=POLYGON_API_KEY)
def get_sentiment(ticker, limit=10):
    """
    Fetches the most recent news headlines for the given ticker and scores a sentiment for it.
    """
    try:
        import time
        time.sleep(12)  # avoid rate limiting
        news = client.list_ticker_news(ticker, limit=limit)
        scores = []
        for article in news:
            headline = article.title
            score = TextBlob(headline).sentiment.polarity
            scores.append(score)
        if not scores:
            return 0.0
        return sum(scores) / len(scores)
    except Exception as e:
        print(f"Warning: sentiment fetch failed for {ticker}, using neutral — {e}")
        return 0.0  # fall back to neutral if rate limited
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
