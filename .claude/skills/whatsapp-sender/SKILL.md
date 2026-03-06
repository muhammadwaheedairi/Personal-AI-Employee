---
name: whatsapp-sender
description: Send approved WhatsApp messages from the AI Employee vault using WhatsApp MCP tools. This skill should be used when WhatsApp files appear in /Approved folder, or when the user asks to send WhatsApp messages, execute approved replies, or process outgoing WhatsApp queue. Uses send_whatsapp and draft_whatsapp MCP tools, respects DRY_RUN mode, logs all actions, and handles errors gracefully.
---

# WhatsApp Sender

Send approved WhatsApp messages via WhatsApp MCP server. Process files from `/Approved/`, validate phone numbers, send or draft messages, log actions, and move completed files to `/Done/`.

## Workflow

1. **Read** approved WhatsApp file from `/Approved/` folder
2. **Validate** phone number format (must be +[country_code][number])
3. **Validate** message body (not empty, reasonable length)
4. **Check DRY_RUN** mode status from environment
5. **Determine action** — send or draft based on recipient trust level
6. **Call MCP tool** — `send_whatsapp` or `draft_whatsapp` via WhatsApp MCP server
7. **Handle response** — success, error, or dry-run simulation
8. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
9. **Move file** to `/Done/` with status metadata
10. Output `<promise>TASK_COMPLETE</promise>`

## Decision Tree: Send vs Draft

```
Approved WhatsApp file in /Approved/
    │
    ├─ DRY_RUN=true? → Log simulation, move to /Done/
    │
    ├─ Unknown/new phone number? → draft_whatsapp (safer)
    │
    ├─ Financial keywords in message? → draft_whatsapp (requires review)
    │
    ├─ Known contact + routine message? → send_whatsapp
    │
    └─ Error occurred? → Log error, escalate to /Pending_Approval/
```

## Recipient Trust Levels

**Known/Trusted Recipients** (safe to send):
- Previous WhatsApp conversation participants
- Phone numbers in recent /Done/ WhatsApp files
- Explicitly marked as `trusted: true` in approval file
- Contacts from Company_Handbook.md or client list

**Unknown Recipients** (draft only):
- First-time contacts
- New phone numbers never seen before
- No prior WhatsApp history
- Marked as `trusted: false` or no trust field

## Phone Number Format

**Required format:** `+[country_code][number]`

**Valid examples:**
- Pakistan: `+923001234567`
- USA: `+14155551234`
- UK: `+447700900123`
- India: `+919876543210`

**Invalid formats:**
- Without +: `923001234567` ❌
- With spaces: `+92 300 1234567` ❌
- With dashes: `+92-300-1234567` ❌
- Without country code: `3001234567` ❌

## MCP Tool Usage

### send_whatsapp

Use for known, trusted recipients:

```python
# Load WhatsApp MCP tools first
result = mcp_call("send_whatsapp", {
    "to": "+923001234567",
    "body": "Thank you for your inquiry. We'll get back to you shortly."
})

# Expected responses:
# Success: "WhatsApp sent to +923001234567"
# Failure: "WhatsApp failed to +923001234567"
# DRY_RUN: "[DRY RUN] Would send_whatsapp to +923001234567: Thank you for your inquiry..."
# Error: "Error: {error_message}"
```

**Important:** Takes ~50-60 seconds to complete due to browser automation.

### draft_whatsapp

Use for unknown recipients or sensitive content:

```python
result = mcp_call("draft_whatsapp", {
    "to": "+923009999999",
    "body": "Thank you for reaching out. Your invoice is attached.",
    "context": "Invoice request from new client"
})

# Expected responses:
# Success: "Draft saved to WHATSAPP_draft_{timestamp}.md — move to /Approved to send"
# DRY_RUN: "[DRY RUN] Would draft_whatsapp to +923009999999: Thank you for reaching out..."
```

## Approved WhatsApp File Format

Expected format in `/Approved/`:

```markdown
---
type: whatsapp_reply
action: send_whatsapp
to: +923001234567
phone: +923001234567
source_file: WHATSAPP_{timestamp}.md
priority: medium
created: {iso_timestamp}
status: approved
trusted: true
---

# WhatsApp Reply: {contact_name}

**To:** {contact_name} (+923001234567)
**Priority:** {priority}

## Message to Send

{message body content here}

---

## Original Message Context
**Received:** {date}
**Matched Keywords:** {keywords}
**Content:** {original message preview}
```

