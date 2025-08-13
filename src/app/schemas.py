from typing import List, Dict, Optional
from pydantic import BaseModel, model_validator


class ChatRequest(BaseModel):
    prompt: Optional[str] = None
    messages: Optional[List[Dict[str, str]]] = None
    system_prompt: Optional[str] = None

    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None

    @model_validator(mode="after")
    def ensure_prompt_or_messages(self) -> "ChatRequest":
        if not self.prompt and not self.messages:
            raise ValueError("Either 'prompt' or 'messages' must be provided")
        return self


class ChatResponse(BaseModel):
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None