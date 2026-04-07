import time
from datetime import date
from textblob import TextBlob
from polygon import RESTClient
from core.config import POLYGON_API_KEY

client = RESTClient(api_key=POLYGON_API_KEY)
# Daily cache — each ticker gets score once per day
_sentiment_cache = {}
_cache_date = {}
_last_fetch_time = {}  # {ticker: timestamp of last fetch attempt}

FETCH_INTERVAL = 300  # 5 minutes between tickers fetched


def get_sentiment(ticker, limit=10):
    """
    Fetches the most recent news headlines for the given ticker and scores a sentiment for it once per day, and spreaded out to once every 5 minutes it will fetch one ticker
    """
    today=date.today();
    #if fetched once in the day so far, it will fetch cache
    if (_cache_date.get(ticker)==today) and (ticker in _sentiment_cache):
        return _sentiment_cache[ticker];
    now=time.time()
    last=_last_fetch_time.get(ticker,0);
    if now-last<FETCH_INTERVAL:
        return _sentiment_cache.get(ticker,0.0)
    
    #in all other cases it should be able to fetch if it got to this point
    _last_fetch_time[ticker]=now;
    try:
        news=client.list_ticker_news(ticker,limit=limit)
        scores=[]
        for article in news:
            score=TextBlob(article.title).sentiment.polarity
            scores.append(score)
        if (scores):
            result=sum(scores)/len(scores)
        else:
            result=0.0
    except Exception as e:
        print(f"Error, Warning the sentiment failed to fetch for {ticker}, using neutral 0.0 \n-{e}")
        result=0.0;
    _sentiment_cache[ticker]=result;
    _cache_date[ticker]=today;
    return result
        #learned that Ctrl + / will mass comment, very nice
    # try:
    #     import time
    #     time.sleep(12)  # avoid rate limiting
    #     news = client.list_ticker_news(ticker, limit=limit)
    #     scores = []
    #     for article in news:
    #         headline = article.title
    #         score = TextBlob(headline).sentiment.polarity
    #         scores.append(score)
    #     if not scores:
    #         return 0.0
    #     return sum(scores) / len(scores)
    # except Exception as e:
    #     print(f"Warning: sentiment fetch failed for {ticker}, using neutral — {e}")
    #     return 0.0  # fall back to neutral if rate limited
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
    df=df.copy()
    df['sentiment']=score#all rows will have same score
    return df
