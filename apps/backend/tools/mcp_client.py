from langchain_mcp_adapters.client import MultiServerMCPClient
from core.config import TAVILY_API_KEY, AVIATIONSTACK_API_KEY

_mcp_client: MultiServerMCPClient | None = None


def get_mcp_client() -> MultiServerMCPClient:
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MultiServerMCPClient({
            "tavily": {
                "transport": "streamable_http",
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
            },
            "aviationstack": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                     "--with",
                    "mcp<2.0.0",
                    "aviationstack-mcp"
                ],
                "env": {
                    "AVIATION_STACK_API_KEY": AVIATIONSTACK_API_KEY
                }
            }
        })
    return _mcp_client


async def get_all_tools():
    """Returns all tools from all configured MCP servers."""
    client = get_mcp_client()
    return await client.get_tools()


async def get_tavily_tools():
    """Returns all Tavily tools."""
    tools = await get_all_tools()
    return [t for t in tools if t.name.startswith("tavily_")]


async def get_aviationstack_tools():
    """Returns all Aviation Stack tools."""
    tools = await get_all_tools()
    return [t for t in tools if not t.name.startswith("tavily_")]


async def get_tavily_search_tool():
    """Returns specifically the tavily_search tool for backward compatibility."""
    tools = await get_tavily_tools()
    return next((t for t in tools if t.name == "tavily_search"), None)


async def tavily_mcp_search(query: str):
    """Convenience function to perform a tavily search directly."""
    tool = await get_tavily_search_tool()
    if not tool:
        raise RuntimeError("Tavily search tool not found via MCP client.")
    return await tool.ainvoke({"query": query})
