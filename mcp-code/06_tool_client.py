"""Steps 8-10: call the tool, read a resource, and get the prompt."""

import asyncio
import sys

from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(command=sys.executable, args=["04_server_with_prompt.py"])


async def main() -> None:
    async with Client(SERVER) as client:
        result = await client.call_tool("get_product", {"product_id": "P200"})
        print("Tool text content:", result.content[0].text)
        print("Tool structured content:", result.structured_content)
        print("Is error:", result.is_error)

        bad = await client.call_tool("get_product", {"product_id": "X999"})
        print("\nUnknown product -> is_error:", bad.is_error, "|", bad.content[0].text)

        resource = await client.read_resource("catalog://products/P100")
        print("\nResource:", resource.contents[0].uri)
        print(resource.contents[0].text)

        prompt = await client.get_prompt(
            "product_description", {"product_id": "P300", "tone": "excited"}
        )
        print("\nPrompt messages:")
        for message in prompt.messages:
            print(f"  [{message.role}] {message.content.text}")


if __name__ == "__main__":
    asyncio.run(main())
