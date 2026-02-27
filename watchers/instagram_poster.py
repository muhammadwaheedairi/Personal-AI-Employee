"""
Instagram Poster - Gold Tier
Auto-posts images to Instagram using Playwright.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

SESSION_PATH    = ".instagram_session"
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
BROWSER_ARGS    = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--window-size=1280,900",
]


class InstagramPoster(BaseWatcher):

    def __init__(self):
        super().__init__(vault_path=Config.VAULT_PATH, check_interval=300)
        self.queue_path   = self.vault_path / "Plans" / "instagram_queue"
        self.posted_path  = self.vault_path / "Done"  / "instagram_posted"
        self.session_path = Path(SESSION_PATH)
        self.queue_path.mkdir(parents=True, exist_ok=True)
        self.posted_path.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

    # ── BaseWatcher ───────────────────────────────────────────────

    def check_for_updates(self) -> list:
        posts = []
        for ext in IMAGE_EXTENSIONS:
            for img in self.queue_path.glob(f"*{ext}"):
                caption_file = img.with_suffix(".md")
                posts.append({
                    "image": img,
                    "caption_file": caption_file if caption_file.exists() else None,
                })
        self.logger.info(f"Found {len(posts)} image(s) in Instagram queue")
        return posts

    def create_action_file(self, item: dict) -> Path:
        image_path = item["image"]
        caption    = self._get_caption(item["caption_file"], image_path)
        if Config.DRY_RUN:
            self.logger.info(f"[DRY RUN] Would post: {image_path.name}")
            return self._archive(image_path, item["caption_file"], "dry_run")
        success = self._post_to_instagram(str(image_path), caption)
        return self._archive(image_path, item["caption_file"], "posted" if success else "failed")

    # ── Helpers ───────────────────────────────────────────────────

    def _get_caption(self, caption_file, image_path: Path) -> str:
        if caption_file and caption_file.exists():
            raw   = caption_file.read_text()
            lines = raw.splitlines()
            if lines and lines[0].strip() == "---":
                try:
                    end   = lines.index("---", 1)
                    lines = lines[end + 1:]
                except ValueError:
                    pass
            caption = "\n".join(lines).strip()
            if caption:
                return caption
        return f"#{image_path.stem.replace('_', '')} #AI #Automation #BuildingInPublic"

    def _load_cookies(self) -> list:
        cookies_file = self.session_path / "cookies.json"
        if not cookies_file.exists():
            self.logger.error("cookies.json not found in .instagram_session/")
            return []
        pw_cookies = []
        for c in json.load(open(cookies_file)):
            cookie = {
                "name":     c["name"],
                "value":    c["value"],
                "domain":   c["domain"],
                "path":     c.get("path", "/"),
                "secure":   c.get("secure", False),
                "httpOnly": c.get("httpOnly", False),
            }
            if c.get("expirationDate"):
                cookie["expires"] = int(c["expirationDate"])
            pw_cookies.append(cookie)
        return pw_cookies

    def _click_next(self, page):
        for sel in [
            '[role="button"]:has-text("Next")',
            'button:has-text("Next")',
            '[aria-label="Next"]',
        ]:
            try:
                page.wait_for_selector(sel, timeout=20000).click()
                time.sleep(2)
                return
            except Exception:
                continue
        self.logger.warning("Next button not found")

    # ── Core Flow ─────────────────────────────────────────────────

    def _post_to_instagram(self, image_path: str, caption: str) -> bool:
        try:
            pw_cookies = self._load_cookies()
            if not pw_cookies:
                return False

            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=not bool(os.environ.get("DISPLAY")),
                    args=BROWSER_ARGS,
                    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 900},
                    slow_mo=80,
                )
                browser.add_cookies(pw_cookies)
                page = browser.pages[0] if browser.pages else browser.new_page()

                # Remove webdriver fingerprint so Instagram renders properly
                page.add_init_script(
                    "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
                )

                # Step 1 — Validate session
                page.goto("https://www.instagram.com", wait_until="domcontentloaded")
                try:
                    page.wait_for_selector('[aria-label="New post"], [aria-label="Create"]', timeout=20000)
                except Exception:
                    pass
                time.sleep(2)
                if "login" in page.url.lower():
                    self.logger.error("Session expired — re-export cookies.json!")
                    browser.close()
                    return False
                self.logger.info("Session valid")

                # Step 2 — Click New Post → Post menu item
                new_post_btn = None
                for sel in ['[aria-label="New post"]', '[aria-label="Create"]', 'a[href="/create/style/"]']:
                    new_post_btn = page.query_selector(sel)
                    if new_post_btn:
                        break
                if not new_post_btn:
                    self.logger.error("New post button not found!")
                    browser.close()
                    return False

                new_post_btn.click()
                time.sleep(2)

                # Click "Post" from the popover menu
                for sel in ['span:text-is("Post")', 'a[href="/create/style/"]', 'div[role="menu"] >> text=Post']:
                    try:
                        page.wait_for_selector(sel, timeout=8000).click()
                        self.logger.info("Post menu item clicked")
                        time.sleep(2)
                        break
                    except Exception:
                        continue

                # Step 3 — Upload image
                try:
                    page.wait_for_selector('text=Select from computer', timeout=15000)
                except Exception:
                    pass

                # Unhide file input and set file directly
                page.evaluate("""
                    document.querySelectorAll('input[type="file"]').forEach(el => {
                        el.style.cssText = 'display:block!important;visibility:visible!important;'
                            + 'opacity:1!important;position:fixed!important;top:0;left:0;width:1px;height:1px;';
                        el.removeAttribute('hidden');
                        el.removeAttribute('aria-hidden');
                    });
                """)
                time.sleep(0.5)
                try:
                    page.locator('input[accept*="image"], input[accept*="video"], input[type="file"]') \
                        .first.set_input_files(image_path, timeout=10000)
                    self.logger.info("Image uploaded")
                except Exception:
                    # Fallback: file chooser
                    with page.expect_file_chooser(timeout=20000) as fc:
                        page.click('text=Select from computer')
                    fc.value.set_files(image_path)
                    self.logger.info("Image uploaded via file chooser")

                # Step 4 — Wait for crop preview, then Next
                try:
                    page.wait_for_selector('button:has-text("Next"), [aria-label="Select crop"]', timeout=20000)
                except Exception:
                    time.sleep(5)
                self._click_next(page)
                self.logger.info("Crop — Next clicked")

                # Step 5 — Filter → Next
                self._click_next(page)
                self.logger.info("Filter — Next clicked")

                # Step 6 — Type caption
                for sel in [
                    '[aria-label="Write a caption..."]',
                    '[aria-label="Write a caption\u2026"]',
                    'div[contenteditable="true"][role="textbox"]',
                    'div[contenteditable="true"]',
                    'textarea',
                ]:
                    try:
                        box = page.wait_for_selector(sel, timeout=10000)
                        box.click()
                        time.sleep(0.5)
                        page.keyboard.type(caption, delay=40)
                        self.logger.info("Caption typed")
                        break
                    except Exception:
                        continue

                # Step 7 — Share
                for sel in [
                    'div[role="dialog"] >> text=Share',
                    '[role="button"]:has-text("Share")',
                    'button:has-text("Share")',
                    'div[role="dialog"] button:has-text("Post")',
                    'button:has-text("Post")',
                ]:
                    try:
                        page.wait_for_selector(sel, timeout=8000).click()
                        self.logger.info("Share clicked")
                        break
                    except Exception:
                        continue
                else:
                    self.logger.error("Share button not found!")
                    browser.close()
                    return False

                time.sleep(8)
                self.logger.info("✅ Posted to Instagram successfully!")
                browser.close()
                return True

        except Exception as e:
            self.logger.error(f"Instagram post error: {e}", exc_info=True)
            return False

    # ── Archive ───────────────────────────────────────────────────

    def _archive(self, image_path: Path, caption_file, status: str) -> Path:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        dest = self.posted_path / f"{image_path.stem}_{status}_{ts}{image_path.suffix}"
        image_path.rename(dest)
        if caption_file and Path(caption_file).exists():
            Path(caption_file).rename(self.posted_path / f"{image_path.stem}_{status}_{ts}.md")
        self.logger.info(f"Archived [{status}]: {dest.name}")
        return dest