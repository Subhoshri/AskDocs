from backend.document_processor import extract_text_from_pdf


def test_extract_text_from_valid_pdf(tmp_path):
    import fitz

    pdf_path = tmp_path / "sample.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (50, 50),
        "This is a test document."
    )
    doc.save(pdf_path)
    doc.close()

    pages = extract_text_from_pdf(str(pdf_path))

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "test document" in pages[0]["text"]


def test_empty_pdf(tmp_path):
    import fitz

    pdf_path = tmp_path / "empty.pdf"

    doc = fitz.open()
    doc.new_page()
    doc.save(pdf_path)
    doc.close()

    pages = extract_text_from_pdf(str(pdf_path))

    assert pages == []