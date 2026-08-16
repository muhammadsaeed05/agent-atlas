import pytest
from unittest.mock import AsyncMock, patch
from schemas.travel_state import TravelState
from agents.planner_agent import planner_node


@pytest.mark.asyncio
async def test_planner_resolves_country_to_cities():
    state: TravelState = {
        "messages": [],
        "user_query": "I want a 7-day trip to Japan with $3000 budget",
        "origin": "",
        "country": "",
        "target_cities": [],
        "duration_days": 5,
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }
    mock_json = (
        '{"origin": "", "country": "Japan", "target_cities": ["Tokyo", "Kyoto"], "duration_days": 7}'
    )
    with patch("agents.planner_agent.acomplete", new=AsyncMock(return_value=mock_json)):
        result = await planner_node(state)
        assert result["country"] == "Japan"
        assert result["target_cities"] == ["Tokyo", "Kyoto"]
        assert result["duration_days"] == 7


@pytest.mark.asyncio
async def test_planner_resolves_origin_and_city():
    state: TravelState = {
        "messages": [],
        "user_query": "Flight from London to New York for 4 days",
        "origin": "",
        "country": "",
        "target_cities": [],
        "duration_days": 5,
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }
    mock_json = (
        '{"origin": "London", "country": "United States", "target_cities": ["New York"], "duration_days": 4}'
    )
    with patch("agents.planner_agent.acomplete", new=AsyncMock(return_value=mock_json)):
        result = await planner_node(state)
        assert result["origin"] == "London"
        assert result["target_cities"] == ["New York"]
        assert result["duration_days"] == 4


@pytest.mark.asyncio
async def test_planner_handles_fallback_gracefully():
    state: TravelState = {
        "messages": [],
        "user_query": "Rome",
        "origin": "",
        "country": "",
        "target_cities": [],
        "duration_days": 5,
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }
    with patch("agents.planner_agent.acomplete", side_effect=Exception("API error")):
        result = await planner_node(state)
        assert result["target_cities"] == ["Rome"]
        assert result["duration_days"] == 5
