#!/usr/bin/env python3
"""
Cloud Orchestrator - Runs on Cloud VM 24/7
Cloud Zone: Email triage + social drafts + Odoo drafts (NO sending, NO WhatsApp)
"""
import subprocess
import time
import logging
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/cloud_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path(os.getenv('VAULT_PATH', 'AI_Employee_Vault'))
CHECK_INTERVAL = 30
AGENT = 'cloud'


def claim_task(task_file: Path) -> bool:
    """Claim-by-move rule — first agent to move wins"""
    in_progress_dir = VAULT_PATH / 'In_Progress' / AGENT
    in_progress_dir.mkdir(parents=True, exist_ok=True)
    dest = in_progress_dir / task_file.name
    try:
        shutil.move(str(task_file), str(dest))
        logger.info(f"✅ Claimed: {task_file.name}")
        return True
    except FileNotFoundError:
        logger.info(f"⏭️ Already claimed: {task_file.name}")
        return False


def process_email_task(task_file: Path):
    """Process EMAIL_*.md — draft reply only, NO sending"""
    logger.info(f"📧 Processing email: {task_file.name}")
    prompt = f"""
You are the Cloud AI Agent. DRAFT ONLY zone.

Read: AI_Employee_Vault/In_Progress/cloud/{task_file.name}

Steps:
1. Read email content
2. Classify intent (invoice/inquiry/complaint/other)
3. Create plan → /Plans/cloud/PLAN_{task_file.stem}.md
4. Create draft reply → /Pending_Approval/cloud/EMAIL_reply_{task_file.stem}.md
5. Write update → /Updates/update_{task_file.stem}.md
6. Move task file → /Done/

CRITICAL:
- DO NOT send email directly
- DO NOT use email MCP send tool
- ONLY write draft to /Pending_Approval/cloud/
- Local agent sends after human approval
- End with TASK_COMPLETE
"""
    _run_qwen(prompt, 'email_triage', task_file.name)


def process_social_draft(task_file: Path, platform: str):
    """Process social media draft — queue only, NO posting"""
    logger.info(f"📱 Processing {platform} draft: {task_file.name}")
    prompt = f"""
You are the Cloud AI Agent. DRAFT ONLY zone.

Read: AI_Employee_Vault/In_Progress/cloud/{task_file.name}

Steps:
1. Read the content/topic
2. Write an engaging {platform} post draft
3. Save draft → /Plans/cloud/{platform}_queue/{task_file.stem}_draft.md
4. Write update → /Updates/update_{task_file.stem}.md
5. Move task file → /Done/

CRITICAL:
- DO NOT post on {platform} directly
- DO NOT use any social media MCP tool
- ONLY write draft to /Plans/cloud/{platform}_queue/
- Local agent posts after human approval
- End with TASK_COMPLETE
"""
    _run_qwen(prompt, f'{platform}_draft', task_file.name)


def process_odoo_draft(task_file: Path):
    """Process Odoo invoice draft — NO posting"""
    logger.info(f"💰 Processing Odoo draft: {task_file.name}")
    prompt = f"""
You are the Cloud AI Agent. DRAFT ONLY zone.

Read: AI_Employee_Vault/In_Progress/cloud/{task_file.name}

Steps:
1. Read invoice request details
2. Use Odoo MCP to check if customer exists (get_customers)
3. If customer missing — create via Odoo MCP (create_customer)
4. Create DRAFT invoice via Odoo MCP (create_invoice) — status stays DRAFT
5. Write approval request → /Pending_Approval/cloud/INVOICE_{task_file.stem}.md
6. Write update → /Updates/update_{task_file.stem}.md
7. Move task file → /Done/

CRITICAL:
- Create invoice in DRAFT status only
- DO NOT post/confirm invoice
- DO NOT mark any payment
- Local agent posts invoice after human approval
- End with TASK_COMPLETE
"""
    _run_qwen(prompt, 'odoo_draft', task_file.name)


def _run_qwen(prompt: str, action_type: str, target: str):
    """Run Qwen Code headless"""
    try:
        result = subprocess.run(
            ['qwen', '-p', prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.getcwd()
        )
        if 'TASK_COMPLETE' in result.stdout:
            logger.info(f"✅ Completed: {target}")
            log_action(action_type, target, 'success')
        else:
            logger.warning(f"⚠️ Incomplete: {target}")
            log_action(action_type, target, 'incomplete')
    except subprocess.TimeoutExpired:
        logger.error(f"❌ Timeout: {target}")
        log_action(action_type, target, 'timeout')
    except Exception as e:
        logger.error(f"❌ Error {target}: {e}")
        log_action(action_type, target, 'error')


def git_sync():
    """Pull latest + push new work to GitHub"""
    try:
        subprocess.run(['git', 'pull', '--rebase'],
                      capture_output=True, timeout=30)
        subprocess.run(['git', 'add', 'AI_Employee_Vault/'],
                      capture_output=True, timeout=10)
        result = subprocess.run(
            ['git', 'diff', '--staged', '--quiet'],
            capture_output=True
        )
        if result.returncode != 0:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            subprocess.run(
                ['git', 'commit', '-m', f'cloud: vault update {timestamp}'],
                capture_output=True, timeout=15
            )
            subprocess.run(['git', 'push'],
                          capture_output=True, timeout=30)
            logger.info("✅ Git sync complete")
    except Exception as e:
        logger.error(f"❌ Git sync failed: {e}")


def log_action(action_type: str, target: str, result: str):
    """Log to vault"""
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'{today}.json'
    logs = []
    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text())
        except Exception:
            logs = []
    logs.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'cloud_orchestrator',
        'target': target,
        'result': result
    })
    log_file.write_text(json.dumps(logs, indent=2))


def check_needs_action():
    """Check /Needs_Action/ for cloud tasks"""
    needs_action = VAULT_PATH / 'Needs_Action'
    if not needs_action.exists():
        return

    # Email tasks
    for f in needs_action.glob('EMAIL_*.md'):
        if claim_task(f):
            process_email_task(VAULT_PATH / 'In_Progress' / AGENT / f.name)
            git_sync()

    # Social draft tasks
    for platform in ['twitter', 'linkedin', 'facebook']:
        for f in needs_action.glob(f'SOCIAL_{platform.upper()}_*.md'):
            if claim_task(f):
                process_social_draft(
                    VAULT_PATH / 'In_Progress' / AGENT / f.name,
                    platform
                )
                git_sync()

    # Odoo draft tasks
    for f in needs_action.glob('INVOICE_*.md'):
        if claim_task(f):
            process_odoo_draft(VAULT_PATH / 'In_Progress' / AGENT / f.name)
            git_sync()


def main():
    logger.info("☁️ Cloud Orchestrator started — 24/7 mode")
    logger.info(f"Vault: {VAULT_PATH} | Agent: {AGENT}")

    # Ensure all required dirs exist
    for folder in [
        'In_Progress/cloud', 'In_Progress/local',
        'Plans/cloud', 'Plans/local',
        'Plans/cloud/twitter_queue',
        'Plans/cloud/linkedin_queue',
        'Plans/cloud/facebook_queue',
        'Pending_Approval/cloud', 'Pending_Approval/local',
        'Updates'
    ]:
        (VAULT_PATH / folder).mkdir(parents=True, exist_ok=True)

    Path('logs').mkdir(exist_ok=True)

    iteration = 0
    while True:
        iteration += 1
        check_needs_action()

        # Git sync every 5 iterations (2.5 min)
        if iteration % 5 == 0:
            git_sync()

        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
