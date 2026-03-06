# Facebook MCP Tools Reference

Complete guide to using the Facebook MCP server tools for posting and queuing content.

## Available Tools

### queue_facebook (RECOMMENDED)

Queue a Facebook post for automated publishing.

**Parameters:**
- `text` (string, required): Post content (recommended 40-80 words / 300-500 chars)
- `topic` (string, optional): Topic/slug for filename (default: "post")

**Returns:**
- Success: `"Facebook post queued: {topic}_{timestamp}.md"`
- DRY_RUN: `"[DRY RUN] Would queue_facebook: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("queue_facebook", {
    "text": "Big news! We just automated our entire social media presence 🤖\n\nTwitter, LinkedIn, and Facebook — all posting automatically.\n\nWould you trust an AI to manage your social media? 👇\n\n#AI #Automation #BuildInPublic",
    "topic": "automation_milestone"
})
```

**Queue File Location:**
`/Vault/Plans/facebook_queue/{topic}_{timestamp}.md`

**Queue File Format:**
```markdown
---
type: facebook_post
created: 2026-03-05T14:30:00Z
---

Big news! We just automated our entire social media presence 🤖

Twitter, LinkedIn, and Facebook — all posting automatically.

Would you trust an AI to manage your social media? 👇

#AI #Automation #BuildInPublic
```

**Processing:**
- FacebookPoster watcher checks queue every 5 minutes (300 seconds)
- Watcher posts to Facebook via Playwright automation
- Posted files moved to `/Vault/Done/facebook_posted/`

---

### post_facebook (USE WITH CAUTION)

Post directly to Facebook without queuing.

**Parameters:**
- `text` (string, required): Post content

**Returns:**
- Success: `"Facebook posted: {text_preview}..."`
- Failure: `"Facebook failed: {text_preview}..."`
- DRY_RUN: `"[DRY RUN] Would post_facebook: {text_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("post_facebook", {
    "text": "🎉 Just shipped a new feature! Check it out. #BuildInPublic"
})
```

**⚠️ Security Warning:**
- **NEVER use post_facebook without explicit human approval**
- **ALWAYS prefer queue_facebook for safety**
- Direct posting bypasses human review
- No undo once posted

---

## When to Use Each Tool

### Use queue_facebook (default):
- ✅ All business updates and announcements
- ✅ Weekly progress reports
- ✅ Milestone celebrations
- ✅ Content generated from vault context
- ✅ Any post that should be reviewed before publishing

### Use post_facebook (rare):
- ⚠️ Only when explicitly instructed by user
- ⚠️ Time-sensitive announcements already approved
- ⚠️ User has reviewed and approved the exact text
- ⚠️ Never for automated/scheduled posts

---

## Facebook Session Requirements

Both tools require:
1. Facebook session saved as cookies.json
2. Cookies stored in path defined by `FACEBOOK_SESSION_PATH` env variable
3. Playwright browser installed (`playwright install chromium`)

**Session management:**
- Uses cookies.json (not persistent browser context)
- Cookies must be refreshed manually when expired
- Session expires after ~30 days of inactivity

**First-time setup:**
```bash
# 1. Export cookies from browser using extension
# Recommended: "Get cookies.txt LOCALLY" Chrome extension
# Export as JSON format

# 2. Save to session path
cp ~/Downloads/facebook.com_cookies.json ~/.local/share/facebook_session/cookies.json

# 3. Test with dry-run
uv run python main.py --facebook --dry-run
```

**When session expires:**
```
Error: "Facebook session expired!"

Solution:
1. Log in to Facebook in browser
2. Export cookies again using browser extension
3. Replace cookies.json file
4. Retry posting
```

---

## Post Content Guidelines

**Length recommendations:**
- **Optimal:** 40-80 words (300-500 characters)
- **Maximum:** No hard limit, but shorter posts perform better
- **Minimum:** 20 words (avoid too short)

