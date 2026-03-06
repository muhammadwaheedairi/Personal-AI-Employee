---
name: calendar-scheduler
description: Schedule client meetings and create reminders using Google Calendar. Use when user asks to schedule meeting, check availability, create reminder, or get upcoming events. Always checks availability before scheduling, routes meeting creation to human approval, and integrates with CEO briefing for upcoming events.
---

# Calendar Scheduler

Schedule client meetings and create reminders using Google Calendar via MCP tools. Handles meeting requests from WhatsApp/email, availability checking, invoice follow-up reminders, and event fetching for CEO briefings.

## Workflow

### Meeting Scheduling Workflow

1. **Receive** meeting request (from WhatsApp, email, or user prompt)
2. **Extract** meeting details (date, time, duration, attendee)
3. **Check availability** using `check_availability` MCP tool
4. **Find free slot** if requested time is busy
5. **Create approval request** in `/Pending_Approval/` with meeting details
6. **Wait** for human to move file to `/Approved/`
7. **Call** `create_event` MCP tool
8. **Log** action to `/Vault/Logs/YYYY-MM-DD.json`
9. **Move** approval file to `/Done/`
10. Output `<promise>TASK_COMPLETE</promise>`

### Reminder Creation Workflow

1. **Receive** reminder request (invoice follow-up, task deadline)
2. **Calculate** reminder datetime
3. **Call** `create_reminder` MCP tool (no approval needed)
4. **Log** action to `/Vault/Logs/YYYY-MM-DD.json`
5. Output `<promise>TASK_COMPLETE</promise>`

### Upcoming Events Workflow (for CEO Briefing)

1. **Call** `get_events` with `days_ahead: 7`
2. **Parse** response for upcoming meetings
3. **Add** to briefing under `## Upcoming This Week` section
4. Output `<promise>TASK_COMPLETE</promise>`

## MCP Tools

See `references/mcp-tools.md` for complete tool documentation.

### create_event

**Purpose:** Create a Google Calendar event for client meetings or project deadlines

**Parameters:**
- `title` (string, required) — Event title
- `start_datetime` (string, required) — Start datetime ISO format: `2026-03-10T10:00:00`
- `end_datetime` (string, required) — End datetime ISO format: `2026-03-10T11:00:00`
- `description` (string, optional) — Event description or agenda
- `attendee_email` (string, optional) — Client email to invite

**Returns:** Event link, event ID

**Security:** ALWAYS require human approval before calling this tool.

**Example:**
```python
result = mcp_call("create_event", {
    "title": "Client Meeting - Acme Corp",
    "start_datetime": "2026-03-10T10:00:00",
    "end_datetime": "2026-03-10T11:00:00",
    "description": "Discuss Q2 project requirements",
    "attendee_email": "client@acme.com"
})
```

### get_events

**Purpose:** Get upcoming calendar events for CEO Briefing or schedule overview

**Parameters:**
- `days_ahead` (integer, optional) — How many days ahead to fetch (default: 7)
- `max_results` (integer, optional) — Max number of events to return (default: 10)

**Returns:** List of upcoming events with titles and start times

**Example:**
```python
result = mcp_call("get_events", {
    "days_ahead": 7,
    "max_results": 10
})
```

### check_availability

**Purpose:** Check free/busy slots before scheduling a meeting

**Parameters:**
- `date` (string, required) — Date to check availability: `2026-03-10`
- `duration_minutes` (integer, optional) — Meeting duration in minutes (default: 60)

**Returns:** Busy slots or confirmation that day is free

**Example:**
```python
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 60
})
```

### create_reminder

**Purpose:** Create a reminder event for invoice follow-ups or task deadlines

**Parameters:**
- `title` (string, required) — Reminder title
- `remind_at` (string, required) — Reminder datetime ISO format: `2026-03-17T09:00:00`
- `note` (string, optional) — Additional note for the reminder

**Returns:** Reminder link

**Security:** Does NOT require approval (non-destructive, 15-minute calendar block)

**Example:**
```python
result = mcp_call("create_reminder", {
    "title": "Follow up on Acme Corp invoice",
    "remind_at": "2026-03-17T09:00:00",
    "note": "Invoice INV/2026/0042 - $5,000 - 7 days overdue"
})
```

## Security Rules

### Meeting Creation (CRITICAL)

**ALWAYS check availability before creating meeting.**

**Workflow:**
1. Call `check_availability` first
2. If busy, find alternative slot or ask user
3. Create approval request in `/Pending_Approval/`
4. Wait for human approval
5. Only then call `create_event`

**NEVER call `create_event` without approval.**

### Reminder Creation

**Reminders do NOT require approval** (non-destructive, just a 15-minute calendar block).

**Safe to call directly:**
- Invoice follow-up reminders
- Task deadline reminders
- Project milestone reminders

### Business Hours

**Timezone:** Asia/Karachi (PKT)  
**Business Hours:** 9:00 AM - 6:00 PM PKT  
**Lunch Break:** 1:00 PM - 2:00 PM PKT (avoid scheduling)

**When suggesting meeting times:**
- Default to business hours
- Avoid lunch break
- Prefer morning slots (10 AM - 12 PM)
- Avoid Fridays after 4 PM

### DRY_RUN Mode

**ALWAYS check DRY_RUN mode before calling MCP tools.**

