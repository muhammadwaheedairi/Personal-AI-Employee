---
name: linkedin-poster
description: Generate and queue LinkedIn posts for the AI Employee. Use when user asks to post on LinkedIn, create business content, announce milestones, share weekly updates, or write sales-generating social content. Reads business context from vault files, writes a formatted post file to /Plans/linkedin_queue/, and the LinkedInPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---

# LinkedIn Poster

Generate compelling LinkedIn posts from business context and queue them for automated publishing via the LinkedInPoster watcher.

## Workflow

1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects, milestones
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Logs/*.json` — this week's metrics and action counts
   - `/Vault/Company_Handbook.md` — brand voice rules and tone guidelines
2. **Identify story** — what's the most interesting/valuable thing that happened?
3. **Write post** using structure from `references/post-structure.md`
4. **Validate content** — no private data, under 1,300 chars, has clear value
5. **Queue post** using `queue_linkedin` MCP tool → saves to `/Plans/linkedin_queue/`
6. **LinkedInPoster watcher** picks it up automatically (checks every 60 min)
7. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
8. Output `<promise>TASK_COMPLETE</promise>`

## MCP Tool Usage

### queue_linkedin (ALWAYS USE THIS)

Queue a post for automated publishing:

```python
result = mcp_call("queue_linkedin", {
    "text": "We just hit 80% email automation — two months ahead of schedule...\n\n#AI #Automation",
    "topic": "email_automation_milestone"
})

# Returns: "LinkedIn post queued: email_automation_milestone_20260305_143000.md"
```

**Queue file location:** `/Vault/Plans/linkedin_queue/{topic}_{timestamp}.md`

**What happens next:**
1. File saved to queue folder
2. LinkedInPoster watcher checks queue every 60 minutes
3. Watcher posts to LinkedIn via Playwright automation
4. Posted file moved to `/Vault/Done/linkedin_posted/`

### post_linkedin (NEVER USE WITHOUT APPROVAL)

⚠️ **Security Warning:** This posts directly to LinkedIn without queuing or human review.

**ONLY use when:**
- User explicitly instructs to post immediately
- User has reviewed and approved the exact text
- Time-sensitive announcement already approved

**Default behavior:** ALWAYS use `queue_linkedin` instead.

## Post File Format

```markdown
---
type: linkedin_post
topic: {topic_slug}
created: {iso_timestamp}
status: queued
---

{post content here — plain text, no markdown headers}

{hashtags on separate line at end}
```

**Example:**
```markdown
---
type: linkedin_post
topic: weekly_update
created: 2026-03-05T14:30:00Z
status: queued
---

This week's numbers:
→ 47 emails triaged automatically
→ 3 invoices sent without manual review
→ 2 hours saved every day

The AI Employee is getting smarter every week.

What repetitive task would you eliminate first?

#AI #Automation #Productivity #BuildInPublic
```

## Content Guidelines

### Character Limits
- **Recommended:** 1,300 characters (best engagement)
- **Maximum:** 3,000 characters (LinkedIn limit)
- **Minimum:** 100 characters (avoid too short)

### Post Structure

```
[Hook — 1-2 lines, bold claim or question]

[Context — what happened, 2-3 lines]

[Value — what reader learns, 2-3 lines]

[CTA — question to drive comments, 1 line]

#Tag1 #Tag2 #Tag3 #Tag4 #Tag5
```

### Hashtags
- **Count:** 3-5 hashtags (optimal for reach)
- **Placement:** Separate line at end of post
- **Mix:** Combine broad (#AI) and niche (#ClaudeCode) tags
- **Relevance:** Only use tags directly related to post content

### Tone (Professional but Approachable)
- Use "we" for company updates
- Use "I" for personal lessons
- Be conversational, not corporate
- Share real numbers when possible
- Admit mistakes and lessons learned
- Focus on reader value, not self-promotion

## Context Sources

See `references/content-ideas.md` for detailed guidance on generating content from vault files.

**Primary sources:**

1. **Business_Goals.md** → Milestones, revenue targets, project status
2. **Done/ folder** → Recent completions, shipped features
3. **Logs/*.json** → Weekly metrics, automation stats
4. **Company_Handbook.md** → Brand voice, tone guidelines

**Post type decision tree:**
```
What happened this week?
    │
    ├─ Hit a milestone? → Milestone announcement
    ├─ Shipped a feature? → Build-in-public update
    ├─ Learned something? → Lesson learned post
    ├─ Solved a problem? → Problem-solution post
    └─ Regular week? → Weekly roundup
```

## Security Rules

- **NEVER post private financial data** (exact revenue, profit margins, client payments)
- **NEVER post client names** without explicit permission
- **NEVER post sensitive business strategy** (pricing, competitive intel)
- **ALWAYS use queue_linkedin** by default (never post_linkedin without approval)
- **ALWAYS validate content** before queuing (no private data, brand-safe)
- **ALWAYS log every action** to `/Vault/Logs/YYYY-MM-DD.json`

## What NOT to Post

❌ Private financial details
❌ Client names without permission
❌ Sensitive business strategy
❌ Negative content (complaints, drama)
❌ Unverified claims
❌ Clickbait or misleading hooks
❌ Personal politics (unless business-relevant)
❌ Confidential information (NDAs, trade secrets)

## Post Templates

See `references/post-structure.md` for complete templates and examples.

**Quick templates:**

### Milestone Announcement
```
We just hit [result] in [timeframe]. Here's what actually made the difference.

[2-3 lines explaining what you did]

The result: [specific outcome]

[Question for audience]

#Hashtags
```

### Weekly Update
```
This week's numbers:
→ [metric 1]
→ [metric 2]
→ [metric 3]

[One line insight]

[Question for audience]

#Hashtags
```

### Build in Public
```
What we built this week: [feature/improvement]

[2-3 lines explaining why it matters]

The impact: [specific benefit]

[Question for audience]

#Hashtags
```

## Example Scenarios

**Scenario 1: Weekly progress post**
```
Input: User asks "Create a LinkedIn post about this week's progress"
Action:
1. Read /Vault/Logs/ for this week's metrics
2. Read /Vault/Done/ for completed tasks
3. Generate weekly roundup post
4. Call queue_linkedin MCP tool
Output: Post queued to /Plans/linkedin_queue/weekly_update_20260305_143000.md
```

**Scenario 2: Milestone announcement**
```
Input: User says "We just hit our Q1 revenue goal, post about it"
Action:
1. Read /Vault/Business_Goals.md for goal details
2. Generate milestone announcement post
3. Validate no private financial data included
4. Call queue_linkedin MCP tool
Output: Post queued to /Plans/linkedin_queue/q1_milestone_20260305_143000.md
```

**Scenario 3: Feature launch**
```
Input: User asks "Announce the new email automation feature"
Action:
1. Read /Vault/Done/ for feature details
2. Generate build-in-public post
3. Include specific benefits and metrics
4. Call queue_linkedin MCP tool
Output: Post queued to /Plans/linkedin_queue/email_automation_launch_20260305_143000.md
```

## Logging Format

Every LinkedIn action must be logged to `/Vault/Logs/YYYY-MM-DD.json`:

**Queue log:**
```json
{
  "timestamp": "2026-03-05T14:30:00Z",
  "action_type": "linkedin_post_queued",
  "topic": "weekly_update",
  "file": "weekly_update_20260305_143000.md",
  "character_count": 387,
  "hashtags": ["#AI", "#Automation", "#Productivity"]
}
```

**Posted log (by watcher):**
```json
{
  "timestamp": "2026-03-05T15:00:00Z",
  "action_type": "linkedin_posted",
  "source_file": "weekly_update_20260305_143000.md",
  "status": "posted",
  "character_count": 387
}
```

## LinkedInPoster Watcher

**How it works:**
1. Checks `/Plans/linkedin_queue/` every 60 minutes (configurable)
2. Posts one file at a time to LinkedIn via Playwright
3. Moves posted files to `/Done/linkedin_posted/`
4. Logs success/failure to `/Vault/Logs/`

**Manual trigger:**
```bash
uv run python main.py --linkedin
```

**Session requirements:**
- LinkedIn session must be authenticated
- Session stored in `LINKEDIN_SESSION_PATH`
- Playwright browser installed

**First-time setup:**
```bash
uv run python main.py --linkedin --dry-run
# Log in to LinkedIn when browser opens
# Session saved for future use
```

## MCP Tools Reference

See `references/mcp-tools.md` for complete MCP tool documentation including:
- Tool parameters and return values
- Queue vs direct posting
- DRY_RUN behavior
- Session requirements
- Timing considerations
- Error handling
- Security best practices

## Content Ideas Reference

See `references/content-ideas.md` for detailed guidance on:
- Generating content from vault context
- Post type decision trees
- Tone guidelines for LinkedIn
- Hashtag strategy
- What NOT to post
- Example content generation workflows

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`