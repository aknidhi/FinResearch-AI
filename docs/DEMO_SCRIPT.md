# 6-Minute Demo Script

## 0:00–0:40 — Problem
“FinSight AI is an educational financial research assistant focused on Indian equities. It combines market data, technical indicators, fundamentals, news sentiment and an AI-generated research memo.”

## 0:40–1:30 — Market dashboard
Enter `RELIANCE.NS`. Explain that `.NS` denotes NSE, while `.BO` can be used for BSE.

Show:
- last price,
- daily move,
- 52-week range,
- volume,
- market status.

## 1:30–2:20 — Technical analysis
Show candlestick chart, SMA20, SMA50 and RSI14. Explain that the rule-based signal is intentionally simple and transparent.

## 2:20–3:00 — News sentiment
Show positive/neutral/negative headline counts and open one article.

## 3:00–3:40 — Fundamentals
Show P/E, market cap, debt/equity, ROE and growth.

## 3:40–4:20 — Comparison
Compare RELIANCE.NS, TCS.NS, INFY.NS and HDFCBANK.NS.

## 4:20–5:20 — AI research
Click “Generate AI Research Report”. Explain:
- Groq model,
- compact prompt,
- retry/backoff,
- deterministic fallback.

## 5:20–6:00 — Portfolio + PDF
Save a position, show P&L and download the PDF. Finish with the compliance disclaimer.

## Backup demo
If Yahoo or Groq is temporarily unavailable, explain that the application has explicit failure handling. The AI report falls back to a deterministic summary instead of showing an API error.
