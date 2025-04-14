from typing import List, Optional
from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
# Import the function from prepare_dataset using relative import
from .prepare_dataset import load_and_prepare_docs
# Import Document if needed for type hinting (optional but good practice)
from langchain.docstore.document import Document

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

    def __init__(self, docs: List[Document]) -> None:
        """
        Initialize the retriever with a list of documents.
        
        Args:
            docs: List of Document objects containing guest information
            
        Raises:
            ValueError: If docs is empty
        """
        if not docs:
            raise ValueError("Cannot initialize retriever with empty documents list.")
        
        print(f"Initializing BM25Retriever with {len(docs)} documents...")
        self.retriever = BM25Retriever.from_documents(docs)
        print("BM25Retriever initialized successfully.")

    def forward(self, query: str) -> str:
        """
        Retrieve and return relevant guest information based on the query.
        
        Args:
            query: Search query for guest information
            
        Returns:
            str: Formatted string containing relevant guest information
        """
        print(f"Retriever received query: '{query}'")
        results = self.retriever.get_relevant_documents(query)
        print(f"Retriever found {len(results)} relevant documents.")
        
        if not results:
            return "No matching guest information found."
            
        # Return top 3 results, clearly separated
        return "\n\n---\n\n".join([doc.page_content for doc in results[:3]])

def load_guest_dataset() -> GuestInfoRetrieverTool:
    """
    Load the guest dataset and initialize the GuestInfoRetrieverTool.
    
    Returns:
        GuestInfoRetrieverTool: Initialized tool with loaded guest data
        
    Raises:
        RuntimeError: If dataset loading fails
    """
    print("Starting guest dataset loading and tool initialization...")
    
    try:
        # Load and prepare the documents
        docs = load_and_prepare_docs()
        if not docs:
            raise RuntimeError("Failed to load guest dataset - no documents found.")
            
        # Initialize the tool with the documents
        guest_info_tool = GuestInfoRetrieverTool(docs)
        print("GuestInfoRetrieverTool is ready.")
        return guest_info_tool
        
    except Exception as e:
        print(f"Error loading guest dataset: {e}")
        raise RuntimeError(f"Failed to initialize GuestInfoRetrieverTool: {e}")
