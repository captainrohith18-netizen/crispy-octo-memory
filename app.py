from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.model_selector import resolve_ollama_model
from core.ollama_client import check_ollama_connection
from core.rag_pipeline import RAGPipeline
from ui.components import metric_card, render_status_chip
from ui.styles import CSS

st.set_page_config(page_title="Local RAG Workshop", page_icon="📚", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
st.markdown('<div class="app-shell">', unsafe_allow_html=True)


def ensure_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = RAGPipeline()
    if "document_summary" not in st.session_state:
        st.session_state.document_summary = None


ensure_session_state()

if "model_state" not in st.session_state:
    st.session_state.model_state = resolve_ollama_model()

model_state = st.session_state.model_state
ollama_connected = check_ollama_connection()

with st.sidebar:
    st.markdown("<div class='sidebar-panel'>", unsafe_allow_html=True)
    st.header("Settings")
    top_k = st.slider("Top-K", min_value=1, max_value=8, value=3)
    min_score = st.slider("Minimum similarity", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
    chunk_size = st.slider("Chunk size", min_value=100, max_value=600, value=250, step=50)
    overlap = st.slider("Chunk overlap", min_value=10, max_value=200, value=50, step=10)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.05)

    if st.button("Refresh model status", use_container_width=True):
        st.session_state.model_state = resolve_ollama_model()
        st.rerun()

    st.markdown("### Troubleshooting")
    if not ollama_connected:
        st.warning("Ollama is not running. Start it with: `ollama serve`.")
    if not model_state.get("model"):
        st.warning(model_state.get("message", "No local Qwen/Llama model was detected."))
    st.markdown("</div>", unsafe_allow_html=True)

header_col, model_col, status_col = st.columns([2.5, 1.1, 1.1])
with header_col:
    st.markdown(
        """
        <div class="brand-card">
            <div class="eyebrow">Document Intelligence</div>
            <div class="big-title">Local RAG Workshop</div>
            <div class="subtitle">PDF/DOCX → extract → chunk → embed → retrieve → ground → answer</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with model_col:
    if model_state.get("model"):
        render_status_chip(f"Model: {model_state['model']}", is_ok=True)
    else:
        render_status_chip("Model: unavailable", is_ok=False)
with status_col:
    render_status_chip("Connected" if ollama_connected else "Not Connected", is_ok=ollama_connected, warning=not ollama_connected)

metrics = st.columns(4)
with metrics[0]:
    metric_card("Documents", str(1 if st.session_state.document_summary else 0))
with metrics[1]:
    metric_card("Pages", str(st.session_state.document_summary["page_count"] if st.session_state.document_summary else "-"))
with metrics[2]:
    metric_card("Chunks", str(st.session_state.document_summary["chunk_count"] if st.session_state.document_summary else "-"))
with metrics[3]:
    metric_card("Model", model_state.get("model") or "Unavailable")

upload_col, guide_col = st.columns([1.5, 1])

with upload_col:
    st.markdown("<div class='panel-card'><div class='panel-title'>Document Upload</div></div>", unsafe_allow_html=True)
    sample_doc = Path("data/demo/college_syllabus_demo.docx")
    if sample_doc.exists():
        if st.button("Load sample workshop document", use_container_width=True):
            with st.spinner("Loading the built-in demo document..."):
                st.session_state.pipeline.chunk_size = chunk_size
                st.session_state.pipeline.overlap = overlap
                st.session_state.pipeline.top_k = top_k
                st.session_state.pipeline.min_score = min_score
                try:
                    summary = st.session_state.pipeline.index_document(sample_doc)
                    st.session_state.document_summary = summary
                    st.success(f"Loaded demo document: {summary['document_name']}")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Sample document could not be loaded: {exc}")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"], help="Supported formats: PDF and DOCX")
    if uploaded_file is not None:
        target_dir = Path("data/uploads")
        target_dir.mkdir(parents=True, exist_ok=True)
        save_path = target_dir / uploaded_file.name
        save_path.write_bytes(uploaded_file.getvalue())

        with st.spinner("Extracting text, chunking, and generating local embeddings..."):
            st.session_state.pipeline.chunk_size = chunk_size
            st.session_state.pipeline.overlap = overlap
            st.session_state.pipeline.top_k = top_k
            st.session_state.pipeline.min_score = min_score
            try:
                document_summary = st.session_state.pipeline.index_document(save_path)
                st.session_state.document_summary = document_summary
                st.success(f"Indexed {document_summary['document_name']} successfully.")
            except Exception as exc:
                st.error(f"Document processing failed: {exc}")
                st.session_state.document_summary = None

with guide_col:
    st.markdown(
        """
        <div class='panel-card'>
            <div class='panel-title'>Workshop Flow</div>
            <div class='mini-list'>
                <div>1. Upload a document</div>
                <div>2. Extract and clean text</div>
                <div>3. Chunk and embed</div>
                <div>4. Retrieve relevant context</div>
                <div>5. Answer using Ollama</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.document_summary:
    st.markdown("<div class='panel-card'><div class='panel-title'>Knowledge Base / Index Status</div></div>", unsafe_allow_html=True)
    detail_cols = st.columns(4)
    with detail_cols[0]:
        metric_card("Document", st.session_state.document_summary["document_name"])
    with detail_cols[1]:
        metric_card("Pages", str(st.session_state.document_summary["page_count"]))
    with detail_cols[2]:
        metric_card("Chunks", str(st.session_state.document_summary["chunk_count"]))
    with detail_cols[3]:
        metric_card("Characters", f"{st.session_state.document_summary['char_count']:,}")

    st.caption(f"Embedding status: {'Ready' if st.session_state.pipeline.chunk_vectors.size else 'Not ready'}")
    st.caption(f"Retrieval status: {'Ready' if st.session_state.document_summary.get('indexed') else 'Not indexed'}")

st.markdown("<div class='panel-card'><div class='panel-title'>Chat</div></div>", unsafe_allow_html=True)
chat_actions = st.columns([1, 4])
with chat_actions[0]:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the uploaded document")
if prompt:
    if not st.session_state.document_summary:
        st.warning("Please upload a document before asking a question.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            result = st.session_state.pipeline.answer_question(
                prompt,
                top_k=top_k,
                min_score=min_score,
                temperature=temperature,
            )
            answer = result["answer"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

            if result.get("retrieved_chunks"):
                with st.expander("View Retrieved Context"):
                    for item in result["retrieved_chunks"]:
                        metadata = item.get("metadata", {})
                        source_label = f"Chunk {item['chunk_id']} | Source: {item['source']}"
                        if item.get("page_number") is not None:
                            source_label += f" | Page {item['page_number']}"
                        source_label += f" | Similarity: {item['score']:.3f}"
                        if metadata.get("word_count") is not None:
                            source_label += f" | Words: {metadata['word_count']}"
                        if metadata.get("char_count") is not None:
                            source_label += f" | Chars: {metadata['char_count']}"
                        st.markdown(f"**{source_label}**")
                        st.code(item["text"], language="text")
            else:
                st.info("No relevant chunks passed the similarity threshold.")
        except Exception as exc:
            error_message = "The system could not answer the question because no relevant context was found or the model is unavailable."
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            with st.chat_message("assistant"):
                st.markdown(error_message)
            st.warning(str(exc))

if not st.session_state.messages:
    st.info("Upload a PDF or DOCX and ask a question about the content to begin the workshop demo.")

st.markdown('</div>', unsafe_allow_html=True)
