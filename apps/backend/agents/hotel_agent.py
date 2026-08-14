from typing import Any, Dict
from langchain_core.messages import HumanMessage
from schemas.travel_state import TravelState
from tools.mcp_client import tavily_mcp_search
from core import get_chat_model


async def hotel_agent_node(state: TravelState) -> Dict[str, Any]:
    """Agent specialized in finding hotels and accommodations."""
    query = state.get("user_query", "")
    search_results = await tavily_mcp_search(f"hotels and accommodation for {query}")
    
    llm = get_chat_model(temperature=0.2)
    response = await llm.ainvoke([
        HumanMessage(content=f"Find the top accommodations and neighborhood tips from: {search_results}")
    ])
    
    return {
        "hotel_results": response.content,
        "llm_calls": 1,
    }
