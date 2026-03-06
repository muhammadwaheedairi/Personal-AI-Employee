---
name: facebook-poster
description: Generate and queue Facebook posts for the AI Employee. Use when user asks to post on Facebook, share business updates, announce milestones, write community-engaging content, or promote products/services on Facebook. Reads business context from vault files, writes a formatted post file to /Plans/facebook_queue/, and the FacebookPoster watcher auto-publishes it. Also use when reviewing or improving drafts already in the queue.
---

# Facebook Poster

Generate engaging Facebook posts from business context and queue them for automated publishing via the FacebookPoster watcher.

## Workflow

1. **Gather context** from vault:
   - `/Vault/Business_Goals.md` — current goals, metrics, projects, milestones
   - `/Vault/Done/` — recent completions (last 7 days)
   - `/Vault/Logs/*.json` — this week's metrics and action counts
   - `/Vault/Company_Handbook.md` — brand voice rules and tone guidelines
2. **Identify story** — what's the most interesting/valuable thing that happened this week?
3. **Write post** using structure from `references/post-structure.md`
4. **Validate content** — 40-80 words, no private data, warm tone, has CTA
5. **Queue post** using `queue_facebook` MCP tool → saves to `/Plans/facebook_queue/`
6. **FacebookPoster watcher** picks it up automatically (checks every 5 min)
7. **Log action** to `/Vault/Logs/YYYY-MM-DD.json`
8. Output `<promise>TASK_COMPLETE</promise>`

## MCP Tool Usage

### queue_facebook (ALWAYS USE THIS)

```python
result = mcp_call("queue_facebook", {
    "text": "Big news! We just automated our entire social media presence 🤖\n\nTwitter, LinkedIn, and Facebook — all posting automatically.\n\nWould you trust an AI to manage your social media? 👇\n\n#AI #Automation #BuildInPublic",
    "topic": "automation_milestone"
})
```

**What happens:** File saved to `/Plans/facebook_queue/`, watcher posts every 5 min via two-step process.

### post_facebook (NEVER USE WITHOUT APPROVAL)

⚠️ Posts directly without queuing. ONLY use when explicitly instructed by user.

## Content Guidelines

**Length recommendations:**
- Optimal: 40-80 words (300-500 chars)
- Facebook algorithm favors concise, readable posts
- Shorter posts perform better on mobile

**Structure:**
```
[Hook — warm, relatable opening with emoji]
[Context — 2-3 lines]
[Value — what this means for audience]
[CTA — question or reaction prompt]
#Tag1 #Tag2 #Tag3
```

**Hashtags:** 2-4 tags, mix broad (#AI) and niche (#WaheedAI)

**Tone:** Warm, conversational, community-first, use emojis (🎉 🤖 💡 👇)

## Security Rules

- **NEVER** post private financial data
- **NEVER** post client names without permission
- **ALWAYS** use queue_facebook by default
- **ALWAYS** validate content (40-80 words, warm tone, has CTA)
- **ALWAYS** log to `/Vault/Logs/YYYY-MM-DD.json`

## Two-Step Posting Process

Facebook requires a two-step process:

1. **Step 1:** Click "Next" button (opens post settings)
2. **Step 2:** Click "Post" button (publishes)

Both steps use JavaScript click to bypass overlay intercepts. Total time: ~40-50 seconds per post.

## FacebookPoster Watcher

- Checks queue every 5 minutes
- Posts via Playwright automation
- Uses cookies.json for session (refresh manually when expired ~30 days)
- Moves posted files to `/Done/facebook_posted/`

**Manual trigger:** `uv run python main.py --facebook`

**Session setup:**
```bash
# Export cookies from browser using extension
cp ~/Downloads/facebook.com_cookies.json ~/.local/share/facebook_session/cookies.json
```

## References

- `references/post-structure.md` — Hook patterns, templates, examples
- `references/mcp-tools.md` — Complete MCP tool documentation
- `references/content-ideas.md` — Content generation from vault context

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`