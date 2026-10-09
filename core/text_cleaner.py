import re


def clean_text(raw_text: str) -> str:
    """Normalize extracted document text while preserving meaningful structure."""
    if raw_text is None:
        return ""

    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = "".join(ch for ch in text if ch not in {"\x00", "\x01", "\x02", "\x03"})
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = text.strip()
    return text


def normalize_question(question: str) -> str:
    """Prepare a user query for embedding and retrieval generation."""
    if not question:
        return ""
    cleaned = clean_text(question)
    return " ".join(cleaned.split())