## Security Rules

- **NEVER** send to unknown phone numbers without creating draft first
- **ALWAYS** check DRY_RUN mode before calling MCP tools
- **ALWAYS** validate phone number format (must include + and country code)
- **ALWAYS** log every send/draft action to `/Vault/Logs/YYYY-MM-DD.json`
- **NEVER** retry failed sends automatically — escalate to human
- **NEVER** send financial/payment messages without explicit `trusted: true` flag

## Error Handling

See `references/error-handling.md` for complete error handling patterns.

**Common errors:**

| Error | Action |
|-------|--------|
| `WhatsApp session not found` | Escalate to /Pending_Approval with instructions to re-authenticate |
| `Send button not found` | Log error, escalate to human (WhatsApp Web UI may have changed) |
| `Invalid phone number` | Log error, do not send, notify user |
| `Browser timeout` | Log error, escalate to human |
| `DRY_RUN active` | Log simulation, move to /Done/ with dry_run flag |
| `Unknown recipient` | Create draft instead of sending |

**Error escalation format:**

When MCP call fails, copy file back to `/Pending_Approval/` with error context:

```markdown
---
type: whatsapp_reply
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

## Logging Format

Every WhatsApp action must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

**Success log:**
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

**Draft log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_draft_created",
  "source_file": "WHATSAPP_REPLY_20260305_143000.md",
  "recipient": "+923009999999",
  "status": "success",
  "reason": "unknown_recipient"
}
```

**Error log:**
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

## Example Scenarios

**Scenario 1: Send to known contact**
```
Input: /Approved/WHATSAPP_REPLY_20260305_120000.md
Recipient: +923001234567 (known contact, trusted: true)
Action: Call send_whatsapp MCP tool
Result: WhatsApp sent successfully (takes ~50 seconds)
Log: whatsapp_sent with success status
Move: File to /Done/WHATSAPP_REPLY_20260305_120000.md
```

**Scenario 2: Draft for unknown contact**
```
Input: /Approved/WHATSAPP_REPLY_20260305_140000.md
Recipient: +923009999999 (unknown, no trust field)
Action: Call draft_whatsapp MCP tool (safer)
Result: Draft created in /Pending_Approval/WHATSAPP_draft_{timestamp}.md
Log: whatsapp_draft_created with reason: unknown_recipient
Move: File to /Done/WHATSAPP_REPLY_20260305_140000.md
```

**Scenario 3: DRY_RUN mode active**
```
Input: /Approved/WHATSAPP_REPLY_20260305_160000.md
DRY_RUN: true
Action: Simulate send, do not call MCP
Result: "[DRY RUN] Would send_whatsapp to +923001234567"
Log: whatsapp_sent with dry_run: true
Move: File to /Done/WHATSAPP_REPLY_20260305_160000.md
```

**Scenario 4: MCP error**
```
Input: /Approved/WHATSAPP_REPLY_20260305_180000.md
Action: Call send_whatsapp MCP tool
Result: "WhatsApp failed to +923001234567"
Log: whatsapp_send_failed with error details
Escalate: Copy file back to /Pending_Approval/ with error context
```

**Scenario 5: Invalid phone number**
```
Input: /Approved/WHATSAPP_REPLY_20260305_200000.md
Phone: 923001234567 (missing + prefix)
Action: Validate phone number → FAIL
Result: Do not call MCP, log validation error
Escalate: Copy file back to /Pending_Approval/ with validation error
```

## MCP Tools Reference

See `references/mcp-tools.md` for complete MCP tool documentation including:
- Tool parameters and return values
- Phone number format requirements
- DRY_RUN behavior
- Browser session requirements
- Timing considerations (50-60 seconds per send)
- Error messages and meanings
- Best practices and security considerations

## Browser Session Requirements

The `send_whatsapp` tool requires:
1. WhatsApp Web session authenticated and saved
2. Session stored in path defined by `WHATSAPP_SESSION_PATH` env variable
3. Playwright browser installed (`playwright install chromium`)

**First-time setup:**
```bash
# Run watcher once to authenticate
uv run python main.py --whatsapp --dry-run
# Scan QR code when browser opens
# Session will be saved for future use
```

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
