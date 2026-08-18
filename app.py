import streamlit as st

from retrieval.qa_chain import qa_chain


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Ramayana RAG",
    page_icon="🕉️",
    layout="centered",
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🕉️ Ramayana RAG Assistant")

st.caption(
    "Ask quetions about Ramayana"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# User Question
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about the Ramayana..."
)


if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # Assistant
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the Ramayana..."
        ):

            try:

                answer = qa_chain.invoke(question)

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as e:

                st.error(
                    f"Error while generating answer: {e}"
                )