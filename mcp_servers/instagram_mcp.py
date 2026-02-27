"""
Instagram MCP Server - Gold Tier
MCP implementation for posting to Instagram via Playwright.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

server = Server("instagram")


def _post_to_instagram(image_path: str, caption: str) -> str:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from watchers.instagram_poster import InstagramPoster
    poster = InstagramPoster()
    success = poster._post_to_instagram(image_path, caption)
    return "posted" if success else "failed"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_instagram",
            description="Post an image to Instagram with a caption",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Absolute path to image file (.jpg/.png)"},
                    "caption": {"type": "string", "description": "Caption text for the post"},
                },
                "required": ["image_path", "caption"],
            },
        ),
        types.Tool(
            name="queue_instagram",
            description="Queue an Instagram post — saves image path + caption to /Plans/instagram_queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Absolute path to image file"},
                    "caption": {"type": "string", "description": "Caption text"},
                    "topic": {"type": "string", "description": "Topic/slug for filename"},
                },
                "required": ["image_path", "caption"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would {name}: {str(arguments)[:100]}")]

    try:
        if name == "post_instagram":
            image_path = arguments["image_path"]
            caption = arguments["caption"]

            if not Path(image_path).exists():
                return [types.TextContent(type="text", text=f"Error: Image not found: {image_path}")]

            result = await asyncio.get_event_loop().run_in_executor(
                None, _post_to_instagram, image_path, caption
            )
            return [types.TextContent(type="text", text=f"Instagram {result}: {Path(image_path).name}")]

        elif name == "queue_instagram":
            image_path = arguments["image_path"]
            caption = arguments["caption"]
            topic = arguments.get("topic", "post")

            if not Path(image_path).exists():
                return [types.TextContent(type="text", text=f"Error: Image not found: {image_path}")]

            vault = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
            queue = vault / "Plans" / "instagram_queue"
            queue.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Caption file banao
            caption_file = queue / f"{topic}_{timestamp}.md"
            caption_file.write_text(f"""---
type: instagram_post
created: {datetime.now().isoformat()}
image: {image_path}
---

{caption}
""")

            # Image copy karo queue mein
            import shutil
            img_src = Path(image_path)
            img_dest = queue / f"{topic}_{timestamp}{img_src.suffix}"
            shutil.copy2(img_src, img_dest)

            return [types.TextContent(type="text", text=f"Instagram post queued: {img_dest.name} + {caption_file.name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())