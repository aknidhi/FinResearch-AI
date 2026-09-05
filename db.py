import sqlite3
from pathlib import Path
from config import DB_PATH

def _connect():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn=sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS watchlist (
        symbol TEXT PRIMARY KEY,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS portfolio (
        symbol TEXT PRIMARY KEY,
        quantity REAL NOT NULL,
        buy_price REAL NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn

def add_watchlist(symbol):
    conn=_connect()
    conn.execute("INSERT OR IGNORE INTO watchlist(symbol) VALUES (?)",(symbol,))
    conn.commit(); conn.close()

def remove_watchlist(symbol):
    conn=_connect()
    conn.execute("DELETE FROM watchlist WHERE symbol=?",(symbol,))
    conn.commit(); conn.close()

def get_watchlist():
    conn=_connect()
    rows=conn.execute("SELECT symbol FROM watchlist ORDER BY symbol").fetchall()
    conn.close()
    return [r[0] for r in rows]

def save_portfolio(symbol, quantity, buy_price):
    conn=_connect()
    conn.execute("""INSERT INTO portfolio(symbol,quantity,buy_price)
                    VALUES (?,?,?)
                    ON CONFLICT(symbol) DO UPDATE SET
                    quantity=excluded.quantity,
                    buy_price=excluded.buy_price,
                    updated_at=CURRENT_TIMESTAMP""",(symbol,quantity,buy_price))
    conn.commit(); conn.close()

def get_portfolio():
    conn=_connect()
    rows=conn.execute("SELECT symbol,quantity,buy_price FROM portfolio ORDER BY symbol").fetchall()
    conn.close()
    return [{"symbol":r[0],"quantity":r[1],"buy_price":r[2]} for r in rows]
