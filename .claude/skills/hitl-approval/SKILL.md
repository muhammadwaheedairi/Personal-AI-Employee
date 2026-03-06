---
name: hitl-approval
description: Human-in-the-loop approval mechanism for the AI Employee. This skill should be used BEFORE executing any sensitive action (payments, unknown contacts, bulk operations, deletions, config changes). Intercepts sensitive actions, writes approval request to /Pending_Approval/, waits for human decision in /Approved/ or /Rejected/, and only executes after explicit approval. This is a critical safety mechanism that prevents autonomous execution of high-risk actions.
---

# HITL Approval (Human-in-the-Loop)

Intercept and request human approval for sensitive actions before execution. This is the AI Employee's primary safety mechanism.

## Core Principle

**NEVER execute sensitive actions without explicit human approval.**

This skill ensures that high-risk operations (financial, unknown contacts, bulk operations, deletions, system changes) always have human oversight before execution.

## Workflow

1. **Detect** sensitive action about to be executed
2. **Pause** execution immediately (do NOT proceed)
3. **Analyze** action risk level and impact
4. **Create** approval request file in `/Pending_Approval/`
5. **Wait** for human decision (do NOT continue autonomously)
6. **Check** for approval:
   - File moved to `/Approved/` → Execute action
   - File moved to `/Rejected/` → Cancel action
7. **Log** approval/rejection to `/Vault/Logs/YYYY-MM-DD.json`
8. **Execute** action only if approved
9. Output `<promise>TASK_COMPLETE</promise>`

## Actions Requiring Approval (ALWAYS)

### 1. Financial Operations
- Marking invoices as paid
- Processing refunds
- Transferring money
- Confirming payment receipt
- Any action with financial impact

**Why:** Irreversible, legal implications, fraud prevention

### 2. Communication with Unknown Contacts
- Email to first-time recipient
- WhatsApp to new phone number
- Any message to contact not in history

**Why:** Brand reputation, spam risk, wrong recipient

### 3. Bulk Operations
- Sending to 3+ recipients at once
- Mass email campaigns
- Broadcast WhatsApp messages
- Deleting multiple files

**Why:** High impact if error, difficult to undo

### 4. Delete Operations
- Deleting any file from vault
- Removing data permanently
- Clearing folders

**Why:** Irreversible data loss, business impact

**Note:** Moving to /Done/ is archival, NOT deletion - does NOT require approval.

### 5. System Configuration Changes
- Modifying .env variables
- Changing watcher settings
- Updating MCP configs
- Altering cron schedules

**Why:** System stability, security, service disruption risk

## Actions That Do NOT Require Approval

### Safe Operations
- Reading files from vault
- Moving files to /Done/ (archival)
- Creating files in /Plans/
- Updating Dashboard.md
- Writing to /Vault/Logs/
- Queuing posts (queue_linkedin, queue_tweet, queue_facebook)
- Creating drafts (draft_email, draft_whatsapp)
- Communication to known/trusted contacts

## Sensitive Action Detection

See `references/sensitive-actions.md` for complete detection patterns.

**Detection decision tree:**
```
Is this action...
    │
    ├─ Financial? → REQUIRE APPROVAL
    ├─ To unknown contact? → REQUIRE APPROVAL
    ├─ Bulk operation (3+ targets)? → REQUIRE APPROVAL
    ├─ Delete operation? → REQUIRE APPROVAL
    ├─ System config change? → REQUIRE APPROVAL
    └─ Read-only or safe? → PROCEED WITHOUT APPROVAL
```

**High-risk keywords:**
- Financial: "payment", "paid", "refund", "transfer"
- Deletion: "delete", "remove", "rm", "clear"
- Bulk: "all", "bulk", "mass", "broadcast"
- System: "config", "settings", ".env", "cron"

## Approval Request File Format

```markdown
---
type: approval_request
action_type: {email_send|whatsapp_send|payment|delete|bulk_operation|config_change}
priority: {high|medium|low}
created: {iso_timestamp}
status: awaiting_approval
source_file: {original_file}
---

# Approval Request: {Action Description}

## Action Summary
{One-line description}

## Details
{Detailed information}

## Risk Assessment
**Risk Level:** {low|medium|high}
**Reversible:** {yes|no}
**Impact:** {description}

## Why Approval Required
{Explanation}

## To Approve
Move this file to /Approved folder to execute.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human decision*
```

## File Naming Convention

**Format:** `APPROVAL_{action_type}_{timestamp}.md`

**Examples:**
- `APPROVAL_email_unknown_20260306_143000.md`
- `APPROVAL_payment_20260306_143000.md`
- `APPROVAL_bulk_send_20260306_143000.md`
- `APPROVAL_delete_20260306_143000.md`

## Waiting for Human Decision

**After writing approval request:**
1. **STOP** execution immediately
2. **DO NOT** proceed with action
3. **DO NOT** retry or check repeatedly
4. **DO NOT** assume approval
5. **WAIT** for human to move file to /Approved/ or /Rejected/

**Human will:**
- Review the approval request
- Verify all details
- Make decision (approve or reject)
- Move file to appropriate folder

