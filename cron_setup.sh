#!/bin/bash

# Cron Setup Script for Personal AI Employee
# Supports macOS and Linux

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="uv run python"

echo "🤖 Personal AI Employee - Cron Setup"
echo "===================================="
echo ""

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Function to install cron jobs
install_cron() {
    echo "📅 Installing cron jobs..."

    # Backup existing crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true

    # Create new crontab entries
    cat > /tmp/ai_employee_cron.txt <<EOF
# Personal AI Employee - Automated Tasks
# Generated on $(date)

# Daily briefing at 8:00 AM
0 8 * * * cd "$PROJECT_DIR" && $PYTHON_CMD main.py --briefing >> "$PROJECT_DIR/watchers/logs/cron_briefing.log" 2>&1

# Start watchers on system boot (optional - comment out if using PM2)
# @reboot cd "$PROJECT_DIR" && $PYTHON_CMD main.py >> "$PROJECT_DIR/watchers/logs/cron_main.log" 2>&1

# Health check every hour (optional)
# 0 * * * * cd "$PROJECT_DIR" && $PYTHON_CMD -c "from watchers.config import Config; print('Health check OK')" >> "$PROJECT_DIR/watchers/logs/health.log" 2>&1

EOF

    # Merge with existing crontab
    (crontab -l 2>/dev/null || true; cat /tmp/ai_employee_cron.txt) | crontab -

    echo "✅ Cron jobs installed successfully!"
    echo ""
    echo "Installed jobs:"
    crontab -l | grep -A 10 "Personal AI Employee"
}

# Function to uninstall cron jobs
uninstall_cron() {
    echo "🗑️  Removing cron jobs..."

    # Remove AI Employee entries
    crontab -l | grep -v "Personal AI Employee" | grep -v "main.py --briefing" | crontab - 2>/dev/null || true

    echo "✅ Cron jobs removed!"
}

# Function to show Windows instructions
show_windows_instructions() {
    cat <<EOF

📋 Windows Task Scheduler Setup Instructions
============================================

Since you're on Windows, use Task Scheduler instead of cron:

1. Open Task Scheduler (taskschd.msc)

2. Create Daily Briefing Task:
   - Action: Start a program
   - Program: cmd.exe
   - Arguments: /c cd "$PROJECT_DIR" && uv run python main.py --briefing
   - Trigger: Daily at 8:00 AM

3. Create Startup Task (optional):
   - Action: Start a program
   - Program: cmd.exe
   - Arguments: /c cd "$PROJECT_DIR" && uv run python main.py
   - Trigger: At system startup
   - Delay: 1 minute

4. Configure Task Settings:
   - Run whether user is logged on or not
   - Run with highest privileges
   - Configure for: Windows 10/11

Alternative: Use PM2 for Windows
--------------------------------
npm install -g pm2
pm2 start main.py --interpreter python --name ai-employee
pm2 save
pm2 startup

EOF
}

# Main script
OS=$(detect_os)

case "$1" in
    install)
        if [[ "$OS" == "unknown" ]]; then
            echo "❌ Unsupported OS. Please set up scheduling manually."
            exit 1
        fi
        install_cron
        ;;
    uninstall)
        uninstall_cron
        ;;
    windows)
        show_windows_instructions
        ;;
    *)
        echo "Usage: $0 {install|uninstall|windows}"
        echo ""
        echo "Commands:"
        echo "  install    - Install cron jobs (macOS/Linux)"
        echo "  uninstall  - Remove cron jobs (macOS/Linux)"
        echo "  windows    - Show Windows Task Scheduler instructions"
        echo ""
        echo "Current OS: $OS"
        exit 1
        ;;
esac

echo ""
echo "📚 Next Steps:"
echo "1. Verify cron jobs: crontab -l"
echo "2. Check logs: tail -f $PROJECT_DIR/watchers/logs/cron_briefing.log"
echo "3. Test manually: cd $PROJECT_DIR && $PYTHON_CMD main.py --briefing"
echo ""
