import os
import logging
from typing import List, Dict, Optional, Tuple

from groq import Groq

from .logging_config import get_logger


_groq_client: Optional[Groq] = None
_logger: logging.Logger = get_logger(__name__)


def get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is not None:
        return _groq_client

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Please set it in your environment or .env file.")

    _groq_client = Groq(api_key=api_key)
    _logger.info("Initialized Groq client")
    return _groq_client


def get_default_model() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")


def chat_completion(
    *,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
) -> Tuple[str, str, Optional[Dict[str, int]]]:
    """Call Groq Chat Completions API and return (content, model, usage).

    messages: list of {"role": "system|user|assistant", "content": "..."}
    """
    client = get_groq_client()

    model_to_use = model or get_default_model()
    request_kwargs = {
        "messages": messages,
        "model": model_to_use,
    }

    if temperature is not None:
        request_kwargs["temperature"] = temperature
    if max_tokens is not None:
        request_kwargs["max_tokens"] = max_tokens
    if top_p is not None:
        request_kwargs["top_p"] = top_p

    _logger.debug("Sending request to Groq", extra={"model": model_to_use})
    response = client.chat.completions.create(**request_kwargs)

    choice = response.choices[0]
    content = choice.message.content or ""

    usage = None
    if hasattr(response, "usage") and response.usage:
        # Groq returns token usage similar to OpenAI. Keep minimal mapping.
        usage = {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", None) or 0,
            "completion_tokens": getattr(response.usage, "completion_tokens", None) or 0,
            "total_tokens": getattr(response.usage, "total_tokens", None) or 0,
        }

    _logger.info("Groq response received", extra={"model": model_to_use})
    return content, model_to_use, usage