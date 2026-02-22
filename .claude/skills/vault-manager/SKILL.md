---
name: vault-manager
description: Check vault status, update Dashboard.md, and manage files across folders. Use when user asks for status update, summary, or to organize vault.
---

# Vault Manager Skill

## Steps
1. Count files in /Needs_Action, /Done, /Plans folders
2. Read Dashboard.md current status
3. Update Dashboard.md with:
   - Total pending emails
   - Total completed tasks
   - Last checked timestamp
4. Report summary to user

## Dashboard Update Format
- Pending: X emails
- Completed today: X tasks
- Last updated: [timestamp]