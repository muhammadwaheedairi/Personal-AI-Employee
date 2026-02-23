# Changelog

All notable changes to the Personal AI Employee project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-23 - Silver Tier Complete 🥈

### Added
- **LinkedIn Poster Watcher** — Auto-generates and publishes business content
- **WhatsApp Watcher** — Monitors WhatsApp Web for urgent messages and keywords
- **HITL Approval Watcher** — Executes approved actions from `/Approved` folder
- **Email MCP Server** — Gmail send/draft capabilities via Model Context Protocol
- **4 Agent Skills** — gmail-triage, whatsapp-triage, linkedin-poster, daily-briefing
- **Plan.md Creation** — Claude reasoning loop with multi-step task plans
- **Approval Workflow** — `/Pending_Approval` → `/Approved` → Execute pipeline
- **Comprehensive Logging** — All actions logged to `/Vault/Logs/YYYY-MM-DD.json`
- **Dashboard Updates** — Real-time status tracking in `Dashboard.md`
- **Cron Setup Script** — `cron_setup.sh` for automated scheduling

### Changed
- Refactored watchers to use `BaseWatcher` abstract class
- Improved error handling with retry logic
- Enhanced security with DRY_RUN mode by default
- Updated README with modern VIP-style documentation

### Fixed
- Gmail API token refresh handling
- WhatsApp session persistence issues
- LinkedIn queue file processing race conditions

### Security
- Added rate limiting (max 10 email actions/hour)
- Implemented HITL approval for all sensitive actions
- Credentials isolated in `.env` (gitignored)
- Audit trail for all external actions

## [0.1.0] - 2026-02-19 - Bronze Tier Complete 🥉

### Added
- **Gmail Watcher** — Monitors inbox for urgent/important emails
- **Obsidian Vault Structure** — `/Needs_Action`, `/Plans`, `/Done`, `/Logs`
- **Dashboard.md** — Real-time status overview
- **Company_Handbook.md** — Decision rules and guidelines
- **Business_Goals.md** — Revenue targets and KPIs
- **Base Watcher Class** — Abstract template for all watchers
- **Configuration System** — `config.py` for centralized settings
- **Filesystem Watcher** — Monitors drop folders for file triggers
- **Basic Logging** — Runtime logs in `watchers/logs/`

### Infrastructure
- Python 3.13+ project with UV package manager
- Gmail API OAuth2 authentication
- Obsidian vault integration
- Claude Code CLI integration
- `.gitignore` for credentials and tokens

### Documentation
- Initial README with setup instructions
- Gmail API configuration guide
- Testing procedures
- Troubleshooting section

## [0.0.1] - 2026-02-18 - Project Initialization

### Added
- Project structure and repository setup
- `pyproject.toml` with dependencies
- Initial `.env` configuration
- Basic folder structure

---

## Upcoming (Gold Tier Roadmap)

### Planned Features
- [ ] Odoo Community integration for accounting
- [ ] Facebook & Instagram watchers
- [ ] Twitter (X) integration
- [ ] Weekly Business Audit with CEO Briefing
- [ ] Ralph Wiggum loop for autonomous task completion
- [ ] Payment MCP server
- [ ] Calendar MCP server
- [ ] Browser automation MCP server
- [ ] Advanced error recovery and graceful degradation
- [ ] Watchdog process for auto-restart

### Future Enhancements (Platinum Tier)
- [ ] Cloud deployment (24/7 operation)
- [ ] Work-zone specialization (Cloud vs Local)
- [ ] Vault sync via Git/Syncthing
- [ ] Agent-to-Agent communication
- [ ] Advanced security hardening
- [ ] Multi-tenant support
- [ ] Web dashboard UI

---

## Development Notes

### Silver Tier Achievements (2026-02-23)
- Total development time: ~25 hours
- Lines of code: ~2,500
- Watchers implemented: 5
- Agent Skills created: 4
- MCP servers: 1
- Test coverage: Manual testing with real accounts

### Key Learnings
1. **Watcher Pattern** — Lightweight Python scripts are effective for monitoring
2. **HITL Critical** — Human approval prevents costly mistakes
3. **Agent Skills** — Reusable skills dramatically improve maintainability
4. **Obsidian Integration** — Markdown-based workflow is intuitive and flexible
5. **MCP Power** — Model Context Protocol enables clean external actions

### Technical Debt
- Need automated tests for watchers
- WhatsApp session management could be more robust
- Error recovery needs improvement
- Need metrics/monitoring dashboard

---

**Legend:**
- `Added` — New features
- `Changed` — Changes to existing functionality
- `Deprecated` — Soon-to-be removed features
- `Removed` — Removed features
- `Fixed` — Bug fixes
- `Security` — Security improvements
