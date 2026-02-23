# Personal AI Employee — Complete Setup Guide
## Silver Tier Prerequisites & Pre-Setup

---

## PART 1: SOFTWARE PREREQUISITES

### 1.1 Python 3.13+

```bash
# Check version
python3 --version   # needs 3.13+

# If not installed — Ubuntu/Debian
sudo apt update && sudo apt install python3.13

# macOS (Homebrew)
brew install python@3.13

# Windows — download from python.org/downloads
```

### 1.2 UV (Python package manager)

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

### 1.3 Node.js v24+ LTS

```bash
# Check version
node --version   # needs v24+

# Install via nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 24
nvm use 24

# Or download from nodejs.org
```

### 1.4 Claude Code

```bash
# Install globally
npm install -g @anthropic/claude-code

# Verify
claude --version

# Login (first time)
claude login
```

### 1.5 Obsidian v1.10.6+

Download from: https://obsidian.md/download

After install:
1. Open Obsidian
2. Click "Open folder as vault"
3. Select your project's `AI_Employee_Vault/` folder

### 1.6 Git + GitHub Desktop

```bash
# Git
git --version   # usually pre-installed

# GitHub Desktop — download from desktop.github.com
```

### 1.7 PM2 (process manager — keeps watchers alive)

```bash
npm install -g pm2
pm2 --version
```

---

## PART 2: GOOGLE GMAIL API SETUP

> Required for GmailWatcher and EmailMCP to work.

### Step 1 — Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click "New Project" → name it `ai-employee`
3. Click "Create"

### Step 2 — Enable Gmail API

1. In your project: APIs & Services → Library
2. Search "Gmail API" → Click Enable

### Step 3 — Create OAuth Credentials

1. APIs & Services → Credentials → Create Credentials → OAuth Client ID
2. Application type: **Desktop App**
3. Name: `ai-employee-local`
4. Click Create → Download JSON
5. Rename downloaded file to `credentials.json`
6. Place it in project root: `Personal-AI-Employee/credentials.json`

### Step 4 — Configure OAuth Consent Screen

1. APIs & Services → OAuth consent screen
2. User Type: **External**
3. App name: `AI Employee`
4. Add your Gmail as test user
5. Scopes: add `gmail.readonly` and `gmail.send`

### Step 5 — First Auth (generates token.pickle)

```bash
# Run Gmail watcher once — browser will open for login
uv run python main.py --gmail --dry-run

# Browser opens → login with your Google account → Allow
# token.pickle gets created in watchers/token.pickle
# You will NOT need to login again unless token expires
```

---

## PART 3: PROJECT SETUP

### Step 1 — Clone / Open Project

```bash
cd ~/workspace
# If starting fresh:
git clone <your-repo-url> Personal-AI-Employee
cd Personal-AI-Employee

# If already cloned:
cd "Hackathone 0/Personal-AI-Employee"
```

### Step 2 — Create UV Virtual Environment

```bash
uv venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### Step 3 — Install All Dependencies

```bash
uv add \
  google-auth \
  google-auth-oauthlib \
  google-auth-httplib2 \
  google-api-python-client \
  playwright \
  watchdog \
  python-dotenv \
  pyyaml
```

### Step 4 — Install Playwright Browsers

```bash
# Install Chromium (used by WhatsApp and LinkedIn watchers)
uv run playwright install chromium
```

### Step 5 — Create .env File

```bash
cp .env.example .env
```

Now open `.env` and fill in your values:

```env
# Vault path (relative to project root)
VAULT_PATH=./AI_Employee_Vault

# Drop folder (any files dropped here get picked up by FilesystemWatcher)
DROP_FOLDER_PATH=./drop_folder

# Gmail
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_TOKEN_PATH=./watchers/token.pickle
CHECK_INTERVAL=120

# WhatsApp browser session (auto-created on first login)
WHATSAPP_SESSION_PATH=./.whatsapp_session
WHATSAPP_CHECK_INTERVAL=30

# LinkedIn browser session (auto-created on first login)
LINKEDIN_SESSION_PATH=./.linkedin_session
LINKEDIN_CHECK_INTERVAL=300

# IMPORTANT: keep true until you've tested everything
DRY_RUN=true
```

### Step 6 — Create .gitignore entries

Make sure these are in your `.gitignore`:

```
.env
credentials.json
watchers/token.pickle
.whatsapp_session/
.linkedin_session/
__pycache__/
.venv/
*.pyc
```

### Step 7 — Place All New Files

Copy the files you received into their correct locations:

```
Personal-AI-Employee/
├── CLAUDE.md                        ← root (replace existing)
├── main.py                          ← replace existing
├── orchestrator.py                  ← new
├── cron_setup.sh                    ← new
├── .env.example                     ← new
├── mcp_servers/
│   ├── __init__.py                  ← new
│   └── email_mcp.py                 ← new
├── watchers/
│   ├── config.py                    ← replace existing
│   ├── plan_creator.py              ← new
│   ├── whatsapp_watcher.py          ← new
│   ├── linkedin_poster.py           ← new
│   ├── filesystem_watcher.py        ← new
│   └── hitl_approval_watcher.py     ← new
├── .claude/
│   └── skills/
│       ├── gmail-triage/
│       │   ├── SKILL.md
│       │   └── references/classification.md
│       ├── whatsapp-triage/
│       │   ├── SKILL.md
│       │   └── references/intents.md
│       ├── linkedin-poster/
│       │   ├── SKILL.md
│       │   └── references/post-structure.md
│       └── daily-briefing/
│           ├── SKILL.md
│           └── references/briefing-template.md
└── AI_Employee_Vault/
    ├── CLAUDE.md                    ← DELETE this (root CLAUDE.md use hoga)
    ├── Dashboard.md                 ← keep (from Bronze)
    ├── Company_Handbook.md          ← keep (from Bronze)
    ├── Plans/
    │   └── linkedin_queue/
    │       └── example_post.md      ← new
    ├── Needs_Action/                ← keep (from Bronze)
    ├── Done/                        ← keep (from Bronze)
    ├── Logs/                        ← keep (from Bronze)
    ├── Pending_Approval/            ← new folder
    ├── Approved/                    ← new folder
    ├── Rejected/                    ← new folder
    └── Briefings/                   ← new folder
