# Error Handling & Logging Patterns

Comprehensive guide for handling errors and logging email send actions.

## Error Categories

### 1. Pre-Send Validation Errors

**Check before calling MCP:**
- Email address format validation
- Subject line not empty
- Body content not empty
- DRY_RUN mode status
- Recipient is known/approved contact

**Example validation:**
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_send_request(to: str, subject: str, body: str) -> tuple[bool, str]:
    if not validate_email(to):
        return False, f"Invalid email address: {to}"
    if not subject.strip():
        return False, "Subject line cannot be empty"
    if not body.strip():
        return False, "Email body cannot be empty"
    return True, "Valid"
```

---

### 2. MCP Tool Errors

**Common MCP errors:**
- `Gmail token not found` → Authentication issue
- `Token expired` → Needs refresh
- `Permission denied` → API scope issue
- `Network error` → Connection problem

**Handling pattern:**
```python
try:
    result = await mcp_call("send_email", {...})
    if "Error:" in result:
        # Log failure
        log_error("email_send_failed", result)
        # Move to /Pending_Approval for human review
        escalate_to_human(approval_file)
        return False
    return True
except Exception as e:
    log_error("mcp_exception", str(e))
    return False
```

---

### 3. File System Errors

**Common file errors:**
- Approval file not found
- Cannot write to /Done/
- Cannot read from /Approved/
- Log file write failure

**Handling pattern:**
```python
from pathlib import Path

def safe_move_file(source: Path, dest: Path) -> bool:
    try:
        if not source.exists():
            log_error("file_not_found", str(source))
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        source.rename(dest)
        return True
    except Exception as e:
        log_error("file_move_failed", f"{source} -> {dest}: {e}")
        return False
```

---

## Logging Format

### Success Log Entry

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_sent",
  "source_file": "REPLY_20260305_143000_subject.md",
  "recipient": "client@example.com",
  "subject": "Re: Project Update",
  "status": "success",
  "dry_run": false
}
```

### Error Log Entry

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_send_failed",
  "source_file": "REPLY_20260305_143000_subject.md",
  "recipient": "client@example.com",
  "subject": "Re: Project Update",
  "status": "error",
  "error_message": "Gmail token not found",
  "escalated_to_human": true
}
```

### Draft Log Entry

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_draft_created",
  "source_file": "REPLY_20260305_143000_subject.md",
  "recipient": "unknown@example.com",
  "subject": "Re: New Contact",
  "status": "success",
  "reason": "unknown_contact"
}
```

---

## Recovery Strategies

### Strategy 1: Escalate to Human

When to use:
- MCP tool returns error
- Unknown/new recipient
- Financial/sensitive content
- DRY_RUN mode active but user expects real send

**Action:**
1. Copy approval file back to /Pending_Approval/
2. Add error context to file
3. Update Dashboard.md with alert
4. Log escalation

---

### Strategy 2: Create Draft Instead

When to use:
- Uncertain about recipient
- First-time contact
- High-value/sensitive email

**Action:**
1. Call `draft_email` instead of `send_email`
2. Log draft creation
3. Notify user that draft was created
4. Move approval file to /Done/ with draft status

---

### Strategy 3: Retry with Backoff

**NOT RECOMMENDED** for email sending. Never auto-retry failed sends without human review.

---

## Error Notification Format

When escalating errors to human, update the approval file:

```markdown
---
type: email_reply
status: error_requires_review
error: "Gmail token not found"
created: {iso_timestamp}
---

# ⚠️ ERROR: Email Send Failed

**Error:** Gmail token not found

**Original Request:**
- **To:** client@example.com
- **Subject:** Re: Project Update
- **Status:** Failed to send

## Recommended Action
1. Check Gmail authentication: `uv run python main.py --gmail --dry-run`
2. Verify token.pickle exists in watchers/
3. Re-approve this file after fixing authentication

## Original Draft

{original email body}
```

---

## Logging Helper Functions

```python
import json
from datetime import datetime
from pathlib import Path

def log_email_action(action_type: str, details: dict):
    log_file = Path(f"AI_Employee_Vault/Logs/{datetime.now().strftime('%Y-%m-%d')}.json")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action_type": action_type,
        **details
    }

    # Append to daily log
    logs = []
    if log_file.exists():
        logs = json.loads(log_file.read_text())
    logs.append(entry)
    log_file.write_text(json.dumps(logs, indent=2))
```
