# Task Analysis Guide

Guide for analyzing tasks in /Needs_Action/ and determining the appropriate plan structure.

## Task Type Detection

### By Filename Pattern

| Filename Pattern | Task Type | Priority | Skills Needed |
|---|---|---|---|
| `EMAIL_*.md` | Email triage/reply | Based on content | gmail-triage, gmail-sender |
| `WHATSAPP_*.md` | WhatsApp triage/reply | Based on content | whatsapp-triage, whatsapp-sender |
| `PROMPT_post_*.md` | Social media post | Medium | linkedin-poster, twitter-poster, facebook-poster |
| `PROMPT_invoice_*.md` | Invoice generation | High | gmail-sender |
| `PROMPT_research_*.md` | Research task | Medium | browsing-with-playwright |
| `PROMPT_briefing.md` | CEO briefing | High | daily-briefing |
| `PROMPT_*.md` | General task | Medium | Varies |

### By Content Keywords

**High Priority Indicators:**
- "urgent", "asap", "critical", "emergency"
- "payment", "invoice", "financial"
- "deadline", "due by", "time-sensitive"
- "important", "priority"

**Medium Priority Indicators:**
- "please", "can you", "need"
- "help", "question", "inquiry"
- "update", "status", "report"

**Low Priority Indicators:**
- "when you have time", "no rush"
- "FYI", "for your information"
- "optional", "nice to have"

---

## Skill Selection Matrix

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

**LinkedIn Post:**
- Skill: linkedin-poster
- MCP: queue_linkedin, post_linkedin
- Char limit: 1,300

**Twitter Post:**
- Skill: twitter-poster
- MCP: queue_tweet, post_tweet
- Char limit: 250

**Facebook Post:**
- Skill: facebook-poster
- MCP: queue_facebook, post_facebook
- Optimal: 40-80 words

### Utility Tasks

**Web Research/Browsing:**
- Skill: browsing-with-playwright
- MCPs: browser_navigate, browser_snapshot, browser_click, browser_type

**Weekly Briefing:**
- Skill: daily-briefing
- Reads: Business_Goals.md, Done/, Logs/
- Writes: Briefings/{date}_Briefing.md

---

## Time Estimation Guidelines

### Simple Tasks (5-15 minutes)
- Single email reply
- Single social media post
- Archive/triage action
- Simple status update

### Medium Tasks (15-45 minutes)
- Multiple email replies
- Research with 2-3 sources
- Invoice generation
- Multi-platform social posts

### Complex Tasks (45-120 minutes)
- Comprehensive research
- Multi-step workflows
- Project planning
- Weekly briefing generation

### Large Projects (120+ minutes)
- Multi-phase projects
- System integrations
- Comprehensive audits
- Major feature development

**Estimation formula:**
```
Base time + (Number of steps × 5 minutes) + (Number of approvals × 10 minutes)
```

---

## Required Resources Detection

### Skills Detection

**Patterns to look for:**
- "post to LinkedIn" → linkedin-poster
- "send email" → gmail-sender
- "reply to WhatsApp" → whatsapp-sender
- "browse website" → browsing-with-playwright
- "generate briefing" → daily-briefing

### MCP Tools Detection

**Communication MCPs:**
- Email: send_email, draft_email
- WhatsApp: send_whatsapp, draft_whatsapp
- LinkedIn: queue_linkedin, post_linkedin
- Twitter: queue_tweet, post_tweet
- Facebook: queue_facebook, post_facebook

**Browser MCPs:**
- browser_navigate, browser_snapshot
- browser_click, browser_type
- browser_fill_form, browser_take_screenshot

### Vault Files Detection

**Common vault files:**
- Business_Goals.md → for context on goals/metrics
- Company_Handbook.md → for brand voice/tone
- Accounting/Rates.md → for pricing/invoices
- Done/ → for recent completions
- Logs/ → for metrics/stats

---

## Priority Assignment Rules

### High Priority (Immediate Action)
- Contains "urgent", "asap", "emergency"
- Financial/payment related
- Deadline within 24 hours
- Client-facing critical issue
- System outage or error

### Medium Priority (Normal Processing)
- Standard email replies
- Social media posts
- Research requests
- Status updates
- Non-urgent client requests

### Low Priority (When Available)
- FYI messages
- Optional tasks
- Nice-to-have features
- Internal documentation
- Archive/cleanup tasks

---

## Completion Criteria

### Clear Completion Signals

**Email tasks:**
- Reply sent and logged
- Original email moved to /Done/

**WhatsApp tasks:**
- Message sent and logged
- Original message moved to /Done/

**Social media tasks:**
- Post queued and logged
- Prompt moved to /Done/

**Research tasks:**
- Report written to /Done/
- Findings documented

**Project tasks:**
- All phases complete
- All deliverables in /Done/
- Dashboard.md updated

### Ambiguous Completion

If completion criteria unclear:
- Default: "Move to /Done/ when user confirms completion"
- Add note: "Requires human verification"
- Flag in Dashboard.md for review

---

## Special Cases

### Multi-Intent Tasks

If task has multiple intents:
1. Create separate plans for each intent
2. Link plans together in context
3. Prioritize by urgency
4. Execute in logical order

**Example:**
```
Task: "Send invoice to client and post about it on LinkedIn"
→ Plan 1: PLAN_INVOICE_client_20260305.md (high priority)
→ Plan 2: PLAN_LINKEDIN_invoice_announcement_20260305.md (medium priority)
```

### Dependent Tasks

If task depends on another:
1. Note dependency in plan
2. Add prerequisite step
3. Adjust estimated time
4. Update completion criteria

**Example:**
```
Task: "Post about new feature on all platforms"
→ Prerequisite: Feature must be shipped first
→ Check Done/ for feature completion
→ Then create social media plans
```

### Recurring Tasks

If task is recurring:
1. Note recurrence pattern in plan
2. Consider automation opportunity
3. Document in Dashboard.md
4. Create template for future use

**Example:**
```
Task: "Generate weekly briefing"
→ Recurrence: Every Monday 8 AM
→ Automation: Cron job triggers daily-briefing skill
→ Template: Use daily-briefing SKILL.md
```

---

## Error Handling

### Missing Information

If task lacks critical info:
1. Create plan with placeholder steps
2. Add step: "Request clarification from user"
3. Flag in Dashboard.md
4. Set status: pending_info

### Unclear Intent

If task intent is ambiguous:
1. Analyze context clues
2. Make best guess with note
3. Add verification step
4. Route to /Pending_Approval if uncertain

### Resource Unavailable

If required skill/MCP unavailable:
1. Note in plan
2. Suggest alternative approach
3. Flag for user attention
4. Update Dashboard.md

---

## Quality Checklist

Before finalizing plan, verify:
- ✅ Clear objective stated
- ✅ All steps are actionable
- ✅ Priority assigned correctly
- ✅ Time estimate reasonable
- ✅ Required resources identified
- ✅ Completion criteria clear
- ✅ Source file will be moved to /In_Progress/
- ✅ Dashboard.md will be updated
