# AI-Powered Document Q&A System
## Test Cases and Results

**Project Name:** AI-Powered Document Q&A System  
**Application Name:** AskDocs  
**Document Type:** Test Cases and Results  
**Version:** 1.0  
**Testing Type:** Unit Testing, Integration Testing, API Testing, and Manual System Testing  

---

## 1. Introduction

This document describes the testing strategy, test cases, expected behaviour, and observed results for the **AI-Powered Document Q&A System**.

The purpose of testing is to verify that the system correctly performs document ingestion, text extraction, chunking, embedding generation, semantic retrieval, answer generation, source attribution, document management, and error handling. Testing also covers important edge cases such as invalid files, duplicate documents, unsupported questions, multiple documents, document-scoped retrieval, and document deletion.

---

## 2. Testing Objectives

The primary objectives of testing are:

- Verify correct extraction of text from PDF documents.
- Verify correct chunking of extracted text with overlap.
- Verify generation of valid semantic embeddings.
- Verify vector storage and similarity-based retrieval.
- Verify persistence of the vector index and metadata.
- Verify incremental addition of documents.
- Verify document-scoped retrieval.
- Verify relevance filtering and retrieval diversity.
- Verify grounded answer generation.
- Verify handling of questions with insufficient evidence.
- Verify source document and page attribution.
- Verify duplicate document detection.
- Verify upload validation and file-size restrictions.
- Verify document viewing and deletion.
- Verify appropriate API responses for invalid requests.

---

## 3. Testing Environment

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| PDF Processing | PyMuPDF |
| Embedding Model | Sentence Transformers |
| Embedding Model Used | `all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| LLM | Gemini 2.5 Flash |
| Testing Framework | Pytest |
| API Testing | FastAPI TestClient |
| Environment | Local Development Environment |

---

## 4. Testing Strategy

Testing is divided into four levels.

### 4.1 Unit Testing

Individual components are tested independently.

Components tested include:

- PDF text extraction
- Text chunking
- Embedding generation
- Semantic similarity
- Vector-store operations
- RAG pipeline behaviour

### 4.2 Integration Testing

Integration tests verify the interaction between multiple components.

The primary processing flow is:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
FAISS Vector Store
 ↓
Semantic Retrieval
 ↓
Relevant Context
 ↓
LLM
 ↓
Answer + Sources
```

### 4.3 API Testing

The FastAPI endpoints are tested for:

- Valid requests
- Invalid requests
- Input validation
- Document upload
- Document listing
- Document viewing
- Document deletion
- Query processing
- Error handling

### 4.4 End-to-End Testing

The complete application is tested through the Streamlit frontend to verify the actual user workflow.

---

# 5. Unit Test Cases

## 5.1 Document Processing

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-DP-01 | Extract text from valid PDF | Text is extracted successfully | As expected | PASS |
| TC-DP-02 | Preserve page numbers | Extracted text is mapped to the correct page numbers | As expected | PASS |
| TC-DP-03 | Process empty PDF | No extractable pages are returned | As expected | PASS |
| TC-DP-04 | Process multi-page PDF | Each page is processed independently | As expected | PASS |

---

## 5.2 Text Chunking

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-CH-01 | Chunk long text | Multiple chunks are generated | As expected | PASS |
| TC-CH-02 | Verify chunk overlap | Consecutive chunks contain the configured overlap | As expected | PASS |
| TC-CH-03 | Chunk short text | A single chunk is generated | As expected | PASS |
| TC-CH-04 | Preserve page metadata | Page number is retained in each chunk | As expected | PASS |

---

## 5.3 Embedding Generation

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-EM-01 | Generate single embedding | A 384-dimensional embedding is generated | As expected | PASS |
| TC-EM-02 | Generate multiple embeddings | One embedding is generated for each input | As expected | PASS |
| TC-EM-03 | Verify normalization | Embeddings have approximately unit norm | As expected | PASS |

---

