import pymupdf
from backend.document_processor import extract_text_from_pdf

def create_test_pdf(path):
    document = pymupdf.open()

    page1 = document.new_page()
    page1.insert_text((50, 50), "This is page one.")

    page2 = document.new_page()
    page2.insert_text((50, 50), "This is page two.")

    document.save(path)
    document.close()

def test_extract_text_from_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    create_test_pdf(str(pdf_path))
    pages = extract_text_from_pdf(str(pdf_path))

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert pages[1]["page_number"] == 2
    assert "page one" in pages[0]["text"]
    assert "page two" in pages[1]["text"]