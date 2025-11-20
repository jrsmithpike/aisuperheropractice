import asyncio
import json
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


def dump_tool_result(result) -> None:
    content_parts = getattr(result, "content", [])
    if not content_parts:
        print("∅")
        return

    for part in content_parts:
        payload = getattr(part, "data", None)
        if payload is None:
            payload = getattr(part, "text", part)
        if isinstance(payload, (dict, list)):
            print(json.dumps(payload, indent=2))
        else:
            print(payload)


async def main():
    async with client:
        print("\n--- Testing get_unique_tags ---")
        try:
            result = await client.call_tool("get_unique_tags")
            dump_tool_result(result)
        except Exception as e:
            print(f"Error calling get_unique_tags: {e}")

        print("\n--- Testing get_latest_stories ---")
        try:
            result = await client.call_tool("get_latest_stories")
            dump_tool_result(result)
        except Exception as e:
            print(f"Error calling get_latest_stories: {e}")

        print("\n--- Testing get_stories_by_tags ---")
        test_tags = ["Robotics", "LLM"]
        try:
            result = await client.call_tool(
                "get_stories_by_tags", arguments={"tags": test_tags}
            )
            dump_tool_result(result)
        except Exception as e:
            print(f"Error calling get_stories_by_tags: {e}")

        print("\n--- Testing search_stories ---")
        keywords = ["battery", "math", "policy"]
        try:
            result = await client.call_tool(
                "search_stories", arguments={"keywords": keywords}
            )
            dump_tool_result(result)
        except Exception as e:
            print(f"Error calling search_stories: {e}")


if __name__ == "__main__":
    asyncio.run(main())
