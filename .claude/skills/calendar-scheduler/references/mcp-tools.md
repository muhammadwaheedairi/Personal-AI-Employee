# Calendar MCP Tools Reference

Complete documentation for all Google Calendar MCP tools available via `mcp_servers/calendar_mcp.py`.

## Connection Details

**MCP Server:** `mcp_servers/calendar_mcp.py`  
**Protocol:** Google Calendar API v3  
**Authentication:** OAuth 2.0 via token.pickle (same as Gmail)  
**Timezone:** Asia/Karachi (PKT)  
**DRY_RUN:** Respects `DRY_RUN=true` in `.env` — returns simulation messages instead of executing

## Tool: create_event

**Purpose:** Create a Google Calendar event for client meetings or project deadlines

**Parameters:**
```json
{
  "title": "string (required) - Event title",
  "start_datetime": "string (required) - Start datetime ISO format: 2026-03-10T10:00:00",
  "end_datetime": "string (required) - End datetime ISO format: 2026-03-10T11:00:00",
  "description": "string (optional) - Event description or agenda",
  "attendee_email": "string (optional) - Client email to invite"
}
```

**Behavior:**
1. Creates event in primary Google Calendar
2. Sets timezone to Asia/Karachi
3. Sends invitation email to attendee if provided
4. Returns event link and ID

**Returns:**
```
Success:
"✅ Event created: Client Meeting - Acme Corp
Link: https://calendar.google.com/calendar/event?eid=...
Event ID: abc123xyz"

DRY_RUN:
"[DRY RUN] Would create event: Client Meeting - Acme Corp from 2026-03-10T10:00:00 to 2026-03-10T11:00:00"

Error:
"❌ Error creating event: [error details]"
```

**Security Warning:**
This tool creates an official calendar event and sends invitations. ALWAYS require human approval before calling.

**Example Usage:**
```python
# WRONG - Never call directly without approval
result = mcp_call("create_event", {
    "title": "Client Meeting - Acme Corp",
    "start_datetime": "2026-03-10T10:00:00",
    "end_datetime": "2026-03-10T11:00:00",
    "description": "Discuss Q2 project requirements",
    "attendee_email": "client@acme.com"
})

# CORRECT - Always create approval request first
# 1. Check availability
# 2. Create APPROVAL_meeting_acme_20260310.md in /Pending_Approval/
# 3. Wait for human to move to /Approved/
# 4. Then call create_event
```

**Implementation Details:**
- Uses Google Calendar API v3
- Timezone: Asia/Karachi (hardcoded)
- Sends email invitations via `sendUpdates='all'`
- Returns htmlLink for easy access

---

## Tool: get_events

**Purpose:** Get upcoming calendar events for CEO Briefing or schedule overview

**Parameters:**
```json
{
  "days_ahead": "integer (optional) - How many days ahead to fetch (default: 7)",
  "max_results": "integer (optional) - Max number of events to return (default: 10)"
}
```

**Behavior:**
1. Fetches events from now to `days_ahead` days in the future
2. Returns events sorted by start time
3. Includes event title and start datetime

**Returns:**
```
Success:
"📅 Upcoming events (next 7 days):

• Client Meeting - Acme Corp
  Start: 2026-03-10T10:00:00+05:00

• Project Review - Beta Inc
  Start: 2026-03-12T14:00:00+05:00

• Weekly Team Sync
  Start: 2026-03-14T15:00:00+05:00"

No events:
"No events in next 7 days"

Error:
"❌ Error fetching events: [error details]"
```

**Example Usage:**
```python
# Get next 7 days of events (for CEO briefing)
result = mcp_call("get_events", {
    "days_ahead": 7,
    "max_results": 10
})

# Get next 30 days of events
result = mcp_call("get_events", {
    "days_ahead": 30,
    "max_results": 20
})

# Get default (7 days, 10 events)
result = mcp_call("get_events", {})
```

