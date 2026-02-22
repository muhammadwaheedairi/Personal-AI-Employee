# Personal AI Employee - Bronze Tier

An autonomous AI assistant powered by Claude Code and Obsidian that monitors Gmail and processes tasks automatically.

## Features (Bronze Tier)
- ✅ Gmail monitoring with automatic task creation
- ✅ Obsidian vault for knowledge management
- ✅ Claude Code integration for task processing
- ✅ Structured logging and audit trail
- ✅ YAML frontmatter for task metadata
- ✅ Priority-based task categorization

## Prerequisites

### Required Software
- **Python 3.13+** - [Download](https://www.python.org/downloads/)
- **Claude Code CLI** - [Install](https://claude.com/product/claude-code)
- **Obsidian v1.10.6+** - [Download](https://obsidian.md/download)
- **Gmail account** with API access enabled

### Hardware Requirements
- Minimum: 8GB RAM, 4-core CPU, 20GB free disk space
- Stable internet connection (10+ Mbps recommended)

## Setup Instructions

### 1. Clone and Setup Python Environment

```bash
cd "/home/muhammadwaheed/workspace/Hackathone 0/Personal-AI-Employee"

# UV should already be initialized
# Verify dependencies are installed
uv pip list
```

### 2. Configure Gmail API

#### Step 2.1: Enable Gmail API in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2.2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Download the credentials JSON file
5. Save it as `credentials.json` in the project root

#### Step 2.3: First-Time Authentication

```bash
# Run the watcher for the first time
cd watchers
uv run python gmail_watcher.py
```

This will:
- Open a browser window for OAuth consent
- Ask you to authorize the application
- Save the token as `token.pickle` for future use

### 3. Initialize Obsidian Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Navigate to: `/home/muhammadwaheed/workspace/Hackathone 0/Personal-AI-Employee/AI_Employee_Vault`
4. Click "Open"

You should see:
- Dashboard.md
- Company_Handbook.md
- CLAUDE.md
- Folders: Inbox, Needs_Action, Done, Plans, Logs

### 4. Configure Environment Variables

The `.env` file is already configured with:

```
VAULT_PATH=/home/muhammadwaheed/workspace/Hackathone 0/Personal-AI-Employee/AI_Employee_Vault
GMAIL_CREDENTIALS_PATH=/home/muhammadwaheed/workspace/Hackathone 0/Personal-AI-Employee/credentials.json
CHECK_INTERVAL=120
DRY_RUN=false
```

Adjust these values if needed.

### 5. Run the Gmail Watcher

```bash
cd watchers
uv run python gmail_watcher.py
```

The watcher will:
- Check Gmail every 120 seconds (2 minutes)
- Look for unread + important emails
- Create .md files in `/Needs_Action` folder
- Log all activity to `logs/GmailWatcher.log`

### 6. Use Claude Code with the Vault

#### Option A: Interactive Mode

```bash
# Navigate to the vault
cd "AI_Employee_Vault"

# Start Claude Code
claude

# Then give instructions like:
# "Read all files in Needs_Action and process them according to Company_Handbook.md"
```

#### Option B: Direct Command

```bash
cd "AI_Employee_Vault"
claude "Check Needs_Action folder, process any pending tasks, update Dashboard.md"
```

#### Option C: Point Claude to Vault from Project Root

```bash
claude --cwd "AI_Employee_Vault" "Process pending tasks"
```

## Project Structure

```
Personal-AI-Employee/
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Dashboard.md            # Status dashboard
│   ├── Company_Handbook.md     # Decision rules
│   ├── CLAUDE.md               # AI instructions
│   ├── Inbox/                  # Incoming items
│   ├── Needs_Action/           # Tasks to process
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # Task plans
│   └── Logs/                   # Audit logs
├── watchers/                   # Watcher scripts
│   ├── __init__.py
│   ├── config.py               # Configuration loader
│   ├── base_watcher.py         # Abstract base class
│   └── gmail_watcher.py        # Gmail implementation
├── logs/                       # Runtime logs
├── .env                        # Environment config
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # UV project config
└── README.md                   # This file
```

## Testing

### Test 1: Verify Setup

```bash
# Check Python environment
uv pip list | grep google

# Check vault structure
ls -la "AI_Employee_Vault"

# Check environment variables
cat .env
```

### Test 2: Test Gmail Watcher

1. Send yourself an email and mark it as "important"
2. Run the watcher:
   ```bash
   cd watchers
   uv run python gmail_watcher.py
   ```
3. Wait for the check interval (120 seconds)
4. Check `AI_Employee_Vault/Needs_Action/` for new .md file
5. Press Ctrl+C to stop the watcher

### Test 3: Test Claude Code Integration

1. Ensure there's a task file in `Needs_Action/`
2. Run Claude:
   ```bash
   cd "AI_Employee_Vault"
   claude "Read the task in Needs_Action, summarize it, and update Dashboard.md"
   ```
3. Verify Claude:
   - Reads the task file
   - Updates Dashboard.md
   - Can move files to Done/

### Test 4: End-to-End Flow

1. Send test email (mark as important)
2. Start watcher: `cd watchers && uv run python gmail_watcher.py`
3. Wait for task file creation
4. Stop watcher (Ctrl+C)
5. Process with Claude:
   ```bash
   cd "AI_Employee_Vault"
   claude "Process all tasks in Needs_Action according to Company_Handbook.md"
   ```
6. Verify:
   - Task processed
   - File moved to Done/
   - Dashboard.md updated

## Usage Patterns

### Daily Workflow

1. **Morning**: Start the watcher
   ```bash
   cd watchers && uv run python gmail_watcher.py &
   ```

2. **Throughout the day**: Check Dashboard in Obsidian

3. **Process tasks**: Run Claude periodically
   ```bash
   cd "AI_Employee_Vault"
   claude "Process pending tasks"
   ```

4. **Evening**: Review completed tasks in Done/ folder

### Customizing Rules

Edit `Company_Handbook.md` to change:
- Priority keywords
- Response time expectations
- Action thresholds
- Error handling behavior

Claude will read these rules when processing tasks.

## Troubleshooting

### Issue: "credentials.json not found"

**Solution**: Download OAuth credentials from Google Cloud Console and save as `credentials.json` in project root.

### Issue: "Permission denied" when accessing Gmail

**Solution**: 
1. Delete `token.pickle`
2. Run watcher again to re-authenticate
3. Make sure you grant all requested permissions

### Issue: Watcher stops running

**Solution**: 
- Check `logs/GmailWatcher.log` for errors
- Verify internet connection
- Ensure Gmail API quota not exceeded

### Issue: Claude can't read vault files

**Solution**:
- Verify you're in the correct directory
- Use `--cwd` flag to point to vault
- Check file permissions

### Issue: No emails detected

**Solution**:
- Verify emails are marked as "important" in Gmail
- Check Gmail filters/labels
- Reduce CHECK_INTERVAL in .env for faster polling
- Check `AI_Employee_Vault/Logs/processed_emails.txt` to see what's been processed

## Security Notes

- ✅ `.env` file is gitignored (contains paths)
- ✅ `credentials.json` is gitignored (OAuth secrets)
- ✅ `token.pickle` is gitignored (access token)
- ✅ All sensitive files excluded from version control
- ⚠️ Never commit credentials to Git
- ⚠️ Rotate OAuth credentials monthly

## Next Steps (Silver Tier)

After completing Bronze Tier, consider:
- Adding WhatsApp watcher
- Implementing MCP servers for actions
- Adding human-in-the-loop approval workflow
- Setting up cron/Task Scheduler for automation
- Creating Agent Skills for AI functionality

## Resources

- [Claude Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Obsidian Help](https://help.obsidian.md/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Hackathon Guide](./Personal_AI_Employee_Hackathon.md)

## License

This project is for educational purposes as part of the Personal AI Employee Hackathon.

---
**Status**: Bronze Tier Complete ✅
