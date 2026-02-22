"""Base watcher class - abstract template for all watchers"""
from abc import ABC, abstractmethod
from pathlib import Path
import logging
import time
from datetime import datetime

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Ensure folders exist
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
    
    def _setup_logger(self):
        """Configure logging for this watcher"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        
        # File handler
        log_file = Path('logs') / f'{self.__class__.__name__}.log'
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
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
        """Check source for new items. Return list of items to process."""
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder for the item."""
        pass
    
    def run(self):
        """Main loop - continuously check for updates"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring interval: {self.check_interval}s')
        self.logger.info(f'Vault path: {self.vault_path}')
        
        while True:
            try:
                items = self.check_for_updates()
                if items:
                    self.logger.info(f'Found {len(items)} new items')
                    for item in items:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created: {filepath.name}')
                else:
                    self.logger.debug('No new items found')
                    
            except KeyboardInterrupt:
                self.logger.info('Shutting down gracefully...')
                break
            except Exception as e:
                self.logger.error(f'Error in main loop: {e}', exc_info=True)
            
            time.sleep(self.check_interval)
