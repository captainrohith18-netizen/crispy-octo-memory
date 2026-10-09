# crispy-octo-memory

A local document Q&A app powered by Ollama and a retrieval pipeline. This project is a beginner-friendly local RAG (Retrieval-Augmented Generation) application designed for workshop use. It lets users upload a PDF or DOCX file, extract text, split it into meaningful chunks, generate local embeddings, retrieve the most relevant chunks using cosine similarity, and pass the retrieved context into a locally running Ollama model.

## Why this project exists

The goal is to teach the actual pipeline behind modern AI document Q&A systems without relying on paid APIs or cloud services.

The conceptual flow is:

Document → Extract → Clean → Chunk → Embed → Compare → Retrieve → Context → LLM → Answer

## Technology stack

- Python 3.11
- Streamlit for the UI
- PyMuPDF for PDF extraction
- python-docx for DOCX extraction
- Sentence Transformers for local embeddings
- NumPy + scikit-learn for cosine similarity
- Ollama for local model execution
- Requests for API communication

## RAG concept explained simply

A document is not sent to the model as one giant block. Instead:

1. The text is extracted.
2. The text is split into useful chunks.
3. Each chunk is turned into a vector embedding.
4. The question is also converted to an embedding.
5. Cosine similarity measures which chunks are most semantically similar to the question.
6. The best chunks are retrieved.
7. Only that retrieved context is sent to the LLM.
8. The model answers using the supplied document evidence.

This is why the system is called retrieval-augmented generation: retrieval happens before generation.

## Project structure

```text
rag_workshop/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── model_selector.py
│   ├── ollama_client.py
│   └── rag_pipeline.py
├── ui/
│   ├── components.py
│   └── styles.py
├── data/
│   ├── demo/
│   └── uploads/
├── scripts/
│   ├── generate_demo_documents.py
│   └── package_classroom_bundle.py
├── tests/
│   ├── test_chunking.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   ├── test_model_selection.py
│   └── test_document_loader.py
└── dist/
```

## Local installation

```bash
cd rag_workshop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Demo document generation

The project includes a demo generator script that creates a ready-to-use sample syllabus in both DOCX and PDF formats.

```bash
cd rag_workshop
python3 scripts/generate_demo_documents.py
```

This creates:

- `data/demo/college_syllabus_demo.docx`
- `data/demo/college_syllabus_demo.pdf`

## Ollama installation and setup

### Install Ollama

Follow the official instructions for your OS:

- macOS: `brew install ollama`
- Linux: use the official installer script
- Windows: use the official Windows installer

Start the server:

```bash
ollama serve
```

## Model installation

Primary preference: Qwen

```bash
ollama pull qwen:latest
```

Fallback: Llama

```bash
ollama pull llama3.2:latest
```

The application checks the local Ollama API and automatically prefers Qwen when available. If Qwen is not installed, it uses a compatible Llama model if one is installed.

## Run the app

```bash
streamlit run app.py
```

## Package for classroom distribution

A zip bundle can be generated for workshop delivery with:

```bash
cd rag_workshop
python3 scripts/package_classroom_bundle.py
```

This creates a distributable archive in `dist/rag_workshop_classroom_bundle.zip`.

## Example workshop questions

- What are the eligibility requirements?
- Summarize the key deadlines mentioned in the document.
- Which sections discuss assessment criteria?
- What are the required materials or prerequisites?
- What is not mentioned in the uploaded document?

## Demo workflow

1. Upload a syllabus or policy PDF/DOCX.
2. Observe the extracted text and chunk count.
3. Ask a natural-language question.
4. Inspect the retrieved chunks and similarity scores.
5. Observe the answer from the local Ollama model.
6. Verify that the answer is grounded in the document context.

## Model policy

The project uses a single educational policy:

- Prefer local Qwen if installed.
- Fallback to local Llama if Qwen is unavailable.
- If neither model is installed, show a clear setup message instead of crashing.

## Troubleshooting

- If Ollama responds with a connection error, run `ollama serve`.
- If the model is missing, install it with `ollama pull qwen:latest` or `ollama pull llama3.2:latest`.
- If a PDF is empty or image-only, no meaningful text may be extracted.
- If a DOCX file has no paragraphs, the app will show a clear message.
- If no chunk matches the question, the app will say that no relevant context was found.

## Important teaching points

- Embeddings capture semantic meaning rather than exact keyword matching.
- Cosine similarity measures directional similarity between vectors.
- Retrieval is separate from generation.
- The LLM should not invent unsupported facts.
- The retrieved context is treated as reference data, not as a system instruction.

## Final note

This implementation is designed to be simple, reproducible, and classroom-friendly. It focuses on the core mechanics of local RAG without adding unnecessary complexity.
