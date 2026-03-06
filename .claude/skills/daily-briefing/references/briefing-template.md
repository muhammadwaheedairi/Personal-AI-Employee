# Briefing Template

Standard format for Monday Morning CEO Briefing output.

## File Format

**Filename:** `YYYY-MM-DD_Briefing.md`  
**Location:** `/Vault/Briefings/`

## Template Structure

```markdown
---
type: briefing
date: {YYYY-MM-DD}
week: {week_number}
generated: {iso_timestamp}
---

# CEO Briefing — {Day}, {Month} {Date}, {Year}

## Executive Summary

{2-3 sentence overview of the week — key wins, major concerns, overall trajectory}

---

## Revenue & Financial Health

### This Month (MTD)
- **Revenue:** ${amount} / ${monthly_target} ({percentage}%)
- **Expenses:** ${amount}
- **Net Position:** ${amount} ({Profitable|Break-even|Loss})

### Key Financial Metrics
- Invoices sent this week: {count}
- Payments received: {count}
- Outstanding invoices: {count} (${total_amount})
- Overdue invoices (>7 days): {count} (${total_amount})

**Status:** {Green|Yellow|Red}  
**Notes:** {Any financial concerns or wins}

---

## This Week's Activity

### Completed Tasks ({count})
- {task_1} — {date}
- {task_2} — {date}
- {task_3} — {date}
...

### Communication Stats
- **Emails processed:** {count}
- **WhatsApp messages handled:** {count}
- **Social media posts:** {count} (LinkedIn: {x}, Twitter: {y}, Facebook: {z})

### Automation Metrics
- **Total actions automated:** {count}
- **Time saved (estimated):** {hours} hours
- **Human approvals required:** {count}

---

## Current Status

### Pending Actions ({count})
- {action_1} — {priority}
- {action_2} — {priority}
- {action_3} — {priority}

### Awaiting Approval ({count})
- {approval_1} — {type} — {age}
- {approval_2} — {type} — {age}

### Active Plans ({count})
- {plan_1} — {status} — {age}
- {plan_2} — {status} — {age}

---

## Bottlenecks & Concerns

### Overdue Plans (>48h)
- {plan_1} — {age} — {reason_if_known}
- {plan_2} — {age} — {reason_if_known}

### Blocked Tasks
- {task_1} — {blocking_reason}
- {task_2} — {blocking_reason}

### System Issues
- {issue_1} — {severity}
- {issue_2} — {severity}

**Overall Health:** {Green|Yellow|Red}

---

## Proactive Recommendations

### Financial Opportunities
- {recommendation_1}
- {recommendation_2}

### Process Improvements
- {recommendation_1}
- {recommendation_2}

### Upcoming Deadlines (Next 7 Days)
- {deadline_1} — {date}
- {deadline_2} — {date}

### Suggested Actions
- [ ] {action_1}
- [ ] {action_2}
- [ ] {action_3}

---

## Business Goals Progress

{For each goal in Business_Goals.md, show progress}

### Goal: {goal_name}
- **Target:** {target_metric}
- **Current:** {current_metric}
- **Progress:** {percentage}%
- **Status:** {On Track|At Risk|Behind}
- **Notes:** {context}

---

## Next Week Focus

1. {priority_1}
2. {priority_2}
3. {priority_3}

---

*Generated automatically by AI Employee on {date} at {time}*
```

## Section Guidelines

### Executive Summary
- 2-3 sentences maximum
- Lead with the most important insight
- Mention key wins or major concerns
- Set the tone for the rest of the briefing

**Example:**
```
Strong week with 23 tasks completed and $12,000 in new revenue. Two overdue plans need attention (invoice follow-up and client onboarding). Overall trajectory is positive with Q1 revenue at 78% of target.
```

### Revenue & Financial Health
- Always include MTD revenue vs target
- Calculate percentage progress toward monthly goal
- Flag overdue invoices (>7 days old)
- Use status indicators: Green (on track), Yellow (needs attention), Red (critical)

### This Week's Activity
- List completed tasks from /Done/ folder (last 7 days)
- Include communication stats from logs
- Show automation metrics to demonstrate AI Employee value

### Current Status
- List pending actions from /Needs_Action/
- List items awaiting approval from /Pending_Approval/
- Show active plans from /Plans/ with status

### Bottlenecks & Concerns
- Flag any Plan.md files older than 48h still pending
- Identify blocked tasks and why they're blocked
- Note any system issues or errors from logs
- Use overall health indicator: Green/Yellow/Red

