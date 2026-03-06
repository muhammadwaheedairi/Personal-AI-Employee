# Subscription Audit Report Template

Standard format for subscription audit output.

## File Format

**Filename:** `Subscription_Audit_YYYY-MM-DD.md`  
**Location:** `/Vault/Briefings/`

## Template Structure

```markdown
---
type: subscription_audit
date: {YYYY-MM-DD}
generated: {iso_timestamp}
total_subscriptions: {count}
flagged_subscriptions: {count}
potential_annual_savings: {amount}
---

# Subscription Audit — {Day}, {Month} {Date}, {Year}

## Executive Summary

**Total Subscriptions:** {count}  
**Total Monthly Cost:** ${amount}  
**Total Annual Cost:** ${amount}  
**Flagged for Review:** {count}  
**Potential Annual Savings:** ${amount}

{1-2 sentence overview of findings}

---

## Flagged Subscriptions

### High Severity ({count}) — Immediate Action Recommended

#### {Service Name 1}
- **Monthly Cost:** ${amount}
- **Annual Cost:** ${amount}
- **Last Charged:** {date}
- **Issue:** {Unused 60+ days | Cost increased 50%+ | Clear duplicate}
- **Last Activity:** {date or "No activity found"}
- **Recommendation:** Cancel immediately
- **Annual Savings:** ${amount}
- **Approval File:** `APPROVAL_cancel_{service}_{date}.md`

#### {Service Name 2}
- **Monthly Cost:** ${amount}
- **Annual Cost:** ${amount}
- **Last Charged:** {date}
- **Issue:** {issue description}
- **Last Activity:** {date or "No activity found"}
- **Recommendation:** {recommendation}
- **Annual Savings:** ${amount}
- **Approval File:** `APPROVAL_cancel_{service}_{date}.md`

**Total High Severity Savings:** ${amount}/year

---

### Medium Severity ({count}) — Review Recommended

#### {Service Name 1}
- **Monthly Cost:** ${amount}
- **Annual Cost:** ${amount}
- **Last Charged:** {date}
- **Issue:** {Unused 30-60 days | Cost increased 20-50% | Possible duplicate}
- **Last Activity:** {date}
- **Usage:** {usage_description}
- **Recommendation:** {recommendation}
- **Potential Savings:** ${amount}/year
- **Approval File:** `APPROVAL_cancel_{service}_{date}.md` (if applicable)

**Total Medium Severity Savings:** ${amount}/year

---

### Low Severity ({count}) — Monitor

#### {Service Name 1}
- **Monthly Cost:** ${amount}
- **Annual Cost:** ${amount}
- **Last Charged:** {date}
- **Issue:** {Light usage | Cost increased 10-20% | Minor overlap}
- **Last Activity:** {date}
- **Usage:** {usage_description}
- **Recommendation:** Monitor usage, consider downgrade
- **Note:** {additional context}

---

## Active Subscriptions (No Issues)

### Streaming ({count})
- **{Service Name}** — ${amount}/month — Used {count} times in last 30 days
- **{Service Name}** — ${amount}/month — Used {count} times in last 30 days

### Software & Productivity ({count})
- **{Service Name}** — ${amount}/month — Active project dependency
- **{Service Name}** — ${amount}/month — Daily use

### Cloud & Infrastructure ({count})
- **{Service Name}** — ${amount}/month — Production systems
- **{Service Name}** — ${amount}/month — Active development

### Other ({count})
- **{Service Name}** — ${amount}/month — {usage_note}

**Total Healthy Subscriptions Cost:** ${amount}/month (${amount}/year)

---

## Duplicate Functionality Analysis

### Cloud Storage
**Services:** {service1}, {service2}, {service3}  
**Total Cost:** ${amount}/month  
**Recommendation:** {recommendation}  
**Potential Savings:** ${amount}/year

### Video Conferencing
**Services:** {service1}, {service2}  
**Total Cost:** ${amount}/month  
**Recommendation:** {recommendation}  
**Potential Savings:** ${amount}/year

### {Category}
**Services:** {list}  
**Total Cost:** ${amount}/month  
**Recommendation:** {recommendation}  
**Potential Savings:** ${amount}/year

---

## Cost Increase Analysis

### Recent Price Increases

#### {Service Name}
- **Previous Price:** ${amount}/month
- **Current Price:** ${amount}/month
- **Increase:** {percentage}% (+${amount}/month)
- **Annual Impact:** +${amount}/year
- **Recommendation:** {recommendation}

#### {Service Name}
- **Previous Price:** ${amount}/month
- **Current Price:** ${amount}/month
- **Increase:** {percentage}% (+${amount}/month)
- **Annual Impact:** +${amount}/year
- **Recommendation:** {recommendation}

**Total Annual Impact of Price Increases:** +${amount}/year

---

## Recommendations

### Immediate Actions (High Priority)

1. **Cancel {Service Name}** — Unused for {days} days, save ${amount}/year
2. **Cancel {Service Name}** — Duplicate of {other_service}, save ${amount}/year
3. **Review {Service Name}** — Price increased {percentage}%, evaluate alternatives

### Review This Month (Medium Priority)

1. **Evaluate {Service Name}** — Light usage, consider downgrade
2. **Compare {Service1} vs {Service2}** — Overlapping features, consolidate
3. **Monitor {Service Name}** — Recent price increase, watch for further changes

### Long-term Optimization

1. **Annual billing** — Switch {service} to annual for {percentage}% discount
2. **Bundle services** — Combine {service1} + {service2} for savings
3. **Negotiate** — Contact {service} for enterprise/volume discount

---

## Financial Summary

| Category | Monthly | Annual |
|---|---|---|
| Current Total Cost | ${amount} | ${amount} |
| High Severity Savings | ${amount} | ${amount} |
| Medium Severity Savings | ${amount} | ${amount} |
| Low Severity Savings | ${amount} | ${amount} |
| **Potential New Total** | **${amount}** | **${amount}** |
| **Total Savings** | **${amount}** | **${amount}** |

**Savings Percentage:** {percentage}% reduction in subscription costs

---

## Next Steps

1. Review approval files in `/Pending_Approval/` folder
2. Approve cancellations for unused subscriptions
3. Contact services with price increases to negotiate or cancel
4. Consolidate duplicate services
5. Schedule next audit for {date}

---

## Approval Files Created

The following approval files have been created in `/Pending_Approval/`:

- `APPROVAL_cancel_{service1}_{date}.md` — ${amount}/year savings
- `APPROVAL_cancel_{service2}_{date}.md` — ${amount}/year savings
- `APPROVAL_cancel_{service3}_{date}.md` — ${amount}/year savings

**Total Potential Savings:** ${amount}/year

Move files to `/Approved/` to proceed with cancellations.

---

*Generated automatically by AI Employee on {date} at {time}*
```

