# Personal AI Employee — Claude Code Config

## Project
Gold-tier autonomous AI Employee. Vault: `./AI_Employee_Vault/`. All tasks flow through
Obsidian markdown files: Watchers → /Needs_Action → Plans → /Pending_Approval → /Approved → /Done.

## Run commands
```bash
uv run python main.py --dry-run       # safe test, no external actions
uv run python main.py                 # full orchestrator (all watchers)
uv run python main.py --gmail         # Gmail watcher only
uv run python main.py --whatsapp      # WhatsApp watcher only
uv run python main.py --linkedin      # LinkedIn poster only
uv run python main.py --twitter       # Twitter poster only
uv run python main.py --facebook      # Facebook poster only
uv run python main.py --instagram     # Instagram poster only
uv run python main.py --hitl          # HITL approval watcher only
uv run python main.py --briefing      # trigger weekly CEO briefing
./cron_setup.sh install               # install cron jobs (Mac/Linux)
./cron_setup.sh windows               # Windows Task Scheduler instructions
```

## Skills
@.claude/skills/gmail-triage/SKILL.md
@.claude/skills/whatsapp-triage/SKILL.md
@.claude/skills/linkedin-poster/SKILL.md
@.claude/skills/daily-briefing/SKILL.md

## Skill Usage Rules
- **gmail-triage**: Use when EMAIL_*.md appears in /Needs_Action or user asks to check/triage emails
- **whatsapp-triage**: Use when WHATSAPP_*.md appears in /Needs_Action or user asks to handle WhatsApp messages
- **linkedin-poster**: Use when user asks to post on LinkedIn or create business content
- **daily-briefing**: Use when PROMPT_daily_briefing.md appears in /Plans, on Monday mornings, or when user asks for weekly summary/CEO briefing/business audit

## Vault rules — MUST follow
- NEVER delete files — move to /Done instead
- NEVER send email or WhatsApp directly — write to /Pending_Approval first
- NEVER post on social media without checking queue folder first
- ALWAYS log every external action to /Vault/Logs/YYYY-MM-DD.json
- ALWAYS end autonomous tasks with `TASK_COMPLETE`
- DRY_RUN=true in .env during development — check before any send action

## Workflow
New task in /Needs_Action → load appropriate skill → create Plan.md in /Plans → execute steps →
sensitive action needs approval → write /Pending_Approval file → await human →
/Approved triggers MCP or watcher → log → move all files to /Done → update Dashboard.md

## Social Media Queues
- LinkedIn posts → /Plans/linkedin_queue/*.md → `uv run python main.py --linkedin`
- Twitter posts  → /Plans/twitter_queue/*.md  → `uv run python main.py --twitter`
- Facebook posts → /Plans/facebook_queue/*.md → `uv run python main.py --facebook`
- Instagram posts→ /Plans/instagram_queue/*.md→ `uv run python main.py --instagram`

## Weekly CEO Briefing Workflow
Triggered every Monday at 8 AM or when user asks for briefing:
1. Load **daily-briefing** skill
2. Read Business_Goals.md, Done/ files, Logs/*.json
3. Detect bottlenecks — Plans older than 48h still pending
4. Write briefing to /Vault/Briefings/{YYYY-MM-DD}_Briefing.md
5. Update Dashboard.md with Last Briefing date
6. Move PROMPT_daily_briefing.md to /Done/

## Code style
- Python 3.13+, type hints on all function signatures
- All watchers extend BaseWatcher from `watchers/base_watcher.py`
- Config always from `watchers/config.py` — never hardcode paths
- Secrets only via environment variables — never in vault or code

## Security
- DRY_RUN=true is the default — confirm it is false before live actions
- Payments always require HITL — never auto-approve any payment action
- Credentials: `.env` file only, never commit (already in .gitignore)
- WhatsApp/Email sends always require human approval via /Approved folder