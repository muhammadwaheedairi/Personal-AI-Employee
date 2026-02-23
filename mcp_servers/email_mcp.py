"""
Email MCP Server - Silver Tier
Proper MCP implementation using the mcp library.
"""
import asyncio
import pickle
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CREDENTIALS_PATH = Path(os.getenv("GMAIL_CREDENTIALS_PATH", "./credentials.json"))
TOKEN_PATH = Path(os.getenv("GMAIL_TOKEN_PATH", "./watchers/token.pickle"))
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

server = Server("email")

def _get_service():
    creds = None
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, "wb") as f:
                pickle.dump(creds, f)
        else:
            raise RuntimeError("Gmail token not found. Run --gmail --dry-run first.")
    return build("gmail", "v1", credentials=creds)

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="send_email",
            description="Send an email via Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body"},
                },
                "required": ["to", "subject", "body"],
            },
        ),
        types.Tool(
            name="draft_email",
            description="Create a Gmail draft",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    to = arguments["to"]
    subject = arguments["subject"]
    body = arguments["body"]

    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would {name} to {to}: {subject}")]

    try:
        service = _get_service()
        msg = MIMEMultipart()
        msg["to"] = to
        msg["subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        if name == "send_email":
            service.users().messages().send(userId="me", body={"raw": raw}).execute()
            return [types.TextContent(type="text", text=f"Email sent to {to}")]
        else:
            service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
            return [types.TextContent(type="text", text=f"Draft created for {to}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
