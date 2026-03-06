# Personal AI Employee — Claude Code Config

## Project
Platinum-tier autonomous AI Employee. Vault: `./AI_Employee_Vault/`. All tasks flow through
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
uv run python main.py --hitl          # HITL approval watcher only
uv run python main.py --briefing      # trigger weekly CEO briefing
./cron_setup.sh install               # install cron jobs (Mac/Linux)
./cron_setup.sh windows               # Windows Task Scheduler instructions
```

## Skills
@.claude/skills/plan-creator/SKILL.md
@.claude/skills/gmail-triage/SKILL.md
@.claude/skills/gmail-sender/SKILL.md
@.claude/skills/whatsapp-triage/SKILL.md
@.claude/skills/whatsapp-sender/SKILL.md
@.claude/skills/hitl-approval/SKILL.md
@.claude/skills/linkedin-poster/SKILL.md
@.claude/skills/twitter-poster/SKILL.md
@.claude/skills/facebook-poster/SKILL.md
@.claude/skills/browsing-with-playwright/SKILL.md
@.claude/skills/daily-briefing/SKILL.md
@.claude/skills/subscription-audit/SKILL.md
@.claude/skills/odoo-accounting/SKILL.md
@.claude/skills/calendar-scheduler/SKILL.md

## Skill Usage Rules

**Meta-Orchestration:**
- **plan-creator**: Use when any new file appears in /Needs_Action or user asks to create a plan/analyze a task. This meta-skill orchestrates the workflow by creating structured Plan.md files with steps, resources, and timeline.

**Safety:**
- **hitl-approval**: Use BEFORE executing any sensitive action (payments, unknown contacts, bulk operations, deletions, config changes). Intercepts sensitive actions, writes approval request to /Pending_Approval/, waits for human decision, and only executes after explicit approval.

**Email Communication:**
- **gmail-triage**: Use when EMAIL_*.md appears in /Needs_Action or user asks to check/triage emails
- **gmail-sender**: Use when email files appear in /Approved or user asks to send emails/execute approved replies

**WhatsApp Communication:**
- **whatsapp-triage**: Use when WHATSAPP_*.md appears in /Needs_Action or user asks to handle WhatsApp messages
- **whatsapp-sender**: Use when WhatsApp files appear in /Approved or user asks to send WhatsApp messages

**Social Media:**
- **linkedin-poster**: Use when user asks to post on LinkedIn, create business content, or announce milestones (1,300 char limit)
- **twitter-poster**: Use when user asks to post on Twitter/X, share updates, or write viral tweets (250 char limit)
- **facebook-poster**: Use when user asks to post on Facebook, share business updates, or write community-engaging content (40-80 words optimal)

**Utilities:**
- **browsing-with-playwright**: Use when tasks require web browsing, form submission, web scraping, UI testing, or any browser interaction (NOT for static content - use curl/wget instead)
- **daily-briefing**: Use when PROMPT_daily_briefing.md appears in /Plans, on Monday mornings, or when user asks for weekly summary/CEO briefing/business audit
- **subscription-audit**: Use when PROMPT_subscription_audit.md appears in /Plans, on Sunday nights, or when user asks to audit subscriptions/check recurring payments/find unused services
- **odoo-accounting**: Use when user asks to create invoice, add customer, check revenue, or get accounting summary. Always verifies customer exists, routes invoice creation to /Pending_Approval/, and integrates with CEO briefing
- **calendar-scheduler**: Use when user asks to schedule meeting, check availability, create reminder, or get upcoming events. Always checks availability before scheduling, routes meeting creation to /Pending_Approval/, and integrates with CEO briefing

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

## Weekly CEO Briefing Workflow
Triggered every Monday at 8 AM or when user asks for briefing:
1. Load **daily-briefing** skill
2. Read Business_Goals.md, Done/ files, Logs/*.json
3. Detect bottlenecks — Plans older than 48h still pending
4. Write briefing to /Vault/Briefings/{YYYY-MM-DD}_Briefing.md
5. Update Dashboard.md with Last Briefing date
6. Move PROMPT_daily_briefing.md to /Done/

## Odoo MCP — Accounting (Gold Tier)
MCP server: `mcp_servers/odoo_mcp.py`
Credentials: injected via `env` block in `~/.claude/settings.json` under this project's mcpServers config — never hardcoded in code or `.env`.

### Odoo Tool Usage Rules
- **create_customer**: Use when a new client needs to be added to Odoo before invoicing
- **create_invoice**: Use when user asks to generate an invoice — always confirm customer exists first
- **get_invoices**: Use for accounting audit, CEO briefing revenue section, or when user asks for invoice list
- **get_customers**: Use to verify customer exists before creating invoice
- **get_accounting_summary**: Use every Monday in CEO Briefing to populate revenue section

### Odoo Workflow
Invoice request detected → load **odoo-accounting** skill → verify customer exists with `get_customers` →
if missing `create_customer` → create approval request in /Pending_Approval/ → await human approval →
`create_invoice` → log to /Vault/Logs/YYYY-MM-DD.json → update Dashboard.md

### Odoo in CEO Briefing
Every Monday briefing MUST include Odoo accounting summary:
1. Call `get_accounting_summary` with period=`this_month`
2. Add revenue data to /Vault/Briefings/{date}_Briefing.md under ## Revenue section
3. Flag any unpaid invoices as bottlenecks

### Odoo Security Rules
- Invoice creation ALWAYS requires human approval via /Pending_Approval (create_invoice posts immediately)
- Customer creation does NOT require approval (non-destructive, can be edited later)
- Payment marking ALWAYS requires human approval via /Pending_Approval
- Never store Odoo credentials in code or vault — use `~/.claude/settings.json` env block only
- Always use odoo-accounting skill for invoice workflows — never call create_invoice directly

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