import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
)

from langchain_core.output_parsers import StrOutputParser

from retrieval.retriever import retriever
from prompts.qa_prompt import qa_prompt


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError(
        "GOOGLE_API_KEY is missing from .env"
    )


# --------------------------------------------------
# Gemini 2.5 Flash
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)


# --------------------------------------------------
# Format Documents
# --------------------------------------------------

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


format_docs_runnable = RunnableLambda(
    format_docs
)


# --------------------------------------------------
# RAG Runnable
# --------------------------------------------------

qa_chain = (
    {
        "context": retriever | format_docs_runnable,
        "question": RunnablePassthrough(),
    }
    | qa_prompt
    | llm
    | StrOutputParser()
)


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    question = (
        "Who advised Dasharatha to invite "
        "Rishyashringa?"
    )

    answer = qa_chain.invoke(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)