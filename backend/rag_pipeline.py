import os

from .document_processor import extract_text_from_pdf
from .chunker import chunk_pages
from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .rag import AnswerGenerator


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()
        self.vector_store = None

        api_key = os.getenv("GEMINI_API_KEY")

        self.answer_generator = None

        if api_key:
            self.answer_generator = AnswerGenerator(api_key)

    def index_document(
        self,
        file_path,
        document_id,
        filename
    ):

        pages = extract_text_from_pdf(file_path)

        chunks = chunk_pages(pages)

        for index, chunk in enumerate(chunks):

            chunk["document_id"] = document_id
            chunk["chunk_id"] = f"{document_id}_{index}"
            chunk["filename"] = filename

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.encode(texts)

        if self.vector_store is None:

            dimension = embeddings.shape[1]

            self.vector_store = VectorStore(
                dimension
            )

        self.vector_store.add(
            embeddings,
            chunks
        )

        return len(chunks)

    def retrieve(
        self,
        question,
        top_k=5
    ):

        query_embedding = self.embedding_model.encode(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

    def answer(
        self,
        question,
        top_k=5
    ):

        retrieved_chunks = self.retrieve(
            question,
            top_k=top_k
        )

        if self.answer_generator is None:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        answer = self.answer_generator.generate(
            question,
            retrieved_chunks
        )

        return answer, retrieved_chunks