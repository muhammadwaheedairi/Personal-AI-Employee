# Plan Templates

Standard templates for creating structured plans based on task type.

## Base Plan Template

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

---

## Email Reply Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: EMAIL_{timestamp}_{subject}.md
source_type: email
priority: {high|medium|low}
status: pending
estimated_time: 15
---

# Plan: Email Reply — {subject}

## Context
**From:** {sender_email}
**Subject:** {subject}
**Received:** {date}
**Intent:** {detected_intent}

## Objective
Draft reply addressing: {specific points to address}

## Steps
- [ ] Load gmail-triage skill to analyze intent
- [ ] Draft appropriate response using Company_Handbook.md tone
- [ ] Write draft to /Pending_Approval/REPLY_{timestamp}.md
- [ ] Await human approval
- [ ] Log action to /Vault/Logs/YYYY-MM-DD.json

## Required Resources
- Skills: gmail-triage, gmail-sender
- MCPs: send_email, draft_email
- Vault files: Company_Handbook.md

## Completion Rule
Move this file and EMAIL_*.md to /Done/ when reply is sent or archived.
```

---

## WhatsApp Reply Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: WHATSAPP_{timestamp}.md
source_type: whatsapp
priority: {high|medium|low}
status: pending
estimated_time: 20
---

# Plan: WhatsApp — {intent}

## Context
**Received:** {date}
**Priority:** {priority}
**Matched Keywords:** {keywords}

## Objective
{one-line goal}

## Steps
- [ ] Load whatsapp-triage skill to analyze intent
- [ ] Determine action: reply, invoice, or escalate
- [ ] Draft response or create invoice plan
- [ ] Write to /Pending_Approval/ for human review
- [ ] Log action to /Vault/Logs/YYYY-MM-DD.json

## Required Resources
- Skills: whatsapp-triage, whatsapp-sender
- MCPs: send_whatsapp, draft_whatsapp
- Vault files: Company_Handbook.md, Accounting/Rates.md

## Completion Rule
Move this file and WHATSAPP_*.md to /Done/ when action is complete.
```

---

## Social Media Post Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: PROMPT_{topic}.md
source_type: prompt
priority: medium
status: pending
estimated_time: 10
---

# Plan: Social Media Post — {topic}

## Context
User requested: {request summary}

## Objective
Generate and queue {platform} post about {topic}

## Steps
- [ ] Load {platform}-poster skill
- [ ] Read Business_Goals.md for context
- [ ] Read Done/ folder for recent completions
- [ ] Generate post content (under {char_limit} chars)
- [ ] Queue post using queue_{platform} MCP tool
- [ ] Log action to /Vault/Logs/YYYY-MM-DD.json

## Required Resources
- Skills: {platform}-poster
- MCPs: queue_{platform}
- Vault files: Business_Goals.md, Done/, Logs/

## Completion Rule
Move this file and PROMPT_*.md to /Done/ when post is queued.
```

---

## Invoice Generation Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: {source_filename}
source_type: {email|whatsapp}
priority: high
status: pending
estimated_time: 30
---

# Plan: Generate Invoice — {client_name}

## Context
**Client:** {client_name}
**Request:** Invoice for {service/period}
**Source:** {email|whatsapp}

## Objective
Generate and send invoice to {client_name}

## Steps
- [ ] Read Accounting/Rates.md for current pricing
- [ ] Calculate amount for {service/period}
- [ ] Create invoice content (client, amount, bank details, due date)
- [ ] Write to /Pending_Approval/INVOICE_{client}_{timestamp}.md
- [ ] Await human approval
- [ ] Send invoice via email MCP to client email on file
- [ ] Log to /Vault/Logs/YYYY-MM-DD.json

## Required Resources
- Skills: gmail-sender (for sending invoice)
- MCPs: send_email
- Vault files: Accounting/Rates.md, Company_Handbook.md

## Completion Rule
Move this file and source file to /Done/ when invoice is sent and confirmed.
```

---

## Research/Investigation Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: PROMPT_{topic}.md
source_type: prompt
priority: medium
status: pending
estimated_time: 45
---

# Plan: Research — {topic}

## Context
User requested: {research request}

## Objective
Research {topic} and provide comprehensive findings

## Steps
- [ ] Define research scope and key questions
- [ ] Identify information sources (vault files, web, docs)
- [ ] Load browsing-with-playwright skill if web research needed
- [ ] Gather and analyze information
- [ ] Synthesize findings into structured report
- [ ] Write report to /Done/RESEARCH_{topic}_{timestamp}.md
- [ ] Update Dashboard.md with findings summary

## Required Resources
- Skills: browsing-with-playwright (if web research needed)
- MCPs: browser_navigate, browser_snapshot (if needed)
- Vault files: {relevant vault files}

## Completion Rule
Move this file and PROMPT_*.md to /Done/ when research report is complete.
```

---

## Multi-Step Project Plan Template

```markdown
---
type: plan
created: {iso_timestamp}
source_file: PROMPT_{project}.md
source_type: prompt
priority: high
status: pending
estimated_time: 120+
---

# Plan: Project — {project_name}

## Context
User requested: {project description}

## Objective
{high-level project goal}

## Phases

### Phase 1: Planning
- [ ] Define project scope and requirements
- [ ] Identify all required skills and MCPs
- [ ] Create sub-plans for each major component
- [ ] Estimate timeline and resources

### Phase 2: Execution
- [ ] {Major task 1}
- [ ] {Major task 2}
- [ ] {Major task 3}

### Phase 3: Review & Completion
- [ ] Test/validate all components
- [ ] Document results
- [ ] Update Dashboard.md
- [ ] Move all files to /Done/

## Required Resources
- Skills: {list all skills needed}
- MCPs: {list all MCP tools needed}
- Vault files: {list all files to read/write}

## Completion Rule
Move this file and all related files to /Done/ when all phases are complete and validated.
```

---

## Template Selection Guide

| Source File Type | Use Template |
|---|---|
| EMAIL_*.md | Email Reply Plan |
| WHATSAPP_*.md | WhatsApp Reply Plan |
| PROMPT_post_*.md | Social Media Post Plan |
| PROMPT_invoice_*.md | Invoice Generation Plan |
| PROMPT_research_*.md | Research/Investigation Plan |
| PROMPT_project_*.md | Multi-Step Project Plan |
| Other | Base Plan Template |
