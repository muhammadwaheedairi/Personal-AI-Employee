---
name: plan-creator
description: Create structured execution plans for tasks in the AI Employee vault. This skill should be used when any new file appears in /Needs_Action folder, or when the user asks to create a plan, analyze a task, or organize work. Reads task files, analyzes requirements, creates detailed Plan.md with steps/resources/timeline, moves source to /In_Progress/, and updates Dashboard.md. This is a meta-skill that orchestrates the workflow for all incoming tasks.
---

# Plan Creator

Create structured execution plans for any task that lands in `/Needs_Action/`. This meta-skill orchestrates the AI Employee workflow by analyzing tasks and generating actionable plans.

## Workflow

1. **Detect** new file in `/Needs_Action/`
2. **Read** the file and understand the task
3. **Analyze** task type, priority, and requirements (see `references/task-analysis.md`)
4. **Select** appropriate plan template (see `references/plan-templates.md`)
5. **Create** structured Plan.md in `/Plans/` with:
   - Clear objective
   - Step-by-step checklist
   - Priority level (high/medium/low)
   - Estimated completion time
   - Required skills and MCPs
   - Completion criteria
6. **Move** original file from `/Needs_Action/` to `/In_Progress/`
7. **Update** Dashboard.md with new plan entry
8. **Log** action to `/Vault/Logs/YYYY-MM-DD.json`
9. Output `<promise>TASK_COMPLETE</promise>`

## Task Type Detection

### By Filename Pattern

| Filename | Task Type | Template | Priority |
|---|---|---|---|
| `EMAIL_*.md` | Email triage/reply | Email Reply Plan | Based on content |
| `WHATSAPP_*.md` | WhatsApp triage/reply | WhatsApp Reply Plan | Based on content |
| `PROMPT_post_*.md` | Social media post | Social Media Post Plan | Medium |
| `PROMPT_invoice_*.md` | Invoice generation | Invoice Generation Plan | High |
| `PROMPT_research_*.md` | Research task | Research/Investigation Plan | Medium |
| `PROMPT_briefing.md` | CEO briefing | Use daily-briefing skill | High |
| `PROMPT_*.md` | General task | Base Plan Template | Medium |

### By Content Keywords

**High Priority Indicators:**
- "urgent", "asap", "critical", "emergency"
- "payment", "invoice", "financial"
- "deadline", "due by", "time-sensitive"

**Medium Priority Indicators:**
- "please", "can you", "need"
- "help", "question", "inquiry"

**Low Priority Indicators:**
- "when you have time", "no rush"
- "FYI", "optional"

## Plan File Format

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {original_filename}
source_type: {email|whatsapp|prompt|manual}
priority: {high|medium|low}
status: pending
estimated_time: {minutes}
---

# Plan: {Task Title}

## Context
{Brief description of what triggered this plan}

## Objective
{One-line clear goal statement}

## Steps
- [ ] {Step 1}
- [ ] {Step 2}
- [ ] {Step 3}
...

## Required Resources
- Skills: {list of skills needed}
- MCPs: {list of MCP tools needed}
- Vault files: {list of files to read}

