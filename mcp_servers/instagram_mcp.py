"""
Instagram MCP Server - Gold Tier
MCP implementation for posting to Instagram via Playwright.
Uses Gemini API for AI image generation.
"""
import asyncio
import os
import base64
import tempfile
from pathlib import Path
from datetime import datetime

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_IMAGE_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict"

server = Server("instagram")


async def _generate_image(prompt: str) -> str:
    """Generate image using Gemini Imagen API, return temp file path."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{GEMINI_IMAGE_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    # Base64 image extract karo
    image_b64 = data["predictions"][0]["bytesBase64Encoded"]
    image_bytes = base64.b64decode(image_b64)

    # Temp file mein save karo
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    tmp.write(image_bytes)
    tmp.close()
    return tmp.name


def _post_to_instagram(image_path: str, caption: str) -> str:
    """Post image + caption to Instagram via Playwright."""
    import sys
    import time
    import json
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from playwright.sync_api import sync_playwright

    SESSION_PATH = ".instagram_session"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    cookies_file = Path(SESSION_PATH) / "cookies.json"
    if not cookies_file.exists():
        return "failed: cookies.json not found"

    cookies_data = json.load(open(cookies_file))
    pw_cookies = []
    for c in cookies_data:
        cookie = {
            "name": c["name"], "value": c["value"],
            "domain": c["domain"], "path": c.get("path", "/"),
            "secure": c.get("secure", False), "httpOnly": c.get("httpOnly", False),
        }
        if c.get("expirationDate"):
            cookie["expires"] = int(c["expirationDate"])
        pw_cookies.append(cookie)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                SESSION_PATH, headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage",
                      "--host-resolver-rules=MAP www.instagram.com 157.240.202.174, MAP instagram.com 157.240.202.174"],
                user_agent=USER_AGENT,
            )
            browser.add_cookies(pw_cookies)
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("https://www.instagram.com", wait_until="domcontentloaded")
            time.sleep(20)

            if "login" in page.url.lower():
                browser.close()
                return "failed: session expired"

            # New post button click
            new_post = page.query_selector('[aria-label="New post"]')
            if not new_post:
                new_post = page.query_selector('a[href="/create/style/"]')
            if not new_post:
                browser.close()
                return "failed: new post button not found"

            new_post.click()
            time.sleep(3)

            # File upload
            file_input = page.query_selector('input[type="file"]')
            if file_input:
                file_input.set_input_files(image_path)
                time.sleep(5)
            else:
                browser.close()
                return "failed: file input not found"

            # Next button x2
            for step in ["Select crop", "Add filters", "Add caption"]:
                next_btn = page.get_by_role("button", name="Next")
                if next_btn:
                    next_btn.click()
                    time.sleep(3)

            # Caption type karo
            caption_box = page.query_selector('textarea[aria-label="Write a caption..."]')
            if not caption_box:
                caption_box = page.query_selector('[contenteditable="true"]')
            if caption_box:
                caption_box.fill(caption)
                time.sleep(2)

            # Share button click
            share_btn = page.get_by_role("button", name="Share")
            if share_btn:
                share_btn.click()
                time.sleep(8)
                browser.close()
                return "posted"

            browser.close()
            return "failed: share button not found"

    except Exception as e:
        return f"failed: {e}"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_instagram",
            description="Generate an AI image using Gemini and post it to Instagram with a caption",
            inputSchema={
                "type": "object",
                "properties": {
                    "caption": {"type": "string", "description": "Instagram post caption with hashtags"},
                    "image_prompt": {"type": "string", "description": "Prompt for Gemini to generate the image"},
                },
                "required": ["caption", "image_prompt"],
            },
        ),
        types.Tool(
            name="queue_instagram",
            description="Queue an Instagram post — writes to /Plans/instagram_queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "caption": {"type": "string", "description": "Post caption"},
                    "image_prompt": {"type": "string", "description": "Image generation prompt"},
                    "topic": {"type": "string", "description": "Topic/slug for filename"},
                },
                "required": ["caption", "image_prompt"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would {name}: {str(arguments)[:100]}")]

    try:
        if name == "post_instagram":
            caption = arguments["caption"]
            image_prompt = arguments["image_prompt"]

            # Step 1: Image generate karo
            image_path = await _generate_image(image_prompt)

            # Step 2: Instagram pe post karo
            result = await asyncio.get_event_loop().run_in_executor(
                None, _post_to_instagram, image_path, caption
            )

            # Cleanup
            Path(image_path).unlink(missing_ok=True)

            return [types.TextContent(type="text", text=f"Instagram {result}")]

        elif name == "queue_instagram":
            caption = arguments["caption"]
            image_prompt = arguments["image_prompt"]
            topic = arguments.get("topic", "post")
            vault = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
            queue = vault / "Plans" / "instagram_queue"
            queue.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = queue / f"{topic}_{timestamp}.md"
            filepath.write_text(f"""---
type: instagram_post
created: {datetime.now().isoformat()}
image_prompt: {image_prompt}
---

{caption}
""")
            return [types.TextContent(type="text", text=f"Instagram post queued: {filepath.name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
