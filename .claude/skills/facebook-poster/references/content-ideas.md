# Facebook Content Ideas & Context Sources

Guide for generating Facebook post ideas from business context and vault files.

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
- Milestone announcements with celebration
- Progress updates with community engagement
- Behind-the-scenes stories
- Achievement celebrations

---

### 2. Done Folder

**Location:** `/Vault/Done/`

**What to extract:**
- Recently completed tasks (last 7 days)
- Finished projects
- Resolved issues
- Shipped features

**Post ideas:**
- Weekly roundup with visual appeal
- "What we shipped this week" updates
- Build-in-public progress reports
- Before/after transformations

---

### 3. Company_Handbook.md

**Location:** `/Vault/Company_Handbook.md`

**What to extract:**
- Brand voice and tone guidelines
- Company values and mission
- Product/service descriptions
- Target audience

**Use for:**
- Ensuring warm, conversational tone
- Aligning posts with company values
- Staying on-brand with messaging
- Understanding community expectations

---

### 4. Logs Folder

**Location:** `/Vault/Logs/*.json`

**What to extract:**
- Action counts (emails processed, invoices sent)
- Automation metrics
- Time saved calculations
- System performance data

**Post ideas:**
- "This week's numbers" posts with emojis
- Automation impact stories
- Productivity transformation reports
- Community-friendly stats

---

## Post Type Decision Tree

```
What happened this week?
    │
    ├─ Hit a milestone? → Celebration post with emojis 🎉
    │
    ├─ Shipped a feature? → Build-in-public update with CTA
    │
    ├─ Learned something? → Value post with community question
    │
    ├─ Solved a problem? → Story post with relatable hook
    │
    └─ Regular week? → Weekly roundup with engagement prompt
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
- What's the most interesting thing that happened this week?
- What would our community find valuable or inspiring?
- What demonstrates progress or learning?
- What's shareable and relatable?
- Can I tell this story in 40-80 words?

### Step 3: Structure Post

Use templates from `post-structure.md`:
1. Hook (warm, relatable opening with emoji)
2. Context (what happened, 2-3 lines)
3. Value (what this means for audience)
4. CTA (question or reaction prompt)
5. Hashtags (2-4 relevant tags)

### Step 4: Validate Content

Check:
- ✅ 40-80 words (300-500 chars optimal)
- ✅ No private financial data
- ✅ No client names without permission
- ✅ No sensitive business information
- ✅ Warm, conversational tone
- ✅ Has clear CTA for engagement
- ✅ Includes 2-4 hashtags

---

## Post Ideas by Business Context

### Revenue Milestone
```
Context: Hit monthly revenue target
Post: "🎉 Big milestone today!

We just crossed $X in monthly revenue. Here's what made the difference: [one specific tactic]

This is what happens when you [key insight].

Have you hit a big milestone recently? Share below! 👇

#Entrepreneurship #SmallBusiness #BuildInPublic"
```

### Feature Launch
```
Context: Shipped new automation feature
Post: "We've been building something exciting behind the scenes 🤖

This week we finally shipped it: [feature name]

What it does: [one-line benefit]

Would you use something like this? Let us know! 👇

#AI #Automation #BuildInPublic"
```

### Lesson Learned
```
Context: Made a mistake or faced a challenge
Post: "💡 Here's something I learned the hard way:

[Mistake or challenge in 2-3 lines]

The fix: [one-line solution]

Have you faced something similar? Drop a comment! 👇

#Founder #Lessons #Entrepreneurship"
```

### Weekly Progress
```
Context: Regular week of work
Post: "This week's AI Employee report 📊

→ [metric 1]
→ [metric 2]
→ [metric 3]

The future of work is here. Are you ready?

What would you automate first? 👇

#AI #Productivity #Automation"
```

### Client Win
```
Context: Successful client project
Post: "🎉 Client success story!

A client just saved [X hours/week] with our solution.

How? [One-line explanation]

This is why we do what we do.

