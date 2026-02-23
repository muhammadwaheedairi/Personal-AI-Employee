"""
Configuration loader for all watchers and services.
All values read from environment variables (via .env file).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of this file's directory)
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


class Config:
    # ── Core paths ─────────────────────────────────────────────────── #
    VAULT_PATH = Path(os.getenv("VAULT_PATH", "./AI_Employee_Vault"))
    DROP_FOLDER_PATH = os.getenv("DROP_FOLDER_PATH", "./drop_folder")

    # ── Gmail ──────────────────────────────────────────────────────── #
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "./credentials.json")
    GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "./watchers/token.pickle")
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "120"))          # seconds

    # ── WhatsApp ───────────────────────────────────────────────────── #
    WHATSAPP_SESSION_PATH = os.getenv("WHATSAPP_SESSION_PATH", "./.whatsapp_session")
    WHATSAPP_CHECK_INTERVAL = int(os.getenv("WHATSAPP_CHECK_INTERVAL", "30"))

    # ── LinkedIn ───────────────────────────────────────────────────── #
    LINKEDIN_SESSION_PATH = os.getenv("LINKEDIN_SESSION_PATH", "./.linkedin_session")
    LINKEDIN_CHECK_INTERVAL = int(os.getenv("LINKEDIN_CHECK_INTERVAL", "300"))

    # ── Behaviour ─────────────────────────────────────────────────── #
    DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

    # ── Derived vault sub-paths (convenience) ─────────────────────── #
    NEEDS_ACTION = VAULT_PATH / "Needs_Action"
    DONE         = VAULT_PATH / "Done"
    LOGS         = VAULT_PATH / "Logs"
    PLANS        = VAULT_PATH / "Plans"
    PENDING      = VAULT_PATH / "Pending_Approval"
    APPROVED     = VAULT_PATH / "Approved"
    REJECTED     = VAULT_PATH / "Rejected"