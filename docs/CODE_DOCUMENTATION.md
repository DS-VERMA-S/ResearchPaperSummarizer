## Overview

This service exposes a FastAPI API that proxies chat completion requests to the Groq API (replacing prior OpenAI usage). It includes structured logging and simple health checks.

## Directory structure

- `src/app/main.py`: FastAPI application entrypoint and HTTP routes
- `src/app/llm.py`: Groq client initialization and chat completion wrapper
- `src/app/logging_config.py`: Application and uvicorn logging configuration
- `src/app/schemas.py`: Pydantic request/response models
- `requirements.txt`: Python dependencies
- `.env.example`: Example environment variables

## Configuration

- `GROQ_API_KEY` (required): Your Groq API key
- `GROQ_MODEL` (optional): Default model, default `llama3-8b-8192`
- `LOG_LEVEL` (optional): Python logging level, default `INFO`
- `HOST`, `PORT` (optional): Bind address and port (used for `__main__` run mode)

## How the code runs when you start FastAPI

1. You start the server with uvicorn, e.g.:
   - `python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000`
   - or run the module: `python src/app/main.py`
   - or run the top-level entrypoint: `python main.py`
2. On module import, `.env` is loaded (if present) and logging is configured.
3. The FastAPI `app` instance is created and CORS middleware is attached.
4. When a request hits `POST /chat`:
   - The `ChatRequest` payload is validated (must include either `prompt` or `messages`).
   - The request is normalized into OpenAI-compatible `messages` format.
   - `llm.chat_completion` calls Groq's Chat Completions API and returns content, model, and token usage.
   - A `ChatResponse` is returned with the assistant content and metadata.
5. Logs are emitted for key events and errors; uvicorn logs share the same formatting.

## API

- `GET /` → `{ status: "ok", service: "Groq FastAPI Service" }`
- `GET /healthz` → `{ status: "ok", model: "<default-model>" }`
- `POST /chat`
  - Request body (one of):
    - `{ "prompt": "Hello", "system_prompt": "You are helpful", "model": "llama3-8b-8192" }`
    - `{ "messages": [{"role":"system","content":"You are helpful"},{"role":"user","content":"Hello"}] }`
  - Response body: `{ "content": "...", "model": "...", "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} }`

## Local setup & run

1. Python 3.10+ recommended
2. `cp .env.example .env` and set `GROQ_API_KEY`
3. `python -m venv .venv && source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. Run the server:
   - `python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000`
6. Test with curl:
```bash
curl -s -X POST http://localhost:8000/chat \
  -H 'content-type: application/json' \
  -d '{"prompt": "Say hello in one sentence"}' | jq
```

## Notes

- Replace any existing OpenAI calls by importing and using `llm.chat_completion` with `messages` format.
- Logging can be tuned via `LOG_LEVEL`. The same format is applied to uvicorn logs.