What's your biggest time-waster? Let's talk solutions! 👇

#Productivity #SmallBusiness #AI"
```

---

## Tone Guidelines for Facebook

**Warm and conversational:**
- Write like you're talking to a friend
- Use "we" for company updates
- Use "I" for personal stories
- Be approachable and friendly
- Avoid corporate jargon

**Community-first:**
- Always include a CTA (question or reaction prompt)
- Invite comments and shares
- Respond to comments promptly
- Build relationships, not just broadcast

**Authentic and transparent:**
- Share real numbers when possible
- Admit mistakes and lessons
- Show behind-the-scenes work
- Be honest about challenges

**Encouraging and positive:**
- Facebook audience responds to positivity
- Celebrate wins (yours and others')
- Inspire and motivate
- Focus on solutions, not problems

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
❌ **Overly promotional** (Facebook penalizes hard sells)

---

## Hashtag Strategy

**Use 2-4 tags (Facebook best practice):**
- Too few: miss discoverability
- Too many: looks spammy, reduces reach

**Mix broad and niche:**
- Broad: #AI, #Automation, #Entrepreneurship (high volume)
- Niche: #WaheedAI, #BuildInPublic, #TechPakistan (targeted)

**Relevant to content:**
- Don't use trending tags unrelated to post
- Match tags to post topic and audience
- Include industry-specific tags

**Common tag sets:**

**AI/Automation:**
`#AI #Automation #BuildInPublic #WaheedAI`

**Business/Entrepreneurship:**
`#Entrepreneur #SmallBusiness #Founder #Productivity`

**Tech/Development:**
`#Python #OpenSource #LLM #TechPakistan`

**Community/Engagement:**
`#Community #Networking #Learning #Growth`

---

## Engagement Optimization

**CTAs that drive comments:**
- "What would you do?" (invites opinions)
- "Have you faced this?" (invites experiences)
- "Drop a comment if..." (direct instruction)
- "Tag someone who..." (encourages shares)
- "What's your biggest...?" (invites sharing)

**Emojis that boost engagement:**
- 🎉 (celebration, milestones)
- 🤖 (AI, automation)
- 💡 (tips, insights)
- 👇 (directing to comments)
- 📊 (stats, reports)
- ✅ (checklists, achievements)

**Timing considerations:**
- Facebook algorithm favors posts with early engagement
- Watcher posts every 5 minutes
- Best times: weekday mornings and evenings
- Avoid late nights and weekends for business content

---

## Example: Generating Post from Vault Context

**Input context:**
- Business_Goals.md shows: "Q1 Goal: Automate 80% of email triage"
- Done/ shows: EMAIL_triage_complete.md from 2 days ago
- Logs show: 47 emails processed this week, 2 hours saved

**Generated post:**
```
Big news! We just hit 80% email automation — two months ahead of schedule 🎉

Our AI Employee now processes Gmail, flags urgent messages, and drafts replies. All locally, zero data leaves our machine.

The result: 2 hours back every day. 47 emails triaged this week without manual review.

What's the first thing you'd automate if you had an AI employee? 👇

#AI #Automation #Productivity #BuildInPublic
```

**Word count:** 67 words (optimal range)
**Character count:** 412 chars (optimal range)
**Value:** Specific metrics, clear benefit, relatable question
**Safe:** No private data, no client names, verifiable claims
**Engaging:** Emoji hook, concrete numbers, direct CTA

---

## Platform-Specific Content Strategy

**Facebook (300-500 chars):**
- Warm, community-focused
- Questions and engagement prompts
- Celebration and storytelling
- Emojis and visual appeal

**LinkedIn (1300 chars):**
- Professional, authoritative
- Detailed insights and analysis
- Thought leadership
- Business-focused

**Twitter (250 chars):**
- Punchy, direct
- Quick updates and tips
- Fast-paced, high-frequency
- Brevity is key

**Strategy:** Facebook is the middle ground — more personal than LinkedIn, more detailed than Twitter.
