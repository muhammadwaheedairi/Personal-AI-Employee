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
@.qwen/skills/gmail-triage/SKILL.md
@.qwen/skills/whatsapp-triage/SKILL.md
@.qwen/skills/linkedin-poster/SKILL.md
@.qwen/skills/facebook-poster/SKILL.md
@.qwen/skills/twitter-poster/SKILL.md
@.qwen/skills/browsing-with-playwright/SKILL.md
@.qwen/skills/daily-briefing/SKILL.md

## Skill Usage Rules
- **gmail-triage**: Use when EMAIL_*.md appears in /Needs_Action or user asks to check/triage emails
- **whatsapp-triage**: Use when WHATSAPP_*.md appears in /Needs_Action or user asks to handle WhatsApp messages
- **linkedin-poster**: Use when user asks to post on LinkedIn or create business content
- **facebook-poster**: Use when user asks to post on Facebook, share business updates, announce milestones, or create community-engaging content
- **twitter-poster**: Use when user asks to post on Twitter/X, share updates, write viral tweets, or create engagement-driving content
- **browsing-with-playwright**: Use when tasks require web browsing, form submission, web scraping, UI testing, or any browser interaction (NOT for static content - use curl/wget instead)
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

## Odoo MCP — Accounting (Gold Tier)
MCP server: `mcp_servers/odoo_mcp.py`
Credentials: injected via `env` block in `~/.qwen/settings.json` under this project's mcpServers config — never hardcoded in code or `.env`.

### Odoo Tool Usage Rules
- **create_customer**: Use when a new client needs to be added to Odoo before invoicing
- **create_invoice**: Use when user asks to generate an invoice — always confirm customer exists first
- **get_invoices**: Use for accounting audit, CEO briefing revenue section, or when user asks for invoice list
- **get_customers**: Use to verify customer exists before creating invoice
- **get_accounting_summary**: Use every Monday in CEO Briefing to populate revenue section

### Odoo Workflow
Invoice request detected → `get_customers` to verify → if missing `create_customer` →
`create_invoice` → log to /Vault/Logs/YYYY-MM-DD.json → update Dashboard.md

### Odoo in CEO Briefing
Every Monday briefing MUST include Odoo accounting summary:
1. Call `get_accounting_summary` with period=`this_month`
2. Add revenue data to /Vault/Briefings/{date}_Briefing.md under ## Revenue section
3. Flag any unpaid invoices as bottlenecks

### Odoo Security Rules
- Invoice creation does NOT require HITL (it is non-destructive)
- Payment marking ALWAYS requires human approval via /Pending_Approval
- Never store Odoo credentials in code or vault — use `~/.qwen/settings.json` env block only

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
---

## Platinum Tier — Cloud vs Local Zone Rules

### Agent Identity
- If running on Cloud VM → I am the **Cloud Agent**
- If running on Local machine → I am the **Local Agent**

### Cloud Agent — Allowed Actions
```
✅ Detect Gmail emails
✅ Create email drafts → write to /Pending_Approval/cloud/
✅ Create plans → write to /Plans/cloud/
✅ Create draft invoices in Odoo (no posting)
✅ Write status updates to /Updates/
✅ Run git_sync.sh cloud after each task
```

### Cloud Agent — Forbidden Actions
```
❌ NEVER send email directly
❌ NEVER touch WhatsApp
❌ NEVER post on social media
❌ NEVER write directly to Dashboard.md
❌ NEVER post or pay invoices in Odoo
```

### Local Agent — Responsibilities
```
✅ Process human approvals
✅ Send final emails via Email MCP
✅ Send WhatsApp messages via WhatsApp MCP
✅ Post to social media (Twitter/LinkedIn/Facebook)
✅ Post Odoo invoices and payments (after approval)
✅ Update Dashboard.md
✅ Merge /Updates/ folder into Dashboard.md
✅ Run git_sync.sh local after each task
```

### Claim-by-Move Rule
```
New task appears in /Needs_Action/
        ↓
Move it to /In_Progress/cloud/
        ↓
Move succeeded = task is mine ✅
Move failed = claimed by another agent ⏭️ SKIP
```

### Folder Zone Ownership
```
/Needs_Action/           ← Watchers write here
/In_Progress/cloud/      ← Cloud claims here
/In_Progress/local/      ← Local claims here
/Plans/cloud/            ← Cloud plans
/Plans/local/            ← Local plans
/Pending_Approval/cloud/ ← Cloud drafts (Local approves)
/Updates/                ← Cloud writes status here
Dashboard.md             ← Local ONLY writes here
```

### Dashboard Update Rule
```
Cloud NEVER writes directly to Dashboard.md
Cloud writes to → /Updates/update_TIMESTAMP.md
Local reads /Updates/ → merges into Dashboard.md
```

### Git Sync Rule
```
After every completed task run:
bash git_sync.sh cloud   # on Cloud VM
bash git_sync.sh local   # on Local machine

Files that sync:
✅ AI_Employee_Vault/
✅ QWEN.md, README.md

Files that NEVER sync:
❌ .env
❌ watchers/token.pickle
❌ .whatsapp_session
❌ .twitter_session
❌ .linkedin_session
❌ .facebook_session
❌ credentials.json
```

### Task Completion Signal
At the end of every autonomous task output:
```
TASK_COMPLETE
```
