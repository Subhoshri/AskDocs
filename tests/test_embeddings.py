from backend.embeddings import EmbeddingModel


def test_embedding_dimension():
    model = EmbeddingModel()

    embeddings = model.encode(
        ["This is a test sentence."]
    )

    assert embeddings.shape[0] == 1
    assert embeddings.shape[1] == 384


def test_embedding_normalized():
    import numpy as np

    model = EmbeddingModel()

    embeddings = model.encode(
        ["This is a test sentence."]
    )

    norm = np.linalg.norm(embeddings[0])

    assert np.isclose(norm, 1.0, atol=1e-5)


def test_multiple_embeddings():
    model = EmbeddingModel()

    embeddings = model.encode([
        "First sentence.",
        "Second sentence.",
        "Third sentence."
    ])

    assert embeddings.shape == (3, 384)