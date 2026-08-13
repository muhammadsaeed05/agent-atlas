from langchain_mcp_adapters.client import MultiServerMCPClient
from core.config import TAVILY_API_KEY

_mcp_client: MultiServerMCPClient | None = None
_tavily_search_tool = None


def get_mcp_client() -> MultiServerMCPClient:
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MultiServerMCPClient({
            "tavily": {
                "transport": "streamable_http",
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
            }
        })
    return _mcp_client


async def get_tavily_search_tool():
    global _tavily_search_tool
    if _tavily_search_tool is not None:
        return _tavily_search_tool

    client = get_mcp_client()
    tools = await client.get_tools()
    _tavily_search_tool = next((tool for tool in tools if tool.name == "tavily_search"), None)
    return _tavily_search_tool


async def tavily_mcp_search(query: str):
    tool = await get_tavily_search_tool()
    if not tool:
        raise RuntimeError("Tavily search tool not found via MCP client.")
    return await tool.ainvoke({"query": query})
