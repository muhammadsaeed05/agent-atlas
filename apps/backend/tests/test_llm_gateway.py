import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from core.llm_gateway import (
    ChatGateway,
    get_chat_model,
    acomplete,
    complete,
    _format_messages,
    _setup_langsmith_tracing,
)
import litellm


def test_format_messages():
    # String input
    assert _format_messages("hello world") == [{"role": "user", "content": "hello world"}]

    # Dict input
    raw_dict = [{"role": "user", "content": "test"}]
    assert _format_messages(raw_dict) == raw_dict

    # LangChain messages
    lc_messages = [
        SystemMessage(content="You are a helpful travel assistant."),
        HumanMessage(content="Find flights to Tokyo"),
        AIMessage(content="Here are flights to Tokyo."),
    ]
    formatted = _format_messages(lc_messages)
    assert formatted == [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": "Find flights to Tokyo"},
        {"role": "assistant", "content": "Here are flights to Tokyo."},
    ]


@pytest.mark.asyncio
async def test_acomplete():
    res = await acomplete(
        messages="Plan a trip to Paris",
        model="gpt-4o-mini",
        mock_response="Paris travel plan generated.",
    )
    assert res == "Paris travel plan generated."


def test_complete():
    res = complete(
        messages="Plan a trip to Rome",
        model="gpt-4o-mini",
        mock_response="Rome travel plan generated.",
    )
    assert res == "Rome travel plan generated."


@pytest.mark.asyncio
async def test_chat_gateway_ainvoke():
    chat_model = get_chat_model(
        model="gpt-4o-mini",
        fallback_models=["groq/llama-3.3-70b-versatile"],
        temperature=0.3,
        max_retries=2,
    )
    assert chat_model._llm_type == "litellm_gateway"
    assert chat_model.model == "gpt-4o-mini"
    assert chat_model.fallback_models == ["groq/llama-3.3-70b-versatile"]
    assert chat_model.temperature == 0.3
    assert chat_model.max_retries == 2

    response = await chat_model.ainvoke(
        [HumanMessage(content="Find hotels in Kyoto")],
        mock_response="Found Kyoto Ryokan and Hotels.",
    )
    assert isinstance(response, AIMessage)
    assert response.content == "Found Kyoto Ryokan and Hotels."


def test_chat_gateway_invoke():
    chat_model = get_chat_model(model="gpt-4o-mini")
    response = chat_model.invoke(
        [HumanMessage(content="Test sync invoke")],
        mock_response="Sync response received.",
    )
    assert isinstance(response, AIMessage)
    assert response.content == "Sync response received."


@pytest.mark.asyncio
async def test_fallback_execution():
    # If primary model is invalid, litellm falls back to fallback_models
    response = await acomplete(
        messages="Test fallback",
        model="openai/non-existent-model-xyz",
        fallback_models=["groq/llama-3.3-70b-versatile"],
        num_retries=1,
        mock_response="Fallback succeeded!",
    )
    assert response == "Fallback succeeded!"


def test_langsmith_tracing_setup(monkeypatch):
    monkeypatch.setenv("LANGSMITH_API_KEY", "test_langsmith_key")
    with patch("core.llm_gateway.LANGSMITH_API_KEY", "test_langsmith_key"):
        _setup_langsmith_tracing()
        assert "langsmith" in litellm.success_callback
        assert "langsmith" in litellm.failure_callback


@pytest.mark.asyncio
async def test_travel_workflow_with_llm_gateway():
    from unittest.mock import AsyncMock
    from workflows.travel_workflow import run_travel_workflow

    with patch("agents.hotel_agent.tavily_mcp_search", new_callable=AsyncMock) as mock_hotel, \
         patch("agents.flight_agent.tavily_mcp_search", new_callable=AsyncMock) as mock_flight, \
         patch("core.llm_gateway.litellm.acompletion") as mock_acompletion:

        mock_hotel.return_value = "Hotels in Barcelona"
        mock_flight.return_value = "Flights to Barcelona"

        mock_resp = AsyncMock()
        mock_resp.choices = [AsyncMock(message=AsyncMock(content="Barcelona 3-day itinerary"))]
        mock_acompletion.return_value = mock_resp

        result = await run_travel_workflow("Trip to Barcelona", thread_id="test-thread-gateway")
        assert result["itinerary"] == "Barcelona 3-day itinerary"
        assert result["llm_calls"] == 3
        assert result["flight_results"] == "Barcelona 3-day itinerary"
        assert result["hotel_results"] == "Barcelona 3-day itinerary"
