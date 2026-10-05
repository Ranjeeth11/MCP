"""Step 1: the smallest possible MCP server (no tools, resources, or prompts yet)."""

from mcp.server import MCPServer

mcp = MCPServer("Product Catalog")

if __name__ == "__main__":
    mcp.run()
