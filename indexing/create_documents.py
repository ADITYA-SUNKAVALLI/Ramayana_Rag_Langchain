from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda


def create_documents(chunks):
    """
    Convert Ramayana Q&A pairs into LangChain Documents.

    Original 99 chapters are preserved.
    Each Q&A becomes one retrieval document.
    """

    documents = []

    for chunk in chunks:

        for qa in chunk["qa_pairs"]:

            content = (
                f"Chapter: {chunk['chapter_ordinal']}\n"
                f"Kanda: {chunk['kanda']}\n\n"
                f"Question: {qa['question']}\n\n"
                f"Answer: {qa['answer']}"
            )

            metadata = {
                "chunk_id": chunk["chunk_id"],
                "kanda": chunk["kanda"],
                "chapter_number": chunk["chapter_number"],
                "chapter_ordinal": chunk["chapter_ordinal"],
                "q_no": qa["q_no"],
                "sarga_range": str(chunk["sarga_range"]),
            }

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata,
                )
            )

    print(f"Created {len(documents)} retrieval documents.")

    return documents


create_documents_runnable = RunnableLambda(
    create_documents
)