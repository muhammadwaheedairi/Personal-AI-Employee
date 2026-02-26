"""
LinkedIn MCP Server - Gold Tier
MCP implementation for posting to LinkedIn via Playwright.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

server = Server("linkedin")


def _post_to_linkedin(text: str) -> str:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from watchers.linkedin_poster import LinkedInPoster
    poster = LinkedInPoster()
    success = poster._post_to_linkedin(text)
    return "posted" if success else "failed"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_linkedin",
            description="Post directly to LinkedIn",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Post text"},
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="queue_linkedin",
            description="Queue a LinkedIn post — writes to /Plans/linkedin_queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Post text"},
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
        if name == "post_linkedin":
            text = arguments["text"]
            result = await asyncio.get_event_loop().run_in_executor(
                None, _post_to_linkedin, text
            )
            return [types.TextContent(type="text", text=f"LinkedIn {result}: {text[:50]}...")]

        elif name == "queue_linkedin":
            text = arguments["text"]
            topic = arguments.get("topic", "post")
            vault = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
            queue = vault / "Plans" / "linkedin_queue"
            queue.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = queue / f"{topic}_{timestamp}.md"
            filepath.write_text(f"""---
type: linkedin_post
created: {datetime.now().isoformat()}
---

{text}
""")
            return [types.TextContent(type="text", text=f"LinkedIn post queued: {filepath.name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
