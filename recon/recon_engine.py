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

        # Match using Swift_Ref
        ledger_match = ledger[ledger["Swift_Ref"] == tx_id]

        if ledger_match.empty:
            results.append({
                "transaction_id": tx_id,
                "status": "MISMATCH",
                "reason": "Swift reference not found in core ledger"
            })
            continue

        ledger_row = ledger_match.iloc[0]
        ledger_amount = float(ledger_row["Amount"])
        ledger_currency = ledger_row["Currency"]

        # Layer 1: Exact match
        if amount == ledger_amount and currency == ledger_currency:
            results.append({
                "transaction_id": tx_id,
                "status": "EXACT_MATCH",
                "reason": "Exact match between SWIFT and core"
            })
            continue

        # Layer 2: Soft match
        if currency == ledger_currency and abs(amount - ledger_amount) <= TOLERANCE:
            results.append({
                "transaction_id": tx_id,
                "status": "PARTIAL_MATCH",
                "reason": f"Amount differs within tolerance ({TOLERANCE})"
            })
            continue

        # Layer 3: Hard mismatch
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

    return results