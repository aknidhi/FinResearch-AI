import os

APP_NAME = "FinSight AI"
APP_TAGLINE = "Global Market Research Workspace"
DEFAULT_SYMBOLS = ["AAPL", "MSFT", "RELIANCE.NS", "TSLA"]
DB_PATH = os.getenv("DB_PATH", "data/finsight.db")

def get_secret(name, default=""):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, default)
        return value or default
    except Exception:
        return default

GROQ_MODEL = get_secret("GROQ_MODEL", "openai/gpt-oss-20b")
CACHE_TTL_SECONDS = int(get_secret("CACHE_TTL_SECONDS", "900"))
NEWS_CACHE_TTL_SECONDS = int(get_secret("NEWS_CACHE_TTL_SECONDS", "900"))
