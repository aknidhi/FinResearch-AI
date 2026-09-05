from datetime import datetime, time
from zoneinfo import ZoneInfo
import math

CURRENCY_SYMBOLS = {
    "USD": "$", "INR": "₹", "EUR": "€", "GBP": "£", "JPY": "¥",
    "CNY": "¥", "HKD": "HK$", "SGD": "S$", "AUD": "A$", "CAD": "C$",
    "CHF": "CHF ", "KRW": "₩", "BRL": "R$", "MXN": "MX$", "ZAR": "R",
}

EXCHANGE_TIMEZONES = {
    "NMS": "America/New_York", "NYQ": "America/New_York", "NGM": "America/New_York",
    "NCM": "America/New_York", "BTS": "Europe/Bratislava", "LSE": "Europe/London",
    "GER": "Europe/Berlin", "FRA": "Europe/Berlin", "PAR": "Europe/Paris",
    "HKG": "Asia/Hong_Kong", "JKT": "Asia/Jakarta", "TSE": "Asia/Tokyo",
    "JPX": "Asia/Tokyo", "NSI": "Asia/Kolkata", "BSE": "Asia/Kolkata",
    "NSE": "Asia/Kolkata", "SHG": "Asia/Shanghai", "SHE": "Asia/Shanghai",
    "ASX": "Australia/Sydney", "SGX": "Asia/Singapore", "KSC": "Asia/Seoul",
    "KRX": "Asia/Seoul", "SAO": "America/Sao_Paulo", "TOR": "America/Toronto",
}

def safe_float(value, default=None):
    try:
        if value is None:
            return default
        x = float(value)
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except (TypeError, ValueError):
        return default

def fmt_money(value, currency="USD"):
    x = safe_float(value)
    if x is None:
        return "N/A"
    prefix = CURRENCY_SYMBOLS.get((currency or "USD").upper(), f"{currency or 'USD'} ")
    ax = abs(x)
    if ax >= 1e12: return f"{prefix}{x/1e12:.2f}T"
    if ax >= 1e9: return f"{prefix}{x/1e9:.2f}B"
    if ax >= 1e6: return f"{prefix}{x/1e6:.2f}M"
    if ax >= 1e3: return f"{prefix}{x/1e3:.2f}K"
    return f"{prefix}{x:,.2f}"

def fmt_inr(value):
    return fmt_money(value, "INR")

def exchange_timezone(exchange=""):
    return EXCHANGE_TIMEZONES.get(str(exchange).upper(), "America/New_York")

def market_status(exchange="", timezone=None):
    tz_name = timezone or exchange_timezone(exchange)
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz_name, tz = "America/New_York", ZoneInfo("America/New_York")
    now = datetime.now(tz)
    if now.weekday() >= 5:
        return {"open": False, "label": "Closed · weekend", "timezone": tz_name, "local_time": now}
    # Generic core session; exact hours vary by exchange. This is deliberately presented as indicative.
    market_open, market_close = time(9, 30), time(16, 0)
    if "NS" in exchange.upper() or exchange.upper() in {"NSE", "NSI", "BSE"}:
        market_open, market_close = time(9, 15), time(15, 30)
    if now.time() < market_open:
        label = "Pre-market"
        is_open = False
    elif now.time() <= market_close:
        label = "Open"
        is_open = True
    else:
        label = "Closed · after hours"
        is_open = False
    return {"open": is_open, "label": label, "timezone": tz_name, "local_time": now}

def indian_market_status(now=None):
    # Backward-compatible helper for the internship brief.
    tz = ZoneInfo("Asia/Kolkata")
    now = now.astimezone(tz) if now else datetime.now(tz)
    return market_status("NSE", "Asia/Kolkata") | {"local_time": now}

def clean_symbol(symbol):
    return str(symbol).strip().upper().replace(" ", "")
