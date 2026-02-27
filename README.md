<div align="center">

# 🤖 Personal AI Employee

### Your Autonomous Digital FTE — Built with Claude Code & Obsidian

[![Gold Tier](https://img.shields.io/badge/Hackathon-Gold_Tier_Complete-gold?style=for-the-badge)](./Personal_AI_Employee_Hackathon.md)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude-Code_Powered-orange?style=for-the-badge)](https://claude.com/product/claude-code)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)

*A fully autonomous AI assistant that monitors Gmail, WhatsApp, and 4 social media platforms — processing tasks 24/7 with Odoo accounting integration and human-in-the-loop safety.*

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Gold Tier](#-gold-tier-achievements)

</div>

---

## 🎯 What is This?

A **Digital Full-Time Equivalent (FTE)** that works 168 hours/week at ~10% the cost of a human employee. This Gold Tier AI Employee:

- 📧 **Triages Gmail** — Detects urgent emails, drafts replies, routes to approval
- 💬 **Monitors WhatsApp** — Captures client requests, generates invoices, handles inquiries
- 📱 **Manages Social Media** — Auto-posts to LinkedIn, Twitter, Facebook, Instagram
- 💰 **Odoo Accounting** — Creates invoices, tracks payments, generates financial reports
- 📊 **CEO Briefings** — Weekly business audits with revenue analysis and bottleneck detection
- 🧠 **Reasons Autonomously** — Creates multi-step plans, executes tasks, logs everything
- 🛡️ **Human-in-the-Loop** — Never sends emails, payments, or posts without your approval
- 🔄 **Ralph Wiggum Loop** — Continuously iterates until tasks are complete

**Gold Tier Achievement:** Full autonomous business operations with 9 watchers, 7 MCP servers, 5 agent skills, and Odoo ERP integration.

---

## ✨ Features

### 🔄 Autonomous Watchers

| Watcher | Status | Purpose |
|---------|--------|---------|
| **Gmail Watcher** | ✅ Active | Monitors inbox for urgent/important emails every 2 minutes |
| **WhatsApp Watcher** | ✅ Active | Captures urgent messages via Playwright automation |
| **LinkedIn Poster** | ✅ Active | Auto-publishes business content from queue folder |
| **Twitter Poster** | ✅ Active | Posts tweets automatically with engagement optimization |
| **Facebook Poster** | ✅ Active | Publishes to Facebook with rich media support |
| **Instagram Poster** | ✅ Active | Posts images with captions via Instagram API |
| **HITL Approval** | ✅ Active | Watches `/Pending_Approval` and executes approved actions |
| **Filesystem** | ✅ Active | Monitors drop folders for file-based triggers |
| **Plan Creator** | ✅ Active | Generates multi-step plans from vault tasks |

### 🧠 Claude Agent Skills

All AI functionality is implemented as reusable [Agent Skills](https://docs.anthropic.com/en/docs/build-with-claude/agent-skills):

- **`/gmail-triage`** — Classifies emails, creates plans, drafts replies with intent detection
- **`/whatsapp-triage`** — Detects intent, generates invoices, routes approvals, handles payments
- **`/linkedin-poster`** — Writes compelling posts from business context with engagement hooks
- **`/daily-briefing`** — Generates Monday CEO briefing with Odoo revenue & bottleneck analysis
- **`/browsing-with-playwright`** — Browser automation for web scraping and form filling

### 🔌 MCP Servers (Action Layer)

7 Model Context Protocol servers for external actions:

- **email-mcp** — Gmail send/draft via Google API
- **whatsapp-mcp** — WhatsApp messaging via Playwright
- **twitter-mcp** — Twitter/X posting with character optimization
- **facebook-mcp** — Facebook posting with rich media
- **linkedin-mcp** — LinkedIn publishing with professional formatting
- **instagram-mcp** — Instagram image posting with captions
- **odoo-mcp** — Odoo 19 ERP integration (invoices, customers, accounting)

### 💰 Odoo Accounting Integration (Gold Tier)

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
- ✅ **Error Recovery** — Automatic retry with exponential backoff
- ✅ **Ralph Wiggum Loop** — Continuous iteration until task completion

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SOURCES                             │
│  Gmail │ WhatsApp │ LinkedIn │ Twitter │ Facebook │ Instagram │ Odoo│
└────┬────┴────┬─────┴────┬─────┴────┬────┴────┬─────┴────┬──────┴───┘
     │         │          │          │         │          │
     ▼         ▼          ▼          ▼         ▼          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PERCEPTION LAYER (9 Watchers)                          │
│  Python scripts monitoring external sources continuously            │
│  Gmail • WhatsApp • LinkedIn • Twitter • Facebook • Instagram       │
│  HITL Approval • Filesystem • Plan Creator                          │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│            OBSIDIAN VAULT (Knowledge Base)                          │
│  /Needs_Action → /Plans → /Pending_Approval → /Approved → /Done     │
│  Dashboard.md │ Business_Goals.md │ Logs/ │ Briefings/              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│            REASONING LAYER (Claude Code + Skills)                   │
│  5 Agent Skills: gmail-triage, whatsapp-triage, linkedin-poster,    │
│  daily-briefing, browsing-with-playwright                           │
│  Read → Classify → Plan → Draft → Request Approval                  │
│  Ralph Wiggum Loop: Iterate until task complete                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌────────────────────────────────┐
│  HUMAN APPROVAL      │   │   ACTION LAYER (7 MCP Servers) │
│  Review & Approve    │──▶│   Email • WhatsApp • Social    │
│  /Pending_Approval   │   │   Twitter • Facebook • LinkedIn│
└──────────────────────┘   │   Instagram • Odoo ERP         │
                           └────────┬───────────────────────┘
                                    │
                                    ▼
                           ┌─────────────────────────┐
                           │   EXTERNAL ACTIONS      │
                           │ Send │ Post │ Invoice   │
                           └─────────────────────────┘
```

### Tech Stack

- **Brain:** Claude Code (Sonnet 4.6) with Agent Skills & Ralph Wiggum Loop
- **Memory:** Obsidian vault (local Markdown)
- **Senses:** Python 3.13+ watchers (Gmail API, Playwright, Odoo XML-RPC)
- **Hands:** 7 MCP servers (email, social media, accounting)
- **Orchestration:** main.py + orchestrator.py with thread-based concurrency
- **ERP:** Odoo 19 Community Edition (accounting, invoicing, CRM)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Claude Code CLI ([install](https://claude.com/product/claude-code))
- Obsidian 1.10.6+ ([download](https://obsidian.md/download))
- Gmail account with API access
- Odoo 19 Community Edition (optional, for accounting)
- Node.js 24+ (for MCP servers)

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
```

### Running the System

```bash
# Run all watchers (recommended)
uv run python main.py

# Run specific watcher
uv run python main.py --gmail
uv run python main.py --whatsapp
uv run python main.py --linkedin
uv run python main.py --twitter
uv run python main.py --facebook
uv run python main.py --instagram

# Dry run mode (safe testing)
DRY_RUN=true uv run python main.py

# Trigger daily briefing with Odoo summary
uv run python main.py --briefing
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

---

## 📁 Project Structure

```
Personal-AI-Employee/
├── AI_Employee_Vault/              # Obsidian knowledge base
│   ├── Dashboard.md                # Real-time status
│   ├── Business_Goals.md           # Revenue targets & KPIs
│   ├── Company_Handbook.md         # Decision rules
│   ├── Needs_Action/               # Incoming tasks
│   ├── Plans/                      # Multi-step plans
│   │   ├── linkedin_queue/         # LinkedIn posts
│   │   ├── twitter_queue/          # Twitter posts
│   │   ├── facebook_queue/         # Facebook posts
│   │   └── instagram_queue/        # Instagram posts
│   ├── Pending_Approval/           # Awaiting human review
│   ├── Approved/                   # Ready for execution
│   ├── Done/                       # Completed tasks
│   │   ├── linkedin_posted/        # Published LinkedIn
│   │   ├── twitter_posted/         # Published Twitter
│   │   ├── facebook_posted/        # Published Facebook
│   │   └── instagram_posted/       # Published Instagram
│   ├── Logs/                       # Audit trail (JSON)
│   └── Briefings/                  # Weekly CEO reports
│
├── watchers/                       # Perception layer (9 watchers)
│   ├── base_watcher.py             # Abstract base with retry logic
│   ├── gmail_watcher.py            # Email monitoring
│   ├── whatsapp_watcher.py         # WhatsApp monitoring
│   ├── linkedin_poster.py          # LinkedIn auto-posting
│   ├── twitter_poster.py           # Twitter auto-posting
│   ├── facebook_poster.py          # Facebook auto-posting
│   ├── instagram_poster.py         # Instagram auto-posting
│   ├── hitl_approval_watcher.py    # Approval executor
│   ├── filesystem_watcher.py       # File drop monitoring
│   ├── plan_creator.py             # Plan generation
│   └── config.py                   # Configuration loader
│
├── .claude/skills/                 # Agent Skills (5 skills)
│   ├── gmail-triage/               # Email classification & drafting
│   ├── whatsapp-triage/            # WhatsApp intent detection
│   ├── linkedin-poster/            # Business content generation
│   ├── daily-briefing/             # CEO briefing with Odoo
│   └── browsing-with-playwright/   # Browser automation
│
├── mcp_servers/                    # Action layer (7 MCP servers)
│   ├── email_mcp.py                # Gmail send/draft
│   ├── whatsapp_mcp.py             # WhatsApp messaging
│   ├── twitter_mcp.py              # Twitter posting
│   ├── facebook_mcp.py             # Facebook posting
│   ├── linkedin_mcp.py             # LinkedIn publishing
│   ├── instagram_mcp.py            # Instagram posting
│   └── odoo_mcp.py                 # Odoo ERP integration
│
├── main.py                         # Orchestrator entry point
├── orchestrator.py                 # Master process with threading
├── pyproject.toml                  # Dependencies (uv)
├── .env                            # Environment config
├── CLAUDE.md                       # Claude Code instructions
├── Personal_AI_Employee_Hackathon.md  # Architecture blueprint
└── README.md                       # This file
```

---

## 🏆 Gold Tier Achievements

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
- 4 Agent Skills

### ✅ Gold Tier Additions

#### 🌐 Full Social Media Suite
- **Twitter/X Integration** — Auto-posting with character optimization
- **Facebook Integration** — Rich media posts with engagement tracking
- **Instagram Integration** — Image posting with captions via API
- **4 Social Media Watchers** — Automated queue processing for all platforms

#### 💰 Odoo ERP Integration
- **Odoo MCP Server** — Full XML-RPC integration with Odoo 19
- **Customer Management** — Create and search customers
- **Invoice Generation** — Automated invoicing from WhatsApp/Email
- **Payment Tracking** — Monitor paid/unpaid invoices
- **Accounting Summary** — MTD revenue, expenses, net position
- **CEO Briefing Integration** — Weekly financial reports

#### 🔄 Ralph Wiggum Loop
- **Continuous Iteration** — Agent loops until task completion
- **Error Recovery** — Automatic retry with exponential backoff
- **Graceful Degradation** — Longer wait times after repeated failures
- **Audit Logging** — All errors logged for analysis

#### 🛡️ Advanced Error Recovery
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

**Total Development Time:** ~40 hours
**Lines of Code:** ~4,500
**MCP Servers:** 7
**Agent Skills:** 5
**Watchers:** 9
**Test Coverage:** Manual testing with real accounts (Gmail, WhatsApp, Odoo, Social Media)

---

## 🗺️ Roadmap

### Platinum Tier (Future)

- [ ] Cloud deployment (24/7 operation on VPS)
- [ ] Work-zone specialization (Cloud vs Local)
- [ ] Vault sync via Git/Syncthing
- [ ] Agent-to-Agent communication
- [ ] Advanced security hardening
- [ ] Multi-user support
- [ ] Calendar integration (Google Calendar MCP)
- [ ] Payment gateway integration (Stripe MCP)
- [ ] Browser automation for complex workflows
- [ ] Voice interface (Whisper + TTS)

---

## 🔒 Security Considerations

- **Credentials:** All secrets in `.env` (gitignored)
- **OAuth Tokens:** `token.pickle` never committed
- **DRY_RUN:** Default mode prevents accidental actions
- **Rate Limits:** Max 10 emails/hour, prevents spam
- **HITL Required:** Payments, new contacts, bulk sends
- **Audit Trail:** Every action logged with timestamp & parameters
- **Odoo Security:** Credentials injected via environment, never hardcoded
- **Session Management:** Browser sessions stored locally, never in vault
- **Error Isolation:** Failed actions don't crash entire system

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

**Gold Tier Complete** — Full autonomous business operations with 9 watchers, 7 MCP servers, 5 agent skills, and Odoo ERP integration

[⬆ Back to Top](#-personal-ai-employee)

</div>
