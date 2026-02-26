"""
Instagram Poster - Gold Tier
Auto-posts to Instagram using Playwright.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
SESSION_PATH = ".instagram_session"
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--host-resolver-rules=MAP www.instagram.com 157.240.202.174, MAP instagram.com 157.240.202.174",
]


class InstagramPoster(BaseWatcher):

    def __init__(self):
        super().__init__(
            vault_path=Config.VAULT_PATH,
            check_interval=300,
        )
        self.queue_path = self.vault_path / "Plans" / "instagram_queue"
        self.posted_path = self.vault_path / "Done" / "instagram_posted"
        self.session_path = Path(SESSION_PATH)
        self.queue_path.mkdir(parents=True, exist_ok=True)
        self.posted_path.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        posts = list(self.queue_path.glob("*.md"))
        self.logger.info(f"Found {len(posts)} post(s) in Instagram queue")
        return posts

    def create_action_file(self, item: Path) -> Path:
        text = self._extract_post_text(item)

        if Config.DRY_RUN:
            self.logger.info(f"[DRY RUN] Would post to Instagram: {text[:100]}...")
            return self._archive_post(item, "dry_run")

        success = self._post_to_instagram(text)
        status = "posted" if success else "failed"
        return self._archive_post(item, status)

    def _load_cookies(self) -> list:
        cookies_file = self.session_path / "cookies.json"
        if not cookies_file.exists():
            self.logger.error("cookies.json not found in .instagram_session/")
            return []
        with open(cookies_file) as f:
            cookies_data = json.load(f)
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
        return pw_cookies

    def _post_to_instagram(self, text: str) -> bool:
        try:
            pw_cookies = self._load_cookies()
            if not pw_cookies:
                return False

            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=BROWSER_ARGS,
                    user_agent=USER_AGENT,
                )
                browser.add_cookies(pw_cookies)
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto("https://www.instagram.com", wait_until="domcontentloaded")
                self.logger.info("Waiting for Instagram to load...")
                time.sleep(20)

                title = page.title()
                self.logger.info(f"Page title: {title}")

                if "login" in page.url.lower():
                    self.logger.error("Instagram session expired!")
                    browser.close()
                    return False

                # New post button dhundo
                new_post = None
                for selector in [
                    'a[href="/create/style/"]',
                    '[aria-label="New post"]',
                    'svg[aria-label="New post"]',
                ]:
                    new_post = page.query_selector(selector)
                    if new_post:
                        self.logger.info(f"New post button found: {selector}")
                        break

                if not new_post:
                    self.logger.error("Instagram new post button not found!")
                    page.screenshot(path="/tmp/ig_debug.png")
                    browser.close()
                    return False

                new_post.click()
                time.sleep(3)
                self.logger.info("Instagram post flow initiated!")
                browser.close()
                return True

        except Exception as e:
            self.logger.error(f"Instagram post error: {e}", exc_info=True)
            return False

    def _extract_post_text(self, post_file: Path) -> str:
        raw = post_file.read_text()
        lines = raw.splitlines()
        if lines and lines[0].strip() == "---":
            try:
                end = lines.index("---", 1)
                lines = lines[end + 1:]
            except ValueError:
                pass
        return "\n".join(lines).strip()

    def _archive_post(self, post_file: Path, status: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        dest = self.posted_path / f"{post_file.stem}_{status}_{timestamp}.md"
        post_file.rename(dest)
        self.logger.info(f"Archived [{status}]: {dest.name}")
        return dest
