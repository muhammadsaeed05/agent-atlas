from typing import Any, Dict
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from schemas.travel_state import TravelState
from tools.mcp_client import get_weather_tools
from core import get_chat_model


async def weather_agent_node(state: TravelState) -> Dict[str, Any]:
    """Agent specialized in checking current weather and forecasts for the destination."""
    query = state.get("user_query", "")

    llm = get_chat_model(temperature=0.2)
    tools = await get_weather_tools()

    agent = create_react_agent(llm, tools=tools)

    human_prompt = (
        f"Check weather conditions and forecast for the destination mentioned in: {query}\n\n"
        "Please provide:\n"
        "1. Current temperature and weather condition\n"
        "2. Expected forecast during the trip\n"
        "3. Packing recommendations based on weather\n"
        "4. Any weather advisories or best times for outdoor activities"
    )

    result = await agent.ainvoke({
        "messages": [
            SystemMessage(
                content="You are a weather specialist travel agent. Use the weather tools to fetch accurate current weather and forecasts for the traveler's destination."
            ),
            HumanMessage(content=human_prompt),
        ]
    })

    final_response = result["messages"][-1].content

    return {
        "weather_results": final_response,
        "messages": [AIMessage(content="Weather forecast and advice generated")],
        "llm_calls": max(1, len(result.get("messages", [])) // 2),
    }
