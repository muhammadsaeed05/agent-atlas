"""Core package for settings and utilities."""

from .config import (
    LLM_MODEL,
    LLM_FALLBACK_MODEL,
    LLM_RETRIES,
    LLM_TIMEOUT,
    OPENROUTER_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    LANGCHAIN_TRACING_V2,
)
from .llm_gateway import ChatGateway, get_chat_model, acomplete, complete

__all__ = [
    "ChatGateway",
    "get_chat_model",
    "acomplete",
    "complete",
    "LLM_MODEL",
    "LLM_FALLBACK_MODEL",
    "LLM_RETRIES",
    "LLM_TIMEOUT",
    "OPENROUTER_API_KEY",
    "GROQ_API_KEY",
    "OPENAI_API_KEY",
    "LANGSMITH_API_KEY",
    "LANGSMITH_PROJECT",
    "LANGCHAIN_TRACING_V2",
]
