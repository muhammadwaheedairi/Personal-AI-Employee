# Meeting Scheduling Workflow

Step-by-step workflow for scheduling client meetings with human approval.

## Complete Workflow

```
Meeting Request
    ↓
Extract Meeting Details
    ↓
Check Availability
    ↓
Find Free Slot (if needed)
    ↓
Create Approval Request → /Pending_Approval/
    ↓
Wait for Human Decision
    ↓
Human Moves to /Approved/
    ↓
Call create_event MCP Tool
    ↓
Log Action
    ↓
Move Files to /Done/
    ↓
TASK_COMPLETE
```

## Step-by-Step Instructions

### Step 1: Receive Meeting Request

Meeting requests can come from:
- WhatsApp message: "Can we schedule a meeting next Monday?"
- Email: "Let's meet on March 10 at 10 AM"
- User prompt: "Schedule meeting with Acme Corp"

**Extract information:**
- Date (or relative: "next Monday", "tomorrow")
- Time (or default to 10 AM)
- Duration (or default to 60 minutes)
- Attendee email
- Meeting purpose/agenda

### Step 2: Parse Date and Time

**Convert relative dates:**
```
"next Monday" → Calculate next Monday's date → 2026-03-10
"tomorrow" → Calculate tomorrow's date → 2026-03-07
"March 15" → 2026-03-15
```

**Convert time to 24-hour format:**
```
"10 AM" → 10:00
"2:30 PM" → 14:30
"5 PM" → 17:00
```

**Format as ISO datetime:**
```
Date: 2026-03-10
Time: 10:00
→ 2026-03-10T10:00:00
```

**Calculate end time:**
```
Start: 2026-03-10T10:00:00
Duration: 60 minutes
End: 2026-03-10T11:00:00
```

### Step 3: Check Availability

**ALWAYS check availability before creating approval request.**

```python
# Check if requested time is free
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 60
})

# Parse response
if "fully free" in result:
    availability_status = "free"
elif "Busy slots" in result:
    availability_status = "busy"
    # Extract busy slots from response
```

**Decision:**
- Time is free → Proceed to Step 5
- Time is busy → Proceed to Step 4

### Step 4: Find Alternative Slot (if busy)

If requested time is busy, suggest alternatives:

**Strategy:**
1. Parse busy slots from availability check
2. Find gaps between busy slots
3. Suggest next available slot within business hours
4. Prefer morning slots (10 AM - 12 PM)

**Example:**
```
Requested: 2026-03-10 at 2:00 PM (60 min)
Busy: 2:00 PM - 3:00 PM

Alternatives:
- 10:00 AM - 11:00 AM (morning slot)
- 3:00 PM - 4:00 PM (right after busy slot)
- 4:00 PM - 5:00 PM (late afternoon)
```

**Note in approval request:**
```
Requested time (2:00 PM) is busy. Suggested alternatives:
- 10:00 AM - 11:00 AM
- 3:00 PM - 4:00 PM
```

### Step 5: Create Approval Request

**CRITICAL: Never call create_event without approval.**

Create approval file in `/Pending_Approval/`:

**File naming:** `APPROVAL_meeting_{client_slug}_{YYYY-MM-DD}.md`

**Template:**
```markdown
---
type: meeting_approval
title: Client Meeting - Acme Corp
date: 2026-03-10
start_time: 10:00
end_time: 11:00
attendee: client@acme.com
created: 2026-03-06T14:30:00Z
status: awaiting_approval
source_file: WHATSAPP_20260306_120000.md
---

# Meeting Approval: Client Meeting - Acme Corp

## Meeting Details
**Title:** Client Meeting - Acme Corp
**Date:** Monday, March 10, 2026
**Time:** 10:00 AM - 11:00 AM PKT
**Duration:** 60 minutes
**Attendee:** client@acme.com

## Availability Check
✅ 10:00 AM - 11:00 AM is free

## Agenda
Discuss Q2 project requirements and timeline

## Action
This will create a Google Calendar event and send invitation to client@acme.com.

## To Approve
Move this file to /Approved folder to create meeting.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before creating calendar event*
```

### Step 6: Wait for Human Decision

**DO NOT proceed until human acts.**

Human will:
1. Review meeting details
2. Verify availability
3. Confirm attendee email
4. Make decision:
   - Move to `/Approved/` → Execute
   - Move to `/Rejected/` → Cancel
   - Leave in `/Pending_Approval/` → Still waiting

**Important:** Do NOT check repeatedly or retry. Wait for file to appear in `/Approved/`.

### Step 7: Execute Meeting Creation

**When file appears in `/Approved/`:**

