import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from config import GROQ_MODEL, get_secret
from utils import safe_float

def ai_status():
    return "Groq AI" if get_secret("GROQ_API_KEY") else "Rule-based fallback"

def _fallback_report(symbol, snapshot, fundamentals, technicals, news):
    currency=fundamentals.get("currency", "USD")
    price=safe_float(snapshot.get("price"),0); change=safe_float(snapshot.get("change_pct"),0)
    rsi=safe_float(technicals.get("rsi14"),50); vol=safe_float(technicals.get("volatility"),0)
    signal=technicals.get("signal",{}).get("label","Neutral")
    positives=sum(1 for x in news if x.get("sentiment",0)>0.05); negatives=sum(1 for x in news if x.get("sentiment",0)<-0.05); neutral=max(0,len(news)-positives-negatives)
    return f"""## {fundamentals.get('display_name',symbol)} ({symbol}) — Research Snapshot

**Market view:** {signal} based on a transparent rule-based technical score. Last price: {currency} {price:,.2f}; 1-day move: {change:+.2f}% when available.

### Technicals
- RSI (14): {rsi:.1f} — {"overbought" if rsi>=70 else "oversold" if rsi<=30 else "normal zone"}.
- Annualized historical volatility: {vol:.1f}%.
- SMA 20: {safe_float(technicals.get('sma20'),0):,.2f}; SMA 50: {safe_float(technicals.get('sma50'),0):,.2f}.

### Fundamentals
- P/E: {fundamentals.get('trailingPE') or 'N/A'}
- Debt/Equity: {fundamentals.get('debtToEquity') or 'N/A'}
- Revenue growth: {safe_float(fundamentals.get('revenueGrowth'),0)*100:.2f}% when reported.

### News sentiment
The current headline sample contains **{positives} positive**, **{negatives} negative**, and **{neutral} neutral** headlines.

### Risk notes
Consider volatility, valuation, liquidity, macro conditions, currency effects and third-party data availability. This is analytical research, not a recommendation to buy, sell or hold.

> **Fallback mode:** The Groq service was unavailable or rate-limited, so this memo was generated deterministically from the same dashboard data.
"""

def generate_ai_report(symbol, snapshot, fundamentals, technicals, news):
    key=get_secret("GROQ_API_KEY")
    if not key: return _fallback_report(symbol,snapshot,fundamentals,technicals,news)
    news_text="\n".join(f"- {x.get('title','')} ({x.get('label','Neutral')})" for x in news[:8])
    prompt=f"""You are a conservative global financial research assistant for an educational application. Do NOT give personalized investment advice, price targets, or trading instructions. Use ONLY supplied data. Produce a concise research memo with: executive summary, technical interpretation, fundamental snapshot, news sentiment, risk flags, and what to monitor next. State uncertainty.\n\nSYMBOL: {symbol}\nSNAPSHOT: {snapshot}\nFUNDAMENTALS: {fundamentals}\nTECHNICALS: {technicals}\nNEWS:\n{news_text}"""
    for attempt in range(3):
        try:
            llm=ChatGroq(model=GROQ_MODEL, groq_api_key=key, temperature=0.2, max_tokens=900)
            response=llm.invoke([SystemMessage(content="You are precise, conservative, global and compliance-aware."), HumanMessage(content=prompt)])
            text=response.content if isinstance(response.content,str) else str(response.content)
            return text if text.strip() else _fallback_report(symbol,snapshot,fundamentals,technicals,news)
        except Exception as exc:
            msg=str(exc).lower()
            if any(x in msg for x in ("429","rate","too many","rate_limit")):
                time.sleep(2**attempt)
            else: break
    return _fallback_report(symbol,snapshot,fundamentals,technicals,news)+"\n\n*Groq note: the AI request was unavailable after safe retries; fallback mode was used.*"
