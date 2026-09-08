import numpy as np

from backend.vector_store import VectorStore


def test_add_vectors():
    store = VectorStore(3)

    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ], dtype="float32")

    metadata = [
        {
            "document_id": "doc1",
            "chunk_id": "doc1_0",
            "filename": "a.pdf",
            "page_number": 1,
            "text": "first"
        },
        {
            "document_id": "doc1",
            "chunk_id": "doc1_1",
            "filename": "a.pdf",
            "page_number": 2,
            "text": "second"
        }
    ]

    store.add(embeddings, metadata)

    assert store.index.ntotal == 2
    assert len(store.metadata) == 2


def test_search():
    store = VectorStore(3)

    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ], dtype="float32")

    metadata = [
        {
            "document_id": "doc1",
            "chunk_id": "doc1_0",
            "filename": "a.pdf",
            "page_number": 1,
            "text": "first"
        },
        {
            "document_id": "doc1",
            "chunk_id": "doc1_1",
            "filename": "a.pdf",
            "page_number": 2,
            "text": "second"
        }
    ]

    store.add(embeddings, metadata)

    results = store.search(
        np.array([1.0, 0.0, 0.0]),
        top_k=1
    )

    assert len(results) == 1
    assert results[0]["metadata"]["chunk_id"] == "doc1_0"


def test_delete_document():
    store = VectorStore(3)

    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype="float32")

    metadata = [
        {
            "document_id": "doc1",
            "chunk_id": "doc1_0"
        },
        {
            "document_id": "doc2",
            "chunk_id": "doc2_0"
        },
        {
            "document_id": "doc2",
            "chunk_id": "doc2_1"
        }
    ]

    store.add(embeddings, metadata)

    deleted = store.delete_document("doc2")

    assert deleted is True
    assert store.index.ntotal == 1
    assert len(store.metadata) == 1
    assert store.metadata[0]["document_id"] == "doc1"


def test_delete_nonexistent_document():
    store = VectorStore(3)

    deleted = store.delete_document("does-not-exist")

    assert deleted is False