**Why shorter is better on Facebook:**
- Algorithm favors concise, readable posts
- Users scroll quickly on mobile
- Longer posts get truncated with "See more"
- Engagement drops significantly after 80 words

**Formatting:**
- Plain text only (no markdown)
- Line breaks preserved
- Emojis supported and encouraged (boost engagement)
- URLs auto-linked by Facebook

**Hashtags:**
- 2-4 hashtags recommended
- Place at end of post on separate line
- Use relevant, searchable tags
- Mix broad (#AI) and niche (#WaheedAI) tags

---

## DRY_RUN Mode

When `DRY_RUN=true` in `.env`, both tools return simulation messages:

```
[DRY RUN] Would queue_facebook: Big news! We just automated...
```

**Always check DRY_RUN status before posting to production Facebook account.**

---

## Timing Considerations

**queue_facebook execution time:**
- File write: <1 second
- **Total: instant**

**post_facebook execution time:**
- Browser startup: ~5-10 seconds
- Facebook load: ~20 seconds
- Post submission: ~8-10 seconds (two-step process)
- **Total: ~40-50 seconds per post**

**FacebookPoster watcher:**
- Checks queue every 5 minutes (300 seconds)
- Posts one at a time
- Moves to /Done/ after posting

---

## Two-Step Posting Process

Facebook requires a two-step process:

1. **Step 1: Click "Next" button**
   - Opens post settings page
   - Uses JavaScript click to bypass overlay intercept
   - Wait 3 seconds for page transition

2. **Step 2: Click "Post" button**
   - Publishes the post
   - Uses JavaScript click for reliability
   - Wait 5 seconds for confirmation

**Why two steps?**
- Facebook's UI requires confirming post settings
- Prevents accidental posts
- Allows privacy/audience selection

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Facebook session expired` | Cookies expired | Export new cookies.json from browser |
| `Post box not found` | Facebook UI changed | Check watcher code for updated selectors |
| `Next button not found` | UI change or timing | Increase wait time or update selector |
| `Post button not found` | UI change or timing | Increase wait time or update selector |
| `Permission denied` | File system issue | Check vault path permissions |

---

## Best Practices

1. **Always queue by default** - use `queue_facebook` for all automated posts
2. **Review before posting** - check queued posts in `/Plans/facebook_queue/`
3. **Keep it concise** - aim for 40-80 words (300-500 chars)
4. **Use emojis** - they boost engagement on Facebook
5. **Log every action** - record all posts to `/Vault/Logs/YYYY-MM-DD.json`
6. **Check DRY_RUN** - verify mode before posting to production
7. **Validate content** - ensure no private/financial data in posts
8. **Use descriptive topics** - helps organize queue files
9. **Monitor posted folder** - check `/Done/facebook_posted/` for confirmation
10. **Refresh cookies regularly** - before they expire (~30 days)

---

## Security Considerations

- **Private data**: Never post financial numbers, client names, or sensitive business data
- **Brand safety**: All posts should align with company brand voice
- **Human review**: Queue posts for review, don't auto-post
- **Rate limiting**: Facebook may flag rapid posting as spam (watcher posts every 5 min max)
- **Session security**: Keep cookies.json file secure (contains auth tokens)
- **Community guidelines**: Ensure posts comply with Facebook's community standards

---

## Facebook vs LinkedIn vs Twitter

**Facebook (300-500 chars):**
- Warm, conversational tone
- Community engagement focus
- Questions and reaction prompts
- Emojis and visual appeal
- Longer than Twitter, shorter than LinkedIn

**LinkedIn (1300 chars):**
- Professional, authoritative tone
- Detailed insights and case studies
- Thought leadership content
- Business-focused audience

**Twitter (250 chars):**
- Punchy, direct tone
- Quick updates and tips
- Fast-paced, high-frequency
- Brevity is key

**Strategy:** Adapt content length and tone for each platform's audience.
