---
name: facebook-poster
description: Generate and queue Facebook posts for the AI Employee. Use when user asks to post on Facebook, share business updates, announce milestones, write community-engaging content, or promote products/services on Facebook. Reads business context from vault files, writes a formatted post file to /Plans/facebook_queue/, and the FacebookPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---
# Facebook Poster
Generate engaging Facebook posts from business context and queue them for automated publishing.

## Workflow
1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Company_Handbook.md` — brand voice rules
2. **Write post** using structure in `references/post-structure.md`
3. **Save** to `/Vault/Plans/facebook_queue/{topic}_{timestamp}.md`
4. The **FacebookPoster watcher** picks it up automatically and publishes
5. Output `<promise>TASK_COMPLETE</promise>`

## Post File Format
```markdown
---
type: facebook_post
topic: {topic}
created: {iso_timestamp}
status: queued
---
{post content here — plain text, no markdown headers}
```

## Quick Rules
- **Optimal length: 40–80 words** — Facebook rewards concise, readable posts
- End with **2–4 hashtags** on a separate line
- One clear **call to action** (question, reaction prompt, or link click)
- Conversational and warm tone — Facebook audience is community-first
- Emojis welcome — they increase reach on Facebook

## Post Types & Guidance
See `references/post-structure.md` for hook patterns, templates, and examples by post type.