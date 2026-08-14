from typing import Any, Dict
from langchain_core.messages import HumanMessage
from schemas.travel_state import TravelState
from tools.mcp_client import tavily_mcp_search
from core import get_chat_model


async def flight_agent_node(state: TravelState) -> Dict[str, Any]:
    """Agent specialized in searching flights and travel routes."""
    query = state.get("user_query", "")
    search_results = await tavily_mcp_search(f"flights and routes for {query}")
    
    llm = get_chat_model(temperature=0.2)
    response = await llm.ainvoke([
        HumanMessage(content=f"Find the best flight options and travel logistics from: {search_results}")
    ])
    
    return {
        "flight_results": response.content,
        "llm_calls": 1,
    }
