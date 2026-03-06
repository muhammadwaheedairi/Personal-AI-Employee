---
name: gmail-sender
description: Send approved emails from the AI Employee vault using Gmail MCP tools. This skill should be used when email files appear in /Approved folder, or when the user asks to send emails, execute approved replies, or process outgoing email queue. Uses send_email and draft_email MCP tools, respects DRY_RUN mode, logs all actions, and handles errors gracefully.
---

# Gmail Sender

Send approved emails via Gmail MCP server. Process files from `/Approved/`, validate recipients, send or draft emails, log actions, and move completed files to `/Done/`.

## Workflow

1. **Read** approved email file from `/Approved/` folder
2. **Validate** email parameters (recipient, subject, body)
3. **Check DRY_RUN** mode status from environment
4. **Determine action** — send or draft based on recipient trust level
5. **Call MCP tool** — `send_email` or `draft_email` via email MCP server
6. **Handle response** — success, error, or dry-run simulation
7. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
8. **Move file** to `/Done/` with status metadata
9. Output `<promise>TASK_COMPLETE</promise>`

## Decision Tree: Send vs Draft

```
Approved email file in /Approved/
    │
    ├─ DRY_RUN=true? → Log simulation, move to /Done/
    │
    ├─ Unknown/new recipient? → draft_email (safer)
    │
    ├─ Financial keywords in subject/body? → draft_email (requires review)
    │
    ├─ Known contact + routine reply? → send_email
    │
    └─ Error occurred? → Log error, escalate to /Pending_Approval/
```

## Recipient Trust Levels

**Known/Trusted Recipients** (safe to send):
- Previous email thread participants
- Contacts in recent /Done/ email files
- Domain matches company/client domains
- Explicitly marked as `trusted: true` in approval file

**Unknown Recipients** (draft only):
- First-time contacts
- New domains never seen before
- No prior email history
- Marked as `trusted: false` or no trust field

## MCP Tool Usage

### send_email

Use for known, trusted recipients:

```python
# Load email MCP tools first
result = mcp_call("send_email", {
    "to": "client@example.com",
    "subject": "Re: Project Update",
    "body": "Thank you for your email. The project is on track..."
})

# Expected responses:
# Success: "Email sent to client@example.com"
# DRY_RUN: "[DRY RUN] Would send_email to client@example.com: Re: Project Update"
# Error: "Error: Gmail token not found"
```

### draft_email

Use for unknown recipients or sensitive content:

```python
result = mcp_call("draft_email", {
    "to": "newcontact@example.com",
    "subject": "Re: Inquiry",
    "body": "Thank you for reaching out..."
})

# Expected responses:
# Success: "Draft created for newcontact@example.com"
# DRY_RUN: "[DRY RUN] Would draft_email to newcontact@example.com: Re: Inquiry"
```

## Approved Email File Format

Expected format in `/Approved/`:

```markdown
---
type: email_reply
source_file: EMAIL_{timestamp}_{subject}.md
priority: medium
created: {iso_timestamp}
status: approved
trusted: true
---

# Email Reply: {subject}

**To:** recipient@example.com
**Subject:** Re: {original_subject}

## Draft Reply

{email body content here}

---

## Original Email Context
**From:** sender@example.com
**Received:** {date}
**Content:** {original email snippet}
```

## Security Rules

- **NEVER** send to unknown recipients without creating draft first
- **ALWAYS** check DRY_RUN mode before calling MCP tools
- **ALWAYS** log every send/draft action to `/Vault/Logs/YYYY-MM-DD.json`
- **NEVER** retry failed sends automatically — escalate to human
- **ALWAYS** validate email address format before calling MCP
- **NEVER** send financial/payment emails without explicit `trusted: true` flag

## Error Handling

See `references/error-handling.md` for complete error handling patterns.

**Common errors:**

| Error | Action |
|-------|--------|
| `Gmail token not found` | Escalate to /Pending_Approval with error context |
| `Invalid recipient` | Log error, do not send, notify user |
| `MCP server not responding` | Log error, escalate to human |
| `DRY_RUN active` | Log simulation, move to /Done/ with dry_run flag |
| `Unknown recipient` | Create draft instead of sending |

**Error escalation format:**

When MCP call fails, copy file back to `/Pending_Approval/` with error context:

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

## Logging Format

Every email action must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

**Success log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_sent",
  "source_file": "REPLY_20260305_143000_subject.md",
  "recipient": "client@example.com",
  "subject": "Re: Project Update",
  "status": "success",
  "dry_run": false,
  "mcp_response": "Email sent to client@example.com"
}
```

**Draft log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_draft_created",
  "source_file": "REPLY_20260305_143000_subject.md",
  "recipient": "unknown@example.com",
  "subject": "Re: New Contact",
  "status": "success",
  "reason": "unknown_recipient"
}
```

**Error log:**
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

## Example Scenarios

**Scenario 1: Send to known contact**
```
Input: /Approved/REPLY_20260305_120000_project_update.md
Recipient: client@example.com (known contact)
Action: Call send_email MCP tool
Result: Email sent successfully
Log: email_sent with success status
Move: File to /Done/REPLY_20260305_120000_project_update.md
```

**Scenario 2: Draft for unknown contact**
```
Input: /Approved/REPLY_20260305_140000_new_inquiry.md
Recipient: newperson@example.com (unknown)
Action: Call draft_email MCP tool (safer)
Result: Draft created in Gmail
Log: email_draft_created with reason: unknown_recipient
Move: File to /Done/REPLY_20260305_140000_new_inquiry.md
```

**Scenario 3: DRY_RUN mode active**
```
Input: /Approved/REPLY_20260305_160000_test.md
DRY_RUN: true
Action: Simulate send, do not call MCP
Result: "[DRY RUN] Would send_email to test@example.com"
Log: email_sent with dry_run: true
Move: File to /Done/REPLY_20260305_160000_test.md
```

**Scenario 4: MCP error**
```
Input: /Approved/REPLY_20260305_180000_urgent.md
Action: Call send_email MCP tool
Result: "Error: Gmail token not found"
Log: email_send_failed with error details
Escalate: Copy file back to /Pending_Approval/ with error context
```

## MCP Tools Reference

See `references/mcp-tools.md` for complete MCP tool documentation including:
- Tool parameters and return values
- DRY_RUN behavior
- Error messages and meanings
- Best practices and security considerations

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
