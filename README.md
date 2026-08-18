# 🕉️ Ramayana RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on a structured English translation of the Ramayana.

The project uses **LangChain Runnables**, **NVIDIA NV-Embed-v1**, **ChromaDB**, and **Google Gemini 2.5 Flash** to build a complete semantic retrieval and question-answering pipeline.

## 🚀 Features

- 📖 Ramayana knowledge base stored in JSONL format
- 🔎 Semantic search using NVIDIA NV-Embed-v1
- 🗄️ ChromaDB vector database
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔗 LangChain Runnable / LCEL pipeline
- 🤖 Google Gemini 2.5 Flash for answer generation
- 💬 Interactive Streamlit chatbot
- 🏷️ Metadata-aware document retrieval
- 🔐 API keys managed using environment variables
- 📦 Modular project structure

---

## 🏗️ Architecture

```text
                 Ramayana English JSONL
                          │
                          ▼
                   Load Data
                          │
                          ▼
                Create Documents
                          │
                          ▼
                  NVIDIA NV-Embed-v1
                   Passage Embedding
                          │
                          ▼
                      ChromaDB
                          │
                          │
                    User Question
                          │
                          ▼
                  NVIDIA NV-Embed-v1
                    Query Embedding
                          │
                          ▼
                     Retriever
                          │
                          ▼
                Relevant Documents
                          │
                          ▼
                     QA Prompt
                          │
                          ▼
                Gemini 2.5 Flash
                          │
                          ▼
                       Answer
                          │
                          ▼
                  Streamlit Interface
```

---

## 📁 Project Structure

```text
RAMAYANA_QA_CHAT/
│
├── data/
│   └── ramayana_english.jsonl
│
├── indexing/
│   ├── load_data.py
│   ├── create_documents.py
│   └── create_vectorstore.py
│
├── prompts/
│   └── qa_prompt.py
│
├── retrieval/
│   ├── retriever.py
│   └── qa_chain.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The following files/directories are generated or kept locally and are not included in the repository:

```text
chroma_db/
venv/
.env
data/ramayana_telugu.jsonl
```

---

## 📚 Dataset

The project uses a structured English translation of the Ramayana.

The dataset is stored as:

```text
data/ramayana_english.jsonl
```

Each line represents one chapter and contains information such as:

- Chapter ID
- Kanda
- Chapter number
- Sarga range
- Question-answer pairs

Example:

```json
{
  "chunk_id": "chapter_001",
  "kanda": "Bala Kanda (Book of Childhood)",
  "chapter_ordinal": "Chapter One",
  "chapter_number": 1,
  "sarga_range": [1, 2, 3, 4, 5, 6],
  "qa_pairs": [
    {
      "q_no": 1,
      "question": "At the beginning of creation, who did Lord Narayana create first by His mere will?",
      "answer": "Four-faced Brahma"
    }
  ]
}
```

The original Telugu dataset is intentionally excluded from the public repository.

---

## 🔄 RAG Pipeline

### 1. Load Data

`indexing/load_data.py`

Loads the Ramayana JSONL dataset and converts each JSONL record into Python objects.

---

### 2. Create Documents

`indexing/create_documents.py`

Converts the structured Ramayana data into LangChain `Document` objects.

Each question-answer pair is converted into a retrieval document while preserving metadata such as:

```text
chunk_id
kanda
chapter_number
chapter_ordinal
sarga_range
q_no
```

This allows the retriever to return both the relevant content and its source information.

---

### 3. Generate Embeddings

`indexing/create_vectorstore.py`

The project uses:

```text
NVIDIA NV-Embed-v1
```

The Ramayana documents are converted into vector embeddings.

These embeddings represent the semantic meaning of each question-answer document.

---

### 4. Store Embeddings

The embeddings are stored in:

```text
ChromaDB
```

ChromaDB provides vector similarity search for retrieving the most relevant Ramayana content.

The ChromaDB directory is generated locally and is excluded from GitHub.

---

### 5. Retrieve Relevant Context

When the user asks a question:

```text
User Question
      │
      ▼
