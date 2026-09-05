# Architecture & Data Flow

## 1. Request flow

```text
User
  │
  ▼
Streamlit UI
  │
  ├── symbol validation / normalization
  │
  ├── cached market-data service ──► Yahoo Finance
  │
  ├── cached news service ─────────► NewsAPI (optional)
  │                                  └► Google News RSS fallback
  │
  ├── technical analytics
  │     ├── SMA20
  │     ├── SMA50
  │     ├── RSI14
  │     └── annualized volatility
  │
  ├── SQLite
  │     ├── watchlist
  │     └── portfolio
  │
  └── AI report service
        ├── Groq gpt-oss-20b
        ├── 429 retry/backoff
        └── deterministic fallback
                 │
                 ▼
             PDF export
```

## 2. Reliability strategy

The free stack is intentionally designed to fail gracefully:

- `st.cache_data` reduces repeated Yahoo/news requests.
- LLM prompts are compact.
- Groq failures do not break the dashboard.
- 429 responses are retried only three times.
- Non-rate-limit LLM errors immediately use fallback.
- Empty market data produces a user-readable error.
- News can operate without a NewsAPI key.
- The UI shows the current market state and educational disclaimer.

## 3. Security

Secrets are never hardcoded. Local secrets are ignored by Git and cloud secrets are supplied through Streamlit's secrets interface.

See `docs/SECURITY.md`.
