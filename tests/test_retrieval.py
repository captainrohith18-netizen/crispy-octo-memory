import numpy as np

from core.chunker import Chunk
from core.retriever import retrieve_top_k


def test_retrieve_top_k_returns_best_chunk():
    chunks = [
        Chunk(chunk_id="a", text="The syllabus lists graduation requirements.", source="doc.pdf"),
        Chunk(chunk_id="b", text="The meeting time is 10 AM on Tuesday.", source="doc.pdf"),
    ]
    query_vector = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    chunk_vectors = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ], dtype=np.float32)

    results = retrieve_top_k(query_vector, chunk_vectors, chunks, k=1, min_score=0.0)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "a"
    assert "metadata" in results[0]
    assert results[0]["metadata"]["source"] == "doc.pdf"
