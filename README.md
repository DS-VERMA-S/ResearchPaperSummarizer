# Research Paper RAG Agent

A FastAPI-based Retrieval Augmented Generation (RAG) service that ingests a research PDF and produces:

- Structured analysis: new knowledge/findings, deeper interpretation, gaps/limitations, and practical applications
- Concise summary of the paper
- New research ideas with novelty/feasibility scores

Embeddings and generation use OpenAI APIs.

## Setup

1. Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

- `OPENAI_API_KEY` (required)
- Optional: `OPENAI_MODEL` (default: `gpt-4o-mini`)
- Optional: `EMBEDDING_API_MODEL` (default: `text-embedding-3-small`)

## Run the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs` for Swagger UI.

## Endpoints

- `GET /health` – health check
- `POST /analyze` – multipart file upload for a PDF; returns structured JSON analysis with citations

## CLI

```bash
python app/analyze_paper.py /path/to/paper.pdf --output result.json
```

Outputs a JSON file with the same structure as the API response.
