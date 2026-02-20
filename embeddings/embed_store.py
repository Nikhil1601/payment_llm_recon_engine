from sentence_transformers import SentenceTransformer
import chromadb
from parsers.mt_parser import load_and_parse

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store():
    parsed_data = load_and_parse("data/mt_msg.txt")

    client = chromadb.Client()
    collection = client.get_or_create_collection(name="payments")

    for record in parsed_data:
        doc_text = (
            f"Transaction ID: {record.get('transaction_id')} | "
            f"Amount: {record.get('amount')} {record.get('currency')} | "
            f"Sender: {record.get('sender')} | "
            f"Receiver: {record.get('receiver')}"
        )

        embedding = model.encode(doc_text).tolist()

        collection.add(
            documents=[doc_text],
            embeddings=[embedding],
            ids=[record.get("transaction_id")]
        )

    return collection

# This was absract similarity
# def query_similar(collection, query_text):
#     embedding = model.encode(query_text).tolist()

#     results = collection.query(
#         query_embeddings=[embedding],
#         n_results=3
#     )

#     return results


if __name__ == "__main__":
    collection = build_vector_store()

    # results = query_similar(collection, "EUR payment above 5000")
    results = query_similar(collection, "Payment from OMEGA LTD for 5400.75 GBP")
    print("Query: Payment from OMEGA LTD for 5400.75 GBP")
    print("Query Results:")
    print(results)