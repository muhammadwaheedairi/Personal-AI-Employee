"""
WhatsApp Watcher - Silver Tier
Monitors WhatsApp Web for urgent messages using Playwright.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from watchers.base_watcher import BaseWatcher
from watchers.config import Config

URGENT_KEYWORDS = ["urgent", "asap", "invoice", "payment", "help", "emergency", "important"]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class WhatsAppWatcher(BaseWatcher):

    def __init__(self):
        super().__init__(
            vault_path=Config.VAULT_PATH,
            check_interval=Config.WHATSAPP_CHECK_INTERVAL,
        )
        self.session_path = Path(Config.WHATSAPP_SESSION_PATH)
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.processed_ids: set[str] = self._load_processed_ids()

    def _processed_ids_file(self) -> Path:
        return self.logs / "processed_whatsapp.json"

    def _load_processed_ids(self) -> set[str]:
        f = self._processed_ids_file()
        if f.exists():
            return set(json.loads(f.read_text()))
        return set()

    def _save_processed_id(self, msg_id: str) -> None:
        self.processed_ids.add(msg_id)
        self._processed_ids_file().write_text(json.dumps(list(self.processed_ids)))

    def check_for_updates(self) -> list:
        if Config.DRY_RUN:
            self.logger.info("[DRY RUN] Skipping WhatsApp browser session")
            return []

        urgent_messages = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"],
                    user_agent=USER_AGENT
                )
                page = browser.new_page() if not browser.pages else browser.pages[0]
                page.goto("https://web.whatsapp.com")
                self.logger.info("Waiting for WhatsApp Web to load...")
                time.sleep(30)

                title = page.title()
                self.logger.info(f"Page title: {title}")

                # Pane ka poora text lo aur line by line parse karo
                pane = page.query_selector('#pane-side')
                if not pane:
                    self.logger.error("pane-side not found!")
                    browser.close()
                    return []

                pane_text = pane.inner_text()
                lines = pane_text.split('\n')

                # Urgent keywords wali lines dhundo
                for i, line in enumerate(lines):
                    line_lower = line.lower().strip()
                    if any(kw in line_lower for kw in URGENT_KEYWORDS):
                        # Context ke liye surrounding lines bhi lo
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        context = '\n'.join(lines[start:end]).strip()
                        msg_id = str(hash(context))
                        if msg_id not in self.processed_ids:
                            urgent_messages.append({
                                "id": msg_id,
                                "text": context,
                                "matched_line": line.strip()
                            })
                            self.logger.info(f"Urgent message found: {line.strip()}")

                self.logger.info(f"Found {len(urgent_messages)} urgent messages")
                browser.close()

        except Exception as e:
            self.logger.error(f"WhatsApp browser error: {e}", exc_info=True)

        return urgent_messages

    def create_action_file(self, message: dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.needs_action / f"WHATSAPP_{timestamp}.md"

        filepath.write_text(f"""---
type: whatsapp
source: whatsapp_web
received: {datetime.now().isoformat()}
priority: high
status: pending
msg_id: {message['id']}
---

# WhatsApp Urgent Message

**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Priority:** High

## Message Preview
{message['text']}

## Matched Keyword In
{message.get('matched_line', 'N/A')}

## Suggested Actions
- [ ] Reply to sender
- [ ] Generate invoice if requested
- [ ] Escalate if payment-related

---
*Created by WhatsApp Watcher*
""")
        self._save_processed_id(message["id"])
        self.logger.info(f"Created WhatsApp action file: {filepath.name}")
        return filepath