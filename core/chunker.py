from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional

from core.text_cleaner import clean_text


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    page_number: Optional[int] = None
    metadata: dict | None = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source": self.source,
            "page_number": self.page_number,
            "metadata": self.metadata or {},
            "start_char": self.start_char,
            "end_char": self.end_char,
        }


def _split_words(text: str) -> list[str]:
    return [word for word in text.split() if word]


def _chunk_words(words: list[str], chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0:
        raise ValueError("overlap must be zero or greater")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size

    chunks: list[str] = []
    for start in range(0, len(words), step):
        end = start + chunk_size
        segment = words[start:end]
        if not segment:
            break
        chunks.append(" ".join(segment))
        if end >= len(words):
            break
    return chunks


def chunk_document(
    text: str,
    source_name: str,
    page_texts: Optional[list[str]] = None,
    chunk_size: int = 300,
    overlap: int = 60,
) -> list[Chunk]:
    """Split a document into overlapping chunks with page metadata when available."""
    cleaned = clean_text(text)
    if not cleaned:
        return []

    def build_chunk_records(page_clean: str, page_number: Optional[int]) -> list[Chunk]:
        words = _split_words(page_clean)
        page_chunks = _chunk_words(words, chunk_size=chunk_size, overlap=overlap)
        records: list[Chunk] = []
        running_char_index = 0
        for index, part in enumerate(page_chunks):
            chunk_id = f"{source_name}__p{page_number}__c{index + 1}" if page_number else f"{source_name}__c{index + 1}"
            start_char = running_char_index
            end_char = running_char_index + len(part)
            records.append(
                Chunk(
                    chunk_id=chunk_id,
                    text=part,
                    source=source_name,
                    page_number=page_number,
                    metadata={
                        "page_number": page_number,
                        "word_count": len(_split_words(part)),
                        "char_count": len(part),
                        "chunk_index": index + 1,
                    },
                    start_char=start_char,
                    end_char=end_char,
                )
            )
            running_char_index = end_char - max(1, int(overlap * 1.5))
        return records

    chunks: list[Chunk] = []
    if page_texts and len(page_texts) > 0:
        for page_number, page_text in enumerate(page_texts, start=1):
            page_clean = clean_text(page_text)
            if not page_clean:
                continue
            chunks.extend(build_chunk_records(page_clean, page_number))
        return chunks

    chunks = build_chunk_records(cleaned, None)
    return chunks
