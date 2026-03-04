---
name: gmail-triage
description: Triage and process Gmail action files from the AI Employee vault. Use when EMAIL_*.md files appear in /Needs_Action folder, or when user asks to process emails, draft replies, or handle email-based tasks. Reads email metadata, classifies intent, creates Plan.md with checkboxes, and routes sensitive actions to /Pending_Approval for human approval before sending.
---

# Gmail Triage

Process `EMAIL_*.md` files from `/Needs_Action` using the Read → Plan → Approve → Act workflow.

## Workflow

1. **Read** the `EMAIL_*.md` file (frontmatter + snippet)
2. **Classify** intent — see references/classification.md
3. **Create** `Plans/PLAN_{source}_{timestamp}.md` with checkbox steps
4. **Route** sensitive actions to `/Pending_Approval/` — never send directly
5. **Update** `Dashboard.md` under `## Recent Activity`
6. **Move** source file to `/Done/` when all steps complete
7. Output `<promise>TASK_COMPLETE</promise>`

## Plan.md Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {filename}
source_type: email
priority: {priority}
status: pending
---

# Plan: {subject}

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

- **Never send** to new/unknown contacts without `/Approved` file present
- **Always log** every action to `/Vault/Logs/YYYY-MM-DD.json`
- Max **10 email actions per hour** (rate limit)
- Add signature: `Sent with AI assistance` to all outgoing emails

## Classification Guide

See `references/classification.md` for intent types and step templates.