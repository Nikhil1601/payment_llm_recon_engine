from parsers.mt_parser import load_and_parse
from llm.simple_query_parser import parse_query

def smart_search(mt_file, query):
    parsed_query = parse_query(query)
    payments = load_and_parse(mt_file)

    results = []

    for payment in payments:
        if parsed_query["sender"]:
            if parsed_query["sender"] not in payment["sender"].upper():
                continue

        if parsed_query["currency"]:
            if parsed_query["currency"] != payment["currency"]:
                continue

        if parsed_query["amount"]:
            # Allow small tolerance
            if abs(payment["amount"] - parsed_query["amount"]) > 1:
                continue

        results.append(payment)

    return results