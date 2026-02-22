---
name: email-triage
description: Process pending emails from Needs_Action folder. Use when new emails arrive or when user asks to check emails, process inbox, or triage messages.
---

# Email Triage Skill

## Steps
1. Read all .md files in /Needs_Action folder
2. For each email check priority (high/medium)
3. If priority is HIGH:
   - Create a reply draft in /Plans folder
   - Suggest 3 action options
4. If priority is MEDIUM:
   - Add to pending list in Dashboard.md
5. Move processed files to /Done folder
6. Update Dashboard.md with summary

## Rules
- NEVER send emails automatically
- NEVER delete any file
- Always create Plan.md before any action
- Flag anything money-related for human approval
- Keep replies professional and concise