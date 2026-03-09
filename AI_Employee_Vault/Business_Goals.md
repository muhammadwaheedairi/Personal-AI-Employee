# Business Goals & KPIs — WaheedAI Solutions

---
last_updated: 2026-03-03
review_frequency: weekly
owner: Muhammad Waheed
---

## Revenue Target
- **Monthly Goal:** $5,000
- **Current MTD:** $0 (tracking via Odoo)
- **Currency:** USD
- **Net Profit Target:** $4,869/month (after $131 costs)
- **Alert Threshold:** Flag if MTD below $2,500 (50% of target)

## Active Projects
No active projects currently. Ready for new clients.

## Monthly Costs
| Expense | Cost |
|---------|------|
| AI APIs | $20 |
| Internet/WiFi | $10 |
| Portfolio Hosting | $1 |
| Claude Code Subscription | $100 |
| **Total** | **$131** |

## KPIs — Weekly Targets
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| LinkedIn posts | 7/week (1/day) | < 5/week |
| Twitter posts | 7/week (1/day) | < 5/week |
| Facebook posts | 7/week (1/day) | < 5/week |
| WhatsApp response time | < 24 hours | > 24 hours |
| Email response time | < 24 hours | > 24 hours |
| Unpaid invoices | 0 older than 7 days | Any invoice > 7 days |

## Payment Rules
- Any payment over $100 ALWAYS requires human approval
- Never auto-approve payments to new clients
- Always verify invoice before marking as paid in Odoo
- All payments must go through /Pending_Approval workflow

## Client Communication Rules
- Always respond to WhatsApp within 24 hours
- Always respond to emails within 24 hours
- Be professional but friendly in all communications
- Never promise deadlines without human confirmation
- Always log every client interaction in /Vault/Logs/

## Invoice Rules
- Always create customer in Odoo before invoicing
- Always send invoice via email after WhatsApp/email request
- Flag any unpaid invoice older than 7 days in CEO Briefing
- Invoice creation does not require approval — sending does

## Social Media Rules
- Post once daily on LinkedIn, Twitter, Facebook
- Content focus: AI automation, productivity, WaheedAI Solutions
- Never post anything political or controversial
- Always maintain professional tone
- Queue posts in /Plans/{platform}_queue/ folder

## Alert Rules — CEO Briefing Must Flag
- Monthly revenue below $2,500 (50% of target)
- Any project deadline within 3 days
- No social post in last 2 days
- Unanswered email older than 24 hours
- Unanswered WhatsApp older than 24 hours
- Any unpaid invoice older than 7 days

## Business Focus
- **Company:** WaheedAI Solutions
- **Primary Service:** AI automation for businesses
- **Target Clients:** Small to medium businesses
- **USP:** Local-first, privacy-focused AI Employee solutions
- **Goal:** Help businesses automate repetitive tasks with AI

## Subscription Audit Rules
Flag for review if:
- No usage in 30 days
- Cost increased more than 20%
- Duplicate functionality with another tool