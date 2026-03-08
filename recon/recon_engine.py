import pandas as pd
from parsers.mt_parser import load_and_parse

TOLERANCE = 5.0


def reconcile(mt_file, ledger_file):
    payments = load_and_parse(mt_file)
    ledger = pd.read_csv(ledger_file)
    
    results = []

    for payment in payments:
        tx_id = payment["transaction_id"]
        amount = float(payment["amount"])
        currency = payment["currency"]

        ledger_match = ledger[ledger["Swift_Ref"] == tx_id]

    
    # CASE 1: Reference NOT founds
        # print("----")
        # print("TX:", tx_id)
        # print("MT Amount:", amount, "MT Currency:", currency)
        # print("Ledger Amount:", ledger["Amount"], "Ledger Currency:", ledger["Currency"])
        if ledger_match.empty:

            potential_matches = ledger[
            (ledger["Currency"] == currency) &
            (abs(ledger["Amount"] - amount) <= TOLERANCE)
            ]

            if not potential_matches.empty:
                results.append({
                    "transaction_id": tx_id,
                    "status": "PARTIAL_MATCH",
                    "reason": "Reference missing but matched on currency and amount tolerance"
                })
            else:
                results.append({
                    "transaction_id": tx_id,
                    "status": "MISMATCH",
                    "reason": "No matching reference or financial attributes found"
                })

            continue  # IMPORTANT

    
    # CASE 2: Reference found
    
        ledger_row = ledger_match.iloc[0]
        ledger_amount = float(ledger_row["Amount"])
        ledger_currency = ledger_row["Currency"]

    # Exact match
        # print("----")
        # print("TX:", tx_id)
        # print("MT Amount:", amount, "MT Currency:", currency)
        # print("Ledger Amount:", ledger_amount, "Ledger Currency:", ledger_currency)
        if amount == ledger_amount and currency == ledger_currency:
            results.append({
                "transaction_id": tx_id,
                "status": "EXACT_MATCH",
                "reason": "Exact match between SWIFT and core"
            })
            continue

    # Soft match
        if currency == ledger_currency and abs(amount - ledger_amount) <= TOLERANCE:
            results.append({
                "transaction_id": tx_id,
                "status": "PARTIAL_MATCH",
                "reason": f"Amount differs within tolerance ({TOLERANCE})"
            })
            continue

    # Hard mismatch
        if currency != ledger_currency:
            results.append({
                "transaction_id": tx_id,
                "status": "MISMATCH",
                "reason": "Currency mismatch between SWIFT and core"
            })
        else:
            results.append({
                "transaction_id": tx_id,
                "status": "MISMATCH",
                "reason": "Amount mismatch beyond tolerance"
            })
    print("SWIFT TX:", repr(tx_id))
    print("LEDGER REFS:", ledger["Swift_Ref"].tolist())
    return results
def reconciliation_summary(results):

    summary = {
        "total_transactions": len(results),
        "exact_match": 0,
        "partial_match": 0,
        "mismatch": 0
    }

    for r in results:
        if r["status"] == "EXACT_MATCH":
            summary["exact_match"] += 1
        elif r["status"] == "PARTIAL_MATCH":
            summary["partial_match"] += 1
        else:
            summary["mismatch"] += 1

    return summary