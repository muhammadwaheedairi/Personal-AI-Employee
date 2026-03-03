#!/bin/bash
# Git Sync Script - Both Local and Cloud use this
# Syncs vault state via GitHub (secrets never sync)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

AGENT=${1:-"local"}  # Pass 'cloud' or 'local' as argument
LOG_FILE="logs/git_sync.log"

mkdir -p logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$AGENT] $1" | tee -a "$LOG_FILE"
}

log "🔄 Starting git sync..."

# Pull latest changes
log "Pulling from GitHub..."
git pull --rebase origin main 2>&1 | tee -a "$LOG_FILE"

if [ $? -ne 0 ]; then
    log "❌ Git pull failed — resolving conflicts..."
    git rebase --abort 2>/dev/null
    git pull origin main 2>&1 | tee -a "$LOG_FILE"
fi

# Stage vault changes only (never secrets)
git add AI_Employee_Vault/ 2>&1

# Check if there are changes to commit
if git diff --staged --quiet; then
    log "✅ No changes to push"
    exit 0
fi

# Commit with agent name
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "$AGENT: vault sync $TIMESTAMP" 2>&1 | tee -a "$LOG_FILE"

# Push to GitHub
log "Pushing to GitHub..."
git push origin main 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "✅ Git sync complete!"
else
    log "❌ Git push failed!"
    exit 1
fi
