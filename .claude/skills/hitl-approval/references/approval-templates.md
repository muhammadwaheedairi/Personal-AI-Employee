# Approval Request Templates

Standard templates for creating approval request files in /Pending_Approval/.

## Base Approval Request Template

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
{One-line description of what will be executed}

## Details
{Detailed information about the action}

## Risk Assessment
**Risk Level:** {low|medium|high}
**Reversible:** {yes|no}
**Impact:** {description of potential impact}

## Why Approval Required
{Explanation of why this needs human review}

## To Approve
Move this file to /Approved folder to execute the action.

## To Reject
Move this file to /Rejected folder to cancel the action.

---
*Awaiting human decision*
```

---

## Email to Unknown Contact Template

```markdown
---
type: approval_request
action_type: email_send
priority: medium
created: {iso_timestamp}
status: awaiting_approval
source_file: {EMAIL_filename}
recipient: {email_address}
recipient_status: unknown
---

# Approval Request: Send Email to Unknown Contact

## Action Summary
Send email to {email_address} (first-time contact)

## Details
**To:** {email_address}
**Subject:** {subject}
**Domain:** {domain} (never contacted before)

## Email Content Preview
```
{first 200 chars of email body}
```

## Risk Assessment
**Risk Level:** Medium
**Reversible:** No (once sent, cannot unsend)
**Impact:** First impression with new contact, brand reputation

## Why Approval Required
- Recipient not in contact history (/Done/ folder)
- Domain never seen before
- No prior relationship established
- Potential for wrong recipient or spam perception

## To Approve
Move this file to /Approved folder to send the email.

## To Reject
Move this file to /Rejected folder to cancel sending.

---
*Awaiting human decision*
```

---

## WhatsApp to Unknown Number Template

```markdown
---
type: approval_request
action_type: whatsapp_send
priority: medium
created: {iso_timestamp}
status: awaiting_approval
source_file: {WHATSAPP_filename}
recipient: {phone_number}
recipient_status: unknown
---

# Approval Request: Send WhatsApp to Unknown Number

## Action Summary
Send WhatsApp message to {phone_number} (first-time contact)

## Details
**To:** {phone_number}
**Country Code:** {country_code}
**Contact History:** None found

## Message Content
```
{message body}
```

## Risk Assessment
**Risk Level:** Medium
**Reversible:** No (once sent, cannot unsend)
**Impact:** First impression, potential spam perception, privacy concerns

## Why Approval Required
- Phone number not in contact history
- No prior WhatsApp conversation
- No `trusted: true` flag in source file
- Potential for wrong number or unwanted contact

## To Approve
Move this file to /Approved folder to send the message.

## To Reject
Move this file to /Rejected folder to cancel sending.

---
*Awaiting human decision*
```

---

## Payment/Financial Action Template

```markdown
---
type: approval_request
action_type: payment
priority: high
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_filename}
amount: {amount}
---

# ⚠️ FINANCIAL APPROVAL REQUIRED: {Action Description}

## Action Summary
{Financial action description}

## Financial Details
**Action:** {mark_as_paid|refund|transfer|etc}
**Amount:** ${amount}
**Client:** {client_name}
**Invoice/Reference:** {invoice_id}

## Transaction Context
{Background information about this financial action}

## Risk Assessment
**Risk Level:** HIGH
**Reversible:** NO (financial transactions are permanent)
**Impact:** Direct financial impact, accounting records, legal implications

## Why Approval Required
- All financial operations require human verification
- Irreversible once executed
- Fraud prevention
- Audit trail requirements
- Legal/compliance considerations

## To Approve
Move this file to /Approved folder to execute the financial action.

## To Reject
Move this file to /Rejected folder to cancel the action.

---
**⚠️ CRITICAL: This is a financial operation. Verify all details before approving.**
```

---

## Bulk Operation Template

```markdown
---
type: approval_request
action_type: bulk_operation
priority: high
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_filename}
target_count: {number_of_targets}
---

# Approval Request: Bulk Operation ({target_count} targets)

## Action Summary
{Description of bulk operation}

## Bulk Operation Details
**Operation Type:** {send|delete|update|etc}
**Number of Targets:** {count}
**Target List:**
1. {target_1}
2. {target_2}
3. {target_3}
... ({total} total)

## Operation Preview
{Preview of what will happen to each target}