### Proactive Recommendations
- Suggest financial opportunities (e.g., "Invoice Client X for completed project")
- Recommend process improvements based on patterns
- List upcoming deadlines from Business_Goals.md
- Provide actionable next steps

### Business Goals Progress
- For each goal in Business_Goals.md, calculate progress
- Show current vs target metrics
- Assign status: On Track / At Risk / Behind
- Add context notes if status is not "On Track"

### Next Week Focus
- 3-5 priority items for the coming week
- Based on bottlenecks, goals, and upcoming deadlines
- Actionable and specific

## Tone Guidelines

- **Professional but conversational** — write for a CEO who wants facts, not fluff
- **Data-driven** — use specific numbers, not vague statements
- **Action-oriented** — focus on what needs to happen next
- **Honest** — don't sugarcoat problems, but frame them constructively
- **Concise** — respect the reader's time, get to the point

## What to Include

✅ Specific metrics and numbers  
✅ Completed tasks with dates  
✅ Financial status and trends  
✅ Bottlenecks and blockers  
✅ Proactive recommendations  
✅ Progress toward stated goals  

## What to Exclude

❌ Vague statements ("things are going well")  
❌ Excessive detail on routine tasks  
❌ Technical jargon without context  
❌ Complaints without solutions  
❌ Information already obvious from Dashboard.md  

## Example Briefing Excerpt

```markdown
# CEO Briefing — Monday, March 6, 2026

## Executive Summary

Strong week with 23 tasks completed and $12,000 in new revenue. Two overdue plans need attention (invoice follow-up and client onboarding). Overall trajectory is positive with Q1 revenue at 78% of target.

---

## Revenue & Financial Health

### This Month (MTD)
- **Revenue:** $47,000 / $60,000 (78%)
- **Expenses:** $15,000
- **Net Position:** $32,000 (Profitable)

### Key Financial Metrics
- Invoices sent this week: 3
- Payments received: 2 ($12,000)
- Outstanding invoices: 5 ($23,000)
- Overdue invoices (>7 days): 1 ($5,000 — Client ABC)

**Status:** Green  
**Notes:** On track to hit monthly target. One overdue invoice needs follow-up.

---

## This Week's Activity

### Completed Tasks (23)
- Email reply to Client X about project timeline — Mar 5
- LinkedIn post about Q1 milestone — Mar 4
- Invoice sent to Client Y for February services — Mar 3
- WhatsApp reply to Client Z inquiry — Mar 2
...

### Communication Stats
- **Emails processed:** 47
- **WhatsApp messages handled:** 12
- **Social media posts:** 5 (LinkedIn: 3, Twitter: 2, Facebook: 0)

### Automation Metrics
- **Total actions automated:** 64
- **Time saved (estimated):** 8 hours
- **Human approvals required:** 3

---

## Bottlenecks & Concerns

### Overdue Plans (>48h)
- PLAN_invoice_followup_20260303.md — 72h old — Awaiting client response
- PLAN_client_onboarding_20260302.md — 96h old — Missing onboarding docs

### Blocked Tasks
- None

### System Issues
- None

**Overall Health:** Yellow (2 overdue plans need attention)

---

## Proactive Recommendations

### Financial Opportunities
- Follow up on overdue invoice from Client ABC ($5,000)
- Send invoice to Client D for completed project ($8,000)

### Process Improvements
- Consider automating invoice follow-ups after 7 days
- Create onboarding checklist template to prevent delays

### Upcoming Deadlines (Next 7 Days)
- Q1 revenue report due — Mar 10
- Client E project delivery — Mar 12

### Suggested Actions
- [ ] Send payment reminder to Client ABC
- [ ] Request onboarding docs from Client F
- [ ] Prepare Q1 revenue report

---

## Business Goals Progress

### Goal: Reach $60,000 monthly revenue
- **Target:** $60,000/month
- **Current:** $47,000 MTD
- **Progress:** 78%
- **Status:** On Track
- **Notes:** Need $13,000 more this month. Two pending invoices total $13,000.

### Goal: Automate 80% of email responses
- **Target:** 80%
- **Current:** 73%
- **Progress:** 91%
- **Status:** On Track
- **Notes:** Up from 68% last week. Trending in right direction.

---

## Next Week Focus

1. Follow up on overdue invoice and pending payments
2. Complete client onboarding for Client F
3. Prepare and submit Q1 revenue report

---

*Generated automatically by AI Employee on 2026-03-06 at 08:00*
```
