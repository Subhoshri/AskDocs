import faiss
import numpy as np
import json
from pathlib import Path


class VectorStore:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []

    def add(self, embeddings, metadata):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5):

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            results.append({
                "score": float(score),
                "metadata": self.metadata[index]
            })

        return results

    def save(self, index_path, metadata_path):

        faiss.write_index(
            self.index,
            str(index_path)
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2
            )

    @classmethod
    def load(cls, index_path, metadata_path):

        index = faiss.read_index(
            str(index_path)
        )

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        vector_store = cls(index.d)

        vector_store.index = index
        vector_store.metadata = metadata

        return vector_store

    def delete_document(self, document_id):

        keep_indices = [
            i
            for i, metadata in enumerate(self.metadata)
            if metadata["document_id"] != document_id
        ]
    
        if len(keep_indices) == len(self.metadata):
            return False
    
        # Reconstruct vectors we want to keep
        if keep_indices:
            vectors = np.vstack([
                self.index.reconstruct(i)
                for i in keep_indices
            ])
    
            new_index = faiss.IndexFlatIP(self.index.d)
    
            new_index.add(
                vectors.astype("float32")
            )
    
        else:
            new_index = faiss.IndexFlatIP(self.index.d)
    
        self.index = new_index
    
        self.metadata = [
            self.metadata[i]
            for i in keep_indices
        ]
    
        return True