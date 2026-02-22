from parsers.mt_parser import load_and_parse
from llm.simple_query_parser import parse_query

def smart_search_from_struct(mt_file, query):
    payments = load_and_parse(mt_file)
    parsed_query = parse_query(query)
    results = []

    for payment in payments:

        # Currency filter
        if parsed_query.get("currency"):
            if parsed_query["currency"] != payment["currency"]:
                continue

        # Amount filter
        if parsed_query.get("amount"):
            amount = float(payment["amount"])
            query_amount = float(parsed_query["amount"])

            if parsed_query["operator"] == ">":
                if amount <= query_amount:
                    continue

            elif parsed_query["operator"] == "<":
                if amount >= query_amount:
                    continue

            else:  # "="
                if abs(amount - query_amount) > 1:
                    continue

        results.append(payment)

    return results