**Use Cases:**
- Populate CEO briefing "Upcoming This Week" section
- Check schedule before proposing meeting times
- Generate weekly schedule overview
- Identify busy periods

**Implementation Details:**
- Uses Google Calendar API v3 events.list
- Filters by timeMin (now) and timeMax (now + days_ahead)
- Returns singleEvents=True (expands recurring events)
- Ordered by startTime

---

## Tool: check_availability

**Purpose:** Check free/busy slots before scheduling a meeting

**Parameters:**
```json
{
  "date": "string (required) - Date to check availability: 2026-03-10",
  "duration_minutes": "integer (optional) - Meeting duration in minutes (default: 60)"
}
```

**Behavior:**
1. Queries Google Calendar freebusy API for specified date
2. Returns list of busy time slots
3. Suggests scheduling in gaps of `duration_minutes` or more

**Returns:**
```
Fully free:
"✅ 2026-03-10 is fully free! You can schedule a 60-minute meeting anytime."

Has busy slots:
"📅 Busy slots on 2026-03-10:
• 2026-03-10T10:00:00Z → 2026-03-10T11:00:00Z
• 2026-03-10T14:00:00Z → 2026-03-10T15:30:00Z

Schedule meeting in any gap of 60+ minutes."

Error:
"❌ Error checking availability: [error details]"
```

**Example Usage:**
```python
# Check availability for 60-minute meeting
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 60
})

# Check availability for 30-minute meeting
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 30
})

# Check availability for 2-hour meeting
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 120
})
```

**Use Cases:**
- ALWAYS call before creating meeting approval request
- Find free slots when requested time is busy
- Suggest alternative meeting times
- Verify availability before confirming with client

**Implementation Details:**
- Uses Google Calendar API v3 freebusy.query
- Checks entire day (00:00 to 23:59)
- Returns busy slots in UTC
- Does NOT automatically suggest free slots (Claude should analyze gaps)

---

## Tool: create_reminder

**Purpose:** Create a reminder event for invoice follow-ups or task deadlines

**Parameters:**
```json
{
  "title": "string (required) - Reminder title",
  "remind_at": "string (required) - Reminder datetime ISO format: 2026-03-17T09:00:00",
  "note": "string (optional) - Additional note for the reminder"
}
```

**Behavior:**
1. Creates 15-minute calendar event at specified time
2. Adds "⏰ REMINDER:" prefix to title
3. Sets popup reminder at event time
4. Sets email reminder 30 minutes before

**Returns:**
```
Success:
"✅ Reminder created: Follow up on Acme Corp invoice
At: 2026-03-17T09:00:00
Link: https://calendar.google.com/calendar/event?eid=..."

DRY_RUN:
"[DRY RUN] Would create reminder: Follow up on Acme Corp invoice at 2026-03-17T09:00:00"

Error:
"❌ Error creating reminder: [error details]"
```

**Security:**
Reminders do NOT require approval (non-destructive, just a 15-minute calendar block).

**Example Usage:**
```python
# Invoice follow-up reminder
result = mcp_call("create_reminder", {
    "title": "Follow up: Acme Corp invoice",
    "remind_at": "2026-03-17T09:00:00",
    "note": "Invoice INV/2026/0042 - $5,000 - 7 days overdue. Contact: client@acme.com"
})

# Task deadline reminder
result = mcp_call("create_reminder", {
    "title": "Project deadline: Beta Inc website",
    "remind_at": "2026-03-20T09:00:00",
    "note": "Final delivery due March 22"
})

# Meeting preparation reminder
result = mcp_call("create_reminder", {
    "title": "Prepare for client meeting",
    "remind_at": "2026-03-10T09:00:00",
    "note": "Review proposal before 10 AM meeting"
})
```

**Use Cases:**
- Invoice follow-up reminders (7+ days overdue)
- Project deadline reminders
- Meeting preparation reminders
- Task completion reminders

