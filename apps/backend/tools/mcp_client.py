import sys
from pathlib import Path
from typing import List, Optional
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from core.config import TAVILY_API_KEY, AVIATIONSTACK_API_KEY, OPENWEATHER_API_KEY

_mcp_client: Optional[MultiServerMCPClient] = None
_cached_tools: Optional[List[BaseTool]] = None

WEATHER_TOOL_NAMES = {"get_current_weather", "get_forecast"}


def get_mcp_client() -> MultiServerMCPClient:
    """Initializes and returns the MultiServerMCPClient singleton."""
    global _mcp_client
    if _mcp_client is None:
        weather_server_path = Path(__file__).parent / "weather_mcp_server.py"

        servers = {
            "tavily": {
                "transport": "streamable_http",
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}",
            },
            "aviationstack": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "--with",
                    "mcp<2.0.0",
                    "aviationstack-mcp",
                ],
                "env": {
                    "AVIATION_STACK_API_KEY": AVIATIONSTACK_API_KEY,
                },
            },
            "weather": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [
                    str(weather_server_path),
                ],
                "env": {
                    "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
                },
            },
        }

        _mcp_client = MultiServerMCPClient(servers)
    return _mcp_client


async def get_all_tools(force_refresh: bool = False) -> List[BaseTool]:
    """Returns all tools from configured MCP servers with in-memory caching."""
    global _cached_tools
    if _cached_tools is None or force_refresh:
        client = get_mcp_client()
        _cached_tools = await client.get_tools()
    return _cached_tools


async def get_tavily_tools() -> List[BaseTool]:
    """Returns all Tavily tools."""
    tools = await get_all_tools()
    return [t for t in tools if t.name.startswith("tavily_")]


async def get_weather_tools() -> List[BaseTool]:
    """Returns all Weather MCP tools."""
    tools = await get_all_tools()
    return [t for t in tools if t.name in WEATHER_TOOL_NAMES]


async def get_aviationstack_tools() -> List[BaseTool]:
    """Returns all Aviation Stack flight tools."""
    tools = await get_all_tools()
    return [
        t
        for t in tools
        if not t.name.startswith("tavily_") and t.name not in WEATHER_TOOL_NAMES
    ]


async def get_tavily_search_tool() -> Optional[BaseTool]:
    """Returns specifically the tavily_search tool."""
    tools = await get_tavily_tools()
    return next((t for t in tools if t.name == "tavily_search"), None)


async def tavily_mcp_search(query: str):
    """Convenience helper to perform a Tavily search directly."""
    tool = await get_tavily_search_tool()
    if not tool:
        raise RuntimeError("Tavily search tool not found via MCP client.")
    return await tool.ainvoke({"query": query})


async def close_mcp_client():
    """Resets the client and clears tool cache for clean shutdown."""
    global _mcp_client, _cached_tools
    _cached_tools = None
    _mcp_client = None