## Section Guidelines

### Executive Summary
- Lead with total subscription count and cost
- Highlight flagged subscriptions and potential savings
- Keep to 2-3 sentences maximum
- Focus on actionable insights

**Example:**
```
**Total Subscriptions:** 15  
**Total Monthly Cost:** $287.85  
**Total Annual Cost:** $3,454.20  
**Flagged for Review:** 5  
**Potential Annual Savings:** $876.00

Found 2 unused subscriptions (Netflix, Adobe), 2 duplicates (Dropbox/Google Drive), and 1 significant price increase (Notion). Canceling flagged subscriptions would reduce annual costs by 25%.
```

### Flagged Subscriptions

**High Severity:**
- List subscriptions requiring immediate action
- Include all relevant details (cost, last activity, issue)
- Provide clear recommendation
- Reference approval file created

**Medium Severity:**
- List subscriptions worth reviewing
- Include usage context
- Suggest evaluation criteria
- May or may not have approval file

**Low Severity:**
- List subscriptions to monitor
- Note minor issues
- Provide context for keeping
- No approval files needed

### Active Subscriptions (No Issues)

Group by category for readability:
- Streaming
- Software & Productivity
- Cloud & Infrastructure
- Other

For each, note:
- Monthly cost
- Usage frequency or importance
- Why it's healthy (active use, business critical, etc.)

