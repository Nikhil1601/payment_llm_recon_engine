from langchain_community.llms import Ollama
from rag.retriever import get_relevant_context

llm = Ollama(model="llama3")

def generate_explanation(transaction):

    query = f"{transaction['status']} reconciliation case"

    context = get_relevant_context(query)

    prompt = f"""
    Use the context to explain the reconciliation result.

    Context:
    {context}

    Transaction ID: {transaction['transaction_id']}
    Status: {transaction['status']}
    Reason: {transaction['reason']}

    Explain the reconciliation outcome clearly.
    """

    response = llm.invoke(prompt)

    return response