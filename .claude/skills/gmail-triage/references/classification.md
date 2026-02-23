# Email Classification Guide

## Intent Types & Step Templates

### `urgent` — subject/snippet contains: urgent, asap, deadline, critical, immediately

```markdown
## Steps
- [ ] Read full email from {sender}
- [ ] Identify the specific urgency or request
- [ ] Draft reply addressing the concern
- [ ] Write /Pending_Approval/EMAIL_reply_{timestamp}.md with: action=send_email, to=, subject=, body=
- [ ] Await human approval before sending
- [ ] Log to /Vault/Logs/{date}.json with action_type=email_draft
```

### `invoice_request` — snippet contains: invoice, bill, payment, send me, receipt

```markdown
## Steps
- [ ] Identify client name from sender email
- [ ] Read /Accounting/Rates.md for current billing rate
- [ ] Calculate invoice amount for period requested
- [ ] Generate invoice content (date, line items, total, bank details)
- [ ] Write /Pending_Approval/INVOICE_{client}_{timestamp}.md for approval
- [ ] After approval: send via email MCP with invoice attached
- [ ] Log transaction to /Vault/Logs/{date}.json
```

### `general` — all other emails

```markdown
## Steps
- [ ] Read and summarize email in 2-3 lines
- [ ] Determine if reply is needed (yes/no)
- [ ] If reply needed: draft reply, write to /Pending_Approval/EMAIL_reply_{timestamp}.md
- [ ] If no reply: update Dashboard.md and archive to /Done
- [ ] Log to /Vault/Logs/{date}.json
```

## Priority Mapping

| Keywords in subject/snippet | Priority |
|---|---|
| urgent, asap, critical, emergency | high |
| invoice, payment, deadline | high |
| meeting, reminder, follow up | medium |
| newsletter, update, FYI | low |

## Log Entry Format

```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_draft",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Re: Invoice #123"},
  "approval_status": "pending",
  "result": "draft_created"
}
```