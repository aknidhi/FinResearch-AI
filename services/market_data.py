import re
import pandas as pd
import yfinance as yf
import streamlit as st

from config import CACHE_TTL_SECONDS
from utils import clean_symbol, safe_float

COMMON_SUFFIXES = (".NS", ".BO", ".L", ".TO", ".AX", ".HK", ".T", ".DE", ".PA", ".F", ".SW", ".SS", ".SZ", ".KS", ".KQ", ".SA", ".SI")

def _clean_query(symbol):
    s = clean_symbol(symbol)
    return re.sub(r"[^A-Z0-9.\-^=]", "", s)

@st.cache_data(ttl=3600, show_spinner=False)
def resolve_symbol(query):
    """Resolve a simple ticker into a Yahoo Finance symbol.

    If the user supplies an exchange suffix, it is preserved. For bare tickers,
    Yahoo Finance search is used. Exact history is preferred before search results.
    """
    raw = _clean_query(query)
    if not raw:
        raise ValueError("Enter a ticker symbol, for example AAPL, TSLA, SAP, or RELIANCE.NS.")
    if raw.startswith("^") or raw.endswith("=X") or raw.endswith("=F") or "." in raw:
        return raw
    # First try the bare symbol directly (works for many US-listed securities).
    try:
        h = yf.Ticker(raw).history(period="5d", interval="1d", auto_adjust=False)
        if h is not None and not h.empty:
            return raw
    except Exception:
        pass
    try:
        result = yf.Search(raw, max_results=10)
        quotes = result.quotes or []
        candidates = [q for q in quotes if q.get("symbol") and q.get("quoteType") in {"EQUITY", "ETF", "MUTUALFUND", "INDEX", "CRYPTOCURRENCY"}]
        exact = [q for q in candidates if str(q.get("symbol", "")).upper() == raw]
        if exact:
            return exact[0]["symbol"]
        if candidates:
            # Prefer a highly relevant exact-looking ticker, otherwise Yahoo's ranking.
            for q in candidates:
                sym = str(q.get("symbol", ""))
                if sym.upper().split(".")[0] == raw:
                    return sym
            return candidates[0]["symbol"]
    except Exception:
        pass
    # Friendly fallback for well-known Indian tickers when search is unavailable.
    if raw in {"RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "ITC", "LT"}:
        return raw + ".NS"
    return raw

def normalize_symbol(symbol):
    return resolve_symbol(symbol)

@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_price_history(symbol, period="1y", interval="1d"):
    symbol = normalize_symbol(symbol)
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
    if df is None or df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    required = ["Open", "High", "Low", "Close", "Volume"]
    for c in required:
        if c not in df.columns:
            df[c] = pd.NA
    return df[required].dropna(subset=["Close"])

@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_fundamentals(symbol):
    symbol = normalize_symbol(symbol)
    ticker = yf.Ticker(symbol)
    data = {}
    try:
        info = ticker.info or {}
    except Exception:
        info = {}
    keys = [
        "symbol", "shortName", "longName", "exchange", "fullExchangeName", "exchangeTimezoneName", "quoteType", "currency", "financialCurrency",
        "sector", "industry", "marketCap", "trailingPE", "forwardPE", "priceToBook", "debtToEquity",
        "returnOnEquity", "returnOnAssets", "revenueGrowth", "earningsGrowth", "profitMargins", "dividendYield",
        "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "beta", "bookValue", "currentPrice", "website", "country"
    ]
    for k in keys:
        data[k] = info.get(k)
    data["symbol"] = symbol
    data["currency"] = data.get("currency") or data.get("financialCurrency") or "USD"
    data["display_name"] = data.get("shortName") or data.get("longName") or symbol
    return data

def get_market_snapshot(symbol, history):
    symbol = normalize_symbol(symbol)
    if history.empty:
        return {"symbol": symbol, "price": None, "change_pct": None, "volume": None}
    close = history["Close"].dropna()
    price = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close) > 1 else price
    change = (price / prev - 1) * 100 if prev else 0
    volume = history["Volume"].iloc[-1] if "Volume" in history else None
    return {"symbol": symbol, "price": price, "change_pct": change, "volume": safe_float(volume)}
