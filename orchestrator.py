"""
Orchestrator - Silver Tier
Master process that starts all watchers in background threads
and handles cron-based scheduled tasks (e.g. daily briefing).
Run this single file to start your entire AI Employee.
"""

import logging
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from watchers.config import Config
from watchers.gmail_watcher import GmailWatcher
from watchers.whatsapp_watcher import WhatsAppWatcher
from watchers.linkedin_poster import LinkedInPoster
from watchers.filesystem_watcher import FilesystemWatcher
from watchers.hitl_approval_watcher import HITLApprovalWatcher
from watchers.plan_creator import PlanCreator


# ── Logging setup ─────────────────────────────────────────────────────────── #

def setup_logging() -> logging.Logger:
    log_dir = Config.VAULT_PATH / "Logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "orchestrator.log"),
        ],
    )
    return logging.getLogger("Orchestrator")


logger = setup_logging()


# ── Vault folder bootstrap ────────────────────────────────────────────────── #

def ensure_vault_structure() -> None:
    """Create all required vault folders if they don't exist."""
    folders = [
        Config.NEEDS_ACTION,
        Config.DONE,
        Config.LOGS,
        Config.PLANS,
        Config.PLANS / "linkedin_queue",
        Config.PENDING,
        Config.APPROVED,
        Config.REJECTED,
        Config.VAULT_PATH / "Done" / "linkedin_posted",
        Config.VAULT_PATH / "Briefings",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
    logger.info("Vault folder structure verified")


# ── Thread runner ─────────────────────────────────────────────────────────── #

def _run_in_thread(target_fn, name: str) -> threading.Thread:
    """Start a daemon thread for a watcher's run() method."""
    thread = threading.Thread(target=target_fn, name=name, daemon=True)
    thread.start()
    logger.info(f"Started thread: {name}")
    return thread


# ── Scheduled tasks ───────────────────────────────────────────────────────── #

class Scheduler:
    """
    Lightweight scheduler — checks every minute if a task is due.
    Add tasks as (hour, minute, callable) tuples.
    """

    def __init__(self):
        self._tasks: list[tuple[int, int, callable]] = []
        self._last_run: dict[str, str] = {}   # task_name -> last run date string

    def add_daily(self, hour: int, minute: int, fn: callable) -> None:
        self._tasks.append((hour, minute, fn))

    def tick(self) -> None:
        now = datetime.now()
        for hour, minute, fn in self._tasks:
            if now.hour == hour and now.minute == minute:
                key = f"{fn.__name__}_{now.strftime('%Y-%m-%d')}"
                if self._last_run.get(fn.__name__) != now.strftime("%Y-%m-%d"):
                    logger.info(f"Running scheduled task: {fn.__name__}")
                    try:
                        fn()
                        self._last_run[fn.__name__] = now.strftime("%Y-%m-%d")
                    except Exception as e:
                        logger.error(f"Scheduled task {fn.__name__} failed: {e}", exc_info=True)


def generate_daily_briefing() -> None:
    """
    Trigger Claude Code to read the vault and write a daily briefing.
    Claude reads Needs_Action, Plans, and Done to summarize the day.
    """
    briefing_prompt_file = Config.VAULT_PATH / "Plans" / "PROMPT_daily_briefing.md"
    briefing_prompt_file.write_text(f"""---
type: claude_task
created: {datetime.now().isoformat()}
priority: high
status: pending
---

# Task: Generate Daily Briefing

Read the following and write a briefing to /Vault/Briefings/{datetime.now().strftime('%Y-%m-%d')}_Briefing.md:

1. All files in /Needs_Action/
2. All files in /Done/ (from today)
3. Company_Handbook.md goals

Include:
- Summary of pending actions
- Completed items today
- Proactive suggestions
- Any anomalies or urgent items
""")
    logger.info("Daily briefing prompt written to Plans folder")


# ── Graceful shutdown ─────────────────────────────────────────────────────── #

_shutdown_event = threading.Event()

def _signal_handler(sig, frame):
    logger.info("Shutdown signal received. Stopping orchestrator...")
    _shutdown_event.set()

signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


# ── Main entry point ─────────────────────────────────────────────────────── #

def main() -> None:
    logger.info("=" * 60)
    logger.info("Personal AI Employee - Orchestrator Starting")
    logger.info(f"DRY_RUN mode: {Config.DRY_RUN}")
    logger.info("=" * 60)

    ensure_vault_structure()

    threads = []

    # Start all watchers as daemon threads
    threads.append(_run_in_thread(GmailWatcher().run, "GmailWatcher"))
    threads.append(_run_in_thread(WhatsAppWatcher().run, "WhatsAppWatcher"))
    threads.append(_run_in_thread(LinkedInPoster().run, "LinkedInPoster"))
    threads.append(_run_in_thread(FilesystemWatcher().run, "FilesystemWatcher"))
    threads.append(_run_in_thread(HITLApprovalWatcher().run, "HITLApprovalWatcher"))
    threads.append(_run_in_thread(PlanCreator().run, "PlanCreator"))

    # Setup scheduler
    scheduler = Scheduler()
    scheduler.add_daily(hour=8, minute=0, fn=generate_daily_briefing)

    logger.info("All watchers running. Press Ctrl+C to stop.")

    # Main heartbeat loop
    while not _shutdown_event.is_set():
        scheduler.tick()

        # Log alive threads every 5 minutes
        if datetime.now().minute % 5 == 0 and datetime.now().second < 10:
            alive = [t.name for t in threads if t.is_alive()]
            logger.info(f"Active threads: {alive}")

        time.sleep(10)

    logger.info("Orchestrator stopped cleanly.")


if __name__ == "__main__":
    main()