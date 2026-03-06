---
name: whatsapp-triage
description: Triage and process WhatsApp action files from the AI Employee vault. This skill should be used when WHATSAPP_*.md files appear in /Needs_Action folder, or when user asks to handle WhatsApp messages, draft replies, or generate invoices from chat requests. Reads message content, detects intent, creates Plan.md with steps, and always routes replies to /Pending_Approval — never sends directly to WhatsApp without human approval.
---

# WhatsApp Triage

Process `WHATSAPP_*.md` files from `/Needs_Action/`. Detect intent, assign priority, create action plans, and route all outgoing actions to `/Pending_Approval/`. **All WhatsApp sends require HITL approval** — never act directly.

## Workflow

1. **Read** the `WHATSAPP_*.md` file from `/Needs_Action/`
2. **Detect intent** — see `references/intents.md` for classification patterns
3. **Assign priority** based on urgent keywords (already set by watcher):
   - **high**: urgent, asap, invoice, payment, emergency, important
   - **medium**: help, problem, price, quote, service inquiry
   - **low**: general conversation, thank you messages
4. **Create action plan** in `/Plans/PLAN_WHATSAPP_{timestamp}.md` using templates from `references/action-templates.md`
5. **Route sensitive messages** to `/Pending_Approval/` for human review:
   - Payment/invoice messages (always)
   - Urgent/emergency messages (always)
   - All reply drafts (always — never send without approval)
6. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
7. **Move** source `WHATSAPP_*.md` to `/Done/` when plan is complete
8. Output `<promise>TASK_COMPLETE</promise>`

## Urgent Keywords (from watcher)

The WhatsApp watcher automatically flags messages containing these keywords and marks them as **priority: high**:
- `urgent`
- `asap`
- `invoice`
- `payment`
- `emergency`
- `important`

These are defined in `watchers/whatsapp_watcher.py:18`:
```python
URGENT_KEYWORDS = ["urgent", "asap", "invoice", "payment", "emergency", "important"]
```

## Action Decision Tree

```
WHATSAPP_*.md arrives in /Needs_Action/
    │
    ├─ Contains "payment" or "invoice"? → Generate invoice plan → /Pending_Approval/ (high priority)
    │
    ├─ Contains "urgent" or "emergency"? → Draft urgent response → /Pending_Approval/ (high priority)
    │
    ├─ Contains "price" or "quote"? → Draft pricing response → /Pending_Approval/ (medium priority)
    │
    ├─ Service inquiry? → Draft informative response → /Pending_Approval/ (medium priority)
    │
    └─ General message? → Determine if response needed → /Pending_Approval/ or archive
```

## WHATSAPP_*.md File Format

Files created by the watcher have this structure:

```markdown
---
type: whatsapp
source: whatsapp_web
received: {iso_timestamp}
priority: high
status: pending
msg_id: {hash_id}
---

# WhatsApp Urgent Message

**Received:** {date_time}
**Priority:** High

## Message Preview
{message_text_with_context}

## Matched Keyword In
{line_that_triggered_urgent_flag}

## Suggested Actions
- [ ] Reply to sender
- [ ] Generate invoice if requested
- [ ] Escalate if payment-related
```

## Plan.md Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: {high|medium|low}
status: pending
---

# Plan: WhatsApp — {detected_intent}

## Context
**Received:** {date}
**Priority:** {priority}
**Matched Keywords:** {keywords}

## Objective
{one-line goal — e.g., "Draft reply to urgent client inquiry about project status"}

## Steps
- [ ] {step 1}
- [ ] {step 2}
- [ ] {step 3}
...

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when {completion condition}.
```

## Security Rules

- **NEVER** send WhatsApp messages directly — always write drafts to `/Pending_Approval/`
- **ALWAYS** route payment/invoice messages to `/Pending_Approval/` for human review
- **ALWAYS** route urgent messages to `/Pending_Approval/` for immediate human attention
- **ALWAYS** log every action to `/Vault/Logs/YYYY-MM-DD.json`
- **NEVER** delete WHATSAPP_*.md files — move to `/Done/` instead
- **NEVER** confirm payment receipt without explicit human verification

## Approval File Format

When routing replies to `/Pending_Approval/`, use this format:

```markdown
---
type: whatsapp_reply
action: send_whatsapp
to: {contact_name}
phone: {phone_number}
source_file: WHATSAPP_{timestamp}.md
priority: {high|medium|low}
created: {iso_timestamp}
status: awaiting_approval
---

# WhatsApp Reply: {contact_name}

**To:** {contact_name} ({phone_number})
**Priority:** {priority}

