from core.chunker import chunk_document


def test_chunk_document_creates_multiple_chunks():
    text = " ".join([f"Sentence {index} explains a concept for workshop learning." for index in range(1, 40)])
    chunks = chunk_document(text, source_name="demo.pdf", chunk_size=12, overlap=3)
    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
    assert chunks[0].source == "demo.pdf"


def test_chunk_document_handles_empty_text():
    chunks = chunk_document("", source_name="empty.pdf", chunk_size=10, overlap=2)
    assert chunks == []
