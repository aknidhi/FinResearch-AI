# FinSight AI — Internship Completion Report

## Executive summary

This project implements the **Track A foundation expanded into a Global Market Research Assistant** from the supplied internship brief. The application combines global market data, technical indicators, fundamentals, news sentiment, an LLM research layer, a SQLite database and a professional Streamlit interface.

The original brief defines Track A around a Streamlit UI, Python/pandas/yfinance, SQLite, financial APIs, technical analysis, sentiment analysis and Streamlit deployment. This implementation follows that structure while replacing the brief's example LLM with Groq because the project requirement is to use a free Groq-based setup.

## Functional modules

| Module | Implementation |
|---|---|
| Market data | Yahoo Finance / yfinance |
| Global symbols | ticker-first resolution with Yahoo Finance exchange suffix support |
| Technical analysis | SMA20, SMA50, RSI14, volatility |
| News | NewsAPI optional + Google News RSS fallback |
| Sentiment | TextBlob |
| Fundamentals | P/E, debt/equity, growth, ROE, market cap |
| Comparison | Multi-symbol performance/risk table |
| Storage | SQLite |
| AI | LangChain + Groq |
| Rate-limit resilience | 3 retries + exponential backoff + fallback |
| UI | Streamlit + Plotly |
| Reports | ReportLab PDF |
| Deployment | Streamlit Community Cloud |
| Testing | pytest + GitHub Actions |
| Cloud development | Google Colab notebook |

## Assessment alignment

### Financial functionality — 40 points
Implemented:
- two core financial tools: market data and news/sentiment,
- technical calculations,
- fundamentals,
- comparison,
- SQLite watchlist/portfolio.

### Data accuracy — 20 points
Implemented:
- deterministic financial calculations,
- exchange suffix handling,
- exchange-aware local market context,
- historical data fallback,
- no fabricated values when market data is unavailable.

### UI/UX — 15 points
Implemented:
- dashboard metric cards,
- interactive candlestick chart,
- technical signal panel,
- sentiment dashboard,
- comparison chart,
- portfolio table,
- PDF export,
- clear error messages and disclaimer.

### Deployment — 15 points
Implemented:
- `requirements.txt`,
- Streamlit entrypoint,
- secrets example,
- deployment instructions,
- cloud-safe configuration.

### Documentation — 10 points
Included:
- README,
- architecture documentation,
- security/compliance notes,
- demo script,
- viva Q&A,
- Colab notebook,
- test suite.

## Deliberate production-minded decisions

### 1. LLM is not the calculator
Financial metrics are calculated in Python. The LLM receives the resulting values and produces a readable research memo. This makes the core calculations testable.

### 2. Rate limits do not crash the application
The Groq layer retries 429/rate-limit failures with bounded exponential backoff and then generates a deterministic fallback memo.

### 3. Data-source failure is expected
Yahoo Finance and news providers can be temporarily unavailable. The UI handles empty results rather than inventing values.

### 4. Compliance is explicit
The app presents research and education only, does not promise returns, and does not present itself as a regulated investment-advice service.

## Future roadmap

For a true Track B production system:
- PostgreSQL/Supabase for durable storage,
- Redis for shared caching,
- FastAPI + LangGraph,
- authentication and role-based access,
- richer transformer-based financial NLP,
- backtesting,
- portfolio optimization,
- real-time alerts,
- audit logs,
- monitoring and formal compliance review.
