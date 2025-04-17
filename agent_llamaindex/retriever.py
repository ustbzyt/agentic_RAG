from llama_index.core.tools import FunctionTool
from llama_index.retrievers.bm25 import BM25Retriever
from .prepare_dataset import load_and_prepare_docs


docs = load_and_prepare_docs()
bm25_retriever = BM25Retriever.from_defaults(nodes=docs)

def get_guest_info_retriever(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = bm25_retriever.retrieve(query)
    if results:
        return "\n\n".join([doc.text for doc in results[:3]])
    else:
        return "No matching guest information found."

# Initialize the tool
guest_info_retriever = FunctionTool.from_defaults(fn=get_guest_info_retriever, name="guest_info_retriever", description="Retrieve detailed information about gala guests based on their name or relation.")