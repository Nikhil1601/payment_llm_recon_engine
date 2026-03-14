from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_relevant_context(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="rag/chroma_db",
        embedding_function=embeddings
    )

    docs = db.similarity_search(query, k=2)

    context = "\n".join([d.page_content for d in docs])

    return context