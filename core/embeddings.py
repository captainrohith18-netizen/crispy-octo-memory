from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np


@lru_cache(maxsize=1)
def get_sentence_transformer():
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2", device="cpu")
    except Exception:
        return None


def normalize_embeddings(matrix: np.ndarray) -> np.ndarray:
    """Normalize embedding vectors to unit length for cosine similarity."""
    matrix = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def _hash_fallback_embedding(text: str, dimensions: int = 384) -> np.ndarray:
    """A lightweight local fallback when an embedding model is unavailable."""
    tokens = text.lower().split()
    vector = np.zeros(dimensions, dtype=np.float32)
    for idx, token in enumerate(tokens):
        value = abs(hash(token)) % dimensions
        vector[value] += 1.0 + (idx % 7) * 0.05
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def embed_texts(texts: Iterable[str], model_name: str = "sentence-transformers/paraphrase-MiniLM-L6-v2") -> np.ndarray:
    """Generate embeddings for a list of texts using the local sentence-transformer if available."""
    text_list = [text for text in texts if text and text.strip()]
    if not text_list:
        return np.empty((0, 0), dtype=np.float32)

    encoder = get_sentence_transformer()
    if encoder is not None:
        vectors = encoder.encode(text_list, convert_to_numpy=True, normalize_embeddings=True)
        return np.asarray(vectors, dtype=np.float32)

    vectors = np.vstack([_hash_fallback_embedding(text) for text in text_list])
    return normalize_embeddings(vectors)


def embed_query(question: str) -> np.ndarray:
    """Generate a single embedding for a question."""
    return embed_texts([question])[0]
