---
name: subscription-audit
description: Audit recurring subscription payments to identify wasteful spending. Use when PROMPT_subscription_audit.md appears in /Plans, every Sunday night, or when user asks to audit subscriptions, check recurring payments, or find unused services. Reads bank transactions, detects recurring charges, flags unused/duplicate/expensive subscriptions, and creates cancellation approval requests.
---

# Subscription Audit

Audit recurring subscription payments to identify wasteful spending. Triggered every Sunday night or by `PROMPT_subscription_audit.md` appearing in `/Plans`.

## Workflow

1. **Read** bank transactions from `/Vault/Accounting/Current_Month.md`
2. **Detect** recurring subscription payments using keywords from `references/subscription-keywords.md`
3. **Analyze** each subscription for:
   - Usage activity in last 30 days
   - Cost increases (>20% vs previous months)
   - Duplicate functionality with other subscriptions
4. **Flag** problematic subscriptions with severity (high/medium/low)
5. **Write** audit report to `/Vault/Briefings/Subscription_Audit_{YYYY-MM-DD}.md` using template from `references/audit-template.md`
6. **Create** approval files in `/Pending_Approval/` for each cancellation suggestion
7. **Log** audit action to `/Vault/Logs/YYYY-MM-DD.json`
8. Output `<promise>TASK_COMPLETE</promise>`

## Subscription Detection

### Recurring Payment Patterns

A transaction is considered a subscription if:
- Same merchant name appears in multiple months
- Amount is consistent (within 10% variance)
- Frequency is monthly, quarterly, or annual
- Merchant matches known subscription keywords

### Detection Algorithm

```
For each transaction in Current_Month.md:
    1. Extract merchant name and amount
    2. Check if merchant matches subscription keywords
    3. Search previous months for same merchant
    4. If found 2+ times with similar amounts → recurring subscription
    5. Calculate frequency (monthly/quarterly/annual)
```

### Subscription Keywords

See `references/subscription-keywords.md` for complete list of known subscription services and their merchant name patterns.

**Common patterns:**
- Streaming: netflix, spotify, youtube, hulu, disney, apple music
- Software: adobe, microsoft, notion, slack, github, figma
- Cloud: aws, google cloud, azure, digitalocean, heroku
- Productivity: dropbox, evernote, todoist, asana, trello
- Communication: zoom, calendly, loom, slack

## Usage Activity Detection

To determine if a subscription has been used in the last 30 days:

1. **Check vault activity:**
   - Search `/Vault/Done/` for files mentioning the service
   - Search `/Vault/Logs/` for actions related to the service
   - Check `/Vault/Business_Goals.md` for active projects using the service

2. **Activity indicators:**
   - Files created/modified using the service
   - Log entries mentioning the service
   - References in completed tasks or plans

3. **No activity = unused:**
   - No mentions in Done/ folder (last 30 days)
   - No log entries (last 30 days)
   - Not mentioned in Business_Goals.md

**Example:**
```
Subscription: Adobe Creative Cloud ($54.99/month)
Activity check:
- Search Done/ for "adobe", "photoshop", "illustrator" → 0 results
- Search Logs/ for "adobe" → 0 results
- Check Business_Goals.md for design projects → None found
Result: UNUSED (flag for cancellation)
```

## Cost Increase Detection

To detect cost increases:

1. **Compare current month vs previous months:**
   - Read `/Vault/Accounting/` folder for previous month files
   - Find same merchant in previous months
   - Calculate percentage change

2. **Flag if increase >20%:**
   - Previous: $9.99/month
   - Current: $12.99/month
   - Increase: 30% → FLAG

3. **Note in audit report:**
   - Show old price vs new price
   - Calculate annual impact
   - Suggest review or cancellation

**Example:**
```
Subscription: Notion
Previous: $8/month (Jan-Feb)
Current: $10/month (Mar)
Increase: 25%
Annual impact: +$24/year
Recommendation: Review if still needed at new price
```

## Duplicate Functionality Detection

Identify subscriptions with overlapping functionality:

### Common Duplicates

| Category | Services | Recommendation |
|---|---|---|
| Cloud Storage | Dropbox + Google Drive + iCloud | Keep one |
| Video Conferencing | Zoom + Google Meet + Microsoft Teams | Keep one |
| Project Management | Asana + Trello + Notion | Keep one |
| Design Tools | Figma + Adobe XD + Sketch | Keep one |
| Note-taking | Notion + Evernote + OneNote | Keep one |
| Communication | Slack + Microsoft Teams + Discord | Keep one |

### Detection Logic

```
For each subscription:
    1. Identify category (storage, video, design, etc.)
    2. Find other subscriptions in same category
    3. If 2+ subscriptions in same category → flag as duplicate
    4. Recommend keeping the most-used one
```

