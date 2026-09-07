# AI Knowledge Assistant

A command-line AI application that answers questions from your own documents using Retrieval Augmented Generation (RAG). It combines embeddings for semantic search with a Large Language Model (LLM) to provide grounded, source-cited answers. This is the capstone project of the **Young Python Wizard** Module 8 series.

---

## Features

- 📄 Load and process text documents from a folder.
- ✂️ Automatically chunk documents into manageable pieces.
- 🧠 Generate embeddings using sentence-transformers (local, free).
- 🔍 Perform semantic search to find the most relevant chunks.
- 💬 Answer questions using an LLM (OpenAI) or a built-in mock generator.
- 📚 Cite source documents for every answer.
- 🗄️ Persistent storage using SQLite (chunks and embeddings).

---

## Project Structure

```
knowledge_assistant/
├── models/
│   ├── __init__.py
│   └── document.py
├── services/
│   ├── __init__.py
│   ├── embedding_service.py
│   ├── retrieval_service.py
│   └── generation_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   └── document_repository.py
├── data/
│   └── sample_docs/
│       ├── README.md
│       ├── python_basics.txt
│       ├── solar_system.txt
│       └── machine_learning.txt
├── main.py
└── requirements.txt
```

- **`models/`** – Data classes (`Document`).
- **`services/`** – Business logic (embedding, retrieval, generation).
- **`storage/`** – Database connection, initialization, and repository.
- **`data/sample_docs/`** – Example documents for testing.
- **`main.py`** – Command-line interface and RAG pipeline orchestration.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Optional: OpenAI API Key

If you want the assistant to use a real LLM (OpenAI GPT-3.5 or GPT-4), set your API key as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."
```

Or create a `.env` file:

```
OPENAI_API_KEY=sk-...
```

If no key is set, the assistant will use a simple extractive fallback (returns the most relevant chunk).

---

## Running the Application

```bash
python main.py
```

On first run, you'll be prompted to enter a path to your documents folder. For example:

```
Enter documents directory path (or 'skip' if already loaded): data/sample_docs
```

The assistant will chunk, embed, and index the documents. Then you can ask questions:

```
Question (or 'quit'): What is the capital of France?
```

The assistant will retrieve relevant chunks and generate an answer, showing the sources used.

---

## How It Works

### 1. Document Loading and Chunking

The `main.py` script scans a directory for `.txt` files. Each file is read and split into chunks of 500 characters. Chunking helps ensure that only relevant parts of a document are retrieved.

### 2. Embedding

`EmbeddingService` uses the `sentence-transformers` library with the `all-MiniLM-L6-v2` model. Each chunk is converted into a dense vector (384 dimensions). These embeddings capture semantic meaning.

### 3. Storage

Embeddings and chunk content are stored in a SQLite database (`knowledge.db`). The `documents` table has columns for title, content, chunk_index, and embedding (as JSON).

### 4. Retrieval

When a user asks a question, it is also embedded. `RetrievalService` computes cosine similarity between the question embedding and all document embeddings. The top-k most similar chunks (default 3) are returned.

### 5. Generation

`GenerationService` constructs a prompt with the retrieved context and the user's question. If an OpenAI API key is available, it calls GPT to generate an answer. Otherwise, it returns the most relevant chunk as a simple answer.

### 6. Sources

For transparency, the assistant displays the source document title and chunk index for each retrieved piece of context.

---

## Prompt Used for Generation

The system prompt instructs the model to answer based only on the provided context:

```
You are a helpful knowledge assistant. Answer the user's question based ONLY on the provided context.
If the answer is not in the context, say "I cannot answer based on the provided documents."
```

---

## Sample Documents

The `data/sample_docs/` folder includes three text files:

- `python_basics.txt` – Introduction to Python programming.
- `solar_system.txt` – Facts about planets and the Sun.
- `machine_learning.txt` – Overview of ML concepts.

You can add your own `.txt` files to this folder to customize the knowledge base.

---

## Extending the Project

Here are some ideas to enhance the assistant:

- Add PDF support using `pypdf` or `pdfplumber`.
- Implement faster vector search with FAISS or ChromaDB.
- Add a web interface using Gradio or Flask.
- Support follow-up questions by adding conversation memory.
- Use a local LLM (e.g., Llama) instead of OpenAI.
- Add automatic evaluation with a set of test questions.
- Implement document update/removal.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy building! 🧠🐍