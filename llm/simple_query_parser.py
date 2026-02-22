import re

def parse_query(query):
    result = {
        "sender": None,
        "currency": None,
        "amount": None,
        "operator": None
    }

    query_upper = query.upper()

    # Currency
    currency_match = re.search(r"\b(USD|EUR|GBP|INR|AUD|CHF|HKD)\b", query_upper)
    if currency_match:
        result["currency"] = currency_match.group(1)

    # Amount
    amount_match = re.search(r"\b\d+(\.\d+)?\b", query_upper)
    if amount_match:
        result["amount"] = float(amount_match.group())

    # Comparison operators
    if "MORE THAN" in query_upper or "GREATER THAN" in query_upper or "ABOVE" in query_upper:
        result["operator"] = ">"
    elif "LESS THAN" in query_upper or "BELOW" in query_upper:
        result["operator"] = "<"
    else:
        result["operator"] = "="

    return result