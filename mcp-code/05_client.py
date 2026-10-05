"""Steps 5-7: a client that starts the server over stdio and discovers what it offers."""

import asyncio
import sys

from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(command=sys.executable, args=["04_server_with_prompt.py"])


async def main() -> None:
    async with Client(SERVER) as client:
        print("Connected to:", client.server_info.name if client.server_info else "?")
        print("Protocol version:", client.protocol_version)

        tools = await client.list_tools()
        print("\nTools:")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")
            print(f"    inputSchema: {tool.input_schema}")

        resources = await client.list_resources()
        print("\nResources:")
        for resource in resources.resources:
            print(f"  - {resource.uri} ({resource.mime_type})")

        templates = await client.list_resource_templates()
        print("\nResource templates:")
        for template in templates.resource_templates:
            print(f"  - {template.uri_template}")

        prompts = await client.list_prompts()
        print("\nPrompts:")
        for prompt in prompts.prompts:
            args = [a.name for a in prompt.arguments or []]
            print(f"  - {prompt.name} {args}: {prompt.description}")


if __name__ == "__main__":
    asyncio.run(main())
