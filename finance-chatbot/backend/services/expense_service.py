# backend/services/expense_service.py

import json
import uuid
from datetime import datetime
from services.budget_service import update_budget_spent

DB_FILE = "expenses.json"
LAST_ACTION_FILE = "last_action.json"


# Load all expenses
def get_all_expenses():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Save a new expense
def save_expense(expense):
    expenses = get_all_expenses()

    # ✅ ADD UNIQUE ID
    expense["id"] = str(uuid.uuid4())

    # Optional timestamp (nice upgrade)
    expense["created_at"] = datetime.now().isoformat()

    expenses.append(expense)

    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    save_last_action({
        "type": "add",
        "data": expense
    })

    update_budget_spent(expense["category"], expense["amount"])

    return expense


# ✅ NEW: Delete by ID (for frontend)
def delete_expense_by_id(expense_id):
    expenses = get_all_expenses()

    new_expenses = [e for e in expenses if e.get("id") != expense_id]

    with open(DB_FILE, "w") as f:
        json.dump(new_expenses, f, indent=4)

    return True


# ✅ NEW: Update by ID (for frontend)
def update_expense_by_id(expense_id, new_data):
    expenses = get_all_expenses()

    for e in expenses:
        if e.get("id") == expense_id:
            e["amount"] = new_data.get("amount", e["amount"])
            e["category"] = new_data.get("category", e["category"])

    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    return True


# Delete last expense (existing)
def delete_last_expense():
    expenses = get_all_expenses()
    if not expenses:
        return None

    last = expenses.pop()

    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    save_last_action({
        "type": "delete",
        "data": last
    })

    return last


# Update an expense (existing chatbot logic)
def update_expense(old_amount, old_category, new_amount, new_category):
    expenses = get_all_expenses()
    for e in expenses:
        if e["amount"] == old_amount and e["category"] == old_category:
            e["amount"] = new_amount
            e["category"] = new_category
            with open(DB_FILE, "w") as f:
                json.dump(expenses, f, indent=4)
            return e
    return None


def deduct_expense(amount, category):
    expenses = get_all_expenses()

    for e in expenses:
        if e["category"] == category and e["amount"] >= amount:
            e["amount"] -= amount

            if e["amount"] == 0:
                expenses.remove(e)

            with open(DB_FILE, "w") as f:
                json.dump(expenses, f, indent=4)

            return e

    return None


def save_last_action(action):
    with open(LAST_ACTION_FILE, "w") as f:
        json.dump(action, f)


def get_last_action():
    try:
        with open(LAST_ACTION_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def undo_last_action():
    action = get_last_action()
    if not action:
        return None

    expenses = get_all_expenses()

    if action["type"] == "add":
        if expenses:
            expenses.pop()

    elif action["type"] == "delete":
        expenses.append(action["data"])

    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    return action


def fix_last_category(new_category):
    expenses = get_all_expenses()
    if not expenses:
        return None

    last = expenses[-1]
    old_category = last["category"]

    last["category"] = new_category

    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    return old_category, new_category


def clear_all_expenses():
    with open(DB_FILE, "w") as f:
        json.dump([], f)