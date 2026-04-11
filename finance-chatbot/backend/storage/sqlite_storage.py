import sqlite3
from datetime import datetime

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

def add_expense(amount, category, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date)
    )
    conn.commit()

def get_all_expenses():
    cursor.execute("SELECT amount, category, date FROM expenses")
    return cursor.fetchall()

def get_monthly_summary():
    data = get_all_expenses()
    summary = {}
    for amount, category, date in data:
        summary[category] = summary.get(category, 0) + (amount or 0)
    return summary