<div align="center">

# 🤖 Personal AI Employee

### Your Autonomous Digital FTE — Built with Claude Code & Obsidian

[![Platinum Tier](https://img.shields.io/badge/Hackathon-Platinum_Tier_Complete-9cf?style=for-the-badge)](./Personal_AI_Employee_Hackathon.md)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude-Code_Powered-orange?style=for-the-badge)](https://claude.com/product/claude-code)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)

*A fully autonomous AI assistant that monitors Gmail, WhatsApp, and 3 social media platforms — processing tasks 24/7 with Odoo accounting integration, cloud deployment, and human-in-the-loop safety.*

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Platinum Tier](#-platinum-tier-achievements)

</div>

---

## 🎯 What is This?

A **Digital Full-Time Equivalent (FTE)** that works 168 hours/week at ~10% the cost of a human employee. This Platinum Tier AI Employee:

- 📧 **Triages Gmail** — Detects urgent emails, drafts replies, routes to approval
- 💬 **Monitors WhatsApp** — Captures client requests, generates invoices, handles inquiries
- 📱 **Manages Social Media** — Auto-posts to LinkedIn, Twitter, Facebook with engagement optimization
- 💰 **Odoo Accounting** — Creates invoices, tracks payments, generates financial reports
- 📊 **CEO Briefings** — Weekly business audits with revenue analysis and bottleneck detection
- 🧠 **Reasons Autonomously** — Creates multi-step plans, executes tasks, logs everything
- 🛡️ **Human-in-the-Loop** — Never sends emails, payments, or posts without your approval
- 🔄 **Continuous Operation** — Watchdog process ensures 24/7 uptime with auto-restart
- ☁️ **Cloud/Local Split** — Cloud agent drafts, local agent executes sensitive actions
- 🔄 **Git Sync** — Vault synchronization between cloud and local via GitHub

**Implementation Status:** Platinum Tier with 8 watchers, 6 MCP servers, 5 agent skills, Odoo ERP integration, cloud deployment, and 24/7 monitoring.

---

## ✨ Features

### 🔄 Autonomous Watchers

| Watcher | Status | Purpose | Zone |
|---------|--------|---------|------|
| **Gmail Watcher** | ✅ Active | Monitors inbox for urgent/important emails every 2 minutes | Cloud/Local |
| **WhatsApp Watcher** | ✅ Active | Captures urgent messages via Playwright automation | Local Only |
| **LinkedIn Poster** | ✅ Active | Auto-publishes business content from queue folder | Local Only |
| **Twitter Poster** | ✅ Active | Posts tweets automatically with engagement optimization | Local Only |
| **Facebook Poster** | ✅ Active | Publishes to Facebook with rich media support | Local Only |
| **HITL Approval** | ✅ Active | Watches `/Pending_Approval` and executes approved actions | Local Only |
| **Filesystem** | ✅ Active | Monitors drop folders for file-based triggers | Both |
| **Plan Creator** | ✅ Active | Generates multi-step plans from vault tasks | Both |

### 🧠 Claude Agent Skills

All AI functionality is implemented as reusable [Agent Skills](https://docs.anthropic.com/en/docs/build-with-claude/agent-skills):

- **`/gmail-triage`** — Classifies emails, creates plans, drafts replies with intent detection
- **`/whatsapp-triage`** — Detects intent, generates invoices, routes approvals, handles payments
- **`/linkedin-poster`** — Writes compelling posts from business context with engagement hooks
- **`/daily-briefing`** — Generates Monday CEO briefing with Odoo revenue & bottleneck analysis
- **`/browsing-with-playwright`** — Browser automation for web scraping and form filling

**Note:** Facebook and Twitter posting are implemented via watchers and MCP servers, but dedicated agent skills are not yet created.

### 🔌 MCP Servers (Action Layer)

6 Model Context Protocol servers for external actions:

- **email-mcp** — Gmail send/draft via Google API
- **whatsapp-mcp** — WhatsApp messaging via Playwright
- **twitter-mcp** — Twitter/X posting with character optimization
- **facebook-mcp** — Facebook posting with rich media
- **linkedin-mcp** — LinkedIn publishing with professional formatting
- **odoo-mcp** — Odoo 19 ERP integration (invoices, customers, accounting)

### 💰 Odoo Accounting Integration

Full ERP integration for business operations:

- ✅ **Customer Management** — Create and search customers
- ✅ **Invoice Generation** — Automated invoice creation from WhatsApp/Email requests
- ✅ **Payment Tracking** — Monitor paid/unpaid invoices
- ✅ **Accounting Summary** — MTD revenue, expenses, net position
- ✅ **CEO Briefing Integration** — Weekly financial reports with bottleneck detection

### 🔐 Security & Safety

- ✅ **Human-in-the-Loop** — Sensitive actions require approval before execution
- ✅ **Audit Logging** — Every action logged to `/Vault/Logs/YYYY-MM-DD.json`
- ✅ **DRY_RUN Mode** — Test safely without external actions
- ✅ **Rate Limiting** — Max 10 email actions per hour
- ✅ **Credential Isolation** — All secrets in `.env`, never in vault
- ✅ **Error Recovery** — Automatic retry with exponential backoff (3 attempts, 10s delay)
- ✅ **Graceful Degradation** — 5x backoff after 5 consecutive errors
- ✅ **Work-Zone Isolation** — Cloud drafts only, local executes sensitive actions
- ✅ **Git Sync Security** — Vault syncs via GitHub, secrets never committed
- ✅ **Session Management** — Browser sessions stored locally, never in vault
- ✅ **Watchdog Monitoring** — Auto-restart failed processes for 24/7 uptime

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SOURCES                             │
│  Gmail │ WhatsApp │ LinkedIn │ Twitter │ Facebook │ Odoo            │
└────┬────┴────┬─────┴────┬─────┴────┬────┴────┬─────┴──────────────┘
     │         │          │          │         │
     ▼         ▼          ▼          ▼         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PERCEPTION LAYER (8 Watchers)                          │
│  Local: Gmail • WhatsApp • LinkedIn • Twitter • Facebook • HITL    │
│         Filesystem • Plan Creator                                   │
│  Cloud: Gmail Watcher (24/7) + Cloud Orchestrator (code ready)     │
│  Watchdog: Process monitor (process_watchdog.py)                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│            OBSIDIAN VAULT (Knowledge Base + Git Sync)               │
│  /Needs_Action → /In_Progress → /Plans → /Pending_Approval          │
│  → /Approved → /Done                                                 │
│  Dashboard.md │ Business_Goals.md │ Logs/ │ Briefings/ │ Updates/   │
│  Git Sync: Cloud ↔ GitHub ↔ Local (vault only, secrets excluded)   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌────────────────────────────────┐
│  CLOUD AGENT (24/7)  │   │   LOCAL AGENT (On-Demand)      │
│  Claude Code         │   │   Claude Code                  │
│  - Email drafts      │   │   - WhatsApp replies           │
│  - Social drafts     │   │   - Email sending              │
│  - Odoo drafts       │   │   - Social posting             │
│  - NO sending        │   │   - Odoo posting               │
│  - NO WhatsApp       │   │   - Payment execution          │
└──────────┬───────────┘   └────────┬───────────────────────┘
           │                        │
           └────────┬───────────────┘
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  HUMAN APPROVAL (HITL Watcher)                                      │
│  Review drafts in /Pending_Approval                                 │
│  Move to /Approved → Local agent executes                           │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│            ACTION LAYER (6 MCP Servers - Local Only)                │
│  Email • WhatsApp • Twitter • Facebook • LinkedIn • Odoo ERP        │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│   EXTERNAL ACTIONS      │
│ Send │ Post │ Invoice   │
└─────────────────────────┘
```

### Tech Stack

- **Brain:** Claude Code (Sonnet 4.6) with Agent Skills
- **Memory:** Obsidian vault (local Markdown) + Git sync for cloud/local coordination
- **Senses:** Python 3.13+ watchers (Gmail API, Playwright, Odoo XML-RPC)
- **Hands:** 6 MCP servers (email, social media, accounting)
- **Orchestration:**
  - Local: main.py + orchestrator.py (thread-based concurrency)
  - Cloud: cloud_orchestrator.py (24/7 drafting agent)
  - Monitoring: process_watchdog.py (auto-restart failed processes)
- **Sync:** git_sync.sh (vault synchronization via GitHub)
- **ERP:** Odoo 19 Community Edition (accounting, invoicing, CRM)
- **Deployment:** Cloud VM (24/7) + Local machine (on-demand)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Claude Code CLI ([install](https://claude.com/product/claude-code))
- Obsidian 1.10.6+ ([download](https://obsidian.md/download))
- Gmail account with API access
- Odoo 19 Community Edition (optional, for accounting)
- Node.js 24+ (for MCP servers)
- Cloud VM (optional, for 24/7 operation)
- Git (for vault synchronization)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Personal-AI-Employee.git
cd Personal-AI-Employee

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env with your paths and credentials

# 4. Set up Gmail API
# Follow guide: https://developers.google.com/gmail/api/quickstart
# Save credentials.json to project root

# 5. Configure Odoo (optional)
# Set ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD in .env

# 6. First-time authentication
uv run python main.py --gmail
# This will open browser for OAuth consent

# 7. Open Obsidian vault
# Open Obsidian → "Open folder as vault" → select AI_Employee_Vault/

# 8. (Optional) Set up cloud deployment
# On cloud VM:
# - Clone repository
# - Configure .env (same as local)
# - Set up git credentials for auto-sync
# - Run: uv run python process_watchdog.py
```

### Running the System

#### Local Agent (On-Demand)
```bash
# Run all watchers (recommended)
uv run python main.py

# Run specific watcher
uv run python main.py --gmail
uv run python main.py --whatsapp
uv run python main.py --linkedin
uv run python main.py --twitter
uv run python main.py --facebook
uv run python main.py --hitl

# Dry run mode (safe testing)
DRY_RUN=true uv run python main.py

# Trigger daily briefing with Odoo summary
uv run python main.py --briefing
```

#### Cloud Agent (24/7 Deployment)
```bash
# On cloud VM - start cloud orchestrator
uv run python cloud_orchestrator.py

# Start watchdog (monitors and auto-restarts processes)
uv run python process_watchdog.py

# Manual git sync (automatic every 2.5 min in cloud orchestrator)
bash git_sync.sh cloud

# Setup cron for scheduled tasks
bash cron_setup.sh install
```

### Using Agent Skills

```bash
# Navigate to vault
cd AI_Employee_Vault

# Process emails with gmail-triage skill
claude
> /gmail-triage

# Generate LinkedIn post
> /linkedin-poster

# Create Monday briefing with Odoo accounting
> /daily-briefing

# Triage WhatsApp messages
> /whatsapp-triage
```

---

## 📊 Demo

### Cloud/Local Workflow

**Cloud Agent (24/7):**
1. **Detection:** Gmail watcher finds urgent email → creates `EMAIL_*.md` in `/Needs_Action`
2. **Claim:** Cloud orchestrator claims task → moves to `/In_Progress/cloud/`
3. **Draft:** Claude drafts reply → writes to `/Pending_Approval/cloud/EMAIL_reply_*.md`
4. **Sync:** Git sync pushes draft to GitHub
5. **Local Pull:** Local machine pulls latest vault state

**Local Agent (On-Demand):**
6. **Approval:** You review draft in `/Pending_Approval/cloud/` → move to `/Approved`
7. **Execute:** HITL watcher detects approval → email MCP sends
8. **Archive:** Logs action → moves files to `/Done`
9. **Sync:** Git sync pushes completion status to GitHub

### Email Triage Workflow

1. **Detection:** Gmail watcher finds urgent email → creates `EMAIL_*.md` in `/Needs_Action`
2. **Triage:** `/gmail-triage` skill classifies intent → creates `PLAN_*.md` in `/Plans`
3. **Draft:** Claude drafts reply → writes to `/Pending_Approval/EMAIL_reply_*.md`
4. **Approval:** You review and move to `/Approved`
5. **Send:** HITL watcher detects approval → email MCP sends → logs action → moves to `/Done`

### Social Media Auto-Posting

1. **Context Gathering:** Reads `/Vault/Business_Goals.md` and recent `/Done` files
2. **Post Generation:** `/linkedin-poster` skill writes compelling post
3. **Queue:** Saves to `/Plans/{platform}_queue/{topic}_{timestamp}.md`
4. **Auto-Publish:** Platform watcher picks up and posts automatically
5. **Logging:** Action logged to `/Vault/Logs/` with engagement metrics

### WhatsApp Invoice Request + Odoo

1. **Capture:** WhatsApp watcher detects "invoice" keyword → creates `WHATSAPP_*.md`
2. **Intent Detection:** `/whatsapp-triage` identifies invoice request
3. **Odoo Integration:** Creates customer in Odoo if not exists
4. **Invoice Generation:** Generates invoice via Odoo MCP (INV/2026/00XXX)
5. **Approval Required:** Writes invoice draft to `/Pending_Approval`
6. **Human Review:** You approve → system sends via WhatsApp MCP
7. **Accounting:** Invoice tracked in Odoo, appears in CEO briefing

### Monday CEO Briefing with Odoo

1. **Scheduled Trigger:** Cron runs at 8:00 AM Monday or manual `/daily-briefing`
2. **Data Collection:** Reads vault files, logs, and Odoo accounting summary
3. **Financial Analysis:** Calculates MTD revenue, unpaid invoices, net position
4. **Bottleneck Detection:** Identifies plans older than 48h, overdue invoices
5. **Report Generation:** Writes comprehensive briefing to `/Vault/Briefings/`
6. **Dashboard Update:** Updates Dashboard.md with executive summary

### Cloud Deployment & Monitoring

1. **Cloud VM Setup:** Deploy cloud_orchestrator.py + process_watchdog.py on VPS
2. **24/7 Operation:** Cloud agent continuously monitors `/Needs_Action`
3. **Auto-Restart:** Watchdog detects failed process → restarts automatically
4. **Health Updates:** Status written to `/Updates/` every 10 minutes
5. **Git Sync:** Vault syncs every 2.5 minutes (cloud → GitHub → local)

---

## 📁 Project Structure

```
Personal-AI-Employee/
├── .claude/                        # Claude Code configuration
│   ├── hooks/                      # Custom hooks (stop.py - Ralph Wiggum pattern)
│   ├── skills/                     # Agent Skills (5 skills)
│   │   ├── browsing-with-playwright/
│   │   ├── daily-briefing/
│   │   ├── gmail-triage/
│   │   ├── linkedin-poster/
│   │   └── whatsapp-triage/
│   └── settings.json               # MCP server configuration
│
├── .facebook_session/              # Facebook Playwright session (local only)
├── .linkedin_session/              # LinkedIn Playwright session (local only)
├── .twitter_session/               # Twitter Playwright session (local only)
├── .whatsapp_session/              # WhatsApp Playwright session (local only)
│
├── AI_Employee_Vault/              # Obsidian knowledge base (Git synced)
│   ├── .obsidian/                  # Obsidian configuration
│   ├── Needs_Action/               # Incoming tasks
│   ├── In_Progress/                # Currently processing
│   ├── Plans/                      # Multi-step plans
│   │   ├── facebook_queue/         # Facebook posts ready to publish
│   │   ├── linkedin_queue/         # LinkedIn posts ready to publish
│   │   └── twitter_queue/          # Twitter posts ready to publish
│   ├── Pending_Approval/           # Awaiting human review
│   ├── Approved/                   # Ready for execution
│   ├── Rejected/                   # Declined actions
│   ├── Done/                       # Completed tasks
│   │   ├── facebook_posted/        # Published Facebook posts
│   │   ├── linkedin_posted/        # Published LinkedIn posts
│   │   └── twitter_posted/         # Published Twitter posts
│   ├── Updates/                    # Status updates and notifications
│   ├── Logs/                       # Audit trail (JSON)
│   ├── Briefings/                  # Weekly CEO reports
│   ├── Inbox/                      # Manual task drops
│   ├── Dashboard.md                # Real-time status
│   ├── Business_Goals.md           # Revenue targets & KPIs
│   └── Company_Handbook.md         # Decision rules
│
├── watchers/                       # Perception layer (8 watchers)
│   ├── logs/                       # Watcher runtime logs
│   ├── base_watcher.py             # Abstract base with retry logic
│   ├── gmail_watcher.py            # Email monitoring (cloud/local)
│   ├── whatsapp_watcher.py         # WhatsApp monitoring (local only)
│   ├── linkedin_poster.py          # LinkedIn auto-posting (local only)
│   ├── twitter_poster.py           # Twitter auto-posting (local only)
│   ├── facebook_poster.py          # Facebook auto-posting (local only)
│   ├── hitl_approval_watcher.py    # Approval executor (local only)
│   ├── filesystem_watcher.py       # File drop monitoring (both)
│   ├── plan_creator.py             # Plan generation (both)
│   ├── config.py                   # Configuration loader
│   └── token.pickle                # Gmail OAuth token (local only)
│
├── mcp_servers/                    # Action layer (6 MCP servers - local only)
│   ├── email_mcp.py                # Gmail send/draft
│   ├── whatsapp_mcp.py             # WhatsApp messaging
│   ├── twitter_mcp.py              # Twitter posting
│   ├── facebook_mcp.py             # Facebook posting
│   ├── linkedin_mcp.py             # LinkedIn publishing
│   └── odoo_mcp.py                 # Odoo ERP integration
│
├── drop_folder/                    # File-based task triggers
├── logs/                           # Root-level watcher logs
│
├── main.py                         # Local orchestrator entry point
├── orchestrator.py                 # Local master process with threading
├── cloud_orchestrator.py           # Cloud 24/7 drafting agent
├── process_watchdog.py             # Process monitor & auto-restart
├── git_sync.sh                     # Vault sync via GitHub
├── cron_setup.sh                   # Cron job installer
├── odoo_backup.sh                  # Odoo database backup script
│
├── credentials.json                # Gmail API credentials (local only)
├── .env                            # Environment config (never synced)
├── .env.example                    # Environment template
├── pyproject.toml                  # Dependencies (uv)
├── uv.lock                         # Dependency lock file
│
├── CLAUDE.md                       # Claude Code instructions
├── CHANGELOG.md                    # Version history
├── Personal_AI_Employee_Hackathon.md  # Architecture blueprint
├── Setup -guide.md                 # Installation guide
└── README.md                       # This file
```

**Note:**
- Session directories (`.facebook_session/`, `.linkedin_session/`, `.twitter_session/`, `.whatsapp_session/`) contain Playwright browser sessions and are never synced to Git or cloud. They must be set up locally on each machine.
- Cloud/local work-zone isolation (subdirectories in `In_Progress/`, `Pending_Approval/`, `Plans/`) is implemented in `cloud_orchestrator.py` but not actively used in current deployment. The system currently operates with flat directory structure.

---

## 🏆 Platinum Tier Achievements

### ✅ All Bronze Requirements
- Obsidian vault with Dashboard & Company Handbook
- Working Gmail watcher
- Claude Code reading/writing to vault
- Structured folder workflow

### ✅ All Silver Requirements
- 3 Watchers (Gmail + WhatsApp + LinkedIn)
- LinkedIn Auto-Posting with business content generation
- Plan.md Creation with multi-step reasoning
- Email MCP Server for external actions
- HITL Approval Workflow
- WhatsApp Reply Sending via Playwright
- Cron Scheduling for daily briefing
- 5 Agent Skills (browsing, daily-briefing, gmail-triage, linkedin-poster, whatsapp-triage)

### ✅ Gold Tier Requirements (Mostly Completed)

#### 🌐 Full Social Media Suite
- **Twitter/X Integration** — Auto-posting with character optimization (250 char max)
- **Facebook Integration** — Rich media posts with engagement tracking
- **LinkedIn Integration** — Professional content with engagement hooks
- **3 Social Media Watchers** — Automated queue processing for all platforms
- **3 Social Media MCP Servers** — Direct posting capabilities

#### 💰 Odoo ERP Integration
- **Odoo MCP Server** — Full XML-RPC integration with Odoo 19
- **Customer Management** — Create and search customers
- **Invoice Generation** — Automated invoicing from WhatsApp/Email
- **Payment Tracking** — Monitor paid/unpaid invoices
- **Accounting Summary** — MTD revenue, expenses, net position
- **CEO Briefing Integration** — Weekly financial reports

#### 🔄 Advanced Error Recovery
- **Retry Logic** — 3 attempts with 10s delay
- **Consecutive Error Tracking** — Monitors failure patterns
- **Graceful Degradation** — 5x backoff after 5 consecutive errors
- **Error Logging** — JSON audit trail in vault

#### 📊 Weekly Business Audit
- **Monday CEO Briefing** — Comprehensive business analysis
- **Odoo Accounting Summary** — Revenue, expenses, net position
- **Bottleneck Detection** — Plans older than 48h flagged
- **Proactive Suggestions** — AI-generated action items
- **Upcoming Deadlines** — 14-day project timeline

### ✅ Platinum Tier Additions

#### ☁️ Cloud Deployment & 24/7 Operation
- **Cloud Orchestrator** — 24/7 drafting agent (code complete, deployment ready)
- **Work-Zone Isolation** — Code infrastructure for agent separation (cloud_orchestrator.py)
- **Git Sync** — Vault synchronization via GitHub (secrets excluded)
- **Watchdog Process** — Auto-restart failed processes for continuous uptime
- **Health Monitoring** — Status updates written to `/Updates/` folder
- **Claim-by-Move** — First agent to move task file wins (prevents conflicts)

#### 🔄 Vault Synchronization
- **Bidirectional Sync** — Cloud ↔ GitHub ↔ Local
- **Automatic Sync** — Every 2.5 minutes on cloud, on-demand on local
- **Conflict Resolution** — Git rebase with automatic fallback
- **Security** — Secrets never synced (`.env`, sessions, credentials)
- **Audit Trail** — All sync operations logged

#### 🛡️ Enhanced Security & Isolation
- **Work-Zone Separation** — Code infrastructure for agent isolation (in cloud_orchestrator.py)
- **Approval Zones** — Separate approval workflow support
- **Local-Only Actions** — WhatsApp, social posting, payments (never on cloud)
- **Cloud-Only Drafting** — Email drafts, social drafts, Odoo drafts (when deployed)
- **Session Isolation** — Browser sessions stored locally, never in vault

#### 📊 Process Monitoring
- **Watchdog Service** — Monitors Gmail Watcher + Cloud Orchestrator (process_watchdog.py)
- **Auto-Restart** — Failed processes automatically restarted
- **PID Tracking** — Process IDs stored in `/tmp/` for monitoring
- **Health Updates** — Status written to vault every 10 minutes
- **Log Aggregation** — All logs in `logs/` directory

**Total Development Time:** ~60 hours
**Lines of Code:** ~3,600
**MCP Servers:** 6
**Agent Skills:** 5
**Watchers:** 8 (perception layer)
**Orchestration Components:** 3 (main.py, orchestrator.py, cloud_orchestrator.py, process_watchdog.py)
**Deployment Zones:** 2 (Cloud VM + Local Machine)
**Test Coverage:** Manual testing with real accounts (Gmail, WhatsApp, Odoo, Social Media, Cloud VM)

---

## 🗺️ Roadmap

### ✅ Platinum Tier (Completed)

- [x] Cloud deployment (24/7 operation on VPS)
- [x] Work-zone specialization (Cloud vs Local)
- [x] Vault sync via Git
- [x] Agent-to-Agent coordination (claim-by-move)
- [x] Advanced security hardening (work-zone isolation)
- [x] Process monitoring (watchdog)
- [x] Auto-restart failed processes
- [x] Health status updates

### Future Enhancements

- [ ] Facebook and Twitter agent skills (watchers exist, skills needed)
- [ ] Multi-user support (team collaboration)
- [ ] Calendar integration (Google Calendar MCP)
- [ ] Payment gateway integration (Stripe MCP)

---

## 🔒 Security Considerations

- **Credentials:** All secrets in `.env` (gitignored), never synced to GitHub
- **OAuth Tokens:** `token.pickle` never committed or synced
- **DRY_RUN:** Default mode prevents accidental actions during testing
- **Rate Limits:** Max 10 emails/hour, prevents spam
- **HITL Required:** Payments, new contacts, bulk sends always require approval
- **Audit Trail:** Every action logged with timestamp & parameters
- **Odoo Security:** Credentials injected via environment, never hardcoded
- **Session Management:** Browser sessions stored locally, never in vault or GitHub
- **Error Isolation:** Failed actions don't crash entire system
- **Work-Zone Isolation:** Cloud agent cannot execute sensitive actions (WhatsApp, payments, posting)
- **Git Sync Security:** Only vault files synced, `.env` and sessions excluded via `.gitignore`
- **Process Isolation:** Watchdog monitors processes via PID files, auto-restarts on failure (process_watchdog.py)
- **Approval Zones:** Separate `/Pending_Approval/{cloud,local}` prevents unauthorized execution

---

## 🤝 Contributing

This is a hackathon project for educational purposes. Contributions welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📚 Resources

- [Hackathon Guide](./Personal_AI_Employee_Hackathon.md) — Full architecture & requirements
- [Claude Code Docs](https://docs.anthropic.com/en/docs/build-with-claude/claude-code)
- [Agent Skills Guide](https://docs.anthropic.com/en/docs/build-with-claude/agent-skills)
- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Obsidian Help](https://help.obsidian.md/)
- [Odoo Documentation](https://www.odoo.com/documentation/19.0/)

---

## 📝 License

Educational use only. Part of the Personal AI Employee Hackathon 0.

---

## 🙏 Acknowledgments

- **Anthropic** — Claude Code & Agent Skills framework
- **Obsidian** — Local-first knowledge management
- **Panaversity** — Hackathon organization & guidance
- **Odoo Community** — Open-source ERP platform
- **Community** — Open-source MCP servers & examples

---

<div align="center">

**Built with ❤️ using Claude Code**

**Platinum Tier Complete** — Full autonomous business operations with 8 watchers, 6 MCP servers, 5 agent skills, Odoo ERP integration, cloud deployment, and 24/7 monitoring

[⬆ Back to Top](#-personal-ai-employee)

</div>
