"""Configuration loader for watchers"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Explicit .env path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    VAULT_PATH = Path(os.getenv('VAULT_PATH', './AI_Employee_Vault'))
    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', './credentials.json')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 120))
    DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'
    # Folder paths
    NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
    DONE = VAULT_PATH / 'Done'
    LOGS = VAULT_PATH / 'Logs'