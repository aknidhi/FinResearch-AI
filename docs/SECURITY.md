# Security & Compliance Notes

## Secrets
- Never commit `GROQ_API_KEY` or `NEWSAPI_KEY`.
- Use `.streamlit/secrets.toml` locally and Streamlit Cloud Secrets in deployment.
- Rotate keys if they are accidentally exposed.

## Financial compliance posture
The project is deliberately positioned as a **research/education assistant**, not an investment-advice service. It should:
- show data sources where possible,
- disclose data limitations,
- avoid guaranteed returns,
- avoid individualized buy/sell instructions,
- encourage professional advice for actual investment decisions.

## Data
The application does not require user bank credentials, broker credentials, or trading permissions. The portfolio tracker stores only symbols, quantity and buy price in SQLite.

## Production hardening
For a real production deployment, replace local SQLite with a managed database, add authentication, encrypt sensitive data, add structured logging, monitoring, audit trails, and formal legal/compliance review.
