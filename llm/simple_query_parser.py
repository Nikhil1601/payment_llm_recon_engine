import re

def parse_query(query):
    result = {
        "sender": None,
        "currency": None,
        "amount": None
    }

    # Extract currency
    currency_match = re.search(r"\b(USD|EUR|GBP|INR|AUD|CHF|HKD)\b", query)
    if currency_match:
        result["currency"] = currency_match.group(1)

    # Extract amount
    amount_match = re.search(r"\b\d+(\.\d+)?\b", query)
    if amount_match:
        result["amount"] = float(amount_match.group())

    # Extract sender (basic logic)
    sender_match = re.search(r"from ([A-Z\s]+)", query.upper())
    if sender_match:
        result["sender"] = sender_match.group(1).strip()

    return result