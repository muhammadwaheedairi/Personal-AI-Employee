---
name: linkedin-poster
description: Generate and queue LinkedIn posts for the AI Employee. Use when user asks to post on LinkedIn, create business content, announce milestones, share weekly updates, or write sales-generating social content. Reads business context from vault files, writes a formatted post file to /Plans/linkedin_queue/, and the LinkedInPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---

# LinkedIn Poster

Generate compelling LinkedIn posts from business context and queue them for automated publishing.

## Workflow

1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Company_Handbook.md` — brand voice rules
2. **Write post** using structure in `references/post-structure.md`
3. **Save** to `/Vault/Plans/linkedin_queue/{topic}_{timestamp}.md`
4. The **LinkedInPoster watcher** picks it up automatically and publishes
5. Output `<promise>TASK_COMPLETE</promise>`

## Post File Format

```markdown
---
type: linkedin_post
topic: {topic}
created: {iso_timestamp}
status: queued
---

{post content here — plain text, no markdown headers}
```

## Quick Rules

- Max **1,300 characters** for best reach
- End with **3–5 hashtags** on a separate line
- One clear **call to action** (question or prompt)
- No clickbait — only post real, verifiable value

## Post Types & Guidance

See `references/post-structure.md` for hook patterns, templates, and examples by post type.