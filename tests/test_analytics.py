import numpy as np
import pandas as pd
from analytics.technical import rsi, build_analysis
from utils import indian_market_status, clean_symbol

def sample_history(n=80):
    idx=pd.date_range("2025-01-01", periods=n, freq="D")
    close=pd.Series(np.linspace(100,140,n), index=idx)
    return pd.DataFrame({
        "Open":close-1,
        "High":close+2,
        "Low":close-2,
        "Close":close,
        "Volume":np.full(n,100000)
    }, index=idx)

def test_symbol_cleaning():
    assert clean_symbol(" reliance.ns ") == "RELIANCE.NS"

def test_rsi_range():
    x=pd.Series(np.arange(1,40,dtype=float))
    out=rsi(x)
    assert ((out>=0)&(out<=100)).all()

def test_build_analysis_columns():
    out=build_analysis(sample_history())
    for col in ["SMA20","SMA50","RSI14","DailyReturn"]:
        assert col in out.columns
    assert "label" in out.attrs["signal"]