When `DRY_RUN=true`, all MCP calls return simulation messages.

### Logging

**ALWAYS log every calendar action to `/Vault/Logs/YYYY-MM-DD.json`**

## Meeting Approval File Format

When creating meeting approval request in `/Pending_Approval/`:

```markdown
---
type: meeting_approval
title: {meeting_title}
date: {date}
start_time: {start_time}
end_time: {end_time}
attendee: {attendee_email}
created: {iso_timestamp}
status: awaiting_approval
---

# Meeting Approval: {Meeting Title}

## Meeting Details
**Title:** {meeting_title}
**Date:** {date}
**Time:** {start_time} - {end_time} PKT
**Duration:** {duration} minutes
**Attendee:** {attendee_email}

## Availability Check
{availability_check_result}

## Agenda
{description or "To be discussed"}

## Action
This will create a Google Calendar event and send invitation to attendee.

## To Approve
Move this file to /Approved folder to create meeting.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before creating calendar event*
```

**File naming:** `APPROVAL_meeting_{client_slug}_{YYYY-MM-DD}.md`

## Invoice Follow-up Reminders

Automatically create reminders for overdue invoices (7+ days).

**Trigger:** When `odoo-accounting` skill detects unpaid invoice >7 days old

**Workflow:**
1. Detect overdue invoice from Odoo
2. Calculate reminder date (7 days after invoice date)
3. Call `create_reminder` with invoice details
4. Log reminder creation

**Example:**
```python
# Invoice INV/2026/0042 is 7 days overdue
result = mcp_call("create_reminder", {
    "title": "Follow up: Acme Corp invoice",
    "remind_at": "2026-03-17T09:00:00",
    "note": "Invoice INV/2026/0042 - $5,000 - 7 days overdue. Contact: client@acme.com"
})
```

## CEO Briefing Integration

Every Monday, the `daily-briefing` skill calls `get_events` to populate upcoming events section.

**Integration workflow:**
1. Daily-briefing skill triggers on Monday 8 AM
2. Calls `get_events` with `days_ahead: 7`
3. Parses response for upcoming meetings
4. Adds to briefing under `## Upcoming This Week`

**Briefing format:**
```markdown
## Upcoming This Week

### Monday, March 10
- 10:00 AM - Client Meeting - Acme Corp
- 2:00 PM - Project Review - Beta Inc

### Wednesday, March 12
- 11:00 AM - Proposal Discussion - Gamma LLC

### Friday, March 14
- 3:00 PM - Weekly Team Sync
```

## Example Scenarios

**Scenario 1: Meeting request from WhatsApp**
```
Input: WHATSAPP_20260306_120000.md
Content: "Can we schedule a meeting next Monday at 10 AM?"
Sender: client@acme.com

Action:
1. Extract details: Monday (2026-03-10), 10:00 AM, 60 min default
2. Call check_availability for 2026-03-10
3. Result: "10:00 AM - 11:00 AM is free"
4. Create APPROVAL_meeting_acme_20260310.md in /Pending_Approval/
5. Wait for human approval
6. Human moves to /Approved/
7. Call create_event MCP tool
8. Log meeting_created action
9. Move approval file to /Done/
```

**Scenario 2: Meeting request with conflict**
```
Input: EMAIL_20260306_140000_Meeting_request.md
Content: "Let's meet on March 10 at 2 PM"
Sender: newclient@example.com

Action:
1. Extract details: 2026-03-10, 2:00 PM
2. Call check_availability for 2026-03-10
3. Result: "Busy 2:00 PM - 3:00 PM (existing meeting)"
4. Suggest alternative: "3:00 PM - 4:00 PM is free"
5. Create approval request with note about conflict
6. Wait for human to decide (approve alternative or reject)
```

**Scenario 3: Invoice follow-up reminder**
```
Input: Odoo detects invoice INV/2026/0042 is 7 days overdue
Amount: $5,000
Client: Acme Corp

Action:
1. Calculate reminder date: Today + 0 days (immediate)
2. Call create_reminder with invoice details
3. Reminder created for 9:00 AM today
4. Log reminder_created action
5. No approval needed (reminders are non-destructive)
```

**Scenario 4: CEO briefing upcoming events**
```
Input: PROMPT_daily_briefing.md in /Plans/ (Monday 8 AM)

Action:
1. Daily-briefing skill triggers
2. Calls get_events with days_ahead: 7
3. Receives list of 5 upcoming events
4. Formats events by day
5. Adds to briefing under ## Upcoming This Week
```

## Error Handling

**Authentication failed:**
```
Error: Calendar authentication failed
Action: Check token.pickle exists, re-authenticate if needed
```

**Date/time format error:**
```
Error: Invalid datetime format
Action: Ensure ISO format: 2026-03-10T10:00:00
```

**Busy slot conflict:**
```
Result: Busy 10:00 AM - 11:00 AM
Action: Suggest alternative time, create approval with note
```

**DRY_RUN active:**
```
Response: [DRY RUN] Would create event: ...
Action: Log simulation, move files, do NOT wait for real response
```

## References

- `references/mcp-tools.md` — Complete MCP tool documentation with parameters, returns, examples
- `references/meeting-workflow.md` — Step-by-step meeting scheduling workflow with approval templates

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
