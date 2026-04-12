# routes/dashboard.py (or inside chat.py)

from fastapi import APIRouter
from services.expense_service import get_all_expenses
from datetime import datetime

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    expenses = get_all_expenses()

    total = 0
    breakdown = {}
    history = {}
    recent = []

    for e in expenses:
        amt = e.get("amount", 0)
        cat = e.get("category", "misc")
        date = e.get("date", datetime.now().strftime("%Y-%m-%d"))

        total += amt

        # category breakdown
        breakdown[cat] = breakdown.get(cat, 0) + amt

        # daily trend
        history[date] = history.get(date, 0) + amt

        # recent transactions
        recent.append(e)

    # sort recent (latest first)
    recent = sorted(recent, key=lambda x: x["date"], reverse=True)[:5]

    return {
        "total": total,
        "breakdown": breakdown,
        "history": history,
        "recent": recent
    }