from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from core.chunker import chunk_document
from core.document_loader import extract_document_text
from core.embeddings import embed_query, embed_texts
from core.model_selector import resolve_ollama_model
from core.ollama_client import generate_ollama_reply
from core.retriever import retrieve_top_k
from core.text_cleaner import normalize_question


class RAGPipeline:
    """A minimal but educational RAG pipeline for a workshop demo."""

    def __init__(self, chunk_size: int = 250, overlap: int = 50, top_k: int = 3, min_score: float = 0.05):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.top_k = top_k
        self.min_score = min_score
        self.document_name = None
        self.chunks = []
        self.chunk_vectors = np.empty((0, 0), dtype=np.float32)
        self.document_metadata = {}

    def index_document(self, file_path: str | Path) -> dict:
        file_path = Path(file_path)
        payload = extract_document_text(file_path)
        self.document_name = payload["filename"]
        self.document_metadata = {
            "filename": payload["filename"],
            "file_type": payload["file_type"],
            "page_count": payload["page_count"],
            "char_count": payload["char_count"],
        }

        cleaned_text = payload["text"]
        page_texts = payload.get("pages") or [cleaned_text]
        self.chunks = chunk_document(
            cleaned_text,
            source_name=payload["filename"],
            page_texts=page_texts,
            chunk_size=self.chunk_size,
            overlap=self.overlap,
        )

        if self.chunks:
            self.chunk_vectors = embed_texts([chunk.text for chunk in self.chunks])
        else:
            self.chunk_vectors = np.empty((0, 0), dtype=np.float32)

        return {
            "document_name": self.document_name,
            "chunk_count": len(self.chunks),
            "char_count": payload["char_count"],
            "page_count": payload["page_count"],
            "indexed": bool(self.chunks),
        }

    def answer_question(self, question: str, top_k: int | None = None, min_score: float | None = None, temperature: float = 0.1):
        cleaned_question = normalize_question(question)
        if not cleaned_question:
            raise ValueError("Please enter a valid question.")
        if not self.chunks:
            raise ValueError("No document has been indexed yet. Please upload a PDF or DOCX first.")

        query_vector = embed_query(cleaned_question)
        selected_k = top_k or self.top_k
        selected_threshold = self.min_score if min_score is None else min_score

        results = retrieve_top_k(
            query_vector=query_vector,
            chunk_vectors=self.chunk_vectors,
            chunks=self.chunks,
            k=selected_k,
            min_score=selected_threshold,
        )

        for item in results:
            item["metadata"] = {
                **(item.get("metadata") or {}),
                "document_name": self.document_name,
                "retrieved_for": cleaned_question,
                "similarity_score": item["score"],
                "top_k": selected_k,
            }

        if not results:
            return {
                "answer": "No relevant information was found in the uploaded document for that question. Please ask a question related to the document content.",
                "retrieved_chunks": [],
                "used_model": None,
                "model_status": {"model": None, "message": "No matching document context was retrieved."},
            }

        context_parts = []
        for item in results:
            source_label = f"Source: {item['source']}"
            if item.get("page_number") is not None:
                source_label += f" | Page {item['page_number']}"
            source_label += f" | Similarity: {item['score']:.3f}"
            context_parts.append(f"{source_label}\n{item['text']}")

        context_text = "\n\n---\n\n".join(context_parts)
        model_info = resolve_ollama_model()
        if not model_info.get("model"):
            return {
                "answer": model_info.get("message", "No compatible Ollama model was found."),
                "retrieved_chunks": results,
                "used_model": None,
                "model_status": model_info,
            }

        answer = generate_ollama_reply(cleaned_question, context_text, model_info["model"], temperature=temperature)
        return {
            "answer": answer,
            "retrieved_chunks": results,
            "used_model": model_info["model"],
            "model_status": model_info,
        }
