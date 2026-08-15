"""
Travel Planning Workflow Orchestrator.
Connects agents from `agents/` into a LangGraph execution graph.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

from schemas.travel_state import TravelState
from agents import (
    flight_agent_node,
    hotel_agent_node,
    weather_agent_node,
    itinerary_agent_node,
)


def create_travel_workflow(checkpointer: MemorySaver | None = None):
    """Constructs and compiles the multi-agent travel graph."""
    builder = StateGraph(TravelState)

    # 1. Register Agent Nodes
    builder.add_node("flight_agent", flight_agent_node)
    builder.add_node("hotel_agent", hotel_agent_node)
    builder.add_node("weather_agent", weather_agent_node)
    builder.add_node("itinerary_agent", itinerary_agent_node)

    # 2. Fan-out: Run flight, hotel & weather agents concurrently
    builder.add_edge(START, "flight_agent")
    builder.add_edge(START, "hotel_agent")
    builder.add_edge(START, "weather_agent")

    # 3. Fan-in: Wait for all research agents before generating itinerary
    builder.add_edge("flight_agent", "itinerary_agent")
    builder.add_edge("hotel_agent", "itinerary_agent")
    builder.add_edge("weather_agent", "itinerary_agent")

    builder.add_edge("itinerary_agent", END)

    return builder.compile(checkpointer=checkpointer)


# Compiled workflow instance
travel_graph = create_travel_workflow(checkpointer=MemorySaver())


async def run_travel_workflow(user_query: str, thread_id: str = "default") -> Dict[str, Any]:
    """Entrypoint function called by API routers."""
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "user_query": user_query,
        "messages": [HumanMessage(content=user_query)],
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }
    return await travel_graph.ainvoke(initial_state, config=config)
