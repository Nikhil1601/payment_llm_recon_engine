import re


def extract_block4_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract everything inside {4: .... -}
    pattern = r"\{4:(.*?)-\}"
    matches = re.findall(pattern, content, re.DOTALL)

    return matches


def parse_mt_message(message):
    data = {}

    tx_match = re.search(r":20:(.*)", message)
    amt_match = re.search(r":32A:\d{6}([A-Z]{3})([\d,]+)", message)
    sender_match = re.search(r":50K:(.*?)\n:", message, re.DOTALL)
    receiver_match = re.search(r":59:(.*?)\n:", message, re.DOTALL)

    if tx_match:
        data["transaction_id"] = tx_match.group(1).strip()

    if amt_match:
        data["currency"] = amt_match.group(1)
        data["amount"] = float(amt_match.group(2).replace(",", "."))

    if sender_match:
        data["sender"] = sender_match.group(1).strip().replace("\n", " ")

    if receiver_match:
        data["receiver"] = receiver_match.group(1).strip().replace("\n", " ")

    return data


def load_and_parse(file_path):
    raw_messages = extract_block4_messages(file_path)
    parsed = [parse_mt_message(msg) for msg in raw_messages]
    return parsed


if __name__ == "__main__":
    parsed_messages = load_and_parse("data/mt_msg.txt")

    print(f"Total messages parsed: {len(parsed_messages)}")
    for msg in parsed_messages:
        print(msg)