## 5.4 Semantic Similarity

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-SM-01 | Compare semantically similar sentences | Similar sentences receive a higher similarity score | As expected | PASS |
| TC-SM-02 | Compare unrelated sentences | Unrelated sentences receive a lower similarity score | As expected | PASS |

---

## 5.5 Vector Store

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-VS-01 | Add vectors | Vectors and metadata are added successfully | As expected | PASS |
| TC-VS-02 | Perform similarity search | Relevant vectors are returned | As expected | PASS |
| TC-VS-03 | Verify metadata alignment | Correct metadata is returned with retrieved vectors | As expected | PASS |
| TC-VS-04 | Delete document vectors | All vectors belonging to the document are removed | As expected | PASS |
| TC-VS-05 | Delete nonexistent document | No deletion is performed | As expected | PASS |
| TC-VS-06 | Persist vector store | Index and metadata can be restored after restart | As expected | PASS |

---

# 6. RAG Pipeline Test Cases

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-RAG-01 | Ask relevant question | Relevant document chunks are retrieved | As expected | PASS |
| TC-RAG-02 | Generate answer from retrieved context | Answer is generated using retrieved evidence | As expected | PASS |
| TC-RAG-03 | Ask unknown question | System indicates insufficient information | As expected | PASS |
| TC-RAG-04 | Verify source attribution | Document name and page number are returned | As expected | PASS |
| TC-RAG-05 | Incrementally add document | Existing documents remain available | As expected | PASS |
| TC-RAG-06 | Restrict query to selected documents | Only selected documents are searched | As expected | PASS |
| TC-RAG-07 | Apply relevance threshold | Low-relevance results are filtered | As expected | PASS |
| TC-RAG-08 | Apply retrieval diversity | One document does not excessively dominate retrieved results | As expected | PASS |
| TC-RAG-09 | Handle conflicting information | Conflicting information is identified rather than arbitrarily selecting one source | As expected | PASS |

---

# 7. API Test Cases

## 7.1 Document Upload

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-UP-01 | Upload valid PDF | PDF is accepted and indexed | As expected | PASS |
| TC-UP-02 | Upload non-PDF file | Request is rejected | As expected | PASS |
| TC-UP-03 | Upload invalid PDF | Request is rejected | As expected | PASS |
| TC-UP-04 | Upload file larger than 20 MB | Request is rejected with file-size error | As expected | PASS |
| TC-UP-05 | Upload duplicate document | Duplicate upload is rejected | As expected | PASS |
| TC-UP-06 | Upload different PDFs with same filename | Documents are treated independently | As expected | PASS |

---

## 7.2 Document Management

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-DM-01 | List documents | Uploaded documents are returned | As expected | PASS |
| TC-DM-02 | View document | Requested PDF is returned | As expected | PASS |
| TC-DM-03 | View nonexistent document | 404 error is returned | As expected | PASS |
| TC-DM-04 | Delete document | Document and associated vectors are removed | As expected | PASS |
| TC-DM-05 | Delete nonexistent document | 404 error is returned | As expected | PASS |

---

## 7.3 Query API

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-Q-01 | Submit valid question | Answer and sources are returned | As expected | PASS |
| TC-Q-02 | Submit empty question | 400 error is returned | As expected | PASS |
| TC-Q-03 | Submit whitespace-only question | 400 error is returned | As expected | PASS |
| TC-Q-04 | Query without documents | Appropriate error is returned | As expected | PASS |

---

# 8. End-to-End Test Cases

The following scenarios are used to verify the complete application workflow through the frontend.

| ID | Scenario | Expected Behaviour | Status |
|---|---|---|---|
| E2E-01 | Start application and upload PDF | PDF is uploaded and indexed | PASS |
| E2E-02 | Upload multiple PDFs | All selected PDFs are processed independently | PASS |
| E2E-03 | Ask a question about an uploaded document | Relevant answer is generated | PASS |
| E2E-04 | Verify answer sources | Document and page references are displayed | PASS |
| E2E-05 | Ask unsupported question | System avoids generating an unsupported answer | PASS |
| E2E-06 | Select specific documents | Query is restricted to selected documents | PASS |
| E2E-07 | Upload duplicate PDF | Duplicate upload is rejected | PASS |
| E2E-08 | Delete a document | Document is removed from the collection | PASS |
| E2E-09 | Restart backend | Previously indexed documents remain available | PASS |
| E2E-10 | Query after restart | Persisted index remains usable | PASS |

