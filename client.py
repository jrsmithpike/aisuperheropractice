import asyncio
import json
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def main():
    async with client:

        # Test get_latest_stories tool
        print("\n--- Testing get_latest_stories ---")
        try:
            result = await client.call_tool("get_latest_stories")
            print(json.dumps(json.loads(result.content[0].text), indent=2))
        except Exception as e:
            print(f"Error calling get_latest_stories: {e}")

        # Test search_stories tool
        print("\n--- Testing search_stories ---")
        keywords = ["battery", "math", "policy"]
        try:
            result = await client.call_tool(
                "search_stories", arguments={"keywords": keywords}
            )
            print(json.dumps(json.loads(result.content[0].text), indent=2))

        except Exception as e:
            print(f"Error calling search_stories: {e}")


if __name__ == "__main__":
    asyncio.run(main())
