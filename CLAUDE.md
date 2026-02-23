# Personal AI Employee — Claude Code Config

## Project
Silver-tier autonomous AI Employee. Vault: `./AI_Employee_Vault/`. All tasks flow through
Obsidian markdown files: Watchers → /Needs_Action → Plans → /Pending_Approval → /Approved → /Done.

## Run commands
```bash
uv run python main.py --dry-run     # safe test, no external actions
uv run python main.py               # full orchestrator (all watchers)
uv run python main.py --gmail       # single watcher
uv run python main.py --briefing    # trigger daily briefing
./cron_setup.sh install             # install cron jobs (Mac/Linux)
./cron_setup.sh windows             # Windows Task Scheduler instructions
```

## Skills
@.claude/skills/gmail-triage/SKILL.md
@.claude/skills/whatsapp-triage/SKILL.md
@.claude/skills/linkedin-poster/SKILL.md
@.claude/skills/daily-briefing/SKILL.md

## Vault rules — MUST follow
- NEVER delete files — move to /Done instead
- NEVER send email or WhatsApp directly — write to /Pending_Approval first
- ALWAYS log every external action to /Vault/Logs/YYYY-MM-DD.json
- ALWAYS end autonomous tasks with `<promise>TASK_COMPLETE</promise>`
- DRY_RUN=true in .env during development — check before any send action

## Workflow
New task in /Needs_Action → create Plan.md in /Plans → execute steps →
sensitive action needs approval → write /Pending_Approval file → await human →
/Approved triggers MCP → log → move all files to /Done → update Dashboard.md

## Code style
- Python 3.13+, type hints on all function signatures
- All watchers extend BaseWatcher from `watchers/base_watcher.py`
- Config always from `watchers/config.py` — never hardcode paths
- Secrets only via environment variables — never in vault or code

## Security
- DRY_RUN=true is the default — confirm it is false before live actions
- Payments always require HITL — never auto-approve any payment action
- Credentials: `.env` file only, never commit (already in .gitignore)