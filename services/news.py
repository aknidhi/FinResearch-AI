from email.utils import parsedate_to_datetime
import requests
import feedparser
import streamlit as st
from textblob import TextBlob
from config import NEWS_CACHE_TTL_SECONDS, get_secret


def _sentiment(text):
    polarity = float(TextBlob(text).sentiment.polarity)
    if polarity > 0.05: label = "Positive"
    elif polarity < -0.05: label = "Negative"
    else: label = "Neutral"
    return polarity, label

def _query_name(symbol):
    return symbol.replace(".NS", "").replace(".BO", "").replace(".L", "").replace(".TO", "").replace(".AX", "")

def _newsapi(symbol):
    key = get_secret("NEWSAPI_KEY", "")
    if not key: return []
    query = _query_name(symbol)
    try:
        r = requests.get("https://newsapi.org/v2/everything", params={"q": query, "language": "en", "sortBy": "publishedAt", "pageSize": 10, "apiKey": key}, timeout=8)
        r.raise_for_status()
        out=[]
        for a in r.json().get("articles", []):
            title=a.get("title") or ""
            pol,label=_sentiment(title)
            out.append({"title":title,"source":(a.get("source") or {}).get("name","NewsAPI"),"published":a.get("publishedAt","")[:19].replace("T"," "),"url":a.get("url",""),"sentiment":pol,"label":label})
        return out
    except Exception: return []

@st.cache_data(ttl=NEWS_CACHE_TTL_SECONDS, show_spinner=False)
def get_news(symbol):
    news = _newsapi(symbol)
    if news: return news
    query = _query_name(symbol) + " stock"
    try:
        r=requests.get("https://news.google.com/rss/search", params={"q":query,"hl":"en-US","gl":"US","ceid":"US:en"}, timeout=8)
        r.raise_for_status()
        feed=feedparser.parse(r.content)
        out=[]
        for entry in feed.entries[:10]:
            title=entry.get("title","")
            pol,label=_sentiment(title)
            published=entry.get("published","")
            try: published=parsedate_to_datetime(published).strftime("%Y-%m-%d %H:%M")
            except Exception: pass
            source=entry.get("source",{})
            source=source.get("title","Google News") if isinstance(source,dict) else "Google News"
            out.append({"title":title,"source":source,"published":published,"url":entry.get("link",""),"sentiment":pol,"label":label})
        return out
    except Exception: return []
