"""
Filesystem Watcher - Silver Tier
Watches a local drop folder for new files and creates action items.
Uses watchdog library for efficient OS-level file system events.
"""

import shutil
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from watchers.config import Config


class DropFolderHandler(FileSystemEventHandler):
    """Handles new file events in the monitored drop folder."""

    def __init__(self, needs_action: Path, logs_path: Path, logger):
        self.needs_action = needs_action
        self.logger = logger

    def on_created(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Skip hidden/temp files
        if source.name.startswith(".") or source.suffix in {".tmp", ".part"}:
            return

        dest = self.needs_action / f"FILE_{source.name}"
        shutil.copy2(source, dest)
        self._create_metadata(source, dest)
        self.logger.info(f"Detected new file: {source.name}")

    def _create_metadata(self, source: Path, dest: Path) -> None:
        """Create companion .md file describing the dropped file."""
        meta_path = self.needs_action / f"FILE_{source.stem}_meta.md"
        meta_path.write_text(f"""---
type: file_drop
original_name: {source.name}
size_bytes: {source.stat().st_size}
received: {datetime.now().isoformat()}
status: pending
---

# New File: {source.name}

**Dropped:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Size:** {source.stat().st_size:,} bytes
**Type:** {source.suffix.upper() or 'Unknown'}

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize and file appropriately
- [ ] Extract data if applicable

---
*Created by Filesystem Watcher*
""")


class FilesystemWatcher:
    """
    Wraps watchdog Observer to monitor a drop folder.
    Standalone (does not extend BaseWatcher) since watchdog uses event callbacks,
    not a polling loop.
    """

    def __init__(self, logger=None):
        import logging
        self.vault_path = Config.VAULT_PATH
        self.watch_folder = Path(Config.DROP_FOLDER_PATH)
        self.needs_action = self.vault_path / "Needs_Action"
        self.logs = self.vault_path / "Logs"
        self.logger = logger or logging.getLogger(self.__class__.__name__)

        # Ensure folders exist
        for folder in [self.watch_folder, self.needs_action, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """Start watching the drop folder indefinitely."""
        self.logger.info(f"Watching drop folder: {self.watch_folder}")
        handler = DropFolderHandler(self.needs_action, self.logs, self.logger)
        observer = Observer()
        observer.schedule(handler, str(self.watch_folder), recursive=False)
        observer.start()

        try:
            while True:
                import time
                time.sleep(5)
        except KeyboardInterrupt:
            self.logger.info("Filesystem watcher shutting down")
            observer.stop()
        finally:
            observer.join()