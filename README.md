# FinSight AI — Global Market Research

A clean, portfolio-ready **global financial research assistant** built for the Capabl Financial Research AI Agent internship project. The original brief's Track A requirements are preserved, while the application has been expanded from Indian-only symbols to **global ticker-first research**.

## 🌍 Analyze a company with a ticker only

The main input is intentionally simple:

```text
AAPL
TSLA
MSFT
NVDA
SAP
RELIANCE.NS
TCS.NS
7203.T
0700.HK
VOD.L
```

### How ticker resolution works

1. Enter a ticker in the sidebar.
2. Click **Analyze ticker**.
3. If the ticker is already an exchange-qualified Yahoo Finance symbol, it is preserved.
4. If it is a bare ticker such as `AAPL`, the app first tries the bare symbol and then uses Yahoo Finance search to resolve it.
5. The resolved symbol, company name, exchange, currency and asset type are displayed above the dashboard.

**Important:** Bare tickers can be ambiguous. If the search result is not the intended security, use the Yahoo Finance exchange-qualified symbol. Examples: `RELIANCE.NS` (India), `SAP.DE` (Germany), `VOD.L` (UK), `7203.T` (Japan), `0700.HK` (Hong Kong).

The app is designed around Yahoo Finance-supported instruments, including many equities, ETFs, indices and other quoted assets. Availability varies by instrument and exchange.

## Dashboard

- Professional, typography-focused Streamlit UI
- Global ticker resolution and exchange/currency detection
- Price history and candlestick chart
- SMA 20 / SMA 50
- RSI 14
- Annualized volatility
- Fundamental snapshot
- News aggregation + TextBlob sentiment
- Multi-ticker comparison
- SQLite watchlist and portfolio tracker
- Groq + LangChain research memo
- Rate-limit retries + deterministic fallback
- PDF research export
- Input validation and third-party failure handling

## Global ticker examples

| Market | Example | Yahoo Finance style |
|---|---|---|
| United States | Apple | `AAPL` |
| United States | Tesla | `TSLA` |
| Germany | SAP | `SAP.DE` |
| United Kingdom | Vodafone | `VOD.L` |
| Japan | Toyota | `7203.T` |
| Hong Kong | Tencent | `0700.HK` |
| India / NSE | Reliance Industries | `RELIANCE.NS` |
| India / NSE | TCS | `TCS.NS` |

These are examples, not investment recommendations.

## Free-stack architecture

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Market data | Yahoo Finance / yfinance |
| News | Google News RSS fallback; optional NewsAPI |
| Sentiment | TextBlob |
| Analytics | pandas + NumPy |
| Charts | Plotly |
| Database | SQLite |
| LLM | Groq via LangChain |
| Report | ReportLab |
| Development | Google Colab |
| Hosting | Streamlit Community Cloud |

## Groq rate-limit protection

The app uses one compact AI request per report, bounded retries and exponential backoff. If Groq returns a rate-limit/error response or no API key is configured, the application automatically creates a deterministic report from the same financial data.

Default model:

```text
openai/gpt-oss-20b
```

Never commit the real API key to GitHub.

## Run locally

```bash
git clone <YOUR_REPO_URL>
cd financial-research-ai-agent
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Google Colab

Open:

```text
notebooks/Financial_Research_AI_Agent_Colab.ipynb
```

The notebook installs the free dependencies, tests global ticker resolution, loads market data, calculates technical indicators and exercises the AI fallback path.

## Streamlit Cloud deployment

1. Push the **contents** of this project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository.
3. Branch: `main`.
4. Main file: `app.py`.
5. Python: `3.12`.
6. Add Secrets:

```toml
GROQ_API_KEY = "gsk_your_real_key"
GROQ_MODEL = "openai/gpt-oss-20b"
NEWSAPI_KEY = ""
```

7. Deploy.

## Git commands

```bash
git init
git branch -M main
git add .
git commit -m "feat: global FinSight AI research dashboard"
git remote add origin https://github.com/<USERNAME>/financial-research-ai-agent.git
git push -u origin main
```

## Viva explanation

> FinSight AI is a ticker-first global market research application. The user enters a ticker, the market-data layer resolves it through Yahoo Finance, and the dashboard retrieves price history and fundamentals. pandas calculates technical indicators, the news layer provides headline sentiment, SQLite stores watchlists and portfolio positions, and LangChain connects to Groq for an evidence-based research memo. The design is intentionally resilient: market/news failures are handled gracefully, data is cached, and Groq rate limits trigger bounded retries followed by a deterministic fallback report. The system provides research and education rather than personalized investment advice.

## Compliance and limitations

- This application is for educational research, not personalized investment advice.
- Data may be delayed, missing or temporarily unavailable.
- Third-party data terms and exchange restrictions apply.
- Bare tickers may be ambiguous; exchange-qualified symbols are recommended when needed.
- SQLite is suitable for a portfolio/demo application but is not a production multi-user database.
- Mixed-currency portfolio positions are not automatically converted with FX rates.
