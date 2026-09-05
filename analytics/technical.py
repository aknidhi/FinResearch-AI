import numpy as np
import pandas as pd

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    result = 100 - (100 / (1 + rs))
    return result.fillna(50)

def build_analysis(history):
    df = history.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["RSI14"] = rsi(df["Close"], 14)
    df["DailyReturn"] = df["Close"].pct_change()
    vol = df["DailyReturn"].std() * np.sqrt(252) * 100
    last = float(df["Close"].iloc[-1])
    sma20 = float(df["SMA20"].iloc[-1]) if pd.notna(df["SMA20"].iloc[-1]) else last
    sma50 = float(df["SMA50"].iloc[-1]) if pd.notna(df["SMA50"].iloc[-1]) else last
    r = float(df["RSI14"].iloc[-1])
    score = 0
    score += 1 if last > sma20 else -1
    score += 1 if last > sma50 else -1
    score += 1 if r > 55 else (-1 if r < 45 else 0)
    label = "Bullish" if score >= 2 else "Bearish" if score <= -2 else "Neutral"
    df.attrs["annualized_volatility"] = float(vol) if pd.notna(vol) else 0.0
    df.attrs["signal"] = {"label": label, "score": score, "rsi_zone": "Overbought" if r >= 70 else "Oversold" if r <= 30 else "Normal"}
    return df

def comparison_table(symbols, period="6mo"):
    from services.market_data import get_price_history, get_fundamentals
    rows=[]
    for symbol in symbols:
        try:
            h=get_price_history(symbol, period=period, interval="1d")
            if h.empty: continue
            start=float(h["Close"].iloc[0]); end=float(h["Close"].iloc[-1])
            ret=(end/start-1)*100
            vol=float(h["Close"].pct_change().std()*np.sqrt(252)*100)
            f=get_fundamentals(symbol)
            rows.append({
                "Symbol":symbol,
                "Last Price":end,
                "Return %":ret,
                "Volatility %":vol,
                "P/E":f.get("trailingPE"),
                "Market Cap":f.get("marketCap"),
                "Sector":f.get("sector","N/A")
            })
        except Exception:
            continue
    return pd.DataFrame(rows)
