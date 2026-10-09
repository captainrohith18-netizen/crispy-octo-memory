from __future__ import annotations

from pathlib import Path

import fitz
from docx import Document

from core.text_cleaner import clean_text


def extract_pdf_text(file_path: str | Path) -> tuple[str, list[str], int]:
    """Extract text from a PDF, preserving page-level information when available."""
    pdf = fitz.open(file_path)
    pages: list[str] = []
    page_count = pdf.page_count
    try:
        for page_number in range(page_count):
            page = pdf[page_number]
            page_text = page.get_text("text")
            cleaned_page = clean_text(page_text)
            pages.append(cleaned_page)
    finally:
        pdf.close()

    full_text = "\n\n".join(pages)
    return clean_text(full_text), pages, page_count


def extract_docx_text(file_path: str | Path) -> tuple[str, list[str], int]:
    """Extract paragraphs from a DOCX file and return simple page-like segments."""
    doc = Document(str(file_path))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    cleaned_paragraphs = [clean_text(paragraph) for paragraph in paragraphs]
    full_text = "\n\n".join(cleaned_paragraphs)
    return clean_text(full_text), cleaned_paragraphs, max(1, len(cleaned_paragraphs))


def extract_document_text(file_path: str | Path) -> dict:
    """Return extracted text and metadata for a supported file format."""
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        full_text, pages, page_count = extract_pdf_text(file_path)
        return {
            "filename": file_path.name,
            "file_type": "pdf",
            "text": full_text,
            "pages": pages,
            "page_count": page_count,
            "char_count": len(full_text),
        }

    if suffix == ".docx":
        full_text, pages, page_count = extract_docx_text(file_path)
        return {
            "filename": file_path.name,
            "file_type": "docx",
            "text": full_text,
            "pages": pages,
            "page_count": page_count,
            "char_count": len(full_text),
        }

    raise ValueError(f"Unsupported file type: {suffix}. Please upload a PDF or DOCX.")
