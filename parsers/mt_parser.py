import re

def parse_mt_message(message):
    data = {}

    tx_match = re.search(r":20:(.*)", message)
    amt_match = re.search(r":32A:\d{6}([A-Z]{3})(\d+)", message)
    sender_match = re.search(r":50K:(.*)", message)
    receiver_match = re.search(r":59:(.*)", message)

    if tx_match:
        data["transaction_id"] = tx_match.group(1).strip()

    if amt_match:
        data["currency"] = amt_match.group(1)
        data["amount"] = int(amt_match.group(2))

    if sender_match:
        data["sender"] = sender_match.group(1).strip()

    if receiver_match:
        data["receiver"] = receiver_match.group(1).strip()

    return data


def load_and_parse(file_path):
    with open(file_path, "r") as f:
        raw = f.read()

    messages = raw.strip().split("\n\n")
    parsed = [parse_mt_message(msg) for msg in messages]

    return parsed


if __name__ == "__main__":
    parsed_messages = load_and_parse("data/mt_msg.txt")
    print(parsed_messages)