import json
from datetime import datetime

BUDGET_FILE = "budgets.json"
EXPENSE_FILE = "expenses.json"


# ---------- helpers ----------
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def get_month():
    return datetime.now().strftime("%Y-%m")


# ---------- set budget ----------
def set_budget(category: str, limit_amount: float):
    budgets = load_json(BUDGET_FILE)
    month = get_month()

    # check existing
    for b in budgets:
        if b["category"] == category and b["month"] == month:
            b["limit"] = limit_amount
            save_json(BUDGET_FILE, budgets)
            return f"Updated budget for {category}"

    budgets.append({
        "category": category,
        "month": month,
        "limit": limit_amount,
        "spent": 0
    })

    save_json(BUDGET_FILE, budgets)
    return f"Budget set for {category}: {limit_amount}"


# ---------- update spent ----------
def update_budget_spent(category: str, amount: float):
    budgets = load_json(BUDGET_FILE)
    month = get_month()

    for b in budgets:
        if b["category"] == category and b["month"] == month:
            b["spent"] += amount
            save_json(BUDGET_FILE, budgets)
            return


# ---------- status ----------
def get_budget_status(category: str):
    budgets = load_json(BUDGET_FILE)
    month = get_month()

    for b in budgets:
        if b["category"] == category and b["month"] == month:
            percent = (b["spent"] / b["limit"]) * 100 if b["limit"] else 0

            return {
                "category": category,
                "limit": b["limit"],
                "spent": b["spent"],
                "remaining": b["limit"] - b["spent"],
                "percent": round(percent, 2)
            }

    return None