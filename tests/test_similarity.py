import numpy as np

from backend.embeddings import EmbeddingModel


def test_similar_sentences_have_higher_similarity():
    model = EmbeddingModel()

    embeddings = model.encode([
        "The employee receives a monthly stipend.",
        "The employee is paid a monthly stipend.",
        "The weather is sunny today."
    ])

    similarity_related = np.dot(
        embeddings[0],
        embeddings[1]
    )

    similarity_unrelated = np.dot(
        embeddings[0],
        embeddings[2]
    )

    assert similarity_related > similarity_unrelated