from .document_processor import extract_text_from_pdf
from .chunker import chunk_pages

def process_document(file_path, document_id):
    pages = extract_text_from_pdf(file_path)

    chunks = chunk_pages(pages)

    for index, chunk in enumerate(chunks):
        chunk["document_id"] = document_id
        chunk["chunk_id"] = f"{document_id}_{index}"

    return chunks