1. Read approval file to get details
2. Call create_event MCP tool
3. Handle response

```python
# Read approval file
approval_data = read_approval_file("/Approved/APPROVAL_meeting_acme_20260310.md")

# Call MCP tool
result = mcp_call("create_event", {
    "title": approval_data["title"],
    "start_datetime": f"{approval_data['date']}T{approval_data['start_time']}:00",
    "end_datetime": f"{approval_data['date']}T{approval_data['end_time']}:00",
    "description": approval_data.get("agenda", ""),
    "attendee_email": approval_data.get("attendee")
})

# Parse response
if "Event created" in result:
    # Extract event link and ID
    event_link = extract_link(result)
    event_id = extract_id(result)
    status = "success"
else:
    # Handle error
    status = "error"
    error_message = result
```

### Step 8: Log Action

**Always log to `/Vault/Logs/YYYY-MM-DD.json`:**

**Success log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "calendar_meeting_created",
  "title": "Client Meeting - Acme Corp",
  "date": "2026-03-10",
  "start_time": "10:00",
  "end_time": "11:00",
  "attendee": "client@acme.com",
  "event_link": "https://calendar.google.com/calendar/event?eid=...",
  "event_id": "abc123xyz",
  "approval_file": "APPROVAL_meeting_acme_20260310.md",
  "dry_run": false
}
```

**Error log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "calendar_meeting_failed",
  "title": "Client Meeting - Acme Corp",
  "date": "2026-03-10",
  "status": "error",
  "error_message": "Invalid attendee email",
  "approval_file": "APPROVAL_meeting_acme_20260310.md"
}
```

### Step 9: Move Files to /Done/

After successful execution:

1. Move approval file from `/Approved/` to `/Done/`
2. Move source file (if any) to `/Done/`
3. Update Dashboard.md with meeting scheduled

**Example:**
```
/Approved/APPROVAL_meeting_acme_20260310.md → /Done/APPROVAL_meeting_acme_20260310.md
/In_Progress/WHATSAPP_20260306_120000.md → /Done/WHATSAPP_20260306_120000.md
```

### Step 10: Complete

Output: `<promise>TASK_COMPLETE</promise>`

---

## Meeting Approval Templates

### Template 1: Standard Meeting

```markdown
---
type: meeting_approval
title: {meeting_title}
date: {YYYY-MM-DD}
start_time: {HH:MM}
end_time: {HH:MM}
attendee: {email}
created: {iso_timestamp}
status: awaiting_approval
---

# Meeting Approval: {Meeting Title}

## Meeting Details
**Title:** {meeting_title}
**Date:** {day_name}, {month} {day}, {year}
**Time:** {start_time} - {end_time} PKT
**Duration:** {duration} minutes
**Attendee:** {email}

## Availability Check
✅ {start_time} - {end_time} is free

## Agenda
{agenda or "To be discussed"}

## Action
This will create a Google Calendar event and send invitation to {email}.

## To Approve
Move this file to /Approved folder to create meeting.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before creating calendar event*
```

### Template 2: Meeting with Conflict

```markdown
---
type: meeting_approval
title: {meeting_title}
date: {YYYY-MM-DD}
start_time: {HH:MM}
end_time: {HH:MM}
attendee: {email}
created: {iso_timestamp}
status: awaiting_approval
conflict: true
---

# Meeting Approval: {Meeting Title} ⚠️ TIME CONFLICT

## Meeting Details
**Title:** {meeting_title}
**Date:** {day_name}, {month} {day}, {year}
**Requested Time:** {requested_time} - {requested_end} PKT
**Duration:** {duration} minutes
**Attendee:** {email}

## Availability Check
⚠️ Requested time ({requested_time}) is busy

**Busy slots:**
- {busy_slot_1}
- {busy_slot_2}

**Suggested alternatives:**
- {alternative_1}
- {alternative_2}
- {alternative_3}

## Agenda
{agenda}

## Action
Choose one of the suggested times or reject to propose different time to client.

## To Approve
Edit this file with chosen time, then move to /Approved folder.

## To Reject
Move this file to /Rejected folder to propose different time.

---
*Awaiting human decision on meeting time*
```

### Template 3: Urgent Meeting

```markdown
---
type: meeting_approval
title: {meeting_title}
date: {YYYY-MM-DD}
start_time: {HH:MM}
end_time: {HH:MM}
attendee: {email}
created: {iso_timestamp}
status: awaiting_approval
urgent: true
---

# ⚠️ URGENT Meeting Approval: {Meeting Title}

## Meeting Details
**Title:** {meeting_title}
**Date:** {day_name}, {month} {day}, {year} ⚠️ {urgency_note}
**Time:** {start_time} - {end_time} PKT
**Duration:** {duration} minutes
**Attendee:** {email}

## Urgency Context
{why_urgent}

## Availability Check
{availability_status}

## Agenda
{agenda}

## Action
This will create a Google Calendar event and send invitation to {email}.

## To Approve
Move this file to /Approved folder to create meeting immediately.

## To Reject
Move this file to /Rejected folder to decline.

---
**⚠️ URGENT: Please review and decide as soon as possible**
```

