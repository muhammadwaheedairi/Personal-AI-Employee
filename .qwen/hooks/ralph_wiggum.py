#!/usr/bin/env python3
"""
Ralph Wiggum Hook — Qwen Code Version
PostToolUse hook: After every WriteFile/Edit, check if work is complete.
If incomplete work found, sends message back to agent to continue.
"""
import json
import sys
from pathlib import Path

VAULT = Path("AI_Employee_Vault")


def check_incomplete_work() -> list:
    issues = []

    # Needs_Action mein unprocessed files?
    needs_action_files = [
        f for f in (VAULT / "Needs_Action").glob("*.md")
        if f.name != ".gitkeep"
    ]
    if needs_action_files:
        issues.append(
            f"{len(needs_action_files)} unprocessed files in /Needs_Action"
        )

    # Approved mein pending executions?
    approved_files = [
        f for f in (VAULT / "Approved").glob("*.md")
        if f.name != ".gitkeep"
    ]
    if approved_files:
        issues.append(
            f"{len(approved_files)} approved actions pending execution"
        )

    return issues


def main():
    # stdin se Qwen hook event read karo
    try:
        event = json.loads(sys.stdin.read())
    except Exception:
        event = {}

    tool_name = event.get("tool_name", "")
    tool_output = str(event.get("tool_output", ""))

    # Sirf WriteFile/Edit ke baad check karo
    if tool_name not in ("WriteFile", "Edit", "write_file", "str_replace"):
        sys.exit(0)

    # TASK_COMPLETE output mein hai?
    if "TASK_COMPLETE" in tool_output:
        sys.exit(0)

    # Incomplete work check karo
    issues = check_incomplete_work()
    if issues:
        message = (
            f"⚠️ Incomplete work detected: {', '.join(issues)}. "
            f"Please continue working until all tasks are complete. "
            f"Output TASK_COMPLETE when done."
        )
        print(message)
        sys.exit(0)  # Qwen PostToolUse exit code ignored — message matters

    sys.exit(0)


if __name__ == "__main__":
    main()
