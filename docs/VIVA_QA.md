# Viva Questions & Answers

### Why did you choose Track A?
It delivers the core financial-analysis learning outcomes with a free and deployable stack. The project can be expanded later without changing the main UI architecture.

### Why yfinance?
It provides accessible market history and company metadata without requiring a paid brokerage connection.

### Why `.NS` and `.BO`?
Yahoo Finance uses these exchange suffixes for many Indian listings.

### Why RSI?
RSI provides a standard momentum measure that is easy to explain and verify.

### How do you handle Groq rate limits?
The app makes a compact request, retries 429/rate-limit errors with exponential backoff, then switches to a deterministic fallback report.

### Why not rely entirely on an LLM?
Financial calculations should remain deterministic and inspectable. The LLM is used for summarization and interpretation, not for calculating market metrics.

### What happens on weekends/holidays?
The market-status widget reports closure. Historical data remains available. If no current price is returned, the UI shows a clear message rather than inventing data.

### Why SQLite?
It satisfies the internship database requirement with zero infrastructure cost. A managed PostgreSQL/Supabase database would be preferable for a persistent production system.

### Is this investment advice?
No. It is an educational research tool. It explicitly avoids personalized investment recommendations.

### What would you improve next?
Add authentication, durable cloud database, stronger financial NLP, backtesting, alerts, broker integrations, audit logging and formal compliance review.
