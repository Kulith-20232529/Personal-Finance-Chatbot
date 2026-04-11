from datetime import datetime
import re

def parse_expense_message(message: str):
    """
    Extract amount and category from a message like:
    "I spent 500 on food"
    """
    # Default values
    amount = 0
    category = "misc"
    date = datetime.now().strftime("%Y-%m-%d")

    # Regex to find number
    amt_match = re.search(r"\b\d+(\.\d+)?\b", message)
    if amt_match:
        amount = float(amt_match.group())

    # Try to find category after 'on' or 'for'
    cat_match = re.search(r"(?:on|for)\s+(\w+)", message.lower())
    if cat_match:
        category = cat_match.group(1)

    return {
        "amount": amount,
        "category": category,
        "date": date
    }