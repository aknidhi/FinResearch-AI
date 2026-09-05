import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analytics.technical import build_analysis, comparison_table
from config import APP_NAME, APP_TAGLINE, DEFAULT_SYMBOLS
from db import add_watchlist, get_watchlist, remove_watchlist, save_portfolio, get_portfolio
from reports import build_pdf_report
from services.llm import generate_ai_report, ai_status
from services.market_data import get_fundamentals, get_market_snapshot, get_price_history, normalize_symbol
from services.news import get_news
from utils import fmt_money, market_status, safe_float

st.set_page_config(page_title=f"{APP_NAME} · {APP_TAGLINE}", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

# -------------------- Professional UI --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {
  --fs-bg:#0b0f14;
  --fs-panel:#151b23;
  --fs-panel-2:#1b2430;
  --fs-gold:#f5b700;
  --fs-gold-soft:#ffd45c;
  --fs-text:#f8fafc;
  --fs-text-dark:#111827;
  --fs-muted:#a9b5c5;
  --fs-border:#2b3543;
  --fs-blue:#8bb8ff;
}
html, body, [class*="css"] {
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}
body { background:var(--fs-bg); color:var(--fs-text); }
.block-container { max-width:1500px; padding:1.5rem 2rem 3rem; }
[data-testid="stSidebar"] { border-right:1px solid var(--fs-border); background:#0e141b; }
[data-testid="stSidebar"] .block-container { padding:1.4rem 1rem; }
.fs-brand { display:flex; align-items:center; gap:.8rem; margin-bottom:1.6rem; }
.fs-logo { width:42px; height:42px; border-radius:12px; background:var(--fs-gold); color:#111827; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:20px; box-shadow:0 5px 18px rgba(245,183,0,.18); }
.fs-brand-title { font-size:1.15rem; font-weight:800; letter-spacing:-.02em; line-height:1.1; color:var(--fs-text); }
.fs-brand-sub { color:var(--fs-muted); font-size:.72rem; margin-top:.15rem; }
.fs-hero { padding:1.55rem 1.75rem; border:1px solid #4b3b11; border-radius:20px; background:linear-gradient(135deg,#241f0f 0%,#161b22 100%); box-shadow:0 10px 32px rgba(0,0,0,.20); margin-bottom:1rem; }
.fs-eyebrow { text-transform:uppercase; letter-spacing:.12em; color:var(--fs-gold); font-size:.72rem; font-weight:800; margin-bottom:.45rem; }
.fs-hero h1 { margin:0; color:var(--fs-text); font-size:2.1rem; line-height:1.15; letter-spacing:-.04em; font-weight:800; }
.fs-hero p { margin:.55rem 0 0; color:#cbd5e1; font-size:.92rem; line-height:1.6; }
.fs-chip { display:inline-flex; align-items:center; gap:.35rem; padding:.34rem .62rem; border:1px solid #4b5563; border-radius:999px; background:#171e27; font-size:.73rem; font-weight:600; color:#e2e8f0; margin:.25rem .25rem 0 0; }
.fs-section { margin:1.35rem 0 .7rem; }
.fs-section h2 { margin:0; font-size:1.08rem; letter-spacing:-.02em; color:var(--fs-text); font-weight:750; }
.fs-section p { margin:.2rem 0 0; color:var(--fs-muted); font-size:.78rem; line-height:1.5; }
.fs-card { border:1px solid var(--fs-border); border-radius:16px; padding:1rem 1.05rem; background:var(--fs-panel); box-shadow:0 3px 15px rgba(0,0,0,.14); }
.fs-label { color:var(--fs-muted); font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; }
.fs-value { color:var(--fs-text); font-size:1.25rem; font-weight:800; margin-top:.25rem; letter-spacing:-.03em; }
.fs-muted { color:var(--fs-muted); font-size:.78rem; }
.fs-disclaimer { border:1px solid #705a15; background:#211c0d; color:#f8d77a; border-radius:12px; padding:.72rem .9rem; font-size:.78rem; margin:1rem 0; }
.fs-help { border:1px solid #294a75; background:#111d2c; color:#bcd7ff; border-radius:12px; padding:.75rem .9rem; font-size:.78rem; }

/* Custom FinSight metric cards: avoid Streamlit theme-dependent metric DOM entirely. */
.fs-metric {
  min-height: 92px;
  box-sizing: border-box;
  border: 1px solid #b88600;
  border-radius: 14px;
  padding: .82rem .95rem;
  background: linear-gradient(145deg, #f8c62f 0%, #f2b800 100%);
  box-shadow: 0 8px 22px rgba(0,0,0,.18);
  margin-bottom: .55rem;
}
.fs-metric-label {
  color: #4b3a00 !important;
  font-size: .70rem !important;
  line-height: 1.2;
  font-weight: 700 !important;
  letter-spacing: .045em;
  text-transform: uppercase;
}
.fs-metric-value {
  color: #151515 !important;
  font-size: 1.22rem !important;
  line-height: 1.25;
  font-weight: 800 !important;
  letter-spacing: -.025em;
  margin-top: .34rem;
  overflow-wrap: anywhere;
}
.fs-metric-delta {
  color: #3b2f00 !important;
  font-size: .72rem !important;
  font-weight: 700 !important;
  margin-top: .20rem;
}

/* Typography: explicit colors prevent theme inheritance from hiding text. */
h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4, [data-testid="stMarkdownContainer"] h5, [data-testid="stMarkdownContainer"] h6 {
  color: #f8fafc !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
.stMarkdown, .stCaption, .stText, label, p, li, [data-testid="stCaptionContainer"] { color: #cbd5e1; }
[data-testid="stMarkdownContainer"] strong, [data-testid="stMarkdownContainer"] b { color: #f8fafc; }
[data-testid="stHeader"] { background:transparent; }
.stButton > button, .stDownloadButton > button {
  border-radius:10px !important;
  font-weight:700 !important;
  border:1px solid #4b5563 !important;
}
.stButton > button[kind="primary"] {
  background:var(--fs-gold) !important;
  color:#111827 !important;
  border-color:#d49d00 !important;
}
.stButton > button:hover { border-color:var(--fs-gold) !important; }
.stTabs [data-baseweb="tab-list"] { gap:1.25rem; border-bottom:1px solid var(--fs-border); }
.stTabs [data-baseweb="tab"] { font-weight:700; font-size:.82rem; padding:.45rem .1rem .7rem; color:#aab6c5 !important; }
.stTabs [aria-selected="true"] { color:var(--fs-gold) !important; }
.stTabs [data-baseweb="tab-highlight"] { background:var(--fs-gold) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--fs-border); border-radius:12px; overflow:hidden; }
.stExpander { border-color:var(--fs-border) !important; background:var(--fs-panel) !important; }
[data-testid="stAlert"] { border-radius:12px; }
.fs-footer { margin-top:2rem; padding-top:1rem; border-top:1px solid var(--fs-border); color:var(--fs-muted); font-size:.72rem; line-height:1.6; }

/* Form controls */
[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div {
  background:#151b23 !important;
  border-color:#3a4655 !important;
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea { color:#f8fafc !important; }
[data-baseweb="select"] * { color:#f8fafc !important; }

/* Plotly area follows the dashboard palette rather than introducing a white panel. */
.js-plotly-plot, .plot-container { border-radius:14px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)


def money(value, currency):
    return fmt_money(value, currency or "USD")


def pct(value):
    x = safe_float(value)
    return "N/A" if x is None else f"{x:+.2f}%"


def make_chart(df: pd.DataFrame, symbol: str, currency: str):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name=symbol))
    for col, name in [("SMA20", "SMA 20"), ("SMA50", "SMA 50")]:
        if col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], name=name, mode="lines", line=dict(width=1.6)))
    fig.update_layout(
        height=500, margin=dict(l=5, r=5, t=25, b=5), template="plotly_dark",
        title=dict(text=f"{symbol} · price & moving averages", font=dict(size=15, color="#f8fafc")),
        xaxis_rangeslider_visible=False, hovermode="x unified",
        yaxis=dict(title=currency, gridcolor="#2b3543"), xaxis=dict(gridcolor="#202a36"),
        legend=dict(orientation="h", y=1.02, x=0),
    )
    return fig


def metric_delta(value):
    x = safe_float(value)
    return "—" if x is None else f"{x:+.2f}%"


def fs_metric(label, value, delta=None):
    """Theme-independent metric card with guaranteed contrast."""
    label_html = str(label).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    value_html = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    delta_html = "" if delta is None else f'<div class="fs-metric-delta">{str(delta)}</div>'
    st.markdown(
        f'<div class="fs-metric"><div class="fs-metric-label">{label_html}</div>'
        f'<div class="fs-metric-value">{value_html}</div>{delta_html}</div>',
        unsafe_allow_html=True,
    )

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="fs-brand"><div class="fs-logo">◈</div><div><div class="fs-brand-title">FinSight AI</div><div class="fs-brand-sub">Global Market Research</div></div></div>', unsafe_allow_html=True)
    st.markdown("### Research input")
    symbol_input = st.text_input(
        "Ticker symbol", value=st.session_state.get("input_symbol", "AAPL"),
        placeholder="e.g. AAPL, TSLA, SAP, RELIANCE.NS",
        help="Enter a ticker only. Exchange suffixes are optional when Yahoo Finance can resolve the symbol. Examples: AAPL, TSLA, SAP, RELIANCE.NS, 7203.T."
    )
    if st.button("Analyze ticker", type="primary", use_container_width=True):
        st.session_state.input_symbol = symbol_input
        st.session_state.active_symbol = None
        st.session_state.pop("last_report", None)
        st.rerun()
    st.caption("Examples")
    st.caption("AAPL · MSFT · NVDA · TSLA · SAP · 7203.T · RELIANCE.NS · TCS.NS")
    period = st.selectbox("History", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    interval = st.selectbox("Interval", ["1d", "1wk"], index=0)
    st.divider()
    st.markdown("### Watchlist")
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = get_watchlist()
    current_for_watch = st.session_state.get("active_symbol") or symbol_input
    try:
        current_for_watch = normalize_symbol(current_for_watch)
    except Exception:
        current_for_watch = symbol_input.upper().strip()
    a, b = st.columns(2)
    with a:
        if st.button("＋ Add", use_container_width=True):
            add_watchlist(current_for_watch); st.session_state.watchlist = get_watchlist(); st.rerun()
    with b:
        if st.button("− Remove", use_container_width=True):
            remove_watchlist(current_for_watch); st.session_state.watchlist = get_watchlist(); st.rerun()
    if st.session_state.watchlist:
        saved = st.selectbox("Saved tickers", st.session_state.watchlist)
        if st.button("Open saved ticker", use_container_width=True):
            st.session_state.input_symbol = saved; st.session_state.active_symbol = saved; st.session_state.pop("last_report", None); st.rerun()
    st.divider()
    st.markdown("### Global ticker guide")
    st.caption("US: AAPL · UK: VOD.L · Japan: 7203.T · Germany: SAP.DE · India: RELIANCE.NS · Hong Kong: 0700.HK")
    st.caption("For an exchange-listed security, add Yahoo Finance's suffix when needed. Bare tickers are automatically searched first.")

# -------------------- Header --------------------
st.markdown(f"""
<div class="fs-hero">
  <div class="fs-eyebrow">AI-powered financial research</div>
  <h1>{APP_NAME}</h1>
  <p>{APP_TAGLINE} · analyze equities, funds and other Yahoo Finance-supported instruments from a simple ticker input.</p>
  <div style="margin-top:.7rem">
    <span class="fs-chip">Live / historical market data</span><span class="fs-chip">Technicals</span><span class="fs-chip">Fundamentals</span><span class="fs-chip">News sentiment</span><span class="fs-chip">Groq AI</span><span class="fs-chip">PDF export</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fs-help"><b>How to use:</b> type a ticker such as <b>AAPL</b>, <b>TSLA</b>, <b>SAP</b>, or <b>RELIANCE.NS</b> and click <b>Analyze ticker</b>. If a bare ticker is ambiguous, use the exchange-qualified Yahoo Finance symbol shown in the ticker guide.</div>', unsafe_allow_html=True)

# -------------------- Resolve & load --------------------
requested = st.session_state.get("active_symbol") or symbol_input
try:
    symbol = normalize_symbol(requested)
except Exception as exc:
    st.error(str(exc)); st.stop()

try:
    history = get_price_history(symbol, period=period, interval=interval)
    if history.empty:
        st.error(f"No price history was returned for **{symbol}**. Check the ticker or add the correct Yahoo Finance exchange suffix.")
        st.stop()
except Exception as exc:
    st.error(f"Market data error: {exc}"); st.stop()

analysis = build_analysis(history)
snapshot = get_market_snapshot(symbol, history)
fundamentals = get_fundamentals(symbol)
currency = fundamentals.get("currency") or "USD"
name = fundamentals.get("display_name") or symbol
exchange = fundamentals.get("exchange") or fundamentals.get("fullExchangeName") or "Market"
status = market_status(str(fundamentals.get("exchange") or exchange))

# -------------------- Context strip --------------------
st.markdown(f"<div class='fs-section'><h2>{name}</h2><p>{symbol} · {exchange} · {currency} · local market time {status['local_time'].strftime('%d %b %Y, %I:%M %p')}</p></div>", unsafe_allow_html=True)
q1, q2, q3, q4 = st.columns(4)
fs_metric("Market status", status["label"])
fs_metric("Data source", "Yahoo Finance")
fs_metric("AI engine", ai_status())
fs_metric("Asset type", str(fundamentals.get("quoteType") or "Security").title())

st.markdown('<div class="fs-disclaimer">⚠ <b>Research only:</b> FinSight AI provides educational market analysis, not personalized investment advice. Data may be delayed, incomplete or affected by third-party outages. Verify information before making financial decisions.</div>', unsafe_allow_html=True)

# -------------------- Overview cards --------------------
st.markdown('<div class="fs-section"><h2>Market snapshot</h2><p>Current price and key range/volume indicators.</p></div>', unsafe_allow_html=True)
m1,m2,m3,m4,m5 = st.columns(5)
fs_metric("Last price", money(snapshot.get("price"), currency))
fs_metric("1D change", metric_delta(snapshot.get("change_pct")))
fs_metric("52W high", money(fundamentals.get("fiftyTwoWeekHigh"), currency))
fs_metric("52W low", money(fundamentals.get("fiftyTwoWeekLow"), currency))
fs_metric("Volume", f"{safe_float(snapshot.get('volume'),0):,.0f}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview & Technicals", "News & Sentiment", "Fundamentals", "Compare", "AI Research"])

# -------------------- Technical --------------------
with tab1:
    left,right=st.columns([3.2,1])
    with left:
        st.plotly_chart(make_chart(analysis, symbol, currency), use_container_width=True, config={"displaylogo":False})
    with right:
        signal=analysis.attrs.get("signal",{})
        st.markdown("#### Technical signal")
        fs_metric("Composite view", signal.get("label","Neutral"))
        fs_metric("RSI (14)", f"{analysis['RSI14'].iloc[-1]:.1f}" if "RSI14" in analysis else "—")
        fs_metric("SMA 20", money(analysis["SMA20"].iloc[-1], currency))
        fs_metric("SMA 50", money(analysis["SMA50"].iloc[-1], currency))
        fs_metric("Annualized volatility", f"{analysis.attrs.get('annualized_volatility',0):.1f}%")
    with st.expander("View calculation data"):
        st.dataframe(analysis[["Close","SMA20","SMA50","RSI14","DailyReturn"]].tail(25), use_container_width=True)
        st.caption("RSI uses a 14-period relative-strength calculation. Annualized volatility is based on daily returns × √252.")

# -------------------- News --------------------
with tab2:
    news_items=get_news(symbol)
    if news_items:
        news_df=pd.DataFrame(news_items)
        pos=int((news_df["sentiment"]>0.05).sum()); neg=int((news_df["sentiment"]<-0.05).sum()); neu=len(news_df)-pos-neg
        n1,n2,n3=st.columns(3); fs_metric("Positive",pos); fs_metric("Neutral",neu); fs_metric("Negative",neg)
        st.markdown("#### Latest headlines")
        for item in news_items:
            with st.container(border=True):
                st.markdown(f"**{item['title']}**")
                st.caption(f"{item['source']} · {item['published']}")
                st.write(f"Sentiment: **{item['label']}** ({item['sentiment']:+.2f})")
                if item.get("url"): st.link_button("Open article",item["url"])
    else:
        st.info("No recent headlines found. The app will continue to work without news. Add NEWSAPI_KEY for the optional NewsAPI source.")

# -------------------- Fundamentals --------------------
with tab3:
    st.markdown("#### Company profile")
    a,b,c=st.columns(3)
    fs_metric("Company", name); fs_metric("Sector", fundamentals.get("sector") or "N/A"); fs_metric("Industry", fundamentals.get("industry") or "N/A")
    st.markdown("#### Valuation & financial quality")
    f1,f2,f3,f4,f5=st.columns(5)
    fs_metric("P/E", fundamentals.get("trailingPE") if fundamentals.get("trailingPE") is not None else "N/A")
    fs_metric("Forward P/E", fundamentals.get("forwardPE") if fundamentals.get("forwardPE") is not None else "N/A")
    fs_metric("Price / Book", fundamentals.get("priceToBook") if fundamentals.get("priceToBook") is not None else "N/A")
    fs_metric("Debt / Equity", fundamentals.get("debtToEquity") if fundamentals.get("debtToEquity") is not None else "N/A")
    fs_metric("Beta", fundamentals.get("beta") if fundamentals.get("beta") is not None else "N/A")
    g1,g2,g3,g4=st.columns(4)
    fs_metric("Market cap", money(fundamentals.get("marketCap"), currency))
    fs_metric("ROE", f"{safe_float(fundamentals.get('returnOnEquity'),0)*100:.2f}%" if fundamentals.get('returnOnEquity') is not None else "N/A")
    fs_metric("Revenue growth", f"{safe_float(fundamentals.get('revenueGrowth'),0)*100:.2f}%" if fundamentals.get('revenueGrowth') is not None else "N/A")
    fs_metric("Profit margin", f"{safe_float(fundamentals.get('profitMargins'),0)*100:.2f}%" if fundamentals.get('profitMargins') is not None else "N/A")
    st.caption(f"Currency: {currency} · Country: {fundamentals.get('country') or 'N/A'} · Quote type: {fundamentals.get('quoteType') or 'N/A'}")

# -------------------- Comparison --------------------
with tab4:
    st.markdown("#### Compare multiple global tickers")
    compare_input=st.text_input("Tickers (comma-separated)", value=",".join(DEFAULT_SYMBOLS), help="Examples: AAPL,MSFT,NVDA or RELIANCE.NS,TCS.NS,INFY.NS")
    compare_symbols=[x.strip() for x in compare_input.split(",") if x.strip()]
    if st.button("Run comparison",type="primary"):
        with st.spinner("Resolving tickers and loading comparison data…"):
            table=comparison_table(compare_symbols,period="6mo")
        if table.empty: st.warning("No comparison data available for the supplied tickers.")
        else:
            st.dataframe(table,use_container_width=True)
            if "Return %" in table.columns: st.bar_chart(table.set_index("Symbol")["Return %"])

# -------------------- AI Research --------------------
with tab5:
    st.markdown("#### Evidence-based research memo")
    st.caption("One compact Groq request is used when available. Rate-limit failures use bounded retries and automatically fall back to a deterministic report.")
    if st.button("Generate AI research report",type="primary",use_container_width=True):
        news_items=get_news(symbol)
        with st.spinner("Preparing research memo…"):
            report=generate_ai_report(symbol,snapshot,fundamentals,{
                "rsi14":safe_float(analysis["RSI14"].iloc[-1]),
                "sma20":safe_float(analysis["SMA20"].iloc[-1]),
                "sma50":safe_float(analysis["SMA50"].iloc[-1]),
                "volatility":safe_float(analysis.attrs.get("annualized_volatility")),
                "signal":analysis.attrs.get("signal",{}),
            },news_items[:8])
        st.session_state["last_report"]=report
    if st.session_state.get("last_report"):
        st.markdown(st.session_state["last_report"])
        pdf=build_pdf_report(symbol=symbol,snapshot=snapshot,fundamentals=fundamentals,technicals=analysis.attrs,report_text=st.session_state["last_report"])
        st.download_button("Download PDF research report",data=pdf,file_name=f"{symbol.replace('.','_')}_research_report.pdf",mime="application/pdf")

# -------------------- Portfolio --------------------
st.markdown('<div class="fs-section"><h2>Portfolio tracker</h2><p>Store positions locally with SQLite and compare cost against current market value.</p></div>', unsafe_allow_html=True)
portfolio=get_portfolio()
pc1,pc2,pc3,pc4=st.columns(4)
with pc1: p_symbol=st.text_input("Portfolio ticker",value=symbol,key="p_symbol")
with pc2: p_qty=st.number_input("Quantity",min_value=0.0,value=10.0,step=1.0)
with pc3: p_buy=st.number_input(f"Buy price ({currency})",min_value=0.0,value=float(snapshot["price"] or 0),step=1.0)
with pc4:
    if st.button("Save position",use_container_width=True):
        save_portfolio(normalize_symbol(p_symbol),p_qty,p_buy); st.rerun()
portfolio=get_portfolio()
if portfolio:
    rows=[]
    for row in portfolio:
        try:
            h=get_price_history(row["symbol"],period="5d",interval="1d")
            current=float(h["Close"].iloc[-1]); invested=row["quantity"]*row["buy_price"]; value=row["quantity"]*current
            f=get_fundamentals(row["symbol"]); cur=f.get("currency") or currency
            rows.append({"Symbol":row["symbol"],"Qty":row["quantity"],"Buy Price":row["buy_price"],"Current":current,"Currency":cur,"Invested":invested,"Value":value,"P&L":value-invested,"P&L %":((value/invested)-1)*100 if invested else 0})
        except Exception: continue
    if rows:
        pdf_portfolio=pd.DataFrame(rows); st.dataframe(pdf_portfolio,use_container_width=True)
        st.caption("Portfolio totals are meaningful when positions share the same currency; mixed-currency portfolios are shown at position level without FX conversion.")
        same=[r for r in rows if r["Currency"]==currency]
        if same:
            total_invested=sum(r["Invested"] for r in same); total_value=sum(r["Value"] for r in same)
            a,b=st.columns(2); fs_metric(f"Portfolio value · {currency}",money(total_value,currency)); fs_metric("Unrealized P&L",money(total_value-total_invested,currency),f"{((total_value/total_invested)-1)*100:+.2f}%" if total_invested else "—")
    else: st.info("Saved positions exist, but current market prices could not be loaded.")

st.markdown('<div class="fs-footer">FinSight AI is an educational research application. Market data and news are provided by third-party services. It is not a broker, investment adviser or trading platform.</div>',unsafe_allow_html=True)
