from backend.chunker import chunk_pages

def test_chunk_pages():
    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        overlap=200
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert "text" in chunk
        assert "page_number" in chunk
        assert chunk["page_number"] == 1