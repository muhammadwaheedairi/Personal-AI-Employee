# Email Action Templates

Templates for creating action plans based on email intent.

## Reply Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: {high|medium|low}
status: pending
---

# Plan: Email Reply — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Intent:** {detected_intent}

## Objective
Draft reply to address: {one-line summary of what needs to be addressed}

## Steps
- [ ] Review full email content
- [ ] Draft reply addressing: {specific points}
- [ ] Review tone and clarity
- [ ] Write draft to /Pending_Approval/REPLY_{timestamp}_{subject}.md
- [ ] Await human approval before sending

## Completion Rule
Move this file and source EMAIL_*.md to /Done/ when reply is sent or archived.
```

---

## Forward Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: {high|medium|low}
status: pending
---

# Plan: Forward Email — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Reason for forwarding:** {why this needs delegation}

## Objective
Forward to {suggested_recipient} for handling

## Steps
- [ ] Confirm {suggested_recipient} is the right person
- [ ] Draft forwarding message with context
- [ ] Write forward request to /Pending_Approval/FORWARD_{timestamp}_{subject}.md
- [ ] Await human approval before forwarding

## Completion Rule
Move this file and source EMAIL_*.md to /Done/ when forwarded.
```

---

## Archive Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: low
status: pending
---

# Plan: Archive Email — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Intent:** {Information only / Spam / Low priority}

## Objective
Archive email — no action required

## Steps
- [ ] Confirm no action needed
- [ ] Log to /Vault/Logs/YYYY-MM-DD.json
- [ ] Move EMAIL_*.md to /Done/

## Completion Rule
Move this file and source EMAIL_*.md to /Done/ immediately.
```

---

## Urgent Escalation Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: high
status: pending
---

# Plan: URGENT — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Urgency indicators:** {list keywords/context that triggered high priority}

## Objective
Escalate to human for immediate review

## Steps
- [ ] Copy EMAIL_*.md to /Pending_Approval/ for immediate human review
- [ ] Flag in Dashboard.md under "Urgent Items"
- [ ] Await human decision on next action

## Completion Rule
Human will decide next steps. Do not auto-archive.
```

---

## Meeting Response Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: medium
status: pending
---

# Plan: Meeting Response — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Meeting details:** {date/time if mentioned}

## Objective
Respond to meeting invitation

## Steps
- [ ] Check calendar availability (if integrated)
- [ ] Draft response with availability or acceptance
- [ ] Write draft to /Pending_Approval/REPLY_{timestamp}_{subject}.md
- [ ] Await human approval before sending

## Completion Rule
Move this file and source EMAIL_*.md to /Done/ when meeting response is sent.
```

---

## Financial/Payment Escalation Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {EMAIL_filename}
source_type: email
priority: high
status: pending
---

# Plan: FINANCIAL — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Financial keywords detected:** {list keywords}

## Objective
Escalate financial matter to human for review

## Steps
- [ ] Copy EMAIL_*.md to /Pending_Approval/ immediately
- [ ] Flag as financial matter requiring human oversight
- [ ] Do NOT draft any reply without explicit human approval
- [ ] Await human decision

## Completion Rule
Human must approve all financial communications. Do not proceed without approval.
```
