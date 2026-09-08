from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import shutil
import uuid
from typing import List
from dotenv import load_dotenv
from fastapi.responses import FileResponse

load_dotenv()
from .rag_pipeline import RAGPipeline

app = FastAPI(
    title="AskDocs API",
    description="AI-powered document question-answering system",
    version="1.0.0"
)


# Temporary local storage for uploaded documents
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTS = {}

# Create RAG pipeline
pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    document_ids: list[str] | None = None

@app.get("/")
def root():
    return {
        "message": "DocQuery API is running"
    }

@app.get("/documents")
def list_documents():

    if pipeline.vector_store is None:
        return {"documents": []}

    documents = {}

    for metadata in pipeline.vector_store.metadata:

        document_id = metadata["document_id"]

        if document_id not in documents:
            documents[document_id] = {
                "document_id": document_id,
                "filename": metadata["filename"]
            }

    return {
        "documents": list(documents.values())
    }

@app.get("/documents/{document_id}/file")
def view_document(document_id: str):

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf"
    )

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

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )

    DOCUMENTS[document_id] = {
    "document_id": document_id,
    "filename": file.filename,
    "status": "READY",
    "chunks_indexed": num_chunks
    }

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

    try:

        answer, results = pipeline.answer(
        request.question,
        top_k=request.top_k,
        document_ids=request.document_ids
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Answer generation failed: {str(e)}"
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
        "answer": answer,
        "sources": sources
    }