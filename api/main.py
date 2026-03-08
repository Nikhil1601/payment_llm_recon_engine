from fastapi import FastAPI
from api.dependencies import initialize_vector_store, get_collection
from embeddings.embed_store import query_similar
from search.smart_search import smart_search
from search.smart_search_with_comparison import smart_search_from_struct
from recon.recon_engine import reconcile
from recon.recon_engine import reconciliation_summary

app = FastAPI(title="Payment LLM Reconciliation Engine")


@app.on_event("startup")
def startup_event():
    initialize_vector_store()

# to check api is up and running
@app.get("/health")
def health():
    return {"status": "running"}

# for embedding retrieval
@app.get("/search")
def search(query: str):
    collection = get_collection()
    results = query_similar(collection, query)
    return {"results": results}

# hybrid retival logic without llm -: regex based parsing and matching with mt messages
@app.get("/smart_search")
def smart_search_route(query: str):
    results = smart_search("data/mt_msg.txt", query)
    return {"results": results}

@app.get("/smart_search_comparison")
def smart_search_comparison_route(query: str):
    results = smart_search_from_struct("data/mt_msg.txt", query)
    return {"results": results}

@app.get("/reconcile")
def reconcile_endpoint():
    results = reconcile(
        "data/mt_msg.txt",
        "data/transactions.csv"
    )
    return {"reconciliation_results": results}

@app.get("/reconciliation-summary")
def recon_summary():
    results = reconcile(
        "data/mt_msg.txt",
        "data/transactions.csv"
    )
    return reconciliation_summary(results)