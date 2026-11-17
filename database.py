
import sqlite3
from datetime import datetime

DATABASE = "transactions.db"

def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date TEXT,
            amount REAL,
            prediction INTEGER,
            result TEXT,
            fraud_probability REAL
        )
    """)

    conn.commit()
    conn.close()

def save_transaction(amount, prediction, result, probability):

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO transactions
        (transaction_date, amount, prediction, result,
         fraud_probability)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        amount,
        prediction,
        result,
        probability
    ))

    conn.commit()
    conn.close()

def get_transactions():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT * FROM transactions
        ORDER BY id DESC
    """).fetchall()

    transactions = [dict(row) for row in rows]

    conn.close()

    return transactions

def get_stats():

    conn = sqlite3.connect(DATABASE)

    total = conn.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    fraud = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE prediction = 1"
    ).fetchone()[0]

    legitimate = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE prediction = 0"
    ).fetchone()[0]

    conn.close()

    return {
        "total": total,
        "fraud": fraud,
        "legitimate": legitimate
    }