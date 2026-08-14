"""
LLM Gateway Layer.

Provides unified LLM invocation using LiteLLM (supporting OpenRouter, Groq, OpenAI, etc.),
with built-in LangSmith tracing, configurable retries, and model fallback support.
"""

from typing import Any, Dict, List, Optional, Union
import litellm
from pydantic import Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

from core.config import (
    LLM_MODEL,
    LLM_FALLBACK_MODEL,
    LLM_RETRIES,
    LLM_TIMEOUT,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
)


def _setup_langsmith_tracing():
    """Configures LangSmith tracing for LiteLLM if API key is present."""
    if LANGSMITH_API_KEY:
        if "langsmith" not in litellm.success_callback:
            litellm.success_callback.append("langsmith")
        if "langsmith" not in litellm.failure_callback:
            litellm.failure_callback.append("langsmith")


# Initialize tracing callbacks on load
_setup_langsmith_tracing()


def _format_messages(
    messages: Union[str, List[Union[BaseMessage, Dict[str, str]]]]
) -> List[Dict[str, str]]:
    """Converts various message formats into LiteLLM/OpenAI standard dict list."""
    if isinstance(messages, str):
        return [{"role": "user", "content": messages}]

    formatted = []
    for msg in messages:
        if isinstance(msg, dict):
            formatted.append(msg)
        elif isinstance(msg, HumanMessage):
            formatted.append({"role": "user", "content": str(msg.content)})
        elif isinstance(msg, AIMessage):
            formatted.append({"role": "assistant", "content": str(msg.content)})
        elif isinstance(msg, SystemMessage):
            formatted.append({"role": "system", "content": str(msg.content)})
        elif isinstance(msg, BaseMessage):
            role = "user" if msg.type == "human" else "assistant" if msg.type == "ai" else "system"
            formatted.append({"role": role, "content": str(msg.content)})
    return formatted


class ChatGateway(BaseChatModel):
    """
    LangChain-compatible Chat Model powered by the LLM Gateway.
    Integrates seamlessly into LangGraph workflows while supporting
    LiteLLM's multi-provider routing, fallbacks, retries, and LangSmith tracing.
    """
    model: str = Field(default_factory=lambda: LLM_MODEL)
    fallback_models: List[str] = Field(
        default_factory=lambda: [LLM_FALLBACK_MODEL] if LLM_FALLBACK_MODEL else []
    )
    temperature: float = 0.7
    max_retries: int = Field(default_factory=lambda: LLM_RETRIES)
    timeout: float = Field(default_factory=lambda: LLM_TIMEOUT)

    @property
    def _llm_type(self) -> str:
        return "litellm_gateway"

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        formatted = _format_messages(messages)
        response = await litellm.acompletion(
            model=self.model,
            messages=formatted,
            fallbacks=self.fallback_models or None,
            num_retries=self.max_retries,
            temperature=self.temperature,
            timeout=self.timeout,
            stop=stop,
            **kwargs,
        )
        content = response.choices[0].message.content or ""
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        formatted = _format_messages(messages)
        response = litellm.completion(
            model=self.model,
            messages=formatted,
            fallbacks=self.fallback_models or None,
            num_retries=self.max_retries,
            temperature=self.temperature,
            timeout=self.timeout,
            stop=stop,
            **kwargs,
        )
        content = response.choices[0].message.content or ""
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])


async def acomplete(
    messages: Union[str, List[Union[BaseMessage, Dict[str, str]]]],
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    num_retries: Optional[int] = None,
    temperature: float = 0.7,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> str:
    """Direct asynchronous LLM completion helper with retries and fallbacks."""
    formatted = _format_messages(messages)
    active_model = model or LLM_MODEL
    active_fallbacks = fallback_models if fallback_models is not None else ([LLM_FALLBACK_MODEL] if LLM_FALLBACK_MODEL else None)
    active_retries = num_retries if num_retries is not None else LLM_RETRIES
    active_timeout = timeout if timeout is not None else LLM_TIMEOUT

    response = await litellm.acompletion(
        model=active_model,
        messages=formatted,
        fallbacks=active_fallbacks,
        num_retries=active_retries,
        temperature=temperature,
        timeout=active_timeout,
        **kwargs,
    )
    return response.choices[0].message.content or ""


def complete(
    messages: Union[str, List[Union[BaseMessage, Dict[str, str]]]],
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    num_retries: Optional[int] = None,
    temperature: float = 0.7,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> str:
    """Direct synchronous LLM completion helper with retries and fallbacks."""
    formatted = _format_messages(messages)
    active_model = model or LLM_MODEL
    active_fallbacks = fallback_models if fallback_models is not None else ([LLM_FALLBACK_MODEL] if LLM_FALLBACK_MODEL else None)
    active_retries = num_retries if num_retries is not None else LLM_RETRIES
    active_timeout = timeout if timeout is not None else LLM_TIMEOUT

    response = litellm.completion(
        model=active_model,
        messages=formatted,
        fallbacks=active_fallbacks,
        num_retries=active_retries,
        temperature=temperature,
        timeout=active_timeout,
        **kwargs,
    )
    return response.choices[0].message.content or ""


def get_chat_model(
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    temperature: float = 0.7,
    max_retries: Optional[int] = None,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> ChatGateway:
    """Factory helper to obtain a ChatGateway instance for agents and workflows."""
    active_model = model or LLM_MODEL
    active_fallbacks = fallback_models if fallback_models is not None else ([LLM_FALLBACK_MODEL] if LLM_FALLBACK_MODEL else [])
    active_retries = max_retries if max_retries is not None else LLM_RETRIES
    active_timeout = timeout if timeout is not None else LLM_TIMEOUT

    return ChatGateway(
        model=active_model,
        fallback_models=active_fallbacks,
        temperature=temperature,
        max_retries=active_retries,
        timeout=active_timeout,
        **kwargs,
    )
