"""
Personal AI Employee - Main Entry Point
Run this file to start the full AI Employee (Gold Tier).
All watchers, HITL approval, and scheduling start automatically.

Usage:
    uv run python main.py             # Full orchestrator (all watchers)
    uv run python main.py --gmail     # Gmail watcher only
    uv run python main.py --whatsapp  # WhatsApp watcher only
    uv run python main.py --linkedin  # LinkedIn poster only
    uv run python main.py --facebook  # Facebook poster only
    uv run python main.py --twitter   # Twitter poster only
    uv run python main.py --hitl      # HITL approval watcher only
    uv run python main.py --briefing  # Trigger weekly CEO briefing
    uv run python main.py --dry-run   # Safe mode (no external actions)
"""

import argparse
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personal AI Employee")
    parser.add_argument("--gmail", action="store_true", help="Run Gmail watcher only")
    parser.add_argument("--whatsapp", action="store_true", help="Run WhatsApp watcher only")
    parser.add_argument("--linkedin", action="store_true", help="Run LinkedIn poster only")
    parser.add_argument("--facebook", action="store_true", help="Run Facebook poster only")
    parser.add_argument("--twitter", action="store_true", help="Run Twitter poster only")
    parser.add_argument("--filesystem", action="store_true", help="Run filesystem watcher only")
    parser.add_argument("--hitl", action="store_true", help="Run HITL approval watcher only")
    parser.add_argument("--briefing", action="store_true", help="Trigger weekly CEO briefing")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Enable DRY_RUN mode (no real external actions)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Allow --dry-run flag to override .env setting
    if args.dry_run:
        os.environ["DRY_RUN"] = "true"
        print("[DRY RUN] Mode enabled — no external actions will be taken")

    # Single-watcher modes (useful for testing individual components)
    if args.gmail:
        from watchers.gmail_watcher import GmailWatcher
        GmailWatcher().run()

    elif args.whatsapp:
        from watchers.whatsapp_watcher import WhatsAppWatcher
        WhatsAppWatcher().run()

    elif args.linkedin:
        from watchers.linkedin_poster import LinkedInPoster
        LinkedInPoster().run()

    elif args.facebook:
        from watchers.facebook_poster import FacebookPoster
        FacebookPoster().run()

    elif args.twitter:
        from watchers.twitter_poster import TwitterPoster
        TwitterPoster().run()

    elif args.filesystem:
        from watchers.filesystem_watcher import FilesystemWatcher
        FilesystemWatcher().run()

    elif args.hitl:
        from watchers.hitl_approval_watcher import HITLApprovalWatcher
        HITLApprovalWatcher().run()

    elif args.briefing:
        from orchestrator import generate_daily_briefing
        generate_daily_briefing()
        print("Daily briefing prompt written to /Plans — run Claude Code to generate it.")

    else:
        # Default: start full orchestrator with all watchers
        from orchestrator import main as run_orchestrator
        run_orchestrator()


if __name__ == "__main__":
    main()