## Message to Send

{reply_text}

---

## Original Message Context
**Received:** {date}
**Matched Keywords:** {keywords}
**Content:** {original message preview}

---

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder or delete.

---
*Awaiting human approval before sending*
```

## Invoice Approval Format

For invoice generation requests:

```markdown
---
type: invoice
action: generate_invoice
client: {client_name}
source_file: WHATSAPP_{timestamp}.md
priority: high
created: {iso_timestamp}
status: awaiting_approval
---

# Invoice Request: {client_name}

**Client:** {client_name}
**Service/Period:** {description}
**Amount:** ${amount}

## Invoice Details

**To:** {client_name}
**Email:** {client_email}
**Amount:** ${amount}
**Due Date:** {date}
**Bank Details:** {from Company_Handbook.md}

## Description
{service description}

---

## Original WhatsApp Request
**Received:** {date}
**Content:** {original message}

---

## To Approve
Move this file to /Approved folder to generate and send invoice.

## To Reject
Move this file to /Rejected folder.

---
*Awaiting human approval before generating invoice*
```

## Intent Detection Guide

See `references/intents.md` for detailed intent classification patterns:
1. Invoice Request (high priority, always approve)
2. Payment Confirmation/Query (high priority, always approve)
3. Urgent Query/Problem (high priority)
4. Pricing Query (medium priority)
5. Service Inquiry (medium priority)
6. Appointment/Scheduling (medium priority)
7. General/Informational (low priority)

## Action Templates

See `references/action-templates.md` for complete plan templates:
- Reply Plan Template
- Invoice Generation Plan Template
- Urgent Escalation Template
- Payment/Financial Escalation Template
- Pricing Query Plan Template
- General Query Plan Template

## Example Scenarios

**Scenario 1: Invoice request**
```
Input: WHATSAPP_20260305_120000.md
Content: "Hi, can you send me the invoice for this month?"
Matched Keywords: "invoice"
Priority: high
Action: Create invoice generation plan
Output: PLAN_WHATSAPP_20260305_120000_invoice.md in /Plans/
Route: INVOICE_{client}_{timestamp}.md to /Pending_Approval/
```

**Scenario 2: Urgent problem**
```
Input: WHATSAPP_20260305_140000.md
Content: "Urgent! The website is down, clients can't access it"
Matched Keywords: "urgent"
Priority: high
Action: Draft urgent response plan
Output: PLAN_WHATSAPP_20260305_140000_urgent.md in /Plans/
Route: WHATSAPP_REPLY_{timestamp}.md to /Pending_Approval/
```

**Scenario 3: Pricing inquiry**
```
Input: WHATSAPP_20260305_160000.md
Content: "How much do you charge for web design?"
Matched Keywords: "how much", "charge"
Priority: medium
Action: Draft pricing response using /Vault/Accounting/Rates.md
Output: PLAN_WHATSAPP_20260305_160000_pricing.md in /Plans/
Route: WHATSAPP_REPLY_{timestamp}.md to /Pending_Approval/
```

**Scenario 4: Payment confirmation**
```
Input: WHATSAPP_20260305_180000.md
Content: "I just transferred the payment, transaction ID: 12345"
Matched Keywords: "payment", "transferred"
Priority: high
Action: Escalate to human for verification (NEVER auto-confirm)
Output: PLAN_WHATSAPP_20260305_180000_payment.md in /Plans/
Route: Copy WHATSAPP_*.md to /Pending_Approval/ immediately
```

**Scenario 5: Thank you message**
```
Input: WHATSAPP_20260305_200000.md
Content: "Thanks for the quick response!"
Matched Keywords: "thanks"
Priority: low
Action: Archive (no response needed)
Output: Move WHATSAPP_*.md to /Done/, log action
```

## Logging Format

Every WhatsApp action must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

**Triage log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_triage",
  "source_file": "WHATSAPP_20260305_143000.md",
  "intent": "invoice_request",
  "priority": "high",
  "action_taken": "created_invoice_plan",
  "plan_file": "PLAN_WHATSAPP_20260305_143000_invoice.md",
  "routed_to_approval": true
}
```

**Reply draft log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_draft_created",
  "source_file": "WHATSAPP_20260305_143000.md",
  "recipient": "Client Name",
  "intent": "urgent_query",
  "priority": "high",
  "approval_file": "WHATSAPP_REPLY_20260305_143000.md"
}
```

**Archive log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "whatsapp_archived",
  "source_file": "WHATSAPP_20260305_143000.md",
  "intent": "general",
  "priority": "low",
  "reason": "no_response_needed"
}
```

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`