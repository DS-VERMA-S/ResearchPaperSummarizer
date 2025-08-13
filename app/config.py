import os
from typing import Optional


def get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_openai_api_key(required: bool = True) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if required and not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please export it to enable generation."
        )
    return api_key


EMBEDDING_API_MODEL = os.getenv("EMBEDDING_API_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "6"))