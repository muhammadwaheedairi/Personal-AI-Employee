---
name: odoo-accounting
description: Manage customers and invoices in Odoo ERP system. Use when user asks to create invoice, add customer, check revenue, get accounting summary, or manage Odoo records. Always verifies customer exists before invoice creation, routes invoice posting to human approval, and integrates with CEO briefing for revenue reporting.
---

# Odoo Accounting

Manage customers and invoices in Odoo ERP system via MCP tools. Handles customer creation, invoice generation with approval workflow, and revenue reporting for CEO briefings.

## Workflow

### Invoice Creation Workflow

1. **Receive** invoice request (from email, WhatsApp, or user prompt)
2. **Verify** customer exists using `get_customers` MCP tool
3. **Create customer** if not found using `create_customer` MCP tool
4. **Create approval request** in `/Pending_Approval/` with invoice details
5. **Wait** for human to move file to `/Approved/`
6. **Call** `create_invoice` MCP tool (posts invoice automatically)
7. **Log** action to `/Vault/Logs/YYYY-MM-DD.json`
8. **Move** approval file to `/Done/`
9. Output `<promise>TASK_COMPLETE</promise>`

### Customer Creation Workflow

1. **Receive** customer creation request
2. **Check** if customer already exists using `get_customers`
3. **Create** customer using `create_customer` MCP tool
4. **Log** action to `/Vault/Logs/YYYY-MM-DD.json`
5. Output `<promise>TASK_COMPLETE</promise>`

### Accounting Summary Workflow (for CEO Briefing)

1. **Call** `get_accounting_summary` with `period: "this_month"`
2. **Parse** response (total invoiced, paid, unpaid)
3. **Add** to briefing under `## Revenue & Financial Health` section
4. **Flag** unpaid invoices as bottlenecks if overdue
5. Output `<promise>TASK_COMPLETE</promise>`

## MCP Tools

See `references/mcp-tools.md` for complete tool documentation.

### create_invoice

**Purpose:** Create and post customer invoice in Odoo

**Parameters:**
- `customer_name` (string, required) — Customer name (must exist in Odoo)
- `description` (string, required) — Service/product description
- `amount` (number, required) — Invoice amount

**Returns:** Invoice number, amount, status

**Security:** This tool automatically posts the invoice. ALWAYS require human approval before calling.

**Example:**
```python
result = mcp_call("create_invoice", {
    "customer_name": "Acme Corp",
    "description": "Web development services - March 2026",
    "amount": 5000.00
})
# Returns: "Invoice created successfully!\nInvoice #: INV/2026/0042\nAmount: 5000.0\nStatus: posted"
```

### get_invoices

**Purpose:** List customer invoices from Odoo

**Parameters:**
- `status` (string, optional) — Filter by status: `draft`, `posted`, `paid`, `all` (default: `all`)
- `limit` (integer, optional) — Max number of invoices to return (default: 10)

**Returns:** List of invoices with number, customer, amount, status, date

**Example:**
```python
result = mcp_call("get_invoices", {
    "status": "posted",
    "limit": 5
})
```

### create_customer

**Purpose:** Create new customer in Odoo

**Parameters:**
- `name` (string, required) — Customer full name
- `email` (string, optional) — Customer email address
- `phone` (string, optional) — Customer phone number

**Returns:** Customer name and ID

**Example:**
```python
result = mcp_call("create_customer", {
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "+1234567890"
})
# Returns: "Customer created successfully!\nName: Acme Corp\nID: 42"
```

### get_customers

**Purpose:** Search customers in Odoo

**Parameters:**
- `search` (string, optional) — Search by name or email (leave empty for all)
- `limit` (integer, optional) — Max number of customers to return (default: 10)

**Returns:** List of customers with name, email, phone

**Example:**
```python
result = mcp_call("get_customers", {
    "search": "Acme",
    "limit": 5
})
```

### get_accounting_summary

**Purpose:** Get accounting summary for CEO briefing

**Parameters:**
- `period` (string, optional) — Period: `this_month`, `last_month`, `all` (default: `this_month`)

**Returns:** Total invoiced, paid, unpaid, invoice count

**Example:**
```python
result = mcp_call("get_accounting_summary", {
    "period": "this_month"
})
# Returns:
# 📊 Accounting Summary (this_month)
# ━━━━━━━━━━━━━━━━━━━━━━
# Total Invoiced : 47,000.00
# Paid           : 35,000.00
# Unpaid         : 12,000.00
# Total Invoices : 8
# ━━━━━━━━━━━━━━━━━━━━━━
```

## Security Rules

### Invoice Creation (CRITICAL)

**NEVER call `create_invoice` without human approval.**

The `create_invoice` tool automatically posts the invoice to Odoo (makes it official and sends to customer). This is irreversible and has legal/financial implications.

**Required workflow:**
1. Create approval request in `/Pending_Approval/`
2. Wait for human to move to `/Approved/`
3. Only then call `create_invoice` MCP tool

**Approval file format:** See `references/invoice-workflow.md`

### Customer Verification

**ALWAYS check if customer exists before creating invoice.**

**Workflow:**
```
1. Call get_customers with customer name
2. If found → proceed with invoice approval
3. If not found → create customer first, then invoice approval
```

**Example:**
```python
# Check if customer exists
result = mcp_call("get_customers", {"search": "Acme Corp"})

if "No customers found" in result:
    # Create customer first
    mcp_call("create_customer", {
        "name": "Acme Corp",
        "email": "contact@acme.com"
    })
    
# Now proceed with invoice approval request
```

### DRY_RUN Mode

**ALWAYS check DRY_RUN mode before calling MCP tools.**