**Implementation Details:**
- Creates 15-minute event (start to start+15min)
- Timezone: Asia/Karachi
- Popup reminder at event time (0 minutes)
- Email reminder 30 minutes before
- Title prefixed with "⏰ REMINDER:"

---

## Error Handling

**Authentication Errors:**
```
Error: Calendar authentication failed
```
**Action:** Check token.pickle exists at `watchers/token.pickle`, re-authenticate if needed

**Invalid Datetime Format:**
```
Error: time data '2026-03-10 10:00:00' does not match format
```
**Action:** Use ISO format without spaces: `2026-03-10T10:00:00`

**Event Creation Failed:**
```
Error: Invalid attendee email
```
**Action:** Verify email format, check if attendee email is valid

**Freebusy Query Failed:**
```
Error: Invalid date format
```
**Action:** Use date format YYYY-MM-DD (e.g., 2026-03-10)

**DRY_RUN Mode:**
```
Response: [DRY RUN] Would create event: ...
```
**Action:** Log simulation, proceed as if successful, do NOT wait for real response

---

## Datetime Format Guide

**ISO Format (required for all tools):**
```
2026-03-10T10:00:00
```

**Components:**
- `2026-03-10` — Date (YYYY-MM-DD)
- `T` — Separator (required)
- `10:00:00` — Time (HH:MM:SS)

**Examples:**
```
Morning meeting:   2026-03-10T10:00:00
Afternoon meeting: 2026-03-10T14:30:00
Evening reminder:  2026-03-10T17:00:00
```

**Timezone:**
All times are interpreted as Asia/Karachi (PKT) by the MCP server.

**Converting from user input:**
```
User says: "Monday at 10 AM"
→ Determine date: 2026-03-10 (next Monday)
→ Format: 2026-03-10T10:00:00

User says: "March 15 at 2:30 PM"
→ Format: 2026-03-15T14:30:00

User says: "Tomorrow at 9 AM"
→ Calculate tomorrow's date: 2026-03-07
→ Format: 2026-03-07T09:00:00
```

---

## Business Hours Reference

**Timezone:** Asia/Karachi (PKT)  
**Business Hours:** 9:00 AM - 6:00 PM PKT  
**Lunch Break:** 1:00 PM - 2:00 PM PKT (avoid scheduling)

**Preferred meeting times:**
- Morning: 10:00 AM - 12:00 PM
- Afternoon: 2:00 PM - 5:00 PM
- Avoid: Before 9 AM, after 6 PM, 1-2 PM lunch

**Default meeting durations:**
- Quick call: 30 minutes
- Standard meeting: 60 minutes
- Workshop/training: 120 minutes

---

## Security Best Practices

1. **ALWAYS check availability** before creating meeting approval request
2. **ALWAYS require approval** for meeting creation (never call create_event directly)
3. **Reminders do NOT require approval** (safe to call directly)
4. **ALWAYS log calendar actions** to /Vault/Logs/
5. **ALWAYS respect DRY_RUN mode** — check before executing
6. **NEVER schedule outside business hours** without explicit user request

---

## Credentials Configuration

**Location:** Same as Gmail (token.pickle)

**Required scopes:**
```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

**Authentication:**
Uses same OAuth flow as Gmail. Token stored at `watchers/token.pickle`.

**Re-authentication:**
If calendar access fails, re-run Gmail watcher to refresh token with calendar scopes.

---

## Testing with DRY_RUN

**Enable DRY_RUN mode:**
```bash
# In .env file
DRY_RUN=true
```

**Behavior:**
- All MCP calls return `[DRY RUN] Would ...` messages
- No actual calendar events created
- Safe for testing workflows without affecting production calendar

**Testing workflow:**
1. Set DRY_RUN=true
2. Test meeting scheduling workflow
3. Verify approval files created correctly
4. Verify logging works
5. Set DRY_RUN=false for production
