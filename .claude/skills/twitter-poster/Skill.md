---
name: twitter-poster
description: Generate and queue Twitter/X posts for the AI Employee. Use when user asks to post on Twitter/X, share updates, announce milestones, write viral tweets, or create engagement-driving content. Reads business context from vault files, writes a formatted post file to /Plans/twitter_queue/, and the TwitterPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---
# Twitter Poster
Generate compelling tweets from business context and queue them for automated publishing.

## Workflow
1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Company_Handbook.md` — brand voice rules
2. **Write tweet** using structure in `references/post-structure.md`
3. **Save** to `/Vault/Plans/twitter_queue/{topic}_{timestamp}.md`
4. The **TwitterPoster watcher** picks it up automatically and publishes
5. Output `<promise>TASK_COMPLETE</promise>`

## Post File Format
```markdown
---
type: twitter_post
topic: {topic}
created: {iso_timestamp}
status: queued
---
{tweet content here — plain text, no markdown headers}
```

## Quick Rules
- Max **250 characters** (hard limit — TwitterPoster auto-truncates at 247 + "...")
- End with **2–4 hashtags** on same or separate line
- First line must be a strong hook — this is what stops the scroll
- Emojis welcome — they boost engagement on Twitter/X
- No clickbait — only post real, verifiable value

## Post Types & Guidance
See `references/post-structure.md` for hook patterns, templates, and examples by post type.