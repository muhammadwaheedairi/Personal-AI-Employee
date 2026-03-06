---
name: gmail-triage
description: Process EMAIL_*.md files from the AI Employee vault. This skill should be used when EMAIL_*.md files appear in /Needs_Action folder, or when the user asks to check emails, triage Gmail, process inbox, or handle email actions. Detects intent, assigns priority, creates action plans in /Plans/, and routes sensitive emails (financial, urgent, payment-related) to /Pending_Approval/ for human review.
---

# Gmail Triage

Process `EMAIL_*.md` files from `/Needs_Action/`. Detect intent, assign priority, create action plans, and route sensitive emails for human approval.

## Workflow

1. **Read** the `EMAIL_*.md` file from `/Needs_Action/`
2. **Detect intent** — see `references/intents.md` for classification patterns
3. **Assign priority** based on keywords and sender context:
   - **high**: urgent, asap, critical, important, deadline, payment, invoice, financial
   - **medium**: action required, meeting requests, questions
   - **low**: FYI, newsletters, automated notifications
4. **Create action plan** in `/Plans/PLAN_EMAIL_{timestamp}_{subject}.md` using templates from `references/action-templates.md`
5. **Route sensitive emails** to `/Pending_Approval/` for human review:
   - Financial/payment emails (always)
   - Urgent/critical emails (always)
   - Emails requiring replies with commitments or decisions
6. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
7. **Move** source `EMAIL_*.md` to `/Done/` when plan is complete
8. Output `<promise>TASK_COMPLETE</promise>`

## Priority Detection

Priority is determined by analyzing both subject line and email snippet:

```python
priority_keywords = ['urgent', 'asap', 'important', 'deadline', 'critical',
                     'payment', 'invoice', 'billing', 'financial']

priority = 'high' if any(keyword in subject.lower() or keyword in snippet.lower()
                         for keyword in priority_keywords) else 'medium'
```

Additional priority factors:
- **Sender domain**: Client/executive domains → increase priority
- **Thread context**: Ongoing conversations → may increase priority
- **Time sensitivity**: Mentions of specific dates/deadlines → increase priority

## Action Decision Tree

```
Email arrives in /Needs_Action/
    │
    ├─ Contains financial keywords? → /Pending_Approval/ (high priority)
    ├─ Contains urgent keywords? → /Pending_Approval/ (high priority)
    ├─ Requires reply? → Create reply plan in /Plans/
    ├─ Requires forwarding? → Create forward plan in /Plans/
    ├─ Meeting invitation? → Create meeting response plan in /Plans/
    └─ Information only / Spam? → Archive to /Done/
```

## Plan.md Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: EMAIL_{timestamp}_{subject}.md
source_type: email
priority: {high|medium|low}
status: pending
---

# Plan: Email {Action} — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Intent:** {detected_intent}
**Priority:** {priority}

## Objective
{one-line goal — e.g., "Draft reply addressing client's questions about project timeline"}

## Steps
- [ ] {step 1}
- [ ] {step 2}
- [ ] {step 3}
...

## Completion Rule
Move this file and source EMAIL_*.md to /Done/ when {completion condition}.
```

## Security Rules

- **NEVER** send email directly — always write drafts to `/Pending_Approval/`
- **ALWAYS** route financial/payment emails to `/Pending_Approval/` for human review
- **ALWAYS** route urgent emails to `/Pending_Approval/` for immediate human attention
- **ALWAYS** log every action to `/Vault/Logs/YYYY-MM-DD.json`
- **NEVER** delete EMAIL_*.md files — move to `/Done/` instead

## Approval File Format

When routing to `/Pending_Approval/`, use this format:

```markdown
---
type: email_reply
source_file: EMAIL_{timestamp}_{subject}.md
priority: high
created: {iso_timestamp}
status: awaiting_approval
---

# Email Reply: {subject}

**To:** {recipient_email}
**Subject:** Re: {original_subject}
**Priority:** {high|medium|low}

## Draft Reply

{email body here}

---

## Original Email Context
**From:** {sender_email}
**Received:** {date}
**Content:** {snippet or full content}

---
*Awaiting human approval before sending*
```

## Intent Detection Guide

See `references/intents.md` for detailed intent classification patterns:
- Action Required
- Information Only
- Urgent/High Priority
- Delegation Required
- Payment/Financial
- Meeting/Calendar
- Spam/Low Priority

## Action Templates

See `references/action-templates.md` for complete plan templates:
- Reply Plan Template
- Forward Plan Template
- Archive Plan Template
- Urgent Escalation Template
- Meeting Response Template
- Financial/Payment Escalation Template

## Example Usage

**Scenario 1: Urgent client email**
```
Input: EMAIL_20260305_120000_Client_needs_urgent_response.md
Action: Detect "urgent" keyword → priority: high → copy to /Pending_Approval/
Output: PLAN_EMAIL_20260305_120000_urgent_client.md in /Plans/
```

**Scenario 2: Newsletter**
```
Input: EMAIL_20260305_080000_Weekly_newsletter.md
Action: Detect "newsletter" → intent: information_only → archive
Output: Move to /Done/, log action
```

**Scenario 3: Invoice request**
```
Input: EMAIL_20260305_140000_Invoice_for_services.md
Action: Detect "invoice" → priority: high → escalate to /Pending_Approval/
Output: PLAN_EMAIL_20260305_140000_invoice.md with financial flag
```

## Logging Format

Every email action must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "email_triage",
  "source_file": "EMAIL_20260305_143000_subject.md",
  "intent": "action_required",
  "priority": "high",
  "action_taken": "created_reply_plan",
  "plan_file": "PLAN_EMAIL_20260305_143000_subject.md",
  "routed_to_approval": true
}
```

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