When `DRY_RUN=true` in `.env`, all MCP calls return simulation messages:
```
[DRY RUN] Would call Odoo tool: create_invoice with args: {...}
```

**Behavior:**
- Log the dry-run simulation
- Move files as if action succeeded
- Do NOT wait for actual Odoo response

### Logging

**ALWAYS log every Odoo action to `/Vault/Logs/YYYY-MM-DD.json`**

**Log format:**
```json
{
  "timestamp": "2026-03-06T14:30:00Z",
  "action_type": "odoo_invoice_created",
  "customer_name": "Acme Corp",
  "invoice_number": "INV/2026/0042",
  "amount": 5000.00,
  "status": "posted",
  "approval_file": "APPROVAL_invoice_acme_20260306.md"
}
```

## Invoice Approval File Format

When creating invoice approval request in `/Pending_Approval/`:

```markdown
---
type: invoice_approval
customer_name: {customer_name}
amount: {amount}
created: {iso_timestamp}
status: awaiting_approval
---

# Invoice Approval: {Customer Name}

## Invoice Details
**Customer:** {customer_name}
**Amount:** ${amount}
**Description:** {description}

## Customer Information
**Email:** {email or "N/A"}
**Phone:** {phone or "N/A"}
**Odoo ID:** {customer_id or "Will be created"}

## Action
This will create and post an invoice in Odoo. The invoice will be:
- Officially recorded in accounting system
- Visible to customer in their portal
- Included in financial reports

## To Approve
Move this file to /Approved folder to create invoice.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before posting invoice*
```

**File naming:** `APPROVAL_invoice_{customer_slug}_{YYYY-MM-DD}.md`

**Examples:**
- `APPROVAL_invoice_acme_corp_20260306.md`
- `APPROVAL_invoice_john_doe_20260306.md`

## CEO Briefing Integration

Every Monday, the `daily-briefing` skill calls `get_accounting_summary` to populate the revenue section.

**Integration workflow:**
1. Daily-briefing skill triggers on Monday 8 AM
2. Calls `get_accounting_summary` with `period: "this_month"`
3. Parses response for total invoiced, paid, unpaid
4. Adds to briefing under `## Revenue & Financial Health`
5. Flags unpaid invoices as bottlenecks if >7 days old

**Briefing format:**
```markdown
## Revenue & Financial Health

### This Month (MTD)
- **Revenue:** $47,000 / $60,000 (78%)
- **Expenses:** $15,000
- **Net Position:** $32,000 (Profitable)

### Key Financial Metrics
- Invoices sent this week: 3
- Payments received: 2 ($12,000)
- Outstanding invoices: 5 ($23,000)
- Overdue invoices (>7 days): 1 ($5,000)

**Status:** Green
**Notes:** On track to hit monthly target.
```

## Example Scenarios

**Scenario 1: Invoice request from WhatsApp**
```
Input: WHATSAPP_20260306_120000.md
Content: "Hi, can you send me the invoice for this month?"
Sender: Acme Corp contact

Action:
1. Detect intent: invoice_request
2. Call get_customers with "Acme Corp"
3. Customer found → proceed
4. Create APPROVAL_invoice_acme_corp_20260306.md in /Pending_Approval/
5. Wait for human approval
6. Human moves to /Approved/
7. Call create_invoice MCP tool
8. Log invoice_created action
9. Move approval file to /Done/
```

**Scenario 2: New customer invoice request**
```
Input: EMAIL_20260306_140000_Invoice_request.md
Content: "Please invoice us for the web development project - $5,000"
Sender: newclient@example.com (not in Odoo)

Action:
1. Detect intent: invoice_request
2. Call get_customers with "New Client"
3. Customer not found → create customer first
4. Call create_customer with name, email
5. Create APPROVAL_invoice_new_client_20260306.md in /Pending_Approval/
6. Wait for human approval
7. Human moves to /Approved/
8. Call create_invoice MCP tool
9. Log customer_created and invoice_created actions
10. Move approval file to /Done/
```

**Scenario 3: CEO briefing revenue section**
```
Input: PROMPT_daily_briefing.md in /Plans/ (Monday 8 AM)

Action:
1. Daily-briefing skill triggers
2. Calls get_accounting_summary with period: "this_month"
3. Receives:
   Total Invoiced : 47,000.00
   Paid           : 35,000.00
   Unpaid         : 12,000.00
   Total Invoices : 8
4. Adds to briefing:
   - Revenue: $47,000 / $60,000 (78%)
   - Outstanding invoices: 3 ($12,000)
5. Flags overdue invoices if any >7 days old
```

**Scenario 4: DRY_RUN mode active**
```
Input: Invoice approval in /Approved/
DRY_RUN: true

Action:
1. Read approval file
2. Call create_invoice MCP tool
3. Receive: "[DRY RUN] Would call Odoo tool: create_invoice with args: {...}"
4. Log dry-run simulation
5. Move approval file to /Done/ with dry_run flag
6. Do NOT wait for actual invoice creation
```

## Error Handling

**Customer not found:**
```
Error: Customer 'Acme Corp' not found. Create customer first.
Action: Call create_customer, then retry invoice creation
```

**Authentication failed:**
```
Error: Odoo authentication failed. Check credentials.
Action: Escalate to human, do NOT retry
```

**DRY_RUN active:**
```
Response: [DRY RUN] Would call Odoo tool: create_invoice
Action: Log simulation, move files, do NOT wait for real response
```

## References

- `references/mcp-tools.md` — Complete MCP tool documentation with parameters, returns, examples
- `references/invoice-workflow.md` — Step-by-step invoice creation workflow with approval templates

## Completion Signal

Always end with: `<promise>TASK_COMPLETE</promise>`
