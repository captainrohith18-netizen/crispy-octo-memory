from __future__ import annotations

import numpy as np


def cosine_similarity(query_vector: np.ndarray, document_vectors: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between a query vector and each document vector."""
    q = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)
    docs = np.asarray(document_vectors, dtype=np.float32)
    if docs.size == 0:
        return np.asarray([], dtype=np.float32)
    q_norm = q / np.linalg.norm(q, axis=1, keepdims=True)
    docs_norm = docs / np.linalg.norm(docs, axis=1, keepdims=True)
    return np.clip((q_norm @ docs_norm.T).reshape(-1), -1.0, 1.0)


def retrieve_top_k(query_vector: np.ndarray, chunk_vectors: np.ndarray, chunks: list, k: int = 3, min_score: float = 0.0):
    """Return the highest-scoring chunks by cosine similarity."""
    if chunk_vectors.size == 0:
        return []

    scores = cosine_similarity(query_vector, chunk_vectors)
    ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)

    results = []
    for idx, score in ranked[:k]:
        if score < min_score:
            continue
        chunk = chunks[idx]
        metadata = dict(chunk.metadata or {})
        metadata.update(
            {
                "source": chunk.source,
                "chunk_id": chunk.chunk_id,
                "page_number": chunk.page_number,
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
            }
        )
        results.append(
            {
                "chunk_id": chunk.chunk_id,
                "source": chunk.source,
                "page_number": chunk.page_number,
                "score": float(score),
                "text": chunk.text,
                "metadata": metadata,
            }
        )
    return results
