"""
HITL Approval Watcher - Silver Tier
Monitors the /Pending_Approval folder for human decisions.
When a file is moved to /Approved, triggers the corresponding MCP action.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from watchers.config import Config


class HITLApprovalWatcher:
    """
    Polls /Pending_Approval for files, waits for human to move them to
    /Approved or /Rejected, then executes or cancels the action.
    """

    POLL_INTERVAL = 10  # seconds

    def __init__(self, logger=None):
        import logging
        self.vault_path = Config.VAULT_PATH
        self.pending_dir = self.vault_path / "Pending_Approval"
        self.approved_dir = self.vault_path / "Approved"
        self.rejected_dir = self.vault_path / "Rejected"
        self.done_dir = self.vault_path / "Done"
        self.logs_dir = self.vault_path / "Logs"
        self.logger = logger or logging.getLogger(self.__class__.__name__)

        for folder in [
            self.pending_dir,
            self.approved_dir,
            self.rejected_dir,
            self.done_dir,
            self.logs_dir,
        ]:
            folder.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    #  Main loop                                                            #
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Poll approved/rejected folders and process decisions."""
        self.logger.info("HITL Approval Watcher started")
        while True:
            try:
                self._process_approved()
                self._process_rejected()
                self._warn_expiring()
            except Exception as e:
                self.logger.error(f"HITL loop error: {e}", exc_info=True)
            time.sleep(self.POLL_INTERVAL)

    # ------------------------------------------------------------------ #
    #  Approval handling                                                    #
    # ------------------------------------------------------------------ #

    def _process_approved(self) -> None:
        for approval_file in self.approved_dir.glob("*.md"):
            metadata = self._parse_frontmatter(approval_file)
            action_type = metadata.get("action", "unknown")

            self.logger.info(f"Processing approved action: {approval_file.name}")

            result = self._dispatch_action(action_type, metadata)

            self._log_approval(
                approval_file.name, action_type, metadata, "approved", result
            )
            # Archive to Done
            dest = self.done_dir / f"APPROVED_{approval_file.name}"
            approval_file.rename(dest)

    def _process_rejected(self) -> None:
        for rejection_file in self.rejected_dir.glob("*.md"):
            metadata = self._parse_frontmatter(rejection_file)
            self.logger.info(f"Action rejected: {rejection_file.name}")
            self._log_approval(
                rejection_file.name,
                metadata.get("action", "unknown"),
                metadata,
                "rejected",
                "skipped_by_human",
            )
            dest = self.done_dir / f"REJECTED_{rejection_file.name}"
            rejection_file.rename(dest)

    def _warn_expiring(self) -> None:
        """Log a warning for approval files nearing their expiry."""
        now = datetime.now()
        for pending_file in self.pending_dir.glob("*.md"):
            metadata = self._parse_frontmatter(pending_file)
            expires_str = metadata.get("expires")
            if not expires_str:
                continue
            try:
                expires = datetime.fromisoformat(expires_str)
                hours_left = (expires - now).total_seconds() / 3600
                if 0 < hours_left < 2:
                    self.logger.warning(
                        f"Approval expiring in {hours_left:.1f}h: {pending_file.name}"
                    )
            except ValueError:
                pass

    # ------------------------------------------------------------------ #
    #  Action dispatcher                                                    #
    # ------------------------------------------------------------------ #

    def _dispatch_action(self, action_type: str, metadata: dict) -> str:
        """Route approved actions to the correct MCP handler."""
        try:
            if action_type == "send_email":
                return self._execute_email(metadata)
            elif action_type == "payment":
                # Payments always require fresh human confirmation — never auto-execute
                self.logger.warning("Payment action approved but requires manual execution")
                return "payment_manual_required"
            else:
                self.logger.warning(f"No handler for action type: {action_type}")
                return "no_handler"
        except Exception as e:
            self.logger.error(f"Action dispatch failed: {e}", exc_info=True)
            return f"error: {e}"

    def _execute_email(self, metadata: dict) -> str:
        """Call email MCP to send the approved email."""
        # Import here to avoid circular imports at module level
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from mcp_servers.email_mcp import send_email

        result = send_email(
            to=metadata.get("to", ""),
            subject=metadata.get("subject", "(no subject)"),
            body=metadata.get("body", ""),
        )
        return result.get("status", "unknown")

    # ------------------------------------------------------------------ #
    #  Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _parse_frontmatter(self, filepath: Path) -> dict:
        """Parse YAML-style frontmatter from a markdown file."""
        metadata = {}
        lines = filepath.read_text().splitlines()
        if not lines or lines[0].strip() != "---":
            return metadata
        try:
            end = lines.index("---", 1)
        except ValueError:
            return metadata

        for line in lines[1:end]:
            if ":" in line:
                key, _, value = line.partition(":")
                metadata[key.strip()] = value.strip()
        return metadata

    def _log_approval(
        self,
        filename: str,
        action_type: str,
        metadata: dict,
        decision: str,
        result: str,
    ) -> None:
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "actor": "hitl_approval_watcher",
            "filename": filename,
            "decision": decision,
            "metadata": metadata,
            "result": result,
        }
        logs = json.loads(log_file.read_text()) if log_file.exists() else []
        logs.append(entry)
        log_file.write_text(json.dumps(logs, indent=2))