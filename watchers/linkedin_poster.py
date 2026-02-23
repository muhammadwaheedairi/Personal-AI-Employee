"""
LinkedIn Poster - Silver Tier
Auto-posts business content to LinkedIn using Playwright.
Reads post content from /Vault/Plans/linkedin_queue/ folder.
"""

import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class LinkedInPoster(BaseWatcher):

    def __init__(self):
        super().__init__(
            vault_path=Config.VAULT_PATH,
            check_interval=Config.LINKEDIN_CHECK_INTERVAL,
        )
        self.queue_dir = self.vault_path / "Plans" / "linkedin_queue"
        self.posted_dir = self.vault_path / "Done" / "linkedin_posted"
        self.session_path = Path(Config.LINKEDIN_SESSION_PATH)

        for folder in [self.queue_dir, self.posted_dir, self.session_path]:
            folder.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        pending = list(self.queue_dir.glob("*.md"))
        self.logger.info(f"Found {len(pending)} post(s) in LinkedIn queue")
        return pending

    def create_action_file(self, post_file: Path) -> Path:
        post_text = self._extract_post_text(post_file)

        if Config.DRY_RUN:
            self.logger.info(f"[DRY RUN] Would post to LinkedIn:\n{post_text[:200]}...")
            return self._archive_post(post_file, status="dry_run")

        success = self._post_to_linkedin(post_text)
        status = "posted" if success else "failed"
        return self._archive_post(post_file, status=status)

    def _post_to_linkedin(self, text: str) -> bool:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=["--no-sandbox",
                    "--host-resolver-rules=MAP linkedin.com 150.171.22.12, MAP www.linkedin.com 150.171.22.12", "--disable-dev-shm-usage"],
                    user_agent=USER_AGENT
                )
                page = browser.new_page() if not browser.pages else browser.pages[0]
                page.goto("https://www.linkedin.com/feed/")
                self.logger.info("Waiting for LinkedIn feed to load...")
                time.sleep(20)

                title = page.title()
                self.logger.info(f"Page title: {title}")

                # Login check
                if "login" in page.url.lower() or "signin" in page.url.lower():
                    self.logger.error("LinkedIn session expired — please re-login")
                    browser.close()
                    return False

                # Click "Start a post"
                start_post = None
                for selector in [
                    '[data-control-name="share.sharebox_focus_text"]',
                    'button:has-text("Start a post")',
                    '[placeholder*="start a post" i]',
                ]:
                    start_post = page.query_selector(selector)
                    if start_post:
                        break

                if not start_post:
                    self.logger.error("Could not find 'Start a post' button")
                    browser.close()
                    return False

                start_post.click()
                time.sleep(2)

                # Type post content
                editor = page.query_selector('.ql-editor')
                if not editor:
                    self.logger.error("LinkedIn post editor not found")
                    browser.close()
                    return False

                editor.fill(text)
                time.sleep(1)

                # Click Post button
                post_btn = page.get_by_role("button", name="Post", exact=True)
                post_btn.click()
                time.sleep(3)

                browser.close()
                self.logger.info("Successfully posted to LinkedIn")
                return True

        except Exception as e:
            self.logger.error(f"LinkedIn post failed: {e}", exc_info=True)
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = self.posted_dir / f"{post_file.stem}_{status}_{timestamp}.md"
        post_file.rename(dest)
        self.logger.info(f"Archived post [{status}]: {dest.name}")
        return dest
