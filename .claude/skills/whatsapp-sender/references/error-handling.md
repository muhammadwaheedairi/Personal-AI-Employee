# Error Handling & Logging Patterns

Comprehensive guide for handling errors and logging WhatsApp send actions.

## Error Categories

### 1. Pre-Send Validation Errors

**Check before calling MCP:**
- Phone number format validation (must include country code with +)
- Message body not empty
- DRY_RUN mode status
- Recipient is known/approved contact

**Example validation:**
```python
import re

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format: +[country_code][number]"""
    pattern = r'^\+\d{10,15}$'
    return re.match(pattern, phone) is not None

def validate_send_request(to: str, body: str) -> tuple[bool, str]:
    if not validate_phone_number(to):
        return False, f"Invalid phone number format: {to}. Must be +[country_code][number]"
    if not body.strip():
        return False, "Message body cannot be empty"
    if len(body) > 4096:
        return False, f"Message too long: {len(body)} chars (max 4096)"
    return True, "Valid"
```

---

### 2. MCP Tool Errors

**Common MCP errors:**
- `WhatsApp session not found` → Authentication issue
- `Send button not found` → WhatsApp Web UI changed
- `Browser timeout` → Network or loading issue
- `Permission denied` → File system issue

**Handling pattern:**
```python
try:
    result = await mcp_call("send_whatsapp", {"to": phone, "body": message})

    if "failed" in result.lower():
        # Log failure
        log_error("whatsapp_send_failed", result)
        # Escalate to human
        escalate_to_human(approval_file, error=result)
        return False

    if "sent" in result.lower():
        return True

except Exception as e:
    log_error("mcp_exception", str(e))
    return False
```

---

### 3. Browser/Playwright Errors

**Common browser errors:**
- Session expired → Re-authenticate required
- Browser crash → Restart needed
- Network timeout → Retry or escalate
- Element not found → UI changed

**Handling pattern:**
```python
def handle_browser_error(error: str, approval_file: Path) -> None:
    if "session" in error.lower():
        escalate_with_message(
            approval_file,
            "WhatsApp session expired. Run: uv run python main.py --whatsapp --dry-run"
        )
    elif "timeout" in error.lower():
        escalate_with_message(
            approval_file,
            "Browser timeout. Check network connection and try again."
        )
    else:
        escalate_with_message(
            approval_file,
            f"Browser error: {error}. Manual intervention required."
        )
```

---

### 4. File System Errors

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
  "action_type": "whatsapp_sent",
  "source_file": "WHATSAPP_REPLY_20260305_143000.md",
  "recipient": "+923001234567",
  "message_preview": "Thank you for your inquiry...",
  "status": "success",
  "dry_run": false,
  "execution_time_seconds": 52
}
```

### Error Log Entry

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_send_failed",
  "source_file": "WHATSAPP_REPLY_20260305_143000.md",
  "recipient": "+923001234567",
  "status": "error",
  "error_message": "Send button not found",
  "escalated_to_human": true
}
```

### Draft Log Entry

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_draft_created",
  "source_file": "WHATSAPP_REPLY_20260305_143000.md",
  "recipient": "+923009999999",
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
- High-value/sensitive message
- Browser session issues

**Action:**
1. Call `draft_whatsapp` instead of `send_whatsapp`
2. Log draft creation
3. Notify user that draft was created
4. Move approval file to /Done/ with draft status

---

### Strategy 3: Retry with Backoff

**NOT RECOMMENDED** for WhatsApp sending. Never auto-retry failed sends without human review.

**Why:**
- Browser automation is slow (~50 seconds per send)
- Failed sends may have partially succeeded
- Duplicate messages are unprofessional
- Session issues require manual intervention

---

## Error Notification Format

When escalating errors to human, update the approval file:

```markdown
---
type: whatsapp_reply
action: send_whatsapp
to: +923001234567
status: error_requires_review
error: "Send button not found"
created: {iso_timestamp}
---

# ⚠️ ERROR: WhatsApp Send Failed

**Error:** Send button not found

**Original Request:**
- **To:** +923001234567
- **Message:** Thank you for your inquiry...
- **Status:** Failed to send

## Recommended Action
1. Check WhatsApp Web session: `uv run python main.py --whatsapp --dry-run`
2. Verify browser automation is working
3. Re-approve this file after fixing session

## Original Message

{original message body}
```

---

## Phone Number Validation

**Validation rules:**
```python
def validate_phone_number(phone: str) -> tuple[bool, str]:
    """
    Validate phone number format for WhatsApp.
    Returns: (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is required"

    if not phone.startswith("+"):
        return False, f"Phone number must start with + (got: {phone})"

    # Remove + and check if remaining is all digits
    digits = phone[1:]
    if not digits.isdigit():
        return False, f"Phone number must contain only digits after + (got: {phone})"

    # Check length (10-15 digits is standard for international numbers)
    if len(digits) < 10:
        return False, f"Phone number too short: {len(digits)} digits (min 10)"

    if len(digits) > 15:
        return False, f"Phone number too long: {len(digits)} digits (max 15)"

    return True, "Valid"
```

---

## Logging Helper Functions

```python
import json
from datetime import datetime
from pathlib import Path

def log_whatsapp_action(action_type: str, details: dict):
    """Log WhatsApp action to daily log file."""
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

def log_whatsapp_send(source_file: str, recipient: str, success: bool, error: str = None):
    """Log WhatsApp send attempt."""
    log_whatsapp_action(
        "whatsapp_sent" if success else "whatsapp_send_failed",
        {
            "source_file": source_file,
            "recipient": recipient,
            "status": "success" if success else "error",
            "error_message": error if error else None
        }
    )
```

---

## DRY_RUN Handling

**Always check DRY_RUN before sending:**

```python
import os

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

if DRY_RUN:
    log_whatsapp_action("whatsapp_send_simulated", {
        "source_file": approval_file.name,
        "recipient": phone,
        "message_preview": body[:50],
        "dry_run": True
    })
    # Move to /Done/ with dry_run flag
    move_to_done(approval_file, dry_run=True)
else:
    # Actual send via MCP
    result = await mcp_call("send_whatsapp", {"to": phone, "body": body})
```
