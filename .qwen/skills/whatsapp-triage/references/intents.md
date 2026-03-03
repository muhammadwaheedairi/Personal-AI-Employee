# WhatsApp Intent Detection

## Intent Patterns & Step Templates

### `invoice_request` — message contains: invoice, bill, payment, send me, receipt, charges

```markdown
## Steps
- [ ] Identify client from message context
- [ ] Read /Accounting/Rates.md for current rates
- [ ] Calculate amount for the period mentioned
- [ ] Create invoice content (client name, amount, bank details, due date)
- [ ] Write /Pending_Approval/INVOICE_{client}_{timestamp}.md
- [ ] After approval: send invoice via email MCP to client email on file
- [ ] Log to /Vault/Logs/{date}.json with action_type=invoice_generated
```

### `urgent_query` — message contains: urgent, asap, help, emergency, problem, issue

```markdown
## Steps
- [ ] Identify the specific problem or request
- [ ] Draft response addressing the concern using Company_Handbook.md tone rules
- [ ] Write /Pending_Approval/WHATSAPP_reply_{timestamp}.md
- [ ] Await human approval before any send action
- [ ] Log to /Vault/Logs/{date}.json with action_type=whatsapp_draft
```

### `pricing_query` — message contains: price, cost, rate, quote, how much, fee

```markdown
## Steps
- [ ] Read /Accounting/Rates.md for current pricing
- [ ] Draft pricing response with relevant details
- [ ] Write /Pending_Approval/WHATSAPP_reply_{timestamp}.md
- [ ] Await human approval
- [ ] Log interaction
```

### `general` — all other messages

```markdown
## Steps
- [ ] Summarize the message in 1-2 lines
- [ ] Determine if response is needed
- [ ] If yes: draft reply, write to /Pending_Approval/WHATSAPP_reply_{timestamp}.md
- [ ] If no: update Dashboard.md and archive
- [ ] Log to /Vault/Logs/{date}.json
```

## Priority Rules

| Keyword in message | Priority in Plan |
|---|---|
| payment, invoice, money | high |
| urgent, asap, emergency | high |
| help, problem, issue | medium |
| price, quote, rate | medium |
| everything else | low |

## Approval File Format

```markdown
---
action: send_whatsapp
to: {contact_name}
body: {reply_text}
created: {iso_timestamp}
expires: {iso_timestamp_plus_24h}
status: pending
---

## Message to Send
{reply_text}

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```