from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
document_path = "../data/Cadence_Projects.pdf"

num_chunks = pipeline.index_document(
    file_path=document_path,
    document_id="doc_001",
    filename="sample.pdf"
)

print("Number of chunks indexed:", num_chunks)

question = "What is this document about?"

results = pipeline.retrieve(
    question,
    top_k=3
)

print("\nRetrieved results:")

for result in results:
    metadata = result["metadata"]

    print("\n-----------------------")
    print("Score:", result["score"])
    print("File:", metadata["filename"])
    print("Page:", metadata["page_number"])
    print("Chunk:", metadata["chunk_id"])
    print("Text:", metadata["text"][:300])