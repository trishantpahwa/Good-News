from transformers import pipeline
from requests import get
from dotenv import dotenv_values
from datetime import datetime, timedelta

API_KEY = dotenv_values(".env")["API_KEY"]


def handler(event, context):
    good_news = sentiment_analysis("Software development")
    print(good_news)

# This lambda is a layer, to the API that fetches news.
def sentiment_analysis(q, from_date=None, to_date=None):
    # Check for source and pass it in the parameter as list of verified sources.
    sentiment_analysis_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    # data = ["I like studying Hugging Face from Britney, because she introduced me to the easiest way to train machines and make machines learn.", "News"]
    from_date = from_date if from_date != None else str((datetime.now() - timedelta(1)).date())
    to_date = to_date if to_date != None else str(datetime.now().date())
    NEWS_API_URL = "https://newsapi.org/v2/everything?from=" + from_date + "&to=" + to_date + "&q=" + q + "&apiKey=" + API_KEY
    response = get(NEWS_API_URL)
    articles = response.json()["articles"]
    for article in articles:
        news = list(article.values())
        news[0] = news[0]["name"]
        article["good_news"] = True
        for sentence in news:
            _sentence = str(sentence)
            news_type = sentiment_analysis_pipeline(_sentence)
            news_type[0]["sentence"] = _sentence
            if news_type[0]["label"] == "NEG":
                article["good_news"] = False
                break
    for article in articles:
        if article["good_news"] == True:
            print(article)

handler(None, None)