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