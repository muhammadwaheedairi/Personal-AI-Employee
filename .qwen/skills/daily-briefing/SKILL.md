---
name: daily-briefing
description: Generate the Monday Morning CEO Briefing for the AI Employee vault. Use when PROMPT_daily_briefing.md appears in /Plans, when cron triggers at 8 AM, or when user asks to generate a briefing, weekly summary, or business audit. Reads Business_Goals.md, Done folder, and action logs to write a structured briefing to /Vault/Briefings/ and updates Dashboard.md.
---

# Daily Briefing

Generate a structured CEO briefing by auditing the vault. Triggered by cron at 8:00 AM or by `PROMPT_daily_briefing.md` appearing in `/Plans`.

## Workflow

1. **Read** these files:
   - `/Vault/Business_Goals.md` — revenue targets, KPIs, active projects
   - `/Vault/Done/` — list all files modified in the last 7 days
   - `/Vault/Logs/*.json` — count actions taken this week
   - `/Vault/Needs_Action/` — count pending files
2. **Detect** any bottlenecks — Plan.md files older than 48h still `status: pending`
3. **Run Weekly Accounting Audit** — see section below
4. **Write** briefing to `/Vault/Briefings/{YYYY-MM-DD}_Briefing.md` using template in `references/briefing-template.md`
5. **Update** `Dashboard.md` — set `Last Briefing: {date}` under the status section
6. **Move** `PROMPT_daily_briefing.md` to `/Done/`
7. Output `<promise>TASK_COMPLETE</promise>`

## Key Calculations

| Metric | How to Calculate |
|---|---|
| Tasks completed | Count files in `/Done/` with today's or this week's date in filename |
| Pending actions | Count `.md` files in `/Needs_Action/` |
| Emails processed | Count `action_type: email_*` entries in this week's log files |
| WhatsApp handled | Count `action_type: whatsapp_*` entries in this week's log files |
| Social posts | Count `action_type: linkedin_post/twitter_post/facebook_post` in logs |
| Overdue plans | Plan.md files with `created:` older than 48h and `status: pending` |

## Weekly Accounting Audit

Every Monday, perform a full business accounting audit:

1. Read `Business_Goals.md` for monthly targets, project values, and expenses
2. Calculate MTD revenue from completed projects in `/Done/`
3. Check overdue invoices — any files mentioning "invoice" or "payment" older than 7 days
4. Calculate net position = MTD Revenue - Monthly Expenses
5. Add audit summary to briefing under `## Accounting Audit` section

### Accounting Audit Template
```
## Accounting Audit

| Item | Amount |
|---|---|
| MTD Revenue | $X |
| Monthly Expenses | $X |
| Net Position | $X |
| Overdue Invoices | X pending |

**Status:** Profitable / Break-even / Loss
```

## Briefing Template

See `references/briefing-template.md` for the exact output format with all required sections.