import os
from pathlib import Path
from .document_processor import extract_text_from_pdf
from .chunker import chunk_pages
from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .rag import AnswerGenerator

class RAGPipeline:
    def __init__(self):
        self.min_relevance_score = 0.35
        self.embedding_model = EmbeddingModel()

        self.index_path = Path("data/faiss.index")
        self.metadata_path = Path("data/metadata.json")

        self.vector_store = None

        # Load existing vector store if available
        if (
            self.index_path.exists()
            and self.metadata_path.exists()
        ):
            self.vector_store = VectorStore.load(
                self.index_path,
                self.metadata_path
            )

        # Initialize answer generator
        api_key = os.getenv("GEMINI_API_KEY")
        self.answer_generator = None

        if api_key:
            self.answer_generator = AnswerGenerator(api_key)

    def get_document_overview_chunks(self,document_ids=None,chunks_per_document=2):

        if self.vector_store is None:
            return []

        selected = []
        seen_documents = set()

        for metadata in self.vector_store.metadata:
            document_id = metadata["document_id"]

            if document_ids and document_id not in document_ids:
                continue

            if document_id in seen_documents:
                continue

            document_chunks = [
                item
                for item in self.vector_store.metadata
                if item["document_id"] == document_id
            ]

            document_chunks = sorted(
                document_chunks,
                key=lambda x: int(
                    x["chunk_id"].split("_")[-1]
                )
            )

            selected.extend(
                document_chunks[:chunks_per_document]
            )

            seen_documents.add(document_id)

        return [
            {
                "score": 1.0,
                "metadata": metadata
            }
            for metadata in selected
        ]

    def index_document(self,file_path,document_id,filename):
        pages = extract_text_from_pdf(file_path)
        chunks = chunk_pages(pages)

        if not chunks:
            raise ValueError(
                "No extractable text found in the PDF."
            )

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
            self.vector_store = VectorStore(dimension)

        # Add new document to existing collection
        self.vector_store.add(embeddings,chunks)

        # Persist updated collection
        self.vector_store.save(self.index_path,self.metadata_path)

        return len(chunks)

    def retrieve(self,question,top_k=5,document_ids=None):
        if self.vector_store is None:
            return []

        query_embedding = self.embedding_model.encode([question])[0]

        candidate_k = min(20,self.vector_store.index.ntotal)

        results = self.vector_store.search(query_embedding,top_k=candidate_k)

        if document_ids:

            results = [
                result
                for result in results
                if result["metadata"]["document_id"]
                in document_ids
            ]

        self.min_relevance_score
        results = [
        result
        for result in results
        if result["score"] >= self.min_relevance_score
        ]

        if not document_ids:
            document_counts = {}
            diversified_results = []

            for result in results:

                document_id = result["metadata"]["document_id"]

                count = document_counts.get(document_id,0)

                if count >= 2:
                    continue

                diversified_results.append(result)
                document_counts[document_id] = count + 1

            results = diversified_results

        return results[:top_k]

    def answer(self,question,top_k=5,document_ids=None):
        summary_keywords = [
            "what is this document about",
            "what is the document about",
            "summarize this document",
            "summarise this document",
            "summary of this document",
            "what does this document contain"
        ]

        is_summary_question = any(
            keyword in question.lower()
            for keyword in summary_keywords
        )

        if is_summary_question:
            retrieved_chunks = self.get_document_overview_chunks(
                document_ids=document_ids,
                chunks_per_document=2
            )

        else:
            retrieved_chunks = self.retrieve(
                question,
                top_k=top_k,
                document_ids=document_ids
            )

        if self.answer_generator is None:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        answer = self.answer_generator.generate(question,retrieved_chunks)

        return answer, retrieved_chunks

    def delete_document(self, document_id):
        if self.vector_store is None:
            return False

        deleted = self.vector_store.delete_document(document_id)

        if not deleted:
            return False

        self.vector_store.save(self.index_path,self.metadata_path)
        return True