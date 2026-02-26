#!/usr/bin/env python3
"""
Ralph Wiggum Stop Hook
Checks if task is truly complete before Claude stops.
If incomplete work found, returns exit code 1 to continue.
"""
import json
import sys
from pathlib import Path

VAULT = Path("AI_Employee_Vault")

def check_incomplete_work():
    issues = []
    
    # Needs_Action mein files hain?
    needs_action = list((VAULT / "Needs_Action").glob("*.md"))
    if needs_action:
        issues.append(f"{len(needs_action)} unprocessed files in Needs_Action")
    
    # Approved mein files hain jo execute nahi hui?
    approved = list((VAULT / "Approved").glob("*.md"))
    if approved:
        issues.append(f"{len(approved)} approved actions pending execution")
    
    return issues

def main():
    # stdin se Claude ka stop event read karo
    try:
        event = json.loads(sys.stdin.read())
    except:
        event = {}
    
    # TASK_COMPLETE check karo
    transcript = event.get("transcript", [])
    last_messages = str(transcript[-3:]) if transcript else ""
    
    if "TASK_COMPLETE" in last_messages:
        sys.exit(0)  # Claude rok sakte hain
    
    # Incomplete work check karo
    issues = check_incomplete_work()
    if issues:
        print(f"Incomplete work found: {', '.join(issues)}. Continue working.")
        sys.exit(1)  # Claude ko continue karne do
    
    sys.exit(0)  # Sab theek hai, rok sakte hain

if __name__ == "__main__":
    main()