## Completion Rule
Move this file and source file to /Done/ when {completion condition}.
```

## File Naming Convention

**Format:** `PLAN_{source}_{timestamp}.md`

**Examples:**
- `PLAN_EMAIL_20260306_143000.md`
- `PLAN_WHATSAPP_20260306_143000.md`
- `PLAN_post_linkedin_20260306_143000.md`
- `PLAN_invoice_client_20260306_143000.md`

## Skill Selection Guide

### Communication Tasks

**Email:**
- Triage: gmail-triage
- Send: gmail-sender
- MCPs: send_email, draft_email

**WhatsApp:**
- Triage: whatsapp-triage
- Send: whatsapp-sender
- MCPs: send_whatsapp, draft_whatsapp

### Content Creation Tasks

**LinkedIn:** linkedin-poster, queue_linkedin (1,300 char limit)
**Twitter:** twitter-poster, queue_tweet (250 char limit)
**Facebook:** facebook-poster, queue_facebook (40-80 words optimal)

### Utility Tasks

**Web Research:** browsing-with-playwright
**Weekly Briefing:** daily-briefing

## Time Estimation Guidelines

| Task Complexity | Time Range | Examples |
|---|---|---|
| Simple | 5-15 min | Single email reply, single social post |
| Medium | 15-45 min | Multiple replies, research, invoice generation |
| Complex | 45-120 min | Comprehensive research, multi-step workflows |
| Large Project | 120+ min | Multi-phase projects, system integrations |

**Estimation formula:**
```
Base time + (Number of steps × 5 min) + (Number of approvals × 10 min)
```

## Priority Assignment Rules

### High Priority (Immediate Action)
- Contains "urgent", "asap", "emergency"
- Financial/payment related
- Deadline within 24 hours
- Client-facing critical issue

### Medium Priority (Normal Processing)
- Standard email replies
- Social media posts
- Research requests
- Non-urgent client requests

### Low Priority (When Available)
- FYI messages
- Optional tasks
- Internal documentation

## Example Scenarios

**Scenario 1: Email arrives**
```
Input: EMAIL_20260306_120000_Client_inquiry.md in /Needs_Action/
Action:
1. Read email content
2. Detect intent: action_required
3. Priority: medium (no urgent keywords)
4. Select template: Email Reply Plan
5. Create: PLAN_EMAIL_20260306_120000.md in /Plans/
6. Move: EMAIL_*.md to /In_Progress/
7. Update: Dashboard.md
Output: Plan created with 5 steps, estimated 15 minutes
```

**Scenario 2: WhatsApp urgent message**
```
Input: WHATSAPP_20260306_140000.md in /Needs_Action/
Content: "Urgent! Need invoice for this month"
Action:
1. Read message
2. Detect keywords: "urgent", "invoice"
3. Priority: high
4. Select template: Invoice Generation Plan
5. Create: PLAN_WHATSAPP_20260306_140000_invoice.md in /Plans/
6. Move: WHATSAPP_*.md to /In_Progress/
7. Update: Dashboard.md
Output: Plan created with 8 steps, estimated 30 minutes
```

**Scenario 3: Social media request**
```
Input: PROMPT_post_linkedin_milestone.md in /Needs_Action/
Content: "Post about hitting Q1 revenue goal on LinkedIn"
Action:
1. Read prompt
2. Detect task: LinkedIn post
3. Priority: medium
4. Select template: Social Media Post Plan
5. Create: PLAN_post_linkedin_20260306_160000.md in /Plans/
6. Move: PROMPT_*.md to /In_Progress/
7. Update: Dashboard.md
Output: Plan created with 6 steps, estimated 10 minutes
```

## Dashboard.md Update Format

After creating plan, add entry to Dashboard.md:

```markdown
## Active Plans

| Plan | Priority | Created | Est. Time | Status |
|---|---|---|---|---|
| PLAN_EMAIL_20260306_120000.md | Medium | 2026-03-06 12:00 | 15 min | Pending |
| PLAN_WHATSAPP_20260306_140000_invoice.md | High | 2026-03-06 14:00 | 30 min | Pending |
```

## Logging Format

Every plan creation must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-06T14:30:00Z",
  "action_type": "plan_created",
  "source_file": "EMAIL_20260306_120000_Client_inquiry.md",
  "plan_file": "PLAN_EMAIL_20260306_120000.md",
  "priority": "medium",
  "estimated_time": 15,
  "required_skills": ["gmail-triage", "gmail-sender"],
  "status": "pending"
}
```

## Special Cases

### Multi-Intent Tasks

If task has multiple intents, create separate plans:

```
Task: "Send invoice to client and post about it on LinkedIn"
→ PLAN_INVOICE_client_20260306.md (high priority, execute first)
→ PLAN_LINKEDIN_invoice_announcement_20260306.md (medium priority, execute after)
```

### Dependent Tasks

If task depends on another, note in plan:

```markdown
## Steps
- [ ] **Prerequisite:** Check Done/ for feature completion
- [ ] Generate social media content
- [ ] Queue posts to all platforms
```

### Missing Information

If task lacks critical info:

```markdown
## Steps
- [ ] **Action Required:** Request clarification from user on {missing_info}
- [ ] Wait for user response
- [ ] Continue with remaining steps
```

## Quality Checklist

Before finalizing plan, verify:
- ✅ Clear objective stated
- ✅ All steps are actionable
- ✅ Priority assigned correctly
- ✅ Time estimate reasonable
- ✅ Required resources identified
- ✅ Completion criteria clear
- ✅ Source file moved to /In_Progress/
- ✅ Dashboard.md updated

## References

- `references/plan-templates.md` — Complete plan templates for all task types
- `references/task-analysis.md` — Task analysis guide, skill selection matrix, time estimation

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
