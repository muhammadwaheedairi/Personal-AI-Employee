<div align="center">

# 🤖 Personal AI Employee

### Your Autonomous Digital FTE — Built with Claude Code & Obsidian

[![Silver Tier](https://img.shields.io/badge/Hackathon-Silver_Tier_Complete-silver?style=for-the-badge)](./Personal_AI_Employee_Hackathon.md)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude-Code_Powered-orange?style=for-the-badge)](https://claude.com/product/claude-code)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)

*An autonomous AI assistant that monitors Gmail, WhatsApp, and LinkedIn — processing tasks 24/7 with human-in-the-loop safety.*

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Roadmap](#-roadmap)

</div>

---

## 🎯 What is This?

A **Digital Full-Time Equivalent (FTE)** that works 168 hours/week at ~10% the cost of a human employee. This AI Employee:

- 📧 **Triages Gmail** — Detects urgent emails, drafts replies, routes to approval
- 💬 **Monitors WhatsApp** — Captures client requests, generates invoices, handles inquiries
- 📱 **Posts on LinkedIn** — Auto-generates business content to drive sales and engagement
- 🧠 **Reasons Autonomously** — Creates multi-step plans, executes tasks, logs everything
- 🛡️ **Human-in-the-Loop** — Never sends emails or payments without your approval

**Silver Tier Achievement:** All core automation features complete with 4 watchers, 4 agent skills, and full MCP integration.

---

## ✨ Features

### 🔄 Autonomous Watchers

| Watcher | Status | Purpose |
|---------|--------|---------|
| **Gmail Watcher** | ✅ Active | Monitors inbox for urgent/important emails every 2 minutes |
| **WhatsApp Watcher** | ✅ Active | Captures urgent messages & sends automated replies with HITL approval |
| **LinkedIn Poster** | ✅ Active | Auto-publishes business updates from queue folder |
| **HITL Approval** | ✅ Active | Watches `/Pending_Approval` and executes approved actions |
| **Filesystem** | ✅ Active | Monitors drop folders for file-based triggers |

### 🧠 Claude Agent Skills

All AI functionality is implemented as reusable [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):

- **`/gmail-triage`** — Classifies emails, creates plans, drafts replies
- **`/whatsapp-triage`** — Detects intent, generates invoices, routes approvals
- **`/linkedin-poster`** — Writes compelling posts from business context
- **`/daily-briefing`** — Generates Monday CEO briefing with revenue & bottlenecks

### 🔐 Security & Safety

- ✅ **Human-in-the-Loop** — Sensitive actions require approval before execution
- ✅ **Audit Logging** — Every action logged to `/Vault/Logs/YYYY-MM-DD.json`
- ✅ **DRY_RUN Mode** — Test safely without external actions
- ✅ **Rate Limiting** — Max 10 email actions per hour
- ✅ **Credential Isolation** — All secrets in `.env`, never in vault

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                         │
│     Gmail    │    WhatsApp    │    LinkedIn    │   Files    │
└──────┬───────┴────────┬───────┴────────┬───────┴──────┬─────┘
       │                │                │              │
       ▼                ▼                ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                  PERCEPTION LAYER (Watchers)                │
│   Python scripts monitoring external sources continuously   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              OBSIDIAN VAULT (Knowledge Base)                │
│  /Needs_Action → /Plans → /Pending_Approval → /Done         │
│  Dashboard.md │ Business_Goals.md │ Logs/                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              REASONING LAYER (Claude Code)                  │
│  Agent Skills: gmail-triage, whatsapp-triage, linkedin      │
│  Read → Classify → Plan → Draft → Request Approval          │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌────────────────────────┐
│  HUMAN APPROVAL      │   │   ACTION LAYER (MCP)   │
│  Review & Approve    │──▶│   Email MCP Server     │
└──────────────────────┘   └────────┬───────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ EXTERNAL ACTIONS│
                           │ Send │ Post │ Pay│
                           └─────────────────┘
```

### Tech Stack

- **Brain:** Claude Code (Sonnet 4.6) with Agent Skills
- **Memory:** Obsidian vault (local Markdown)
- **Senses:** Python 3.13+ watchers (Gmail API, Playwright)
- **Hands:** MCP servers (email-mcp, future: payment-mcp)
- **Orchestration:** main.py + cron scheduling

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Claude Code CLI ([install](https://claude.com/product/claude-code))
- Obsidian 1.10.6+ ([download](https://obsidian.md/download))
- Gmail account with API access
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

# 5. First-time authentication
uv run python main.py --gmail
# This will open browser for OAuth consent

# 6. Open Obsidian vault
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

# Dry run mode (safe testing)
DRY_RUN=true uv run python main.py

# Trigger daily briefing
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

# Create Monday briefing
> /daily-briefing
```

---

## 📊 Demo

### Email Triage Workflow

1. **Detection:** Gmail watcher finds urgent email → creates `EMAIL_*.md` in `/Needs_Action`
2. **Triage:** `/gmail-triage` skill classifies intent → creates `PLAN_*.md` in `/Plans`
3. **Draft:** Claude drafts reply → writes to `/Pending_Approval/EMAIL_reply_*.md`
4. **Approval:** You review and move to `/Approved`
5. **Send:** HITL watcher detects approval → email MCP sends → logs action → moves to `/Done`

### LinkedIn Auto-Posting

1. **Context Gathering:** Reads `/Vault/Business_Goals.md` and recent `/Done` files
2. **Post Generation:** `/linkedin-poster` skill writes compelling post
3. **Queue:** Saves to `/Plans/linkedin_queue/{topic}_{timestamp}.md`
4. **Auto-Publish:** LinkedIn watcher picks up and posts automatically
5. **Logging:** Action logged to `/Vault/Logs/`

### WhatsApp Invoice Request

1. **Capture:** WhatsApp watcher detects "invoice" keyword → creates `WHATSAPP_*.md`
2. **Intent Detection:** `/whatsapp-triage` identifies invoice request
3. **Plan Creation:** Generates plan with steps: identify client, calculate amount, draft invoice
4. **Approval Required:** Writes invoice draft to `/Pending_Approval`
5. **Human Review:** You approve → system sends via email MCP

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
│   ├── Pending_Approval/           # Awaiting human review
│   ├── Approved/                   # Ready for execution
│   ├── Done/                       # Completed tasks
│   ├── Logs/                       # Audit trail (JSON)
│   └── Briefings/                  # Weekly CEO reports
│
├── watchers/                       # Perception layer
│   ├── base_watcher.py             # Abstract base class
│   ├── gmail_watcher.py            # Email monitoring
│   ├── whatsapp_watcher.py         # WhatsApp monitoring
│   ├── linkedin_poster.py          # Auto-posting
│   ├── hitl_approval_watcher.py    # Approval executor
│   └── config.py                   # Configuration loader
│
├── .claude/skills/                 # Agent Skills
│   ├── gmail-triage/
│   ├── whatsapp-triage/
│   ├── linkedin-poster/
│   └── daily-briefing/
│
├── mcp_servers/                    # Action layer
│   └── email_mcp.py                # Gmail send/draft
│
├── main.py                         # Orchestrator entry point
├── orchestrator.py                 # Master process
├── pyproject.toml                  # Dependencies
├── .env                            # Environment config
└── README.md                       # This file
```

---

## 🎓 Silver Tier Achievements

✅ **All Bronze Requirements**
- Obsidian vault with Dashboard & Company Handbook
- Working Gmail watcher
- Claude Code reading/writing to vault
- Structured folder workflow

✅ **Silver Tier Additions**
- **3 Watchers:** Gmail + WhatsApp + LinkedIn
- **LinkedIn Auto-Posting:** Business content generation for sales
- **Plan.md Creation:** Claude reasoning loop with multi-step plans
- **Email MCP Server:** External action capability
- **HITL Approval Workflow:** `/Pending_Approval` → `/Approved` → Execute
- **WhatsApp Reply Sending:** Approved replies sent automatically via Playwright automation
- **Cron Scheduling:** Daily briefing at 8:00 AM
- **4 Agent Skills:** All AI functionality as reusable skills

**Total Development Time:** ~25 hours
**Lines of Code:** ~2,500
**Test Coverage:** Manual testing with real Gmail/WhatsApp accounts

---

## 🗺️ Roadmap

### Gold Tier (In Progress)

- [ ] Odoo Community integration for accounting
- [ ] Facebook & Instagram watchers
- [ ] Twitter (X) integration
- [ ] Weekly Business Audit with CEO Briefing
- [ ] Ralph Wiggum loop for autonomous task completion
- [ ] Multiple MCP servers (payment, calendar, browser)
- [ ] Comprehensive error recovery

### Platinum Tier (Future)

- [ ] Cloud deployment (24/7 operation)
- [ ] Work-zone specialization (Cloud vs Local)
- [ ] Vault sync via Git/Syncthing
- [ ] Agent-to-Agent communication
- [ ] Advanced security hardening

---

## 🔒 Security Considerations

- **Credentials:** All secrets in `.env` (gitignored)
- **OAuth Tokens:** `token.pickle` never committed
- **DRY_RUN:** Default mode prevents accidental actions
- **Rate Limits:** Max 10 emails/hour, prevents spam
- **HITL Required:** Payments, new contacts, bulk sends
- **Audit Trail:** Every action logged with timestamp & parameters

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
- [Claude Code Docs](https://code.claude.com/docs/en/overview)
- [Agent Skills Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Obsidian Help](https://help.obsidian.md/)

---

## 📝 License

Educational use only. Part of the Personal AI Employee Hackathon 0.

---

## 🙏 Acknowledgments

- **Anthropic** — Claude Code & Agent Skills framework
- **Obsidian** — Local-first knowledge management
- **Panaversity** — Hackathon organization & guidance
- **Community** — Open-source MCP servers & examples

---

<div align="center">

**Built with ❤️ using Claude Code**

[⬆ Back to Top](#-personal-ai-employee)

</div>
