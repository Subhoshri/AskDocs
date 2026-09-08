# AskDocs

AI-powered document question-answering system. Upload PDF documents, ask natural-language questions about their contents, and get answers grounded in the retrieved text with document and page-level source citations.

Built with a Retrieval-Augmented Generation (RAG) pipeline: PyMuPDF for text extraction, Sentence-Transformers for embeddings, FAISS for vector search, and Gemini for grounded answer generation.

---

## Features

- Upload one or more PDF documents
- Ask natural-language questions and get answers grounded in retrieved evidence (not the model's general knowledge)
- Source citations with document name, page number, relevance score, and excerpt
- Duplicate detection via file-content hashing (SHA-256), not filename-based
- Scope a question to specific documents, or search across all of them
- Delete previously uploaded documents
- Persistent index: uploaded documents remain searchable across backend restarts

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend / API | FastAPI + Uvicorn |
| PDF Processing | PyMuPDF |
| Embeddings | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector Search | FAISS (`IndexFlatIP`) |
| LLM | Google Gemini |
| Validation | Pydantic |

---

## Prerequisites

- Python 3.10+
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/app/apikey))

---

## Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd AskDocs
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

This is the only environment variable required. The backend loads it automatically via `python-dotenv` on startup.

---

## Running the Application

The backend and frontend are separate processes and both need to be running. Use two terminals.

### Terminal 1: Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs (Swagger UI) are auto-generated at `http://127.0.0.1:8000/docs`.

### Terminal 2: Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

The UI will open automatically at `http://localhost:8501`.

> Start the backend first, the frontend calls it directly and will error on requests until it's up.

---

## API Reference

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/documents/upload` | Upload and index a PDF (`multipart/form-data`, field name `file`) |
| `GET` | `/documents` | List all indexed documents |
| `GET` | `/documents/{document_id}/file` | View / download the original PDF |
| `DELETE` | `/documents/{document_id}` | Delete a document and its index entries |
| `POST` | `/query` | Ask a question against the indexed documents |

### `POST /documents/upload`

Accepts a single PDF file (`.pdf`, max 20 MB, must start with the `%PDF-` signature). Rejects duplicate content (HTTP 409) based on a SHA-256 hash of the file, regardless of filename.

**Response**

```json
{
  "document_id": "b3f1c9d2-...",
  "filename": "Projects.pdf",
  "status": "READY",
  "chunks_indexed": 42
}
```

### `POST /query`

**Request**

```json
{
  "question": "What projects are available?",
  "top_k": 5,
  "document_ids": null
}
```

`document_ids: null` searches across all uploaded documents. Pass a list of document IDs to scope the search to specific documents.

**Response**

```json
{
  "question": "What projects are available?",
  "answer": "...",
  "sources": [
    {
      "document": "Projects.pdf",
      "page": 1,
      "score": 0.82,
      "excerpt": "Project 1: AI-Powered Document Q&A..."
    }
  ]
}
```

### `DELETE /documents/{document_id}`

Removes the document's PDF file and its entries from the vector index and metadata store.

---

## Project Structure

```
AskDocs/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, API routes
│   ├── document_processor.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── ingestion.py
│   ├── rag.py
│   ├── rag_pipeline.py
│   └── test_full_rag.py
├── frontend/
│   └── app.py                # Streamlit UI
├── tests/
│   ├── test_document_processor.py
│   └── test_chunker.py
├── data/
│   ├── faiss.index           # generated on first upload
│   ├── metadata.json         # generated on first upload
│   └── uploads/               # stored PDFs (UUID-named)
├── .env                       # GEMINI_API_KEY (not committed)
├── .gitignore
└── requirements.txt
```

---

## Running Tests

```bash
pytest
```

Test files are under `tests/` and `backend/test_full_rag.py`. See the accompanying **Unit Test Cases and Results** document for the full test list and outcomes.

---

## Notes & Known Limitations

- Only `.pdf` files are supported; scanned/image-only PDFs are detected and rejected with a clear error (no OCR).
- `data/` (the FAISS index, metadata, and uploaded PDFs) is local and will need to be recreated if the directory is deleted, this is expected for the current single-user MVP.
- Document deletion rebuilds the FAISS index from the remaining vectors; this is a known cost of using `IndexFlatIP` and is documented in the design document.
- No authentication, the API is intended for local/single-user use in its current form.

For the full architecture, design rationale, and production-scaling notes, see the accompanying **Design Document**.