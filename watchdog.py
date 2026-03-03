#!/usr/bin/env python3
"""
Watchdog - Monitor and restart critical cloud processes
Runs on Cloud VM to keep Gmail Watcher + Orchestrator alive 24/7
"""
import subprocess
import time
import logging
import os
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/watchdog.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Processes to monitor (Cloud VM only)
PROCESSES = {
    'gmail_watcher': {
        'cmd': 'uv run python main.py --gmail',
        'pid_file': '/tmp/gmail_watcher.pid'
    },
    'cloud_orchestrator': {
        'cmd': 'uv run python cloud_orchestrator.py',
        'pid_file': '/tmp/cloud_orchestrator.pid'
    }
}

VAULT_PATH = Path(os.getenv('VAULT_PATH', 'AI_Employee_Vault'))
CHECK_INTERVAL = 60  # Check every 60 seconds


def is_process_running(pid_file: str) -> bool:
    """Check if process is running via PID file"""
    pid_path = Path(pid_file)
    if not pid_path.exists():
        return False
    try:
        pid = int(pid_path.read_text().strip())
        # Check if process exists
        os.kill(pid, 0)
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        return False


def start_process(name: str, config: dict) -> bool:
    """Start a process and save its PID"""
    try:
        proc = subprocess.Popen(
            config['cmd'].split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        Path(config['pid_file']).write_text(str(proc.pid))
        logger.info(f"Started {name} with PID {proc.pid}")
        return True
    except Exception as e:
        logger.error(f"Failed to start {name}: {e}")
        return False


def write_health_update(status: dict):
    """Write health status to /Updates/ for Local to merge"""
    updates_dir = VAULT_PATH / 'Updates'
    updates_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    update_file = updates_dir / f'health_{timestamp}.md'
    
    content = f"""---
type: health_update
source: cloud_watchdog
timestamp: {datetime.now().isoformat()}
---

## Cloud Health Status

"""
    for name, running in status.items():
        icon = "✅" if running else "❌"
        content += f"- {icon} {name}: {'Running' if running else 'Restarted'}\n"
    
    update_file.write_text(content)


def check_and_restart():
    """Check all processes and restart if needed"""
    status = {}
    
    for name, config in PROCESSES.items():
        running = is_process_running(config['pid_file'])
        
        if not running:
            logger.warning(f"{name} not running — restarting...")
            success = start_process(name, config)
            status[name] = success
            if success:
                logger.info(f"✅ {name} restarted successfully")
            else:
                logger.error(f"❌ {name} failed to restart")
        else:
            status[name] = True
            logger.debug(f"✅ {name} is running")
    
    return status


def main():
    logger.info("🐕 Watchdog started — monitoring cloud processes")
    
    # Ensure logs directory exists
    Path('logs').mkdir(exist_ok=True)
    
    # Initial start of all processes
    logger.info("Starting all processes...")
    for name, config in PROCESSES.items():
        if not is_process_running(config['pid_file']):
            start_process(name, config)
    
    # Monitor loop
    iteration = 0
    while True:
        time.sleep(CHECK_INTERVAL)
        iteration += 1
        
        status = check_and_restart()
        
        # Write health update every 10 iterations (10 min)
        if iteration % 10 == 0:
            write_health_update(status)
            logger.info(f"Health update written to /Updates/")


if __name__ == '__main__':
    main()
