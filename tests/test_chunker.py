from backend.chunker import chunk_pages


def test_chunking():
    pages = [
        {
            "page_number": 1,
            "text": "a" * 2500
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        overlap=200
    )

    assert len(chunks) > 1
    assert all(
        "text" in chunk and
        "page_number" in chunk
        for chunk in chunks
    )


def test_short_text():
    pages = [
        {
            "page_number": 1,
            "text": "Short document."
        }
    ]

    chunks = chunk_pages(pages)

    assert len(chunks) == 1
    assert chunks[0]["text"] == "Short document."


def test_page_number_preserved():
    pages = [
        {
            "page_number": 3,
            "text": "Some content."
        }
    ]

    chunks = chunk_pages(pages)

    assert chunks[0]["page_number"] == 3