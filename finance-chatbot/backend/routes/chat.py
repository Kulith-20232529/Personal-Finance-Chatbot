from fastapi import APIRouter, Request
from services.analytics import (
    add_expense,
    get_total_spent,
    get_monthly_summary,
    get_category_breakdown
)
from services.expense_service import (
    deduct_expense,
    delete_last_expense,
    update_expense,
    undo_last_action,
    fix_last_category,
    clear_all_expenses   # ✅ NEW
)
from services.budget_service import set_budget, get_budget_status

router = APIRouter()


def parse_expense_message(message: str):
    words = message.lower().split()
    data = {"amount": 0, "category": "misc"}

    if "spent" in words:
        try:
            idx = words.index("spent") + 1
            data["amount"] = float(words[idx])
        except:
            pass

    if "on" in words:
        idx = words.index("on") + 1
        if idx < len(words):
            data["category"] = words[idx]

    return data


# 🔥 Helper to always send chart data
def build_response(text: str):
    breakdown = get_category_breakdown()
    return {
        "response": text,
        "data": breakdown
    }


@router.post("/chat")
async def chat(request: Request):
    req = await request.json()
    message = req.get("message", "").lower()

    # 🧨 0️⃣ CLEAR ALL (SAFE DELETE)
    # ✅ Step 1: Confirm FIRST
    if "confirm delete all" in message:
        clear_all_expenses()
        return build_response("🗑️ All transactions have been deleted.")

    # ✅ Step 2: Ask confirmation
    if "clear all" in message or "delete all" in message:
        return build_response("⚠️ Are you sure? Type 'confirm delete all' to proceed.")


    # 1️⃣ Add expense
    if "spent" in message:
        expense_data = parse_expense_message(message)
        add_expense(expense_data)
        return build_response(
            f"Added {expense_data['amount']} to {expense_data['category']}"
        )

    # 2️⃣ Delete last expense
    if "delete last expense" in message:
        removed = delete_last_expense()
        if removed:
            return build_response(
                f"Removed last expense of {removed['amount']} in {removed['category']}"
            )
        return build_response("No expenses to delete.")

    # 3️⃣ Update expense
    if "update" in message and "to" in message:
        try:
            parts = message.replace("update", "").split("to")
            old_msg, new_msg = parts[0].strip(), parts[1].strip()

            old_data = parse_expense_message(old_msg)
            new_data = parse_expense_message(new_msg)

            updated = update_expense(
                old_data["amount"], old_data["category"],
                new_data["amount"], new_data["category"]
            )

            if updated:
                return build_response(
                    f"Updated expense to {updated['amount']} in {updated['category']}"
                )
            return build_response("No matching expense found to update.")

        except:
            return build_response(
                "Use format: update 200 on food to 200 on groceries"
            )

    # 4️⃣ Deduct expense
    if "remove" in message or "deduct" in message:
        words = message.split()
        try:
            amt = float(words[1])
            category = words[-1]

            result = deduct_expense(amt, category)

            if result:
                return build_response(f"Deducted {amt} from {category}")
            return build_response("No matching expense found.")

        except:
            return build_response("Use format: remove 100 from food")

    # 5️⃣ Total
    if "total" in message:
        total = get_total_spent()
        return build_response(f"Your total expenses are {total}")

    # 6️⃣ Monthly summary
    if "summary" in message:
        summary = get_monthly_summary()
        lines = [f"Total: {summary['total']}"]
        for cat, amt in summary["breakdown"].items():
            lines.append(f"{cat}: {amt}")
        return build_response("\n".join(lines))

    # 7️⃣ Category breakdown
    if "category" in message or "breakdown" in message:
        breakdown = get_category_breakdown()
        lines = [f"{cat}: {amt}" for cat, amt in breakdown.items()]
        return build_response("\n".join(lines))

    # 8️⃣ Undo last action
    if "undo" in message:
        action = undo_last_action()

        if not action:
            return build_response("Nothing to undo.")

        return build_response(f"Undid last action ({action['type']})")

    # 9️⃣ Fix last category
    if "mistake" in message or "meant" in message or "change to" in message:
        words = message.replace("mistake", "").replace("meant", "").replace("change to", "").strip().split()

        if len(words) > 0:
            new_category = words[-1]
        else:
            return build_response("Please specify the correct category.")

        result = fix_last_category(new_category)

        if result:
            old_cat, new_cat = result
            return build_response(f"Changed category from {old_cat} to {new_cat}")

        return build_response("No expense to fix.")

    # 🔟 Set budget
    if "set budget" in message:
        try:
            words = message.split()
            amount = float(words[-1])
            category = words[-2]

            result = set_budget(category, amount)
            return build_response(result)

        except:
            return build_response("Use format: set budget food 20000")

    # 1️⃣1️⃣ Budget status
    if "budget" in message and "status" in message:
        try:
            words = message.split()
            category = words[-1]
        except:
            return build_response("Use format: budget status food")

        result = get_budget_status(category)

        if result:
            return build_response(
                f"""
Budget for {category}:
Spent: {result['spent']}
Limit: {result['limit']}
Remaining: {result['remaining']}
Used: {result['percent']}%
"""
            )

        return build_response("No budget found for this category.")
    
    # 1️⃣2️⃣ Transaction history
    if "history" in message:
        from services.expense_service import get_all_expenses
        expenses = get_all_expenses()
        return {
            "response": "Here is your transaction history",
            "transactions": expenses
        }

    # ❌ fallback
    return build_response("Sorry, I couldn't understand.")