"""Transports: run the same server over Streamable HTTP, then connect with a URL.

Terminal 1:  python 07_transport_example.py server
Terminal 2:  python 07_transport_example.py client
"""

import asyncio
import importlib
import sys

from mcp import Client

URL = "http://127.0.0.1:8000/mcp"


async def run_client() -> None:
    async with Client(URL) as client:
        tools = await client.list_tools()
        print("Tools over HTTP:", [t.name for t in tools.tools])
        result = await client.call_tool("get_product", {"product_id": "P100"})
        print("Result over HTTP:", result.structured_content)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        server = importlib.import_module("04_server_with_prompt")
        server.mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
    else:
        asyncio.run(run_client())
