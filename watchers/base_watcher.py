"""Base watcher class - abstract template for all watchers"""
from abc import ABC, abstractmethod
from pathlib import Path
import logging
import time
from datetime import datetime


class BaseWatcher(ABC):
    MAX_RETRIES = 3
    RETRY_DELAY = 10  # seconds

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval
        self.consecutive_errors = 0
        self.logger = self._setup_logger()
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

    def _setup_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        log_file = Path('logs') / f'{self.__class__.__name__}.log'
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(console)
        logger.addHandler(file_handler)
        return logger

    @abstractmethod
    def check_for_updates(self) -> list:
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        pass

    def _check_with_retry(self) -> list:
        """Check for updates with retry logic on failure."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                items = self.check_for_updates()
                self.consecutive_errors = 0
                return items
            except KeyboardInterrupt:
                raise
            except Exception as e:
                self.logger.error(
                    f"Attempt {attempt}/{self.MAX_RETRIES} failed: {e}",
                    exc_info=True
                )
                if attempt < self.MAX_RETRIES:
                    self.logger.info(f"Retrying in {self.RETRY_DELAY}s...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    self.consecutive_errors += 1
                    self.logger.error(
                        f"All {self.MAX_RETRIES} attempts failed. "
                        f"Consecutive errors: {self.consecutive_errors}"
                    )
                    self._log_error(str(e))
        return []

    def _log_error(self, error: str) -> None:
        """Log error to vault logs for audit trail."""
        try:
            import json
            log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"
            entry = {
                "timestamp": datetime.now().isoformat(),
                "action_type": "watcher_error",
                "actor": self.__class__.__name__,
                "error": error,
                "consecutive_errors": self.consecutive_errors,
            }
            logs = json.loads(log_file.read_text()) if log_file.exists() else []
            logs.append(entry)
            log_file.write_text(json.dumps(logs, indent=2))
        except Exception:
            pass

    def run(self):
        """Main loop with error recovery and graceful degradation."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring interval: {self.check_interval}s')
        self.logger.info(f'Vault path: {self.vault_path}')

        while True:
            try:
                items = self._check_with_retry()
                if items:
                    self.logger.info(f'Found {len(items)} new items')
                    for item in items:
                        try:
                            filepath = self.create_action_file(item)
                            self.logger.info(f'Created: {filepath.name}')
                        except Exception as e:
                            self.logger.error(f'Failed to create action file: {e}')
                else:
                    self.logger.debug('No new items found')

                # Graceful degradation - longer wait after many errors
                if self.consecutive_errors >= 5:
                    wait = self.check_interval * 5
                    self.logger.warning(
                        f"Too many errors ({self.consecutive_errors}), "
                        f"backing off {wait}s"
                    )
                    time.sleep(wait)
                else:
                    time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info('Shutting down gracefully...')
                break
