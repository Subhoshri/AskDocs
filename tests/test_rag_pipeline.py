def test_rag_pipeline_retrieval(monkeypatch):
    from backend.rag_pipeline import RAGPipeline

    pipeline = RAGPipeline()

    pipeline.retrieve = lambda question, top_k=5, document_ids=None: [
        {
            "score": 0.8,
            "metadata": {
                "document_id": "doc1",
                "filename": "test.pdf",
                "page_number": 1,
                "text": "The stipend is 40000 rupees."
            }
        }
    ]

    class FakeGenerator:
        def generate(self, question, retrieved_chunks):
            return "The stipend is 40000 rupees."

    pipeline.answer_generator = FakeGenerator()

    answer, results = pipeline.answer(
        "What is the stipend?"
    )

    assert "40000" in answer
    assert len(results) == 1