import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableLambda

from load_data import load_data_runnable
from create_documents import create_documents_runnable


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------


load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY not found in .env"
    )
# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"


# --------------------------------------------------
# NVIDIA Embeddings
# --------------------------------------------------

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

embeddings = NVIDIAEmbeddings(
    model="nvidia/nv-embed-v1",
    model_type="passage",
    api_key=NVIDIA_API_KEY,
)


# --------------------------------------------------
# Create Vector Store
# --------------------------------------------------

def create_vectorstore(documents):

    print("Creating Chroma vector store...")

    # Remove old database
    if CHROMA_PATH.exists():
        print("Removing old Chroma database...")
        shutil.rmtree(CHROMA_PATH)

    vectorstore = Chroma(
        collection_name="ramayana_qa",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH),
    )

    # Stable document IDs
    ids = [
        f"{doc.metadata['chunk_id']}_q{doc.metadata['q_no']}"
        for doc in documents
    ]

    vectorstore.add_documents(
        documents=documents,
        ids=ids,
    )

    print(
        f"Stored {len(documents)} documents in Chroma."
    )

    return vectorstore


create_vectorstore_runnable = RunnableLambda(
    create_vectorstore
)


# --------------------------------------------------
# Complete Indexing Pipeline
# --------------------------------------------------

indexing_pipeline = (
    load_data_runnable
    | create_documents_runnable
    | create_vectorstore_runnable
)


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":

    print("Starting Ramayana indexing...\n")

    indexing_pipeline.invoke(None)

    print("\n--------------------------------")
    print("INDEXING COMPLETED")
    print("--------------------------------")
    print(f"Chroma DB: {CHROMA_PATH}")