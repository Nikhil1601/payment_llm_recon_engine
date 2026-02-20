from embeddings.embed_store import build_vector_store

collection = None

def get_collection():
    return collection

def initialize_vector_store():
    global collection
    collection = build_vector_store()