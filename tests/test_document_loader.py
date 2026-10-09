import fitz

from core.document_loader import extract_pdf_text


def test_extract_pdf_text_returns_page_count_after_closing_document(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "PDF extraction works")
    document.save(pdf_path)
    document.close()

    text, pages, page_count = extract_pdf_text(pdf_path)

    assert "PDF extraction works" in text
    assert len(pages) == 1
    assert page_count == 1


def test_rag_pipeline_resets_state_for_new_uploads(tmp_path):
    from core.rag_pipeline import RAGPipeline

    doc_one = tmp_path / "alpha.pdf"
    doc_two = tmp_path / "beta.pdf"

    for file_path, text in [
        (doc_one, "Alpha document for testing retrieval"),
        (doc_two, "Beta document for testing retrieval"),
    ]:
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), text)
        document.save(file_path)
        document.close()

    pipeline = RAGPipeline(chunk_size=80, overlap=10)
    multi_summary = pipeline.index_documents([doc_one, doc_two])
    assert multi_summary["document_count"] == 2
    assert len(pipeline.chunks) > 0

    single_summary = pipeline.index_document(doc_one)
    assert single_summary["document_count"] == 1
    assert single_summary["document_name"] == "alpha.pdf"
    assert pipeline.document_name == "alpha.pdf"


def test_rag_pipeline_rejects_unrelated_question(monkeypatch):
    import numpy as np

    from core.chunker import Chunk
    from core.rag_pipeline import RAGPipeline

    pipeline = RAGPipeline(chunk_size=80, overlap=10, min_score=0.0)
    pipeline.document_name = "report.pdf"
    pipeline.chunks = [
        Chunk(
            chunk_id="report__c1",
            text="Revenue grew by 18 percent in the quarterly earnings report.",
            source="report.pdf",
            page_number=1,
            metadata={"page_number": 1},
        )
    ]
    pipeline.chunk_vectors = np.array([[1.0, 0.0]], dtype=np.float32)

    monkeypatch.setattr("core.rag_pipeline.embed_query", lambda question: np.array([1.0, 0.0], dtype=np.float32))
    monkeypatch.setattr("core.rag_pipeline.resolve_ollama_model", lambda: {"model": "qwen", "message": "ok"})

    called = {"value": False}

    def fake_generate(question, context, model, temperature=0.1):
        called["value"] = True
        return "This should not be generated for an unrelated question."

    monkeypatch.setattr("core.rag_pipeline.generate_ollama_reply", fake_generate)

    result = pipeline.answer_question("What is the capital of France?", top_k=3, min_score=0.0)

    assert result["answer"] == "This question is not related to the uploaded document. Please ask a question based on the current document content."
    assert called["value"] is False