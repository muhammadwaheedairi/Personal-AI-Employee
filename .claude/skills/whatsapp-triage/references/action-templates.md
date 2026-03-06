# WhatsApp Action Templates

Templates for creating action plans based on WhatsApp message intent.

## Reply Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: {high|medium|low}
status: pending
---

# Plan: WhatsApp Reply — {intent}

## Context
**Received:** {date}
**Priority:** {priority}
**Matched Keywords:** {keywords}

## Objective
Draft reply to address: {one-line summary}

## Steps
- [ ] Analyze message context and sender intent
- [ ] Draft appropriate response using Company_Handbook.md tone
- [ ] Write draft to /Pending_Approval/WHATSAPP_REPLY_{timestamp}.md
- [ ] Await human approval before sending
- [ ] Log action to /Vault/Logs/YYYY-MM-DD.json

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when reply is sent or archived.
```

---

## Invoice Generation Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: high
status: pending
---

# Plan: Generate Invoice — {client_name}

## Context
**Received:** {date}
**Client:** {client_name}
**Request:** Invoice for {service/period}

## Objective
Generate invoice and send to client

## Steps
- [ ] Identify client from message context
- [ ] Read /Vault/Accounting/Rates.md for current rates
- [ ] Calculate amount for the period/service mentioned
- [ ] Create invoice content (client name, amount, bank details, due date)
- [ ] Write /Pending_Approval/INVOICE_{client}_{timestamp}.md
- [ ] After approval: send invoice via email MCP to client email on file
- [ ] Log to /Vault/Logs/YYYY-MM-DD.json with action_type=invoice_generated
- [ ] Send WhatsApp confirmation message (via approval)

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when invoice is sent and confirmed.
```

---

## Urgent Escalation Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: high
status: pending
---

# Plan: URGENT — {issue_summary}

## Context
**Received:** {date}
**Urgency indicators:** {list keywords that triggered high priority}
**Issue:** {brief description}

## Objective
Escalate urgent matter to human for immediate review

## Steps
- [ ] Copy WHATSAPP_*.md to /Pending_Approval/ for immediate human review
- [ ] Flag in Dashboard.md under "Urgent Items"
- [ ] Determine if immediate response is needed
- [ ] Draft response if applicable
- [ ] Await human decision on next action

## Completion Rule
Human will decide next steps. Do not auto-archive.
```

---

## Payment/Financial Escalation Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: high
status: pending
---

# Plan: PAYMENT — {payment_context}

## Context
**Received:** {date}
**Payment keywords detected:** {list keywords}
**Amount mentioned:** {amount if present}

## Objective
Escalate payment matter to human for review

## Steps
- [ ] Copy WHATSAPP_*.md to /Pending_Approval/ immediately
- [ ] Flag as financial matter requiring human oversight
- [ ] Do NOT draft any payment confirmation without explicit human approval
- [ ] Check if invoice needs to be generated
- [ ] Await human decision

## Completion Rule
Human must approve all payment-related communications. Do not proceed without approval.
```

---

## Pricing Query Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: medium
status: pending
---

# Plan: Pricing Query — {service_type}

## Context
**Received:** {date}
**Query about:** {service/product}

## Objective
Provide pricing information to potential client

## Steps
- [ ] Read /Vault/Accounting/Rates.md for current pricing
- [ ] Identify which service/product they're asking about
- [ ] Draft pricing response with relevant details
- [ ] Include any current promotions or packages
- [ ] Write /Pending_Approval/WHATSAPP_REPLY_{timestamp}.md
- [ ] Await human approval
- [ ] Log interaction to /Vault/Logs/YYYY-MM-DD.json

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when pricing info is sent.
```

---

## General Query Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: low
status: pending
---

# Plan: General Query — {topic}

## Context
**Received:** {date}
**Topic:** {brief summary}

## Objective
{one-line goal}

## Steps
- [ ] Summarize the message in 1-2 lines
- [ ] Determine if response is needed
- [ ] If yes: draft reply using Company_Handbook.md tone, write to /Pending_Approval/
- [ ] If no: update Dashboard.md and archive
- [ ] Log to /Vault/Logs/YYYY-MM-DD.json

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when handled.
```