## Risk Assessment
**Risk Level:** High
**Reversible:** {yes|no}
**Impact:** Affects {count} items/recipients - high impact if error occurs

## Why Approval Required
- Bulk operations have high impact
- Difficult to undo if error occurs
- Potential for mass mistakes
- Each target should be verified

## To Approve
Move this file to /Approved folder to execute bulk operation.

## To Reject
Move this file to /Rejected folder to cancel bulk operation.

---
*Awaiting human decision - verify all targets before approving*
```

---

## Delete Operation Template

```markdown
---
type: approval_request
action_type: delete
priority: high
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_filename}
delete_target: {file_or_folder}
---

# ⚠️ DELETE APPROVAL REQUIRED: {Target Description}

## Action Summary
Delete {file_or_folder}

## Delete Details
**Target:** {full_path}
**Type:** {file|folder|multiple_files}
**Size:** {file_size or item_count}
**Last Modified:** {date}

## Content Preview
{Preview of what will be deleted}

## Risk Assessment
**Risk Level:** HIGH
**Reversible:** NO (permanent data loss)
**Impact:** Data will be permanently removed, cannot be recovered

## Why Approval Required
- Delete operations are irreversible
- Potential for accidental data loss
- Business impact if wrong file deleted
- Compliance/audit requirements

## Alternative Actions
- Move to /Done/ instead (archival, not deletion)
- Create backup before deleting
- Verify this is truly no longer needed

## To Approve
Move this file to /Approved folder to execute deletion.

## To Reject
Move this file to /Rejected folder to cancel deletion.

---
**⚠️ WARNING: This will permanently delete data. Verify before approving.**
```

---

## System Configuration Change Template

```markdown
---
type: approval_request
action_type: config_change
priority: high
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_filename}
config_file: {config_file_path}
---

# Approval Request: System Configuration Change

## Action Summary
Modify {config_file}

## Configuration Change Details
**File:** {config_file_path}
**Change Type:** {add|modify|remove}

**Current Value:**
```
{current_config}
```

**Proposed Value:**
```
{new_config}
```

## Impact Analysis
{Description of what this change will affect}

## Risk Assessment
**Risk Level:** High
**Reversible:** Yes (can revert config)
**Impact:** System behavior change, potential service disruption

## Why Approval Required
- System configuration changes affect stability
- Potential for service disruption
- Security implications
- Difficult to debug if broken

## Rollback Plan
{How to revert if something goes wrong}

## To Approve
Move this file to /Approved folder to apply configuration change.

## To Reject
Move this file to /Rejected folder to cancel change.

---
*Awaiting human decision*
```

---

## Urgent Action Template

```markdown
---
type: approval_request
action_type: {action_type}
priority: urgent
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_filename}
urgency_reason: {reason}
---

# ⚠️ URGENT APPROVAL REQUIRED: {Action Description}

## Action Summary
{Description of urgent action}

## Urgency Context
**Why Urgent:** {explanation}
**Deadline:** {deadline if applicable}
**Consequences of Delay:** {what happens if not done quickly}

## Action Details
{Detailed information about the action}

## Risk Assessment
**Risk Level:** {level}
**Reversible:** {yes|no}
**Impact:** {description}

## Why Approval Required Despite Urgency
{Explanation - even urgent actions need approval if sensitive}

## To Approve
Move this file to /Approved folder to execute immediately.

## To Reject
Move this file to /Rejected folder to cancel.

---
**⚠️ URGENT: Please review and decide as soon as possible.**
```

---

## Template Selection Guide

| Action Type | Use Template | Priority |
|---|---|---|
| Email to unknown contact | Email to Unknown Contact | Medium |
| WhatsApp to unknown number | WhatsApp to Unknown Number | Medium |
| Payment/financial operation | Payment/Financial Action | High |
| Bulk send (3+ recipients) | Bulk Operation | High |
| Delete file/folder | Delete Operation | High |
| System config change | System Configuration Change | High |
| Urgent + sensitive | Urgent Action | Urgent |

---

## Approval File Naming Convention

**Format:** `APPROVAL_{action_type}_{timestamp}.md`

**Examples:**
- `APPROVAL_email_unknown_20260306_143000.md`
- `APPROVAL_payment_20260306_143000.md`
- `APPROVAL_bulk_send_20260306_143000.md`
- `APPROVAL_delete_20260306_143000.md`
- `APPROVAL_config_20260306_143000.md`
