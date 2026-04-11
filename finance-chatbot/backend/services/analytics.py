# backend/services/analytics.py

from datetime import datetime
from services.expense_service import get_all_expenses, save_expense

def get_total_spent():
    expenses = get_all_expenses()
    return sum(e["amount"] for e in expenses if "amount" in e)

def get_category_breakdown():
    expenses = get_all_expenses()
    result = {}
    for e in expenses:
        cat = e.get("category", "misc")
        amt = e.get("amount", 0)
        result[cat] = result.get(cat, 0) + amt
    return result

def get_monthly_summary():
    expenses = get_all_expenses()
    month = datetime.now().month
    year = datetime.now().year
    total = 0
    breakdown = {}
    for e in expenses:
        e_date_str = e.get("date", datetime.now().strftime("%Y-%m-%d"))
        e_date = datetime.strptime(e_date_str, "%Y-%m-%d")
        if e_date.year == year and e_date.month == month:
            amt = e.get("amount", 0)
            cat = e.get("category", "misc")
            total += amt
            breakdown[cat] = breakdown.get(cat, 0) + amt
    return {"total": total, "breakdown": breakdown}

def add_expense(data):
    expense = {
        "amount": data.get("amount", 0),
        "category": data.get("category", "misc"),
        "date": data.get("date", datetime.now().strftime("%Y-%m-%d"))
    }
    save_expense(expense)