**Then:**
- If in /Approved/ → Execute action
- If in /Rejected/ → Cancel action and log

## Execution After Approval

**When file appears in /Approved/:**
1. Read approval file to confirm details
2. Execute the approved action
3. Log execution to /Vault/Logs/
4. Move approval file to /Done/
5. Update Dashboard.md

**Example:**
```
Approval file: APPROVAL_email_unknown_20260306_143000.md
Human moves to: /Approved/
Action: Read file, execute send_email MCP call
Log: email_sent with approval_id
Move: Approval file to /Done/
```

## Handling Rejection

**When file appears in /Rejected/:**
1. Read rejection file (may have human notes)
2. Cancel the action (do NOT execute)
3. Log rejection to /Vault/Logs/
4. Move rejection file to /Done/
5. Update Dashboard.md
6. Notify user of cancellation

**Example:**
```
Approval file: APPROVAL_payment_20260306_143000.md
Human moves to: /Rejected/
Action: Cancel payment operation
Log: payment_cancelled with rejection_reason
Move: Rejection file to /Done/
```

## Logging Format

**Approval request log:**
```json
{
  "timestamp": "2026-03-06T14:30:00Z",
  "action_type": "approval_requested",
  "approval_file": "APPROVAL_email_unknown_20260306_143000.md",
  "action_requested": "send_email",
  "risk_level": "medium",
  "status": "awaiting_decision"
}
```

**Approval granted log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "approval_granted",
  "approval_file": "APPROVAL_email_unknown_20260306_143000.md",
  "action_executed": "send_email",
  "recipient": "newcontact@example.com",
  "status": "executed"
}
```

**Approval rejected log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "approval_rejected",
  "approval_file": "APPROVAL_payment_20260306_143000.md",
  "action_cancelled": "mark_payment_as_paid",
  "reason": "human_rejected",
  "status": "cancelled"
}
```

## Example Scenarios

**Scenario 1: Email to unknown contact**
```
Action: Send email to newcontact@example.com (never contacted before)
Detection: Recipient not in /Done/ history, domain unknown
Decision: REQUIRE APPROVAL
Steps:
1. Pause email send operation
2. Create APPROVAL_email_unknown_20260306_143000.md in /Pending_Approval/
3. Wait for human decision
4. Human reviews and moves to /Approved/
5. Execute send_email MCP call
6. Log approval_granted
7. Move approval file to /Done/
```

**Scenario 2: Payment confirmation**
```
Action: Mark invoice as paid for $5,000
Detection: Financial keyword "paid", high amount
Decision: REQUIRE APPROVAL (financial operations ALWAYS require approval)
Steps:
1. Pause payment operation immediately
2. Create APPROVAL_payment_20260306_143000.md in /Pending_Approval/
3. Wait for human verification
4. Human reviews invoice and payment proof
5. Human moves to /Approved/
6. Execute mark_as_paid operation
7. Log approval_granted with amount
8. Move approval file to /Done/
```

**Scenario 3: Bulk WhatsApp send**
```
Action: Send same message to 5 clients
Detection: Bulk operation (5 recipients)
Decision: REQUIRE APPROVAL
Steps:
1. Pause bulk send operation
2. Create APPROVAL_bulk_send_20260306_143000.md with recipient list
3. Wait for human review
4. Human verifies all recipients are correct
5. Human moves to /Approved/
6. Execute send_whatsapp for each recipient
7. Log approval_granted with recipient count
8. Move approval file to /Done/
```

**Scenario 4: Delete operation rejected**
```
Action: Delete old log files
Detection: Delete operation
Decision: REQUIRE APPROVAL
Steps:
1. Pause delete operation
2. Create APPROVAL_delete_20260306_143000.md in /Pending_Approval/
3. Wait for human decision
4. Human reviews and decides files are still needed
5. Human moves to /Rejected/
6. Cancel delete operation (do NOT delete)
7. Log approval_rejected
8. Move rejection file to /Done/
9. Notify user that deletion was cancelled
```

## Security Rules

**NEVER bypass approval for:**
- Financial operations (no exceptions)
- Unknown contacts (no exceptions)
- Delete operations (no exceptions)

**NEVER assume approval:**
- Do not proceed if file is still in /Pending_Approval/
- Do not retry or check repeatedly
- Do not execute "just in case"

**ALWAYS wait for explicit human action:**
- File moved to /Approved/ = Execute
- File moved to /Rejected/ = Cancel
- File still in /Pending_Approval/ = Wait

## Urgent Actions

**Even if action is urgent, STILL require approval for:**
- Financial operations
- Unknown contacts
- Bulk operations
- Delete operations

**Urgent approval process:**
1. Write to /Pending_Approval/ with `priority: urgent` flag
2. Add "⚠️ URGENT" to approval file title
3. Update Dashboard.md with urgent flag
4. Wait for human decision (do NOT bypass)

## References

- `references/sensitive-actions.md` — Complete detection patterns for all sensitive action types
- `references/approval-templates.md` — Templates for creating approval request files

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
