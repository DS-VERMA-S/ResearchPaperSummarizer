# ResearchPaperSummarizer
AI for research paper summarization and entity extraction

## FastAPI service (Groq-backed)

This project now includes a FastAPI API that uses Groq (replacing OpenAI) for chat completions.

Quickstart:

1. Copy environment file and set your key:
   - `cp .env.example .env` and fill `GROQ_API_KEY`
2. (Recommended) Create a virtual environment and install deps:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
3. Run the API:
   - `python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000`
   - or: `python main.py`
4. Call the chat endpoint:
   - `curl -X POST http://localhost:8000/chat -H 'content-type: application/json' -d '{"prompt":"Hello"}'`

See `docs/CODE_DOCUMENTATION.md` for detailed architecture and runbook.
