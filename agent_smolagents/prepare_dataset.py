from typing import List
import datasets
from langchain.docstore.document import Document
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_document(guest: dict) -> Document:
    """
    Create a Document object from guest data.
    
    Args:
        guest: Dictionary containing guest information
        
    Returns:
        Document: Formatted document with guest information
    """
    return Document(
        page_content="\n".join([
            f"Name: {guest['name']}",
            f"Relation: {guest['relation']}",
            f"Description: {guest['description']}",
            f"Email: {guest['email']}"
        ]),
        metadata={"name": guest["name"]}
    )

def load_and_prepare_docs() -> List[Document]:
    """
    Load the dataset and convert it into Langchain Document objects.
    
    Returns:
        List[Document]: List of Document objects containing guest information
        
    Raises:
        RuntimeError: If dataset loading fails
    """
    logger.info("Loading dataset from Hugging Face Hub...")
    try:
        guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")
        logger.info(f"Dataset loaded with {len(guest_dataset)} entries.")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise RuntimeError(f"Failed to load dataset: {e}")
    
    logger.info("Converting dataset entries to Document objects...")
    try:
        docs = [create_document(guest) for guest in guest_dataset]
        logger.info(f"Created {len(docs)} Document objects.")
        return docs
    except Exception as e:
        logger.error(f"Error creating documents: {e}")
        raise RuntimeError(f"Failed to create documents: {e}")

if __name__ == "__main__":
    try:
        prepared_docs = load_and_prepare_docs()
        print(f"Successfully loaded and prepared {len(prepared_docs)} documents.")
        if prepared_docs:
            print("\nSample Document:")
            print(prepared_docs[0])
    except Exception as e:
        print(f"Error in main execution: {e}", file=sys.stderr)
        sys.exit(1)
