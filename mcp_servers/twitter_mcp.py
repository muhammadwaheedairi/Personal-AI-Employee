"""
Twitter/X MCP Server - Gold Tier
MCP implementation for posting tweets via Playwright.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

server = Server("twitter")


def _post_tweet(text: str) -> str:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from watchers.twitter_poster import TwitterPoster
    poster = TwitterPoster()
    success = poster._post_tweet(text)
    return "posted" if success else "failed"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_tweet",
            description="Post a tweet to Twitter/X (max 250 characters)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Tweet text (max 250 chars)"},
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="queue_tweet",
            description="Queue a tweet for posting — writes to /Plans/twitter_queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Tweet text"},
                    "topic": {"type": "string", "description": "Topic/slug for filename"},
                },
                "required": ["text"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would {name}: {str(arguments)[:100]}")]

    try:
        if name == "post_tweet":
            text = arguments["text"]
            if len(text) > 250:
                text = text[:247] + "..."
            result = await asyncio.get_event_loop().run_in_executor(
                None, _post_tweet, text
            )
            return [types.TextContent(type="text", text=f"Tweet {result}: {text[:50]}...")]

        elif name == "queue_tweet":
            text = arguments["text"]
            topic = arguments.get("topic", "tweet")
            vault = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
            queue = vault / "Plans" / "twitter_queue"
            queue.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = queue / f"{topic}_{timestamp}.md"
            filepath.write_text(f"""---
type: twitter_post
created: {datetime.now().isoformat()}
---

{text}
""")
            return [types.TextContent(type="text", text=f"Tweet queued: {filepath.name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
