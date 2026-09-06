from document_processor import extract_text_from_pdf
from chunker import chunk_pages
from embeddings import EmbeddingModel
from vector_store import VectorStore

class RAGPipeline:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = None

    def index_document(self, file_path, document_id, filename):
        """
        Process a PDF and add its chunks to the vector store.
        """

        # 1. Extract text
        pages = extract_text_from_pdf(file_path)

        # 2. Create chunks
        chunks = chunk_pages(pages)

        # 3. Add metadata
        for index, chunk in enumerate(chunks):
            chunk["document_id"] = document_id
            chunk["chunk_id"] = f"{document_id}_{index}"
            chunk["filename"] = filename

        # 4. Extract text for embedding
        texts = [chunk["text"] for chunk in chunks]

        # 5. Generate embeddings
        embeddings = self.embedding_model.encode(texts)

        # 6. Initialize vector store if necessary
        if self.vector_store is None:
            dimension = embeddings.shape[1]
            self.vector_store = VectorStore(dimension)

        # 7. Add vectors + metadata
        self.vector_store.add(
            embeddings,
            chunks
        )

        return len(chunks)

    def retrieve(self, question, top_k=5):
        """
        Retrieve the most relevant chunks for a question.
        """

        query_embedding = self.embedding_model.encode(
            [question]
        )[0]

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results