**Example:**
```
Detected duplicates:
- Dropbox ($11.99/month) — last used 45 days ago
- Google Drive ($9.99/month) — used daily
- iCloud ($2.99/month) — used weekly

Recommendation: Cancel Dropbox (unused), keep Google Drive + iCloud
Potential savings: $143.88/year
```

## Severity Levels

Assign severity to each flagged subscription:

### High Severity (Immediate Action)
- Unused for 60+ days
- Cost increased >50%
- Clear duplicate with better alternative
- Annual cost >$500

### Medium Severity (Review Recommended)
- Unused for 30-60 days
- Cost increased 20-50%
- Possible duplicate functionality
- Annual cost $100-$500

### Low Severity (Monitor)
- Light usage (1-2 times/month)
- Cost increased 10-20%
- Overlapping features but different use cases
- Annual cost <$100

## Audit Report Format

See `references/audit-template.md` for complete template.

**Report structure:**
```markdown
# Subscription Audit — {Date}

## Executive Summary
- Total subscriptions: {count}
- Total monthly cost: ${amount}
- Flagged for review: {count}
- Potential savings: ${amount}/year

## Flagged Subscriptions

### High Severity ({count})
[List with details]

### Medium Severity ({count})
[List with details]

### Low Severity ({count})
[List with details]

## Active Subscriptions (No Issues)
[List of healthy subscriptions]

## Recommendations
[Prioritized action items]
```

## Cancellation Approval Files

For each flagged subscription, create an approval file in `/Pending_Approval/`:

**Format:**
```markdown
---
type: subscription_cancellation
subscription: {service_name}
monthly_cost: {amount}
annual_savings: {amount}
severity: {high|medium|low}
created: {iso_timestamp}
status: awaiting_approval
---

# Subscription Cancellation: {Service Name}

## Subscription Details
**Service:** {service_name}
**Monthly Cost:** ${amount}
**Annual Cost:** ${annual_amount}
**Last Charged:** {date}

## Why Cancel?
{Reason: unused/duplicate/expensive}

## Usage Analysis
**Last Activity:** {date or "No activity found"}
**Activity in Last 30 Days:** {count} mentions in vault
**Activity in Last 60 Days:** {count} mentions in vault

## Financial Impact
**Monthly Savings:** ${amount}
**Annual Savings:** ${annual_amount}

## To Approve
Move this file to /Approved folder to proceed with cancellation.

## To Reject
Move this file to /Rejected folder to keep subscription.

---
*Awaiting human decision*
```

**File naming:** `APPROVAL_cancel_{service}_{YYYY-MM-DD}.md`

**Examples:**
- `APPROVAL_cancel_netflix_20260309.md`
- `APPROVAL_cancel_adobe_20260309.md`
- `APPROVAL_cancel_dropbox_20260309.md`

## Logging Format

Log audit action to `/Vault/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-09T20:00:00Z",
  "action_type": "subscription_audit",
  "total_subscriptions": 12,
  "flagged_subscriptions": 4,
  "high_severity": 2,
  "medium_severity": 1,
  "low_severity": 1,
  "potential_annual_savings": 876.00,
  "audit_file": "Subscription_Audit_2026-03-09.md",
  "approval_files_created": [
    "APPROVAL_cancel_netflix_20260309.md",
    "APPROVAL_cancel_adobe_20260309.md"
  ]
}
```

## Example Scenarios

**Scenario 1: Unused Netflix subscription**
```
Detection: Netflix charge $15.99/month found in Current_Month.md
Activity check: Search Done/ and Logs/ for "netflix" → 0 results in last 60 days
Severity: High (unused 60+ days)
Action: Create APPROVAL_cancel_netflix_20260309.md in /Pending_Approval/
Potential savings: $191.88/year
```

**Scenario 2: Adobe price increase**
```
Detection: Adobe Creative Cloud $54.99/month (was $49.99 last month)
Cost increase: 10% ($5/month)
Activity check: Used 3 times in last 30 days
Severity: Low (price increase <20%, still used)
Action: Note in audit report, no cancellation approval needed
Recommendation: Monitor for further increases
```

**Scenario 3: Duplicate cloud storage**
```
Detection: Dropbox ($11.99) + Google Drive ($9.99) + iCloud ($2.99)
Category: Cloud storage (3 services)
Activity check:
- Dropbox: 0 mentions in 45 days
- Google Drive: 15 mentions in 30 days
- iCloud: 8 mentions in 30 days
Severity: High (clear duplicate, Dropbox unused)
Action: Create APPROVAL_cancel_dropbox_20260309.md
Potential savings: $143.88/year
```

## References

- `references/subscription-keywords.md` — Complete list of subscription services and merchant name patterns
- `references/audit-template.md` — Full template for audit report output

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