### Duplicate Functionality Analysis

Group subscriptions by category:
- Cloud Storage
- Video Conferencing
- Project Management
- Design Tools
- Note-taking
- Communication

For each group with duplicates:
- List all services in category
- Show total cost
- Recommend which to keep
- Calculate potential savings

### Cost Increase Analysis

List subscriptions with recent price increases:
- Show old vs new price
- Calculate percentage increase
- Show annual impact
- Recommend action (accept, negotiate, cancel)

### Recommendations

**Immediate Actions:**
- High-priority items requiring quick decision
- Clear action items with expected savings
- Numbered list for easy tracking

**Review This Month:**
- Medium-priority items for evaluation
- May require more analysis
- Less urgent than immediate actions

**Long-term Optimization:**
- Strategic improvements
- Opportunities for better pricing
- Process improvements

### Financial Summary

Table format showing:
- Current total cost (monthly and annual)
- Savings by severity level
- Potential new total after cancellations
- Total savings amount and percentage

### Next Steps

Actionable checklist:
1. Review approval files
2. Make cancellation decisions
3. Contact services if needed
4. Consolidate duplicates
5. Schedule next audit

## Tone Guidelines

- **Data-driven** — use specific numbers, not vague statements
- **Objective** — present facts, let user decide
- **Actionable** — every finding should have a clear recommendation
- **Respectful** — don't judge subscription choices, just present data
- **Concise** — respect reader's time, get to the point

## Example Audit Excerpt

