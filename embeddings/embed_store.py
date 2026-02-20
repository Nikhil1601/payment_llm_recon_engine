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
def query_similar(collection, query_text):
    embedding = model.encode(query_text).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    return results

# This is distance-based similarity with a threshold  where smaller distance means more similar eg 0.4 - strict, 0.5 - moderate, 0.6 - lenient
# def query_similar(collection, query_text, threshold=0.5):
#     embedding = model.encode(query_text).tolist()

#     results = collection.query(
#         query_embeddings=[embedding],
#         n_results=3
#     )

#     filtered_results = []
#     print("Raw Query Results:")
#     print(results)
#     for doc, distance in zip(results["documents"][0], results["distances"][0]):
#         if distance-1 < threshold:
#             filtered_results.append({
#                 "document": doc,
#                 "distance": distance
#             })
#     print(f"Filtered {len(filtered_results)} results with distance < {threshold}")
#     return filtered_results

if __name__ == "__main__":
    collection = build_vector_store()

    # results = query_similar(collection, "EUR payment above 5000")
    results = query_similar(collection, "Payment from OMEGA LTD for GBP 5400")
    # print("Query: Payment from OMEGA LTD for 5400 GBP")
    print("Query Results:")
    print(results)
    # print(f"Found {len(results)} similar documents:")
    # for res in results:
    #     print(f"Distance: {res['distance']:.4f} | Document: {res['document']}")