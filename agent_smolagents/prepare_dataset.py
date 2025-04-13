import datasets
from langchain.docstore.document import Document
import sys

def load_and_prepare_docs():
    """Loads the dataset and converts it into Langchain Document objects."""
    print("Loading dataset from Hugging Face Hub...")
    try:
        guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")
        print(f"Dataset loaded with {len(guest_dataset)} entries.")
    except Exception as e:
        print(f"Error loading dataset: {e}", file=sys.stderr)
        # Decide how to handle the error, e.g., return empty list or raise
        return [] # Or raise e
    
    print("Converting dataset entries to Document objects...")
    docs = [
        Document(
            # hardcoded
            page_content="\n".join([
                f"Name: {guest['name']}",
                f"Relation: {guest['relation']}",
                f"Description: {guest['description']}",
                f"Email: {guest['email']}"
            ]),
            metadata={"name": guest["name"]}
        )
        for guest in guest_dataset
    ]
    print(f"Created {len(docs)} Document objects.")
    return docs

# Optional: You can keep this if you want to run this script standalone for testing
if __name__ == "__main__":
    prepared_docs = load_and_prepare_docs()
    print(f"Successfully loaded and prepared {len(prepared_docs)} documents.")
    if prepared_docs:
        print("\nSample Document:")
        print(prepared_docs[0])
