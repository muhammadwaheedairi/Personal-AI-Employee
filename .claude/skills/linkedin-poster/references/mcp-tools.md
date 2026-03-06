# LinkedIn MCP Tools Reference

Complete guide to using the LinkedIn MCP server tools for posting and queuing content.

## Available Tools

### queue_linkedin (RECOMMENDED)

Queue a LinkedIn post for human review and automated publishing.

**Parameters:**
- `text` (string, required): Post content (plain text, max 3000 chars)
- `topic` (string, optional): Topic/slug for filename (default: "post")

**Returns:**
- Success: `"LinkedIn post queued: {topic}_{timestamp}.md"`
- DRY_RUN: `"[DRY RUN] Would queue_linkedin: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("queue_linkedin", {
    "text": "We just automated our entire email workflow...\n\n#AI #Automation",
    "topic": "email_automation_milestone"
})
```

**Queue File Location:**
`/Vault/Plans/linkedin_queue/{topic}_{timestamp}.md`

**Queue File Format:**
```markdown
---
type: linkedin_post
created: 2026-03-05T14:30:00Z
---

We just automated our entire email workflow...

#AI #Automation
```

**Processing:**
- LinkedInPoster watcher checks queue every 60 minutes (configurable)
- Watcher posts to LinkedIn via Playwright automation
- Posted files moved to `/Vault/Done/linkedin_posted/`

---

### post_linkedin (USE WITH CAUTION)

Post directly to LinkedIn without queuing.

**Parameters:**
- `text` (string, required): Post content (plain text, max 3000 chars)

**Returns:**
- Success: `"LinkedIn posted: {text_preview}..."`
- Failure: `"LinkedIn failed: {text_preview}..."`
- DRY_RUN: `"[DRY RUN] Would post_linkedin: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("post_linkedin", {
    "text": "We just automated our entire email workflow...\n\n#AI #Automation"
})
```

**⚠️ Security Warning:**
- **NEVER use post_linkedin without explicit human approval**
- **ALWAYS prefer queue_linkedin for safety**
- Direct posting bypasses human review
- No undo once posted

---

## When to Use Each Tool

### Use queue_linkedin (default):
- ✅ All business updates and announcements
- ✅ Weekly progress reports
- ✅ Milestone celebrations
- ✅ Content generated from vault context
- ✅ Any post that should be reviewed before publishing

### Use post_linkedin (rare):
- ⚠️ Only when explicitly instructed by user
- ⚠️ Time-sensitive announcements already approved
- ⚠️ User has reviewed and approved the exact text
- ⚠️ Never for automated/scheduled posts

---

## LinkedIn Session Requirements

Both tools require:
1. LinkedIn session authenticated and saved
2. Session stored in path defined by `LINKEDIN_SESSION_PATH` env variable
3. Playwright browser installed (`playwright install chromium`)

**First-time setup:**
```bash
# Run poster once to authenticate
uv run python main.py --linkedin --dry-run
# Log in to LinkedIn when browser opens
# Session will be saved for future use
```

---

## Post Content Guidelines

**Character limits:**
- Recommended: 1,300 characters (best engagement)
- Maximum: 3,000 characters (LinkedIn limit)
- Minimum: 100 characters (avoid too short)

**Formatting:**
- Plain text only (no markdown)
- Line breaks preserved
- Emojis supported
- URLs auto-linked by LinkedIn

**Hashtags:**
- 3-5 hashtags recommended
- Place at end of post on separate line
- Use relevant, searchable tags
- Mix broad (#AI) and niche (#ClaudeCode) tags

---

## DRY_RUN Mode

When `DRY_RUN=true` in `.env`, both tools return simulation messages:

```
[DRY RUN] Would queue_linkedin: We just automated our entire email workflow...
```

**Always check DRY_RUN status before posting to production LinkedIn account.**

---

## Timing Considerations

**queue_linkedin execution time:**
- File write: <1 second
- **Total: instant**

**post_linkedin execution time:**
- Browser startup: ~5-10 seconds
- LinkedIn load: ~20 seconds
- Post submission: ~3-5 seconds
- **Total: ~30-40 seconds per post**

**LinkedInPoster watcher:**
- Checks queue every 60 minutes (default)
- Posts one at a time
- Moves to /Done/ after posting

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `LinkedIn session expired` | Need to re-authenticate | Run `--linkedin --dry-run` to re-login |
| `Post editor not found` | LinkedIn UI changed | Check watcher code for updated selectors |
| `Browser timeout` | Network issues | Increase wait time in watcher config |
| `Permission denied` | File system issue | Check vault path permissions |
| `Text too long` | Exceeds 3000 chars | Shorten post content |

---

## Best Practices

1. **Always queue by default** - use `queue_linkedin` for all automated posts
2. **Review before posting** - check queued posts in `/Plans/linkedin_queue/`
3. **Log every action** - record all posts to `/Vault/Logs/YYYY-MM-DD.json`
4. **Check DRY_RUN** - verify mode before posting to production
5. **Validate content** - ensure no private/financial data in posts
6. **Use descriptive topics** - helps organize queue files
7. **Monitor posted folder** - check `/Done/linkedin_posted/` for confirmation

---

## Security Considerations

- **Private data**: Never post financial numbers, client names, or sensitive business data
- **Brand safety**: All posts should align with company brand voice
- **Human review**: Queue posts for review, don't auto-post
- **Rate limiting**: LinkedIn may flag rapid posting as spam
- **Session security**: Keep LinkedIn session files secure