---

# 9. Edge Case Testing

| ID | Edge Case | Expected Behaviour | Status |
|---|---|---|---|
| EC-01 | Empty PDF | System indicates that no extractable text is available | PASS |
| EC-02 | Corrupt PDF | Processing failure is handled without crashing the application | PENDING |
| EC-03 | Scanned/image-only PDF | System indicates that no extractable text is available | PENDING |
| EC-04 | PDF containing images with text | Text content is processed; images are not interpreted | PASS |
| EC-05 | Unsupported file type | Upload is rejected | PASS |
| EC-06 | File larger than 20 MB | Upload is rejected | PASS |
| EC-07 | Duplicate document content | Duplicate upload is rejected | PASS |
| EC-08 | Same filename with different content | Both documents are retained independently | PASS |
| EC-09 | Unknown question | System does not invent an answer | PASS |
| EC-10 | Conflicting documents | Conflicting information is identified | PASS |
| EC-11 | Multiple documents | Relevant information can be retrieved from multiple documents | PASS |
| EC-12 | Document-specific query | Only selected documents are searched | PASS |
| EC-13 | Document deletion | Associated vectors are removed | PASS |
| EC-14 | Backend restart | Persisted index remains available | PASS |
| EC-15 | Broad document-summary question | Response focuses on the main subject of the document | PENDING |

---

# 10. Test Execution

Automated tests are executed using Pytest.

### Command

```bash
pytest -v
```


# 11. Defects and Observations

## 11.1 Retrieval Noise

Semantic retrieval may occasionally return incidental sections such as indexes, acknowledgements, references, or copyright information, particularly for broad questions.

### Handling

The system uses:

- A relevance threshold
- Retrieval diversity
- Document-scoped retrieval
- Prompt-level instructions to ignore irrelevant retrieved excerpts

---

## 11.2 Document Dominance

When multiple documents are indexed, several highly similar chunks from one document may otherwise dominate the retrieval results.

### Handling

The retrieval layer limits the number of chunks contributed by the same document.

---

## 11.3 Production-Scale Retrieval

The current implementation uses a local FAISS index.

For a production deployment, metadata-filtered vector search, reranking, and scalable vector storage would be introduced.

---

# 12. Testing Limitations

The following limitations apply to the current testing scope:

- Testing is primarily performed in a local development environment.
- The current system processes text-based PDFs and does not perform OCR on scanned documents.
- LLM-based answer generation depends on the configured Gemini API.
- Large-scale performance and distributed-load testing are outside the current MVP scope.
- Authentication and multi-user isolation are not part of the current implementation.
- Production infrastructure such as distributed vector databases, queues, worker pools, and object storage is represented in the system-design documentation but is not implemented in the current local MVP.

---

# 13. Conclusion

The testing process verifies the major functional components of the **AI-Powered Document Q&A System**.

Testing covers document ingestion, text extraction, chunking, embedding generation, semantic retrieval, vector storage, persistence, RAG-based question answering, source attribution, multi-document handling, duplicate detection, document scoping, upload validation, and document management.

The combination of automated unit/API tests and manual end-to-end testing provides coverage of both individual components and the complete application workflow.

Further performance and scalability testing would be required before deployment in a production-scale distributed environment.

---

# 14. Test Artifacts

The automated test suite is organized as follows:

```text
tests/
├── test_document_processor.py
├── test_chunker.py
├── test_embeddings.py
├── test_similarity.py
├── test_vector_store.py
├── test_rag_pipeline.py
├── test_upload_validation.py
├── test_document_management.py
└── test_query_api.py
```