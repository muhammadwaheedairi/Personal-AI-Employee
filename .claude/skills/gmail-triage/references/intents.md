# Email Intent Detection

Classify incoming emails by intent to determine the appropriate action.

## Intent Categories

### 1. Action Required
**Indicators:**
- Questions directed at you
- Requests for information, documents, or decisions
- Meeting invitations requiring response
- Tasks assigned to you
- Deadlines mentioned

**Keywords:** "can you", "could you", "please send", "need your", "waiting for", "by [date]", "RSVP"

**Action:** Create reply plan in /Plans/

---

### 2. Information Only
**Indicators:**
- Newsletters, updates, announcements
- CC'd on threads not requiring your input
- Automated notifications (GitHub, Jira, etc.)
- Marketing emails

**Keywords:** "FYI", "for your information", "update:", "newsletter", "unsubscribe"

**Action:** Archive or move to /Done/

---

### 3. Urgent/High Priority
**Indicators:**
- Explicit urgency markers
- Time-sensitive requests
- Executive/client emails
- System alerts or critical issues

**Keywords:** "urgent", "asap", "critical", "important", "deadline", "emergency", "immediately"

**Action:** Flag to /Pending_Approval/ for immediate human review

---

### 4. Delegation Required
**Indicators:**
- Request outside your domain
- Better handled by another team member
- Requires specialized expertise

**Keywords:** "can someone", "who handles", "need help with"

**Action:** Create forward plan in /Plans/ with suggested recipient

---

### 5. Payment/Financial
**Indicators:**
- Invoice requests
- Payment confirmations
- Financial reports
- Budget discussions

**Keywords:** "invoice", "payment", "receipt", "billing", "quote", "$", "USD", "EUR"

**Action:** Always flag to /Pending_Approval/ — financial matters require human oversight

---

### 6. Meeting/Calendar
**Indicators:**
- Meeting invitations
- Schedule requests
- Calendar updates

**Keywords:** "meeting", "call", "schedule", "calendar", "available", "time to meet"

**Action:** Create reply plan with availability check

---

### 7. Spam/Low Priority
**Indicators:**
- Unsolicited marketing
- Obvious spam
- Irrelevant mass emails

**Keywords:** "click here", "limited time offer", "act now", "congratulations you won"

**Action:** Archive immediately, log as spam

---

## Multi-Intent Emails

Some emails may have multiple intents. Prioritize in this order:
1. Payment/Financial (always human review)
2. Urgent/High Priority
3. Action Required
4. Delegation Required
5. Meeting/Calendar
6. Information Only
7. Spam/Low Priority

## Context Clues

Beyond keywords, consider:
- **Sender domain:** Client domains = higher priority
- **Thread history:** Ongoing conversations may be more urgent
- **Time of day:** Late-night emails may indicate urgency
- **Subject line:** ALL CAPS, multiple exclamation marks
