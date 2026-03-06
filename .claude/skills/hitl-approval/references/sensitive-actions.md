# Sensitive Action Detection Patterns

Guide for identifying actions that require human approval before execution.

## Action Categories Requiring HITL

### 1. Financial Actions (ALWAYS REQUIRE APPROVAL)

**Payment Operations:**
- Marking invoices as paid
- Processing refunds
- Transferring money
- Updating payment status
- Confirming payment receipt

**Keywords to detect:**
- "mark as paid", "payment received", "confirm payment"
- "refund", "transfer", "send money"
- "update payment status", "paid invoice"

**Why approval required:**
- Irreversible financial impact
- Legal/accounting implications
- Fraud prevention
- Audit trail requirements

---

### 2. Communication with New/Unknown Contacts (ALWAYS REQUIRE APPROVAL)

**Email to unknown recipients:**
- First-time email to new contact
- Email to domain never seen before
- Bulk email to multiple new contacts

**WhatsApp to unknown numbers:**
- First-time message to new phone number
- Message to number not in recent history
- Bulk WhatsApp to multiple new contacts

**Detection criteria:**
- Recipient not in /Done/ folder history
- Domain/number not in Company_Handbook.md contacts
- No `trusted: true` flag in approval file
- Marked as `unknown_recipient` in metadata

**Why approval required:**
- Brand reputation risk
- Potential spam/harassment
- Wrong recipient risk
- Professional relationship management

---

### 3. Bulk Operations (ALWAYS REQUIRE APPROVAL)

**Bulk sends:**
- Sending same message to 3+ recipients
- Mass email campaigns
- Broadcast WhatsApp messages
- Multi-platform social posts at once

**Bulk deletes:**
- Deleting multiple files at once
- Clearing entire folders
- Mass archive operations

**Detection criteria:**
- Loop or iteration over recipient list
- Multiple send operations in single plan
- Delete operation with wildcard or multiple targets

**Why approval required:**
- High impact if error occurs
- Difficult to undo
- Potential for mass mistakes
- Compliance considerations

---

### 4. Delete Operations (ALWAYS REQUIRE APPROVAL)

**File deletions:**
- Deleting any file from vault
- Removing completed tasks
- Clearing logs or history

**Data deletions:**
- Removing client records
- Deleting business data
- Clearing configuration

**Detection criteria:**
- Any operation using `delete`, `remove`, `rm`
- Moving files to trash/recycle
- Permanent data removal

**Why approval required:**
- Irreversible data loss
- Potential business impact
- Compliance/audit requirements
- Accidental deletion prevention

**Note:** Moving files to /Done/ is NOT deletion - it's archival and does NOT require approval.

---

### 5. System Configuration Changes (REQUIRE APPROVAL)

**Configuration updates:**
- Changing .env variables
- Modifying watcher settings
- Updating MCP server configs
- Changing cron schedules

**Detection criteria:**
- Writing to .env file
- Modifying config.py
- Changing settings.json
- Updating cron_setup.sh

**Why approval required:**
- System stability risk
- Potential service disruption
- Security implications
- Difficult to debug if broken

---

### 6. External API Calls (CONTEXT-DEPENDENT)

**Require approval:**
- First-time API calls to new services
- API calls with financial impact
- API calls that modify external data
- API calls to production systems

**Do NOT require approval:**
- Read-only API calls
- Calls to known/trusted services
- Development/test environment calls
- Explicitly approved API endpoints

**Detection criteria:**
- HTTP POST/PUT/DELETE to external URL
- API call with authentication tokens
- Calls to payment/financial APIs
- Calls to CRM/database systems

---

## Actions That Do NOT Require Approval

### Safe Operations

**File operations:**
- Reading files from vault
- Moving files to /Done/ (archival)
- Creating new files in /Plans/
- Updating Dashboard.md
- Writing to /Vault/Logs/

**Communication to known contacts:**
- Email to previous recipients (in /Done/ history)
- WhatsApp to known numbers (marked `trusted: true`)
- Replies in existing threads

**Content creation:**
- Queuing social media posts (queue_linkedin, queue_tweet, queue_facebook)
- Creating drafts (draft_email, draft_whatsapp)
- Writing plans to /Plans/

**Read-only operations:**
- Reading vault files
- Checking folder contents
- Analyzing logs
- Generating reports

---

## Detection Decision Tree

```
Is this action...
    │
    ├─ Financial? → REQUIRE APPROVAL
    │
    ├─ To unknown contact? → REQUIRE APPROVAL
    │
    ├─ Bulk operation (3+ targets)? → REQUIRE APPROVAL
    │
    ├─ Delete operation? → REQUIRE APPROVAL
    │
    ├─ System config change? → REQUIRE APPROVAL
    │
    ├─ External API with side effects? → REQUIRE APPROVAL
    │
    └─ Read-only or safe operation? → PROCEED WITHOUT APPROVAL
```

---

## Keyword Detection Patterns

### High-Risk Keywords (Always flag for approval)

**Financial:**
- "payment", "paid", "refund", "transfer", "invoice paid"
- "mark as paid", "confirm payment", "payment received"

**Deletion:**
- "delete", "remove", "rm", "clear", "purge", "erase"

**Bulk:**
- "all", "bulk", "mass", "broadcast", "everyone"
- "multiple", "batch", "group send"

**System:**
- "config", "settings", ".env", "cron", "system"

### Medium-Risk Keywords (Context-dependent)

**Communication:**
- "send to", "email", "message", "post"
- Check if recipient is known/unknown

**Modification:**
- "update", "change", "modify", "edit"
- Check what is being modified

---

## Special Cases

### Urgent Actions

Even if action is urgent, STILL require approval for:
- Financial operations
- Unknown contacts
- Bulk operations
- Delete operations

**Urgent approval process:**
1. Write to /Pending_Approval/ with `priority: urgent` flag
2. Add "⚠️ URGENT" to approval file title
3. Update Dashboard.md with urgent flag
4. Wait for human decision (do NOT bypass)

### Recurring Actions

If action is recurring (e.g., weekly briefing):
- First occurrence: Require approval
- Subsequent occurrences: Can proceed if explicitly approved in plan
- Document approval in plan: "Approved for recurring execution"

### Chained Actions

If plan has multiple steps, some requiring approval:
1. Execute safe steps first
2. Stop at first sensitive action
3. Write approval request
4. Wait for approval
5. Resume execution after approval

---

## False Positive Prevention

**Do NOT flag these as requiring approval:**
- Moving files to /Done/ (archival, not deletion)
- Creating drafts (not sending)
- Queuing posts (not posting directly)
- Reading files (read-only)
- Logging actions (safe operation)
- Updating Dashboard.md (safe operation)

**Key distinction:**
- **Queue/Draft** = Safe (human can review before execution)
- **Send/Post directly** = Requires approval (immediate execution)

---

## Approval Bypass Scenarios

**NEVER bypass approval for:**
- Financial operations (no exceptions)
- Unknown contacts (no exceptions)
- Delete operations (no exceptions)

**Can bypass approval if:**
- Explicitly marked `trusted: true` in source file
- Action is read-only
- Action is creating draft/queue (not executing)
- User has pre-approved in plan with clear scope
