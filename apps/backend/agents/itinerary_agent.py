from typing import Any, Dict
from langchain_core.messages import HumanMessage, AIMessage
from schemas.travel_state import TravelState
from core import get_chat_model


async def itinerary_agent_node(state: TravelState) -> Dict[str, Any]:
    """Agent specialized in combining flight and hotel findings into a cohesive plan."""
    llm = get_chat_model(temperature=0.4)
    
    prompt = f"""
    Create a complete travel itinerary based on:
    - User Request: {state.get('user_query')}
    - Flights: {state.get('flight_results')}
    - Accommodation: {state.get('hotel_results')}
    """
    
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    
    return {
        "itinerary": response.content,
        "messages": [AIMessage(content=str(response.content))],
        "llm_calls": 1,
    }
