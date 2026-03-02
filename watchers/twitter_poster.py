"""
Twitter/X Poster - Gold Tier
Auto-posts to Twitter/X using Playwright (browser automation).
No API cost - uses web interface directly.
Session managed via cookies.json — refresh manually when expired.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
SESSION_PATH = Config.TWITTER_SESSION_PATH


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
            self.logger.error("No cookies.json found! Run session setup first.")
            return []
        with open(cookies_file) as f:
            cookies_data = json.load(f)
        pw_cookies = []
        for c in cookies_data:
            cookie = {
                "name": c["name"], "value": c["value"],
                "domain": c.get("domain", ".x.com"),
                "path": c.get("path", "/"),
                "secure": c.get("secure", False),
                "httpOnly": c.get("httpOnly", False),
            }
            if c.get("expirationDate"):
                cookie["expires"] = int(c["expirationDate"])
            elif c.get("expires") and c["expires"] > 0:
                cookie["expires"] = int(c["expires"])
            pw_cookies.append(cookie)
        return pw_cookies

    def _save_cookies(self, browser) -> None:
        cookies = browser.cookies()
        cookies_file = self.session_path / "cookies.json"
        with open(cookies_file, "w") as f:
            json.dump(cookies, f, indent=2)
        self.logger.info(f"Session saved: {len(cookies)} cookies")

    def _post_tweet(self, text: str) -> bool:
        try:
            pw_cookies = self._load_cookies()
            if not pw_cookies:
                return False

            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=not bool(os.environ.get("DISPLAY")),
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled",
                        "--host-resolver-rules=MAP x.com 172.66.0.227, MAP twitter.com 172.66.0.227",
                    ],
                    user_agent=USER_AGENT,
                    slow_mo=80,
                )

                browser.add_cookies(pw_cookies)
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto("https://x.com/home", wait_until="domcontentloaded")
                self.logger.info("Waiting for X/Twitter to load...")
                time.sleep(20)

                self.logger.info(f"Page title: {page.title()}")

                # Session expired check
                if "login" in page.url.lower() or "i/flow" in page.url.lower():
                    self.logger.error("Session expired! Please refresh cookies.json manually.")
                    browser.close()
                    return False

                # Find tweet box
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

                # Click and type
                tweet_box.click()
                time.sleep(2)
                self.logger.info("Typing tweet via keyboard...")
                page.keyboard.type(text, delay=30)
                time.sleep(3)

                # Verify text entered
                content = tweet_box.inner_text().strip()
                self.logger.info(f"Tweet box content: '{content[:80]}'")

                if not content:
                    self.logger.error("Text not entered in tweet box!")
                    page.screenshot(path="/tmp/twitter_debug.png")
                    browser.close()
                    return False

                # Submit via Ctrl+Enter
                self.logger.info("Submitting tweet via Ctrl+Enter...")
                page.keyboard.press("Control+Enter")
                time.sleep(3)

                # Verify submission
                submitted = False
                for i in range(20):
                    time.sleep(1)
                    try:
                        box = page.query_selector('[data-testid="tweetTextarea_0"]')
                        if box:
                            content = box.inner_text().strip()
                            self.logger.info(f"Wait {i+1}s: box='{content[:50]}'")
                            if content == "":
                                self.logger.info("Tweet box empty — submitted!")
                                submitted = True
                                break
                        else:
                            self.logger.info("Tweet box gone — submitted!")
                            submitted = True
                            break
                    except Exception:
                        submitted = True
                        break

                if not submitted:
                    self.logger.error("Tweet submission failed!")
                    browser.close()
                    return False

                self._save_cookies(browser)
                self.logger.info("Tweet posted successfully!")
                browser.close()
                return True

        except Exception as e:
            self.logger.error(f"Twitter post error: {e}", exc_info=True)
            return False