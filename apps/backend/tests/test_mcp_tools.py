import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tools.mcp_client import get_all_tools
import asyncio



async def main():
    tools = await get_all_tools()

    for tool in tools:
        print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())