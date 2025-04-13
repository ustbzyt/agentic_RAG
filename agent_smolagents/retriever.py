from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
# Import the function from prepare_dataset using relative import
from .prepare_dataset import load_and_prepare_docs
# Import Document if needed for type hinting (optional but good practice)
from langchain.docstore.document import Document
from typing import List

class GuestInfoRetrieverTool(Tool):
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about."
        }
    }
    output_type = "string"
    # __init__ now clearly expects a list of Document objects
    def __init__(self, docs: List[Document]):
        # Consider adding error handling if docs is empty or not the expected type
        if not docs:
            raise ValueError("Cannot initialize retriever with empty documents list.")
        print(f"Initializing BM25Retriever with {len(docs)} documents...")
        self.retriever = BM25Retriever.from_documents(docs)
        print("BM25Retriever initialized successfully.")

    def forward(self, query: str):
        print(f"Retriever received query: '{query}'")
        results = self.retriever.get_relevant_documents(query)
        print(f"Retriever found {len(results)} relevant documents.")
        if results:
            # Return top 3 results, clearly separated
            return "\n\n---\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."
        
# Define a function to handle loading data and initializing the tool
def load_guest_dataset() -> GuestInfoRetrieverTool:
    """Loads the guest data and initializes the GuestInfoRetrieverTool."""
    print("Starting guest dataset loading and tool initialization...")
    # 1. Load and prepare the documents
    docs = load_and_prepare_docs()
    # 2. Initialize the tool with the documents
    guest_info_tool = GuestInfoRetrieverTool(docs)
    print("GuestInfoRetrieverTool is ready.")
    return guest_info_tool