---

## Error Handling

### Error: Invalid Datetime Format

**Scenario:** User says "March 10 at 10am" but format is wrong

**Action:**
1. Parse user input carefully
2. Convert to ISO format: 2026-03-10T10:00:00
3. Verify format before calling MCP

### Error: Busy Slot Conflict

**Scenario:** Requested time is busy

**Action:**
1. Parse busy slots from check_availability response
2. Find alternative free slots
3. Create approval request with alternatives
4. Let human decide

### Error: Authentication Failed

**Scenario:** "Calendar authentication failed"

**Action:**
1. Do NOT retry
2. Log error
3. Move approval file back to /Pending_Approval/ with error note
4. Escalate to human to check token.pickle

### Error: DRY_RUN Active

**Scenario:** Response is "[DRY RUN] Would create event: ..."

**Action:**
1. This is NOT an error — it's expected behavior in DRY_RUN mode
2. Log simulation
3. Move files to /Done/ as if successful
4. Do NOT wait for actual event creation

---

## Rejection Handling

**When file appears in `/Rejected/`:**

1. Read rejection file (may have human notes)
2. Cancel meeting creation (do NOT call create_event)
3. Log rejection to /Vault/Logs/
4. Move rejection file to /Done/
5. Notify user of cancellation

**Rejection log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "calendar_meeting_rejected",
  "title": "Client Meeting - Acme Corp",
  "date": "2026-03-10",
  "reason": "human_rejected",
  "approval_file": "APPROVAL_meeting_acme_20260310.md"
}
```

---

## Integration with Other Skills

### WhatsApp Triage → Calendar Scheduler

```
WHATSAPP_*.md in /Needs_Action/
    ↓
whatsapp-triage detects "meeting" keyword
    ↓
Creates PLAN_WHATSAPP_meeting.md
    ↓
Plan executes: Load calendar-scheduler skill
    ↓
calendar-scheduler checks availability
    ↓
Creates approval request
    ↓
Human approves
    ↓
Meeting created in Google Calendar
```

### Email Triage → Calendar Scheduler

```
EMAIL_*.md in /Needs_Action/
    ↓
gmail-triage detects meeting request
    ↓
Creates PLAN_EMAIL_meeting.md
    ↓
Plan executes: Load calendar-scheduler skill
    ↓
calendar-scheduler checks availability
    ↓
Creates approval request
    ↓
Human approves
    ↓
Meeting created in Google Calendar
```

### Daily Briefing → Calendar Scheduler

```
PROMPT_daily_briefing.md in /Plans/
    ↓
daily-briefing skill triggers
    ↓
Calls calendar-scheduler for upcoming events
    ↓
calendar-scheduler calls get_events
    ↓
Returns upcoming meetings
    ↓
daily-briefing adds to briefing report
```

---

## Best Practices

1. **Always check availability** before creating approval request
2. **Always create approval request** — never call create_event directly
3. **Always log actions** to /Vault/Logs/
4. **Always respect DRY_RUN mode** — check before executing
5. **Always move files to /Done/** after completion
6. **Never retry failed operations** without human intervention
7. **Prefer morning slots** (10 AM - 12 PM) when suggesting times
8. **Avoid lunch break** (1 PM - 2 PM) when scheduling
9. **Default to 60 minutes** if duration not specified
10. **Always include attendee email** if available

---

## Quick Reference

**Check availability:**
```python
result = mcp_call("check_availability", {
    "date": "2026-03-10",
    "duration_minutes": 60
})
```

**Create meeting (after approval):**
```python
result = mcp_call("create_event", {
    "title": "Client Meeting - Acme Corp",
    "start_datetime": "2026-03-10T10:00:00",
    "end_datetime": "2026-03-10T11:00:00",
    "description": "Discuss Q2 requirements",
    "attendee_email": "client@acme.com"
})
```

**Get upcoming events:**
```python
result = mcp_call("get_events", {
    "days_ahead": 7,
    "max_results": 10
})
```

**Create reminder:**
```python
result = mcp_call("create_reminder", {
    "title": "Follow up: Acme Corp invoice",
    "remind_at": "2026-03-17T09:00:00",
    "note": "Invoice overdue 7 days"
})
```
