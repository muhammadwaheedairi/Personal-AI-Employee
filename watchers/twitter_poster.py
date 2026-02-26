"""
Twitter/X Poster - Gold Tier
Auto-posts to Twitter/X using Playwright (browser automation).
No API cost - uses web interface directly.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
SESSION_PATH = ".twitter_session"


class TwitterPoster(BaseWatcher):

    def __init__(self):
        super().__init__(
            vault_path=Config.VAULT_PATH,
            check_interval=300,
        )
        self.queue_path = self.vault_path / "Plans" / "twitter_queue"
        self.posted_path = self.vault_path / "Done" / "twitter_posted"
        self.session_path = Path(SESSION_PATH)
        self.queue_path.mkdir(parents=True, exist_ok=True)
        self.posted_path.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        posts = list(self.queue_path.glob("*.md"))
        self.logger.info(f"Found {len(posts)} post(s) in Twitter queue")
        return posts

    def create_action_file(self, item: Path) -> Path:
        tweet_text = self._extract_post_text(item)

        # 250 character limit
        if len(tweet_text) > 250:
            tweet_text = tweet_text[:247] + "..."

        if Config.DRY_RUN:
            self.logger.info(f"[DRY RUN] Would tweet: {tweet_text[:100]}...")
            return self._archive_post(item, "dry_run")

        success = self._post_tweet(tweet_text)
        status = "posted" if success else "failed"
        return self._archive_post(item, status)

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

    def _load_cookies(self) -> list:
        cookies_file = self.session_path / "cookies.json"
        if not cookies_file.exists():
            self.logger.error("cookies.json not found in .twitter_session/")
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

    def _post_tweet(self, text: str) -> bool:
        """Post tweet using Playwright - LinkedIn approach."""
        try:
            pw_cookies = self._load_cookies()
            if not pw_cookies:
                return False

            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--host-resolver-rules=MAP x.com 172.66.0.227, MAP twitter.com 172.66.0.227",
                    ],
                    user_agent=USER_AGENT,
                )
                browser.add_cookies(pw_cookies)

                # LinkedIn approach: use existing page
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto("https://x.com/home", wait_until="domcontentloaded")
                self.logger.info("Waiting for X/Twitter to load...")
                time.sleep(20)

                title = page.title()
                self.logger.info(f"Page title: {title}")

                if "login" in page.url.lower():
                    self.logger.error("Twitter session expired!")
                    browser.close()
                    return False

                # Tweet box dhundo
                tweet_box = None
                for selector in [
                    '[data-testid="tweetTextarea_0"]',
                    '[aria-label="Post text"]',
                    '[placeholder="What is happening?!"]',
                ]:
                    tweet_box = page.query_selector(selector)
                    if tweet_box:
                        self.logger.info(f"Tweet box found: {selector}")
                        break

                if not tweet_box:
                    self.logger.error("Tweet box not found!")
                    page.screenshot(path="/tmp/twitter_debug.png")
                    browser.close()
                    return False

                # LinkedIn style: fill directly
                tweet_box.click()
                time.sleep(2)
                tweet_box.fill(text)
                time.sleep(2)

                # Post button dhundo
                post_btn = None
                for selector in [
                    '[data-testid="tweetButtonInline"]',
                    '[data-testid="tweetButton"]',
                ]:
                    post_btn = page.query_selector(selector)
                    if post_btn:
                        self.logger.info(f"Post button found: {selector}")
                        break

                if not post_btn:
                    self.logger.error("Post button not found!")
                    browser.close()
                    return False

                page.keyboard.press("Escape")
                time.sleep(1)
                post_btn.click(force=True)
                time.sleep(5)
                self.logger.info("Tweet posted successfully!")
                browser.close()
                return True

        except Exception as e:
            self.logger.error(f"Twitter post error: {e}", exc_info=True)
            return False