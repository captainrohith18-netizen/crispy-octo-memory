import numpy as np

from core.embeddings import embed_texts


def test_embed_texts_returns_normalized_vectors():
    vectors = embed_texts(["alpha beta gamma", "delta epsilon zeta"])
    assert vectors.shape[0] == 2
    norms = np.linalg.norm(vectors, axis=1)
    assert np.allclose(norms, np.ones_like(norms), atol=1e-5)
