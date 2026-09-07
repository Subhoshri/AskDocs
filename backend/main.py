from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
import shutil
import uuid

from .rag_pipeline import RAGPipeline

app = FastAPI(
    title="AskDocs API",
    description="AI-powered document question-answering system",
    version="1.0.0"
)


# Temporary local storage for uploaded documents
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Create RAG pipeline
pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/")
def root():
    return {
        "message": "DocQuery API is running"
    }


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    document_id = str(uuid.uuid4())

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        num_chunks = pipeline.index_document(
            file_path=str(file_path),
            document_id=document_id,
            filename=file.filename
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "READY",
        "chunks_indexed": num_chunks
    }


@app.post("/query")
def query_documents(request: QueryRequest):

    if pipeline.vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="No documents have been uploaded yet."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    results = pipeline.retrieve(
        request.question,
        top_k=request.top_k
    )

    sources = []

    for result in results:

        metadata = result["metadata"]

        sources.append({
            "document": metadata["filename"],
            "page": metadata["page_number"],
            "score": result["score"]
        })

    return {
        "question": request.question,
        "retrieved_chunks": results,
        "sources": sources
    }