```markdown
# Subscription Audit — Sunday, March 9, 2026

## Executive Summary

**Total Subscriptions:** 12  
**Total Monthly Cost:** $243.87  
**Total Annual Cost:** $2,926.44  
**Flagged for Review:** 4  
**Potential Annual Savings:** $587.88

Found 2 unused subscriptions (Netflix, Adobe Creative Cloud), 1 duplicate (Dropbox while using Google Drive), and 1 price increase (Notion +25%). Canceling flagged subscriptions would reduce annual costs by 20%.

---

## Flagged Subscriptions

### High Severity (2) — Immediate Action Recommended

#### Netflix
- **Monthly Cost:** $15.99
- **Annual Cost:** $191.88
- **Last Charged:** March 1, 2026
- **Issue:** Unused for 67 days
- **Last Activity:** No mentions in vault since January 2
- **Recommendation:** Cancel immediately
- **Annual Savings:** $191.88
- **Approval File:** `APPROVAL_cancel_netflix_20260309.md`

#### Adobe Creative Cloud
- **Monthly Cost:** $54.99
- **Annual Cost:** $659.88
- **Last Charged:** March 5, 2026
- **Issue:** Unused for 45 days
- **Last Activity:** Last used January 23 for logo design
- **Recommendation:** Cancel or downgrade to Photography plan ($9.99/month)
- **Annual Savings:** $659.88 (full cancel) or $540/year (downgrade)
- **Approval File:** `APPROVAL_cancel_adobe_20260309.md`

**Total High Severity Savings:** $851.76/year

---

### Medium Severity (1) — Review Recommended

#### Dropbox
- **Monthly Cost:** $11.99
- **Annual Cost:** $143.88
- **Last Charged:** March 3, 2026
- **Issue:** Duplicate functionality with Google Drive
- **Last Activity:** Last file uploaded 38 days ago
- **Usage:** Minimal — Google Drive used daily, Dropbox rarely
- **Recommendation:** Migrate files to Google Drive and cancel
- **Potential Savings:** $143.88/year
- **Approval File:** `APPROVAL_cancel_dropbox_20260309.md`

**Total Medium Severity Savings:** $143.88/year

---

### Low Severity (1) — Monitor

#### Notion
- **Monthly Cost:** $10.00
- **Annual Cost:** $120.00
- **Last Charged:** March 1, 2026
- **Issue:** Price increased from $8/month (25% increase)
- **Last Activity:** Used daily for project management
- **Usage:** Active — 47 pages edited in last 30 days
- **Recommendation:** Monitor for further increases, evaluate alternatives if price rises again
- **Note:** Still good value despite increase, heavily used

---

## Active Subscriptions (No Issues)

### Streaming (2)
- **Spotify** — $9.99/month — Used daily for work music
- **YouTube Premium** — $11.99/month — Used 15+ times in last 30 days

### Software & Productivity (3)
- **GitHub** — $4.00/month — Active repositories, CI/CD pipelines
- **Figma** — $12.00/month — Used for all design work
- **Notion** — $10.00/month — Daily use (see note above about price increase)

### Cloud & Infrastructure (2)
- **AWS** — $23.45/month — Production website hosting
- **Google Workspace** — $12.00/month — Email, Drive, Calendar

### Other (2)
- **1Password** — $4.99/month — Password management, daily use
- **Calendly** — $8.00/month — Client scheduling, 12 bookings last month

**Total Healthy Subscriptions Cost:** $96.42/month ($1,157.04/year)

---

## Duplicate Functionality Analysis

### Cloud Storage
**Services:** Dropbox ($11.99/month), Google Drive ($0 — included in Workspace)  
**Total Cost:** $11.99/month  
**Recommendation:** Cancel Dropbox, consolidate to Google Drive  
**Potential Savings:** $143.88/year

---

## Cost Increase Analysis

### Recent Price Increases

#### Notion
- **Previous Price:** $8.00/month
- **Current Price:** $10.00/month
- **Increase:** 25% (+$2.00/month)
- **Annual Impact:** +$24.00/year
- **Recommendation:** Continue using (heavily used), but monitor for further increases

**Total Annual Impact of Price Increases:** +$24.00/year

---

## Recommendations

### Immediate Actions (High Priority)

1. **Cancel Netflix** — Unused for 67 days, save $191.88/year
2. **Cancel or downgrade Adobe Creative Cloud** — Unused for 45 days, save $540-660/year
3. **Migrate Dropbox to Google Drive** — Duplicate service, save $143.88/year

### Review This Month (Medium Priority)

1. **Evaluate Notion alternatives** — Recent 25% price increase, consider Obsidian (free) or Coda
2. **Review streaming usage** — Keep Spotify and YouTube Premium for now, both actively used

### Long-term Optimization

1. **Annual billing** — Switch Spotify to annual for 2 months free ($20 savings)
2. **Bundle services** — Consider YouTube Premium Family plan if sharing with household
3. **Monitor AWS costs** — Review usage monthly, optimize resources

---

## Financial Summary

| Category | Monthly | Annual |
|---|---|---|
| Current Total Cost | $243.87 | $2,926.44 |
| High Severity Savings | $70.98 | $851.76 |
| Medium Severity Savings | $11.99 | $143.88 |
| Low Severity Savings | $0.00 | $0.00 |
| **Potential New Total** | **$160.90** | **$1,930.80** |
| **Total Savings** | **$82.97** | **$995.64** |

**Savings Percentage:** 34% reduction in subscription costs

---

## Next Steps

1. Review approval files in `/Pending_Approval/` folder
2. Approve cancellations for Netflix and Adobe
3. Migrate Dropbox files to Google Drive before canceling
4. Monitor Notion for further price increases
5. Schedule next audit for April 6, 2026

---

## Approval Files Created

The following approval files have been created in `/Pending_Approval/`:

- `APPROVAL_cancel_netflix_20260309.md` — $191.88/year savings
- `APPROVAL_cancel_adobe_20260309.md` — $659.88/year savings
- `APPROVAL_cancel_dropbox_20260309.md` — $143.88/year savings

**Total Potential Savings:** $995.64/year

Move files to `/Approved/` to proceed with cancellations.

---

*Generated automatically by AI Employee on 2026-03-09 at 20:00*
```
