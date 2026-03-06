# WhatsApp Intent Detection

Classify incoming WhatsApp messages by intent to determine the appropriate action.

## Urgent Keywords (from watcher)

The WhatsApp watcher automatically flags messages containing these keywords:
- `urgent`
- `asap`
- `invoice`
- `payment`
- `emergency`
- `important`

All messages with these keywords are marked as **priority: high** in the WHATSAPP_*.md file.

---

## Intent Categories

### 1. Invoice Request

**Indicators:**
- Explicit request for invoice or bill
- Payment-related questions
- Receipt requests

**Keywords:** "invoice", "bill", "payment", "send me invoice", "receipt", "charges", "how much do I owe"

**Priority:** High (always)

**Action:** Generate invoice plan → route to /Pending_Approval/

**Template:** Use Invoice Generation Plan from `action-templates.md`

---

### 2. Payment Confirmation/Query

**Indicators:**
- Payment made notification
- Payment status inquiry
- Bank transfer confirmation

**Keywords:** "paid", "transferred", "sent payment", "payment done", "money sent", "transaction"

**Priority:** High (always)

**Action:** Escalate to human for verification → /Pending_Approval/

**Security Rule:** NEVER confirm payment receipt without human verification

---

### 3. Urgent Query/Problem

**Indicators:**
- Time-sensitive requests
- Problem reports
- Emergency situations

**Keywords:** "urgent", "asap", "emergency", "help", "problem", "issue", "not working", "broken"

**Priority:** High

**Action:** Draft immediate response → route to /Pending_Approval/ for quick approval

**Template:** Use Urgent Escalation Plan from `action-templates.md`

---

### 4. Pricing Query

**Indicators:**
- Questions about rates or costs
- Quote requests
- Service pricing inquiries

**Keywords:** "price", "cost", "rate", "quote", "how much", "fee", "charge", "pricing"

**Priority:** Medium

**Action:** Draft pricing response using /Vault/Accounting/Rates.md

**Template:** Use Pricing Query Plan from `action-templates.md`

---

### 5. Service Inquiry

**Indicators:**
- Questions about services offered
- Availability inquiries
- General business questions

**Keywords:** "do you", "can you", "available", "offer", "provide", "service"

**Priority:** Medium

**Action:** Draft informative response using Company_Handbook.md

---

### 6. Appointment/Scheduling

**Indicators:**
- Meeting requests
- Schedule inquiries
- Availability questions

**Keywords:** "meeting", "schedule", "appointment", "available", "when can", "book"

**Priority:** Medium

**Action:** Draft response with availability or calendar link

---

### 7. General/Informational

**Indicators:**
- Casual conversation
- Thank you messages
- General updates

**Keywords:** "thanks", "thank you", "ok", "got it", "understood"

**Priority:** Low

**Action:** Acknowledge if needed, otherwise archive

---

## Multi-Intent Messages

Some messages may have multiple intents. Prioritize in this order:
1. Payment/Financial (always human review)
2. Invoice Request (always human review)
3. Urgent/Emergency
4. Pricing Query
5. Service Inquiry
6. Appointment/Scheduling
7. General/Informational

---

## Priority Assignment Rules

| Keyword in message | Priority in Plan | Requires Approval |
|---|---|---|
| payment, invoice, money, paid | high | YES (always) |
| urgent, asap, emergency | high | YES |
| important | high | YES |
| help, problem, issue | medium | YES |
| price, quote, rate | medium | YES |
| thanks, ok, got it | low | NO (can archive) |

---

## Context Clues

Beyond keywords, consider:
- **Sender history:** Existing clients vs new contacts
- **Message length:** Long messages may indicate complex issues
- **Time of day:** Late-night messages may indicate urgency
- **Previous conversation:** Ongoing threads have context

---

## Approval File Format

When routing to `/Pending_Approval/`, use this format:

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

---

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