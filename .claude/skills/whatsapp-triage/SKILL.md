---
name: whatsapp-triage
description: Triage and process WhatsApp action files from the AI Employee vault. Use when WHATSAPP_*.md files appear in /Needs_Action folder, or when user asks to handle WhatsApp messages, draft replies, or generate invoices from chat requests. Reads message content, detects intent, creates Plan.md with steps, and always routes replies to /Pending_Approval — never sends directly to WhatsApp without human approval.
---

# WhatsApp Triage

Process `WHATSAPP_*.md` files from `/Needs_Action`. **All outgoing actions require HITL approval** — never act directly on WhatsApp.

## Workflow

1. **Read** the `WHATSAPP_*.md` file
2. **Detect** intent — see `references/intents.md`
3. **Create** `Plans/PLAN_{source}_{timestamp}.md` with checkbox steps
4. **Write** approval file to `/Pending_Approval/` for any outgoing action
5. **Never** send or interact with WhatsApp directly
6. **Log** every action to `/Vault/Logs/YYYY-MM-DD.json`
7. **Move** source file to `/Done/` when complete
8. Output `<promise>TASK_COMPLETE</promise>`

## Plan.md Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {filename}
source_type: whatsapp
priority: high
status: pending
---

# Plan: WhatsApp — {detected_intent}

## Objective
{one line goal}

## Steps
- [ ] {step 1}
- [ ] {step 2}
...

## Completion Rule
Move this file and source file to /Done when all steps checked.
```

## Security Rules

- **NEVER** write to WhatsApp directly — always via `/Approved` → MCP
- Any message containing "payment" → set priority: high in plan
- **Always log** every action to `/Vault/Logs/YYYY-MM-DD.json`

## Intent Guide

See `references/intents.md` for intent detection patterns and step templates.