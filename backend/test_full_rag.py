from .rag_pipeline import RAGPipeline


pipeline = RAGPipeline()


pipeline.index_document(
    file_path="data/Cadence_Projects.pdf",
    document_id="doc_001",
    filename="Cadence_Projects.pdf"
)


question = "What is this document about?"

results = pipeline.retrieve(
    question,
    top_k=3
)


print("\n================ RETRIEVED SOURCES ================\n")

for result in results:

    metadata = result["metadata"]

    print(
        f"Score: {result['score']:.3f}\n"
        f"Document: {metadata['filename']}\n"
        f"Page: {metadata['page_number']}\n"
        f"Chunk: {metadata['chunk_id']}\n"
        f"Text: {metadata['text'][:300]}\n"
    )