"""
WhatsApp MCP Server - Gold Tier
MCP implementation for sending WhatsApp messages via Playwright.
"""
import asyncio
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

server = Server("whatsapp")


def _send_whatsapp(to: str, body: str) -> str:
    """Send WhatsApp message using existing WhatsApp watcher."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from watchers.whatsapp_watcher import WhatsAppWatcher
    watcher = WhatsAppWatcher()
    success = watcher.send_reply(to=to, message=body)
    return "sent" if success else "failed"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="send_whatsapp",
            description="Send a WhatsApp message to a phone number",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Phone number with country code e.g. +923001234567"},
                    "body": {"type": "string", "description": "Message text to send"},
                },
                "required": ["to", "body"],
            },
        ),
        types.Tool(
            name="draft_whatsapp",
            description="Draft a WhatsApp reply for human approval — writes to /Pending_Approval",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Phone number with country code"},
                    "body": {"type": "string", "description": "Draft message text"},
                    "context": {"type": "string", "description": "Why this message is being sent"},
                },
                "required": ["to", "body"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    to = arguments["to"]
    body = arguments["body"]

    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would {name} to {to}: {body[:50]}...")]

    try:
        if name == "send_whatsapp":
            result = await asyncio.get_event_loop().run_in_executor(
                None, _send_whatsapp, to, body
            )
            return [types.TextContent(type="text", text=f"WhatsApp {result} to {to}")]

        elif name == "draft_whatsapp":
            from datetime import datetime
            vault = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
            pending = vault / "Pending_Approval"
            pending.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            context = arguments.get("context", "No context provided")
            filepath = pending / f"WHATSAPP_draft_{timestamp}.md"
            filepath.write_text(f"""---
action: send_whatsapp
to: {to}
body: {body}
context: {context}
created: {datetime.now().isoformat()}
status: pending
---

# WhatsApp Draft — Awaiting Approval

**To:** {to}
**Message:** {body}
**Context:** {context}

Move to /Approved to send.
""")
            return [types.TextContent(type="text", text=f"Draft saved to {filepath.name} — move to /Approved to send")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
