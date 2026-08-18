from pathlib import Path

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY not found in .env"
    )
    

embeddings = NVIDIAEmbeddings(
    model="nvidia/nv-embed-v1",
    model_type="query",
    api_key=NVIDIA_API_KEY,
)


vectorstore = Chroma(
    collection_name="ramayana_qa",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_PATH),
)


retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5
    }
)


if __name__ == "__main__":

    question = (
        "Who advised Dasharatha to invite "
        "Rishyashringa?"
    )

    results = retriever.invoke(question)

    print(f"\nRetrieved {len(results)} documents:\n")

    for i, doc in enumerate(results, start=1):

        print(f"--- Result {i} ---")
        print(doc.page_content)
        print("Metadata:", doc.metadata)
        print()