NVIDIA NV-Embed-v1
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB Similarity Search
      │
      ▼
Relevant Ramayana Documents
```

The retrieved documents are passed to the question-answering chain.

---

### 6. Generate Answer

The retrieved context and user question are passed to:

```text
Gemini 2.5 Flash
```

through a LangChain Runnable pipeline.

```text
Question
   +
Retrieved Context
       │
       ▼
   QA Prompt
       │
       ▼
Gemini 2.5 Flash
       │
       ▼
Generated Answer
```

The model is instructed to answer using the retrieved Ramayana context.

---

## 🔗 LangChain Runnable Pipeline

The project uses LangChain Runnables to connect different components into a sequential pipeline.

Conceptually:

```text
User Question
      │
      ▼
   Retriever
      │
      ▼
Context Formatter
      │
      ▼
   QA Prompt
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Output Parser
      │
      ▼
Final Answer
```

This makes the application modular and allows individual components to be replaced or improved independently.

---

## 🛠️ Technologies Used

### Programming

- Python

### LLM / Generative AI

- Google Gemini 2.5 Flash

### Embeddings

- NVIDIA NV-Embed-v1

### RAG Framework

- LangChain
- LangChain Core
- LangChain Runnables

### Vector Database

- ChromaDB

### Frontend

- Streamlit

### Data Format

- JSONL

### Environment Management

- python-dotenv

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Ramayana_QA_Chat
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```powershell
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```text
NVIDIA_API_KEY=your_nvidia_api_key
GOOGLE_API_KEY=your_google_api_key
```

Never upload `.env` to GitHub.

---

## 🗄️ Create the Vector Database

After configuring the API keys, run:

```bash
python indexing/create_vectorstore.py
```

This will:

1. Load the English Ramayana dataset.
2. Create retrieval documents.
3. Generate embeddings using NVIDIA NV-Embed-v1.
4. Store the embeddings in ChromaDB.

The generated vector database will be created locally in:

```text
chroma_db/
```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The chatbot will open in your browser.

---

## 💬 Example Questions

Example questions that can be asked:

```text
How many ministers did King Dasharatha have?
```

```text
Who advised Dasharatha to invite Rishyashringa?
```

```text
Where was Maharshi Rishyashringa?
```

```text
How did Rishyashringa arrive in Ayodhya?
```

```text
What arrangements did King Dasharatha make for the sacrifice?
```

The chatbot retrieves relevant information from the Ramayana knowledge base before generating the final answer.

---

## 🎯 Project Workflow

```text
Ramayana Data
      │
      ▼
JSONL Dataset
      │
      ▼
Document Creation
      │
      ▼
NVIDIA NV-Embed-v1
      │
      ▼
Vector Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Context
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Final Answer
```

---

## 🔐 Security

API keys are loaded from environment variables.

The following files are intentionally excluded from GitHub:

```text
.env
chroma_db/
venv/
data/ramayana_telugu.jsonl
```

Never hard-code API keys directly into Python files.

---

## 📌 Future Improvements

Possible future improvements include:

- Conversation memory
- Source/chapter citations in answers
- Telugu question support
- Multilingual question answering
- Hybrid keyword + semantic retrieval
- Reranking retrieved documents
- Improved Streamlit UI
- Deployment using Streamlit Cloud or other cloud platforms
- Evaluation using a predefined Ramayana QA benchmark

---

## 👨‍💻 Author

**Aditya Sunkavalli**

B.Tech – Information Technology  
NIT Srinagar

---

## ⭐ Project Goal

This project demonstrates how a domain-specific knowledge base can be combined with vector search and a large language model to build a grounded question-answering system.

The core RAG pipeline is:

```text
Knowledge Base
      ↓
Embeddings
      ↓
Vector Database
      ↓
Retrieval
      ↓
Context
      ↓
LLM
      ↓
Grounded Answer
```