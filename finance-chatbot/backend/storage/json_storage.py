import json
from datetime import datetime

DB_FILE = "expenses.json"

def add_expense(amount, category, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }

    # Load existing data
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # Append new expense
    data.append(expense)

    # Save back
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_all_expenses():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_monthly_summary():
    data = get_all_expenses()
    summary = {}
    for e in data:
        category = e.get("category", "other")
        amount = e.get("amount", 0) or 0
        summary[category] = summary.get(category, 0) + amount
    return summary