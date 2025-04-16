from langchain_community.retrievers import BM25Retriever
from langchain.tools import Tool
from .prepare_dataset import load_and_prepare_docs

docs = load_and_prepare_docs()
bm25_retriever = BM25Retriever.from_documents(docs)

def retrieve_guest_info(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = bm25_retriever.invoke(query)
    if results:
        return "\n\n".join([doc.page_content for doc in results[:3]])
    else:
        return "No matching guest information found."
    
guest_info_retriever = Tool(
    name="guest_info_retriever",
    func=retrieve_guest_info,
    description="Retrieves detailed information about gala guests based on their name or relation."
)
