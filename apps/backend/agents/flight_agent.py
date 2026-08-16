from langchain_core.messages import AIMessage
from typing import Any, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from schemas.travel_state import TravelState
from tools.mcp_client import get_aviationstack_tools
from core import get_chat_model
from langgraph.prebuilt import create_react_agent


async def flight_agent_node(state: TravelState) -> Dict[str, Any]:
    """Agent specialized in searching flights and travel routes using Aviation Stack MCP."""
    query = state.get("user_query", "")
    target_cities = state.get("target_cities", [])
    origin = state.get("origin", "")
    dest_str = ", ".join(target_cities) if target_cities else query
    route_context = f"from {origin} to {dest_str}" if origin else f"to {dest_str}"
    
    llm = get_chat_model(temperature=0.2)
    tools = await get_aviationstack_tools()
    
    # Create a react agent with the MCP tools
    agent = create_react_agent(llm, tools=tools)
    
    human_prompt = (
        f"Find flight options and travel logistics {route_context} for: {query}\n\n"
        "Please generate the flight details covering the following points:\n"
        "1. Likely departure time\n"
        "2. Likely arrival time\n"
        "3. Airline serving this route\n"
        "4. Typical flight duration\n"
        "5. Estimate airfare range\n"
        "6. Peak season pricing warning\n"
        "7. Booking advice"
    )
    
    result = await agent.ainvoke({
        "messages": [
            SystemMessage(content="You are a flight agent. Find the best flight options and travel logistics for the user query using the available tools, particularly the aviationstack tools for accurate flight data."),
            HumanMessage(content=human_prompt)
        ]
    })

    
    final_response = result["messages"][-1].content
    
    return {
        "flight_results": final_response,
        "messages": [
            AIMessage(content="Flight recommendation generated")
        ],
        "llm_calls": max(1, len(result.get("messages", [])) // 2),
    }
