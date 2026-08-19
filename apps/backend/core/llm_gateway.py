"""
LLM Gateway Layer.

Provides unified LLM invocation using LangChain's ChatLiteLLM (from langchain-litellm),
supporting OpenRouter, Groq, OpenAI, Anthropic, etc., with built-in LangSmith tracing,
configurable retries, and multi-provider fallback support.
"""

from typing import Any, Dict, List, Optional, Union
import litellm
from langchain_litellm import ChatLiteLLM
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage

from core.config import (
    LLM_MODEL,
    LLM_FALLBACK_MODEL,
    LLM_RETRIES,
    LLM_TIMEOUT,
    LANGSMITH_API_KEY,
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
) -> List[BaseMessage]:
    """Converts various message formats into standard LangChain BaseMessages."""
    if isinstance(messages, str):
        return [HumanMessage(content=messages)]

    formatted: List[BaseMessage] = []
    for msg in messages:
        if isinstance(msg, BaseMessage):
            formatted.append(msg)
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = str(msg.get("content", ""))
            if role == "system":
                formatted.append(SystemMessage(content=content))
            elif role in ("assistant", "ai"):
                formatted.append(AIMessage(content=content))
            else:
                formatted.append(HumanMessage(content=content))
    return formatted


class ChatGateway(ChatLiteLLM):
    """
    LangChain Chat Model backed by LiteLLM via ChatLiteLLM.
    Integrates seamlessly into LangGraph workflows with support for
    multi-provider routing, fallbacks, retries, and LangSmith tracing.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        fallback_models: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_retries: Optional[int] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ):
        model_name = model or LLM_MODEL
        retries = max_retries if max_retries is not None else LLM_RETRIES
        req_timeout = timeout if timeout is not None else LLM_TIMEOUT

        model_kwargs = dict(kwargs.pop("model_kwargs", {}) or {})
        fallbacks = (
            fallback_models
            if fallback_models is not None
            else ([LLM_FALLBACK_MODEL] if LLM_FALLBACK_MODEL else [])
        )
        if fallbacks:
            model_kwargs["fallbacks"] = fallbacks

        super().__init__(
            model=model_name,
            temperature=temperature,
            max_retries=retries,
            request_timeout=req_timeout,
            model_kwargs=model_kwargs,
            **kwargs,
        )

    @property
    def fallback_models(self) -> List[str]:
        return self.model_kwargs.get("fallbacks", [])

    @property
    def timeout(self) -> float:
        return self.request_timeout


def get_chat_model(
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    temperature: float = 0.7,
    max_retries: Optional[int] = None,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> ChatGateway:
    """Factory helper to obtain a ChatGateway (ChatLiteLLM) instance for agents and workflows."""
    return ChatGateway(
        model=model,
        fallback_models=fallback_models,
        temperature=temperature,
        max_retries=max_retries,
        timeout=timeout,
        **kwargs,
    )


async def acomplete(
    messages: Union[str, List[Union[BaseMessage, Dict[str, str]]]],
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    num_retries: Optional[int] = None,
    temperature: float = 0.7,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> str:
    """Direct asynchronous LLM completion helper using ChatLiteLLM."""
    chat_model = get_chat_model(
        model=model,
        fallback_models=fallback_models,
        temperature=temperature,
        max_retries=num_retries,
        timeout=timeout,
    )
    lc_messages = _format_messages(messages)
    response = await chat_model.ainvoke(lc_messages, **kwargs)
    return str(response.content) if isinstance(response, AIMessage) else str(response)


def complete(
    messages: Union[str, List[Union[BaseMessage, Dict[str, str]]]],
    model: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    num_retries: Optional[int] = None,
    temperature: float = 0.7,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> str:
    """Direct synchronous LLM completion helper using ChatLiteLLM."""
    chat_model = get_chat_model(
        model=model,
        fallback_models=fallback_models,
        temperature=temperature,
        max_retries=num_retries,
        timeout=timeout,
    )
    lc_messages = _format_messages(messages)
    response = chat_model.invoke(lc_messages, **kwargs)
    return str(response.content) if isinstance(response, AIMessage) else str(response)
