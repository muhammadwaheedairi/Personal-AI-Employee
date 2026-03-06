# LinkedIn Content Ideas & Context Sources

Guide for generating LinkedIn post ideas from business context and vault files.

## Primary Context Sources

### 1. Business_Goals.md

**Location:** `/Vault/Business_Goals.md`

**What to extract:**
- Current revenue targets and progress
- Active projects and their status
- Key metrics and KPIs
- Quarterly/monthly goals
- Client wins and milestones

**Post ideas:**
- Milestone announcements (hit revenue target, completed project)
- Progress updates (halfway to goal, X clients onboarded)
- Lessons learned from pursuing goals
- Behind-the-scenes of goal execution

---

### 2. Done Folder

**Location:** `/Vault/Done/`

**What to extract:**
- Recently completed tasks (last 7 days)
- Finished projects
- Resolved issues
- Shipped features

**Post ideas:**
- Weekly roundup of accomplishments
- "What we shipped this week" updates
- Build-in-public progress reports
- Before/after comparisons

---

### 3. Company_Handbook.md

**Location:** `/Vault/Company_Handbook.md`

**What to extract:**
- Brand voice and tone guidelines
- Company values and mission
- Product/service descriptions
- Target audience

**Use for:**
- Ensuring consistent brand voice
- Aligning posts with company values
- Staying on-brand with messaging
- Understanding audience expectations

---

### 4. Logs Folder

**Location:** `/Vault/Logs/*.json`

**What to extract:**
- Action counts (emails processed, invoices sent)
- Automation metrics
- Time saved calculations
- System performance data

**Post ideas:**
- "This week's numbers" posts
- Automation impact reports
- Productivity metrics
- ROI demonstrations

---

## Post Type Decision Tree

```
What happened this week?
    │
    ├─ Hit a milestone? → Milestone announcement post
    │
    ├─ Shipped a feature? → Build-in-public update
    │
    ├─ Learned something? → Lesson learned post
    │
    ├─ Solved a problem? → Problem-solution post
    │
    └─ Regular week? → Weekly roundup post
```

---

## Content Generation Workflow

### Step 1: Gather Context

```python
# Read business goals
goals = read_file("/Vault/Business_Goals.md")

# Get recent completions
done_files = list_files("/Vault/Done/", last_7_days=True)

# Get this week's metrics
logs = read_logs("/Vault/Logs/", this_week=True)

# Get brand voice
handbook = read_file("/Vault/Company_Handbook.md")
```

### Step 2: Identify Story

Ask:
- What's the most interesting thing that happened?
- What would our audience find valuable?
- What demonstrates progress or learning?
- What's shareable and relatable?

### Step 3: Structure Post

Use templates from `post-structure.md`:
1. Hook (attention-grabbing opening)
2. Context (what happened)
3. Value (what reader gains)
4. CTA (call to action)
5. Hashtags (3-5 relevant tags)

### Step 4: Validate Content

Check:
- ✅ No private financial data
- ✅ No client names without permission
- ✅ No sensitive business information
- ✅ Aligns with brand voice
- ✅ Under 1,300 characters
- ✅ Has clear value for reader

---

## Post Ideas by Business Context

### Revenue Milestone
```
Context: Hit monthly revenue target
Hook: "We just crossed $X in monthly revenue. Here's what actually moved the needle."
Value: Share 2-3 specific tactics that worked
CTA: "What's working for your business right now?"
```

### Feature Launch
```
Context: Shipped new automation feature
Hook: "What we built this week with AI automation (and why it matters)."
Value: Explain the problem it solves
CTA: "What would you automate first?"
```

### Lesson Learned
```
Context: Made a mistake or faced a challenge
Hook: "I made a mistake that cost me [X hours/dollars]. Here's what I learned."
Value: Share the lesson and how to avoid it
CTA: "Have you faced something similar?"
```

### Weekly Progress
```
Context: Regular week of work
Hook: "This week's numbers:"
Value: List 3-5 key metrics or accomplishments
CTA: "What's your biggest win this week?"
```

### Client Win
```
Context: Successful client project
Hook: "A client just saved [X hours/week] with our solution."
Value: Explain the transformation
CTA: "What's the biggest time-waster in your business?"
```

---

## Tone Guidelines for LinkedIn

**Professional but approachable:**
- Use "we" for company updates
- Use "I" for personal lessons
- Avoid jargon unless audience-specific
- Be conversational, not corporate

**Authentic and transparent:**
- Share real numbers when possible
- Admit mistakes and lessons
- Show behind-the-scenes work
- Be honest about challenges

**Value-first:**
- Every post should teach or inspire
- Focus on reader benefit, not self-promotion
- Share actionable insights
- Make it worth their time

**Engaging:**
- Ask questions to drive comments
- Use line breaks for readability
- Start strong with a hook
- End with a clear CTA

---

## What NOT to Post

❌ **Private financial details** (exact revenue, profit margins, client payments)
❌ **Client names** without explicit permission
❌ **Sensitive business strategy** (pricing, competitive intel)
❌ **Negative content** (complaints, call-outs, drama)
❌ **Unverified claims** (can't back up with data)
❌ **Clickbait** (misleading hooks, false promises)
❌ **Personal politics** (unless directly relevant to business)
❌ **Confidential information** (NDAs, trade secrets)

---

## Hashtag Strategy

**Mix broad and niche:**
- Broad: #AI, #Automation, #Entrepreneurship (high volume)
- Niche: #ClaudeCode, #AgentEngineering, #BuildInPublic (targeted)

**Use 3-5 tags:**
- Too few: miss discoverability
- Too many: looks spammy

**Relevant to content:**
- Don't use trending tags unrelated to post
- Match tags to post topic and audience
- Include industry-specific tags

**Common tag sets:**

**AI/Automation:**
`#AI #Automation #ClaudeCode #AgentEngineering #BuildInPublic`

**Business/Entrepreneurship:**
`#Entrepreneurship #SmallBusiness #Founder #Productivity #StartupLife`

**Tech/Development:**
`#Python #OpenSource #MCP #LLM #AIAgents`

**Productivity:**
`#Productivity #TimeManagement #Automation #WorkSmart #Efficiency`

---

## Example: Generating Post from Vault Context

**Input context:**
- Business_Goals.md shows: "Q1 Goal: Automate 80% of email triage"
- Done/ shows: EMAIL_triage_complete.md from 2 days ago
- Logs show: 47 emails processed this week, 2 hours saved

**Generated post:**
```
We just hit 80% email automation — two months ahead of schedule.

Our AI Employee now processes Gmail, flags urgent messages, and drafts replies. All locally, zero data leaves our machine.

The result: 2 hours back every day. 47 emails triaged this week without manual review.

What's the first thing you'd automate if you had an AI employee?

#AI #Automation #Productivity #BuildInPublic #ClaudeCode
```

**Character count:** 387 chars (well under 1,300 limit)
**Value:** Specific metrics, clear benefit, relatable question
**Safe:** No private data, no client names, verifiable claims