```

### Step 8 — Create Missing Vault Folders

```bash
mkdir -p AI_Employee_Vault/Pending_Approval
mkdir -p AI_Employee_Vault/Approved
mkdir -p AI_Employee_Vault/Rejected
mkdir -p AI_Employee_Vault/Briefings
mkdir -p AI_Employee_Vault/Plans/linkedin_queue
mkdir -p drop_folder
```

---

## PART 4: WHATSAPP SESSION SETUP

WhatsApp Web needs a one-time browser login to save your session.

```bash
# Run with headless=False to see the browser
# Temporarily edit whatsapp_watcher.py line:
#   headless=True  →  headless=False

uv run python main.py --whatsapp --dry-run

# Browser opens → scan QR code with your phone WhatsApp
# Wait for chats to load → Ctrl+C to stop
# Session saved to .whatsapp_session/
# Change headless back to True
```

---

## PART 5: LINKEDIN SESSION SETUP

Same as WhatsApp — one-time browser login needed.

```bash
# Temporarily edit linkedin_poster.py:
#   headless=True  →  headless=False

uv run python main.py --linkedin --dry-run

# Browser opens → login to LinkedIn
# Wait for feed to load → Ctrl+C
# Session saved to .linkedin_session/
# Change headless back to True
```

---

## PART 6: CONFIGURE CLAUDE CODE MCP

Tell Claude Code about your Email MCP server.

Create or edit `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "python",
      "args": ["/absolute/path/to/Personal-AI-Employee/mcp_servers/email_mcp.py"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "/absolute/path/to/credentials.json",
        "GMAIL_TOKEN_PATH": "/absolute/path/to/watchers/token.pickle",
        "VAULT_PATH": "/absolute/path/to/AI_Employee_Vault",
        "DRY_RUN": "true"
      }
    }
  ]
}
```

> Replace `/absolute/path/to/` with your actual full path.
> On Mac: `/Users/yourname/workspace/...`
> On Windows: `C:/Users/yourname/workspace/...`

---

## PART 7: VERIFY SETUP

Run each component one at a time in DRY_RUN mode before going live.

```bash
# Step 1 — Gmail watcher (should find emails, create .md files)
uv run python main.py --gmail --dry-run

# Step 2 — Plan creator check (should see Plans being created)
uv run python main.py --dry-run
# Wait 15 seconds — check AI_Employee_Vault/Plans/ for PLAN_*.md files

# Step 3 — HITL watcher (move a file to /Approved manually, should log it)
uv run python main.py --hitl --dry-run

# Step 4 — Full orchestrator dry run
uv run python main.py --dry-run
```

Check logs:

```bash
# Orchestrator log
tail -f AI_Employee_Vault/Logs/orchestrator.log

# Action log (today's)
cat AI_Employee_Vault/Logs/$(date +%Y-%m-%d).json
```

---

## PART 8: GO LIVE

Only after all dry-run tests pass:

```bash
# 1. Turn off DRY_RUN in .env
#    DRY_RUN=false

# 2. Start with PM2 (keeps running after terminal closes)
pm2 start main.py --interpreter python3 --name ai-employee
pm2 save
pm2 startup    # auto-start on reboot

# 3. Install cron jobs for scheduled tasks
chmod +x cron_setup.sh
./cron_setup.sh install      # Mac/Linux
./cron_setup.sh windows      # Windows — follow printed instructions

# 4. Point Claude Code at the vault
cd Personal-AI-Employee
claude    # Claude reads CLAUDE.md automatically
```

---

## PART 9: CLAUDE CODE DAILY USE

```bash
# Open project in Claude Code
cd ~/workspace/"Hackathone 0"/Personal-AI-Employee
claude

# Process pending emails
> Process all files in /Needs_Action

# Generate LinkedIn post
> Create a LinkedIn post about this week's AI automation progress

# Trigger briefing
> Generate today's CEO briefing

# Check what's pending approval
> What files are in /Pending_Approval and what do they need?
```

---

## QUICK REFERENCE

| What | Command |
|---|---|
| Start everything | `uv run python main.py` |
| Safe test mode | `uv run python main.py --dry-run` |
| Gmail only | `uv run python main.py --gmail` |
| Trigger briefing | `uv run python main.py --briefing` |
| Start with PM2 | `pm2 start main.py --interpreter python3` |
| View PM2 logs | `pm2 logs ai-employee` |
| Install cron | `./cron_setup.sh install` |
| Check cron status | `./cron_setup.sh status` |
| Open Claude Code | `claude` (from project root) |

---

## TROUBLESHOOTING

**`ModuleNotFoundError`** — run `uv add <module-name>` then retry

**`Gmail 403 Forbidden`** — credentials.json missing or OAuth consent not configured. Re-check Part 2.

**`token.pickle expired`** — delete `watchers/token.pickle` and re-run `--gmail --dry-run` to re-authenticate.

**`WhatsApp QR expired`** — delete `.whatsapp_session/` folder and redo Part 4.

**`Watcher stopped overnight`** — use PM2 (Part 8) or run `./cron_setup.sh install` for @reboot entry.

**`Plans not being created`** — check `watchers/config.py` VAULT_PATH matches your actual folder name.