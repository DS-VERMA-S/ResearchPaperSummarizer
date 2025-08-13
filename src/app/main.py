import os
import logging
from typing import List, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .logging_config import setup_logging, get_logger
from .llm import chat_completion, get_default_model
from .schemas import ChatRequest, ChatResponse

# Load environment variables from .env if present
load_dotenv()

# Configure logging early
setup_logging()
logger = get_logger("app")

app = FastAPI(title="Groq FastAPI Service", version="1.0.0")

# CORS, adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    model = get_default_model()
    has_key = bool(os.getenv("GROQ_API_KEY"))
    logger.info(
        "Service startup",
        extra={
            "model": model,
            "groq_key_present": has_key,
        },
    )


@app.get("/", tags=["meta"])  # Simple root endpoint
async def root() -> Dict[str, str]:
    return {"status": "ok", "service": "Groq FastAPI Service"}


@app.get("/healthz", tags=["meta"])  # Health probe
async def healthz() -> Dict[str, str]:
    return {"status": "ok", "model": get_default_model()}


@app.post("/chat", response_model=ChatResponse, tags=["chat"])  # Chat endpoint
async def chat(payload: ChatRequest) -> ChatResponse:
    try:
        messages: List[Dict[str, str]]
        if payload.messages:
            messages = payload.messages
        else:
            messages = []
            if payload.system_prompt:
                messages.append({"role": "system", "content": payload.system_prompt})
            messages.append({"role": "user", "content": payload.prompt or ""})

        content, model_used, usage = chat_completion(
            messages=messages,
            model=payload.model,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
            top_p=payload.top_p,
        )

        logger.info("Chat completion succeeded", extra={"model": model_used})
        return ChatResponse(content=content, model=model_used, usage=usage)
    except Exception as exc:  # Fast error surface; rely on logs for details
        logger.exception("Chat completion failed")
        raise HTTPException(status_code=500, detail=str(exc))


def get_host_port() -> tuple[str, int]:
    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000
    return host, port


# For local debugging: `python -m uvicorn src.app.main:app --reload`
# Or run this module directly: `python src/app/main.py`
if __name__ == "__main__":
    import uvicorn

    host, port = get_host_port()
    uvicorn.run("src.app.main:app", host=host, port=port, reload=True)