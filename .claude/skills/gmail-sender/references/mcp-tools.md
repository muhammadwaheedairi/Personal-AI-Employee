# Email MCP Tools Reference

Complete guide to using the email MCP server tools for sending emails and creating drafts.

## Available Tools

### send_email

Send an email immediately via Gmail.

**Parameters:**
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject line
- `body` (string, required): Email body content (plain text)

**Returns:**
- Success: `"Email sent to {recipient}"`
- DRY_RUN: `"[DRY RUN] Would send_email to {recipient}: {subject}"`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("send_email", {
    "to": "client@example.com",
    "subject": "Re: Project Update",
    "body": "Thank you for your email. The project is on track..."
})
```

---

### draft_email

Create a Gmail draft without sending.

**Parameters:**
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject line
- `body` (string, required): Email body content (plain text)

**Returns:**
- Success: `"Draft created for {recipient}"`
- DRY_RUN: `"[DRY RUN] Would draft_email to {recipient}: {subject}"`
- Error: `"Error: {error_message}"`

**Example:**
```python
result = await mcp_call("draft_email", {
    "to": "client@example.com",
    "subject": "Re: Project Update",
    "body": "Thank you for your email. The project is on track..."
})
```

---

## DRY_RUN Mode

When `DRY_RUN=true` in `.env`, both tools return simulation messages instead of actually sending/drafting:

```
[DRY RUN] Would send_email to client@example.com: Re: Project Update
```

**Always check DRY_RUN status before sending to production contacts.**

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Gmail token not found` | Token file missing | Run `uv run python main.py --gmail --dry-run` first |
| `Token expired` | Credentials need refresh | MCP server auto-refreshes; if fails, re-authenticate |
| `Invalid recipient` | Malformed email address | Validate email format before calling |
| `Permission denied` | Gmail API scope issue | Check SCOPES in gmail_watcher.py |

---

## Best Practices

1. **Always draft first** for new/unknown contacts
2. **Validate email addresses** before calling MCP tools
3. **Log every send action** to /Vault/Logs/YYYY-MM-DD.json
4. **Check DRY_RUN** before sending to real contacts
5. **Handle errors gracefully** - log failures and notify user
6. **Never retry failed sends** without human review

---

## Security Considerations

- **Unknown contacts**: Always create draft first, never send directly
- **Financial emails**: Require explicit human approval before sending
- **Bulk sends**: Not supported - send one email at a time
- **Attachments**: Not currently supported by MCP server
- **HTML emails**: Not currently supported - plain text only
