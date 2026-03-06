# WhatsApp MCP Tools Reference

Complete guide to using the WhatsApp MCP server tools for sending messages and creating drafts.

## Available Tools

### send_whatsapp

Send a WhatsApp message immediately via Playwright automation.

**Parameters:**
- `to` (string, required): Phone number with country code (e.g., `+923001234567`)
- `body` (string, required): Message text to send

**Returns:**
- Success: `"WhatsApp sent to {phone_number}"`
- Failure: `"WhatsApp failed to {phone_number}"`
- DRY_RUN: `"[DRY RUN] Would send_whatsapp to {phone_number}: {body_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("send_whatsapp", {
    "to": "+923001234567",
    "body": "Thank you for your inquiry. We'll get back to you shortly."
})
```

**Important Notes:**
- Requires WhatsApp Web session to be authenticated (stored in session path)
- Uses Playwright browser automation (headless or headed based on DISPLAY env)
- Takes ~45-50 seconds to complete (browser startup + page load + send)
- Phone number MUST include country code with + prefix
- Message is sent via WhatsApp Web interface

---

### draft_whatsapp

Create a WhatsApp draft for human approval without sending.

**Parameters:**
- `to` (string, required): Phone number with country code
- `body` (string, required): Draft message text
- `context` (string, optional): Why this message is being sent (for human review)

**Returns:**
- Success: `"Draft saved to WHATSAPP_draft_{timestamp}.md — move to /Approved to send"`
- DRY_RUN: `"[DRY RUN] Would draft_whatsapp to {phone_number}: {body_preview}..."`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("draft_whatsapp", {
    "to": "+923001234567",
    "body": "Your invoice for March is ready. Total: $500. Please let me know if you have questions.",
    "context": "Invoice request from client via WhatsApp"
})
```

**Draft File Format:**

The tool creates a file in `/Pending_Approval/WHATSAPP_draft_{timestamp}.md`:

```markdown
---
action: send_whatsapp
to: +923001234567
body: Your invoice for March is ready...
context: Invoice request from client via WhatsApp
created: 2026-03-05T14:30:00Z
status: pending
---

# WhatsApp Draft — Awaiting Approval

**To:** +923001234567
**Message:** Your invoice for March is ready...
**Context:** Invoice request from client via WhatsApp

Move to /Approved to send.
```

---

## Phone Number Format

**Required format:** `+[country_code][number]`

**Examples:**
- Pakistan: `+923001234567`
- USA: `+14155551234`
- UK: `+447700900123`
- India: `+919876543210`

**Invalid formats:**
- Without +: `923001234567` ❌
- With spaces: `+92 300 1234567` ❌
- With dashes: `+92-300-1234567` ❌
- Without country code: `3001234567` ❌

---

## DRY_RUN Mode

When `DRY_RUN=true` in `.env`, both tools return simulation messages instead of actually sending/drafting:

```
[DRY RUN] Would send_whatsapp to +923001234567: Thank you for your inquiry...
```

**Always check DRY_RUN status before sending to real contacts.**

---

## Browser Session Requirements

The `send_whatsapp` tool requires:
1. WhatsApp Web session authenticated and saved
2. Session stored in path defined by `WHATSAPP_SESSION_PATH` env variable
3. Playwright browser installed (`playwright install chromium`)

**First-time setup:**
```bash
# Run watcher once to authenticate
uv run python main.py --whatsapp --dry-run
# Scan QR code when browser opens
# Session will be saved for future use
```

---

## Timing Considerations

**send_whatsapp execution time:**
- Browser startup: ~5-10 seconds
- WhatsApp Web load: ~40 seconds
- Message send: ~3-5 seconds
- **Total: ~50-60 seconds per message**

**draft_whatsapp execution time:**
- File write: <1 second
- **Total: instant**

**Recommendation:** Use `draft_whatsapp` for unknown contacts or when speed matters, then batch-approve drafts.

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `WhatsApp session not found` | No authenticated session | Run `--whatsapp --dry-run` to authenticate |
| `Send button not found` | WhatsApp Web UI changed | Check watcher code for updated selectors |
| `Browser timeout` | Network issues or slow load | Increase wait time in watcher config |
| `Invalid phone number` | Wrong format | Ensure +[country_code][number] format |
| `Permission denied` | File system issue | Check vault path permissions |

---

## Best Practices

1. **Always draft first** for new/unknown contacts
2. **Validate phone numbers** before calling MCP tools (must include country code)
3. **Log every send action** to /Vault/Logs/YYYY-MM-DD.json
4. **Check DRY_RUN** before sending to real contacts
5. **Handle errors gracefully** - log failures and notify user
6. **Never retry failed sends** without human review
7. **Use context parameter** in draft_whatsapp to help human reviewers

---

## Security Considerations

- **Unknown contacts**: Always create draft first, never send directly
- **Financial messages**: Require explicit human approval before sending
- **Bulk sends**: Not supported - send one message at a time
- **Attachments**: Not currently supported by MCP server
- **Media**: Not currently supported - text only
