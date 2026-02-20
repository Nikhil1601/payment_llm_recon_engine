from fastapi import FastAPI
from api.dependencies import initialize_vector_store, get_collection
from embeddings.embed_store import query_similar
# from reconciliation.reconcile import reconcile_payments

app = FastAPI(title="Payment LLM Reconciliation Engine")


@app.on_event("startup")
def startup_event():
    initialize_vector_store()


@app.get("/health")
def health():
    return {"status": "running"}


@app.get("/search")
def search(query: str):
    collection = get_collection()
    results = query_similar(collection, query)
    return {"results": results}


# @app.get("/reconcile")
# def reconcile():
#     matches, mismatches = reconcile_payments(
#         "data/mt_messages.txt",
#         "data/ledger.csv"
#     )

#     return {
#         "matched_transactions": matches,
#         "unmatched_transactions": mismatches
#     }