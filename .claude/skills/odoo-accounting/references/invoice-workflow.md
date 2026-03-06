# Invoice Creation Workflow

Step-by-step workflow for creating invoices in Odoo with human approval.

## Complete Workflow

```
Invoice Request
    ↓
Verify Customer Exists
    ↓
Create Customer (if needed)
    ↓
Create Approval Request → /Pending_Approval/
    ↓
Wait for Human Decision
    ↓
Human Moves to /Approved/
    ↓
Call create_invoice MCP Tool
    ↓
Log Action
    ↓
Move Files to /Done/
    ↓
TASK_COMPLETE
```

## Step-by-Step Instructions

### Step 1: Receive Invoice Request

Invoice requests can come from:
- WhatsApp message: "Can you send me the invoice?"
- Email: "Please invoice us for the project"
- User prompt: "Create invoice for Acme Corp - $5,000"

**Extract information:**
- Customer name
- Amount
- Description/service
- Customer contact info (email, phone)

### Step 2: Verify Customer Exists

**Always check if customer exists before creating invoice.**

```python
# Search for customer
result = mcp_call("get_customers", {
    "search": "Acme Corp",
    "limit": 1
})

if "No customers found" in result:
    customer_exists = False
else:
    customer_exists = True
```

**Decision:**
- Customer exists → Proceed to Step 4
- Customer not found → Proceed to Step 3

### Step 3: Create Customer (if needed)

If customer doesn't exist, create them first:

```python
result = mcp_call("create_customer", {
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "+1234567890"
})

# Log customer creation
log_entry = {
    "timestamp": "2026-03-06T14:30:00Z",
    "action_type": "odoo_customer_created",
    "customer_name": "Acme Corp",
    "customer_id": 42  # extracted from result
}
```

**Note:** Customer creation does NOT require approval (non-destructive).

### Step 4: Create Approval Request

**CRITICAL: Never call create_invoice without approval.**

Create approval file in `/Pending_Approval/`:

**File naming:** `APPROVAL_invoice_{customer_slug}_{YYYY-MM-DD}.md`

**Template:**
```markdown
---
type: invoice_approval
customer_name: Acme Corp
amount: 5000.00
created: 2026-03-06T14:30:00Z
status: awaiting_approval
source_file: WHATSAPP_20260306_120000.md
---

# Invoice Approval: Acme Corp

## Invoice Details
**Customer:** Acme Corp
**Amount:** $5,000.00
**Description:** Web development services - March 2026

## Customer Information
**Email:** contact@acme.com
**Phone:** +1234567890
**Odoo ID:** 42

## Action
This will create and post an invoice in Odoo. The invoice will be:
- Officially recorded in accounting system
- Visible to customer in their portal
- Included in financial reports
- Sent to customer (if email configured)

## Financial Impact
**Revenue:** +$5,000.00
**Outstanding Receivables:** +$5,000.00 (until paid)

## To Approve
Move this file to /Approved folder to create invoice.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before posting invoice*
```

### Step 5: Wait for Human Decision

**DO NOT proceed until human acts.**

Human will:
1. Review approval request
2. Verify customer details
3. Confirm amount and description
4. Make decision:
   - Move to `/Approved/` → Execute
   - Move to `/Rejected/` → Cancel
   - Leave in `/Pending_Approval/` → Still waiting

**Important:** Do NOT check repeatedly or retry. Wait for file to appear in `/Approved/`.

### Step 6: Execute Invoice Creation

**When file appears in `/Approved/`:**

1. Read approval file to get details
2. Call create_invoice MCP tool
3. Handle response

```python
# Read approval file
approval_data = read_approval_file("/Approved/APPROVAL_invoice_acme_20260306.md")

# Call MCP tool
result = mcp_call("create_invoice", {
    "customer_name": approval_data["customer_name"],
    "description": approval_data["description"],
    "amount": approval_data["amount"]
})

# Parse response
if "Invoice created successfully" in result:
    # Extract invoice number from response
    invoice_number = extract_invoice_number(result)  # e.g., "INV/2026/0042"
    status = "success"
else:
    # Handle error
    status = "error"
    error_message = result
```

### Step 7: Log Action

**Always log to `/Vault/Logs/YYYY-MM-DD.json`:**

**Success log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "odoo_invoice_created",
  "customer_name": "Acme Corp",
  "invoice_number": "INV/2026/0042",
  "amount": 5000.00,
  "description": "Web development services - March 2026",
  "status": "posted",
  "approval_file": "APPROVAL_invoice_acme_20260306.md",
  "dry_run": false
}
```

**Error log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "odoo_invoice_failed",
  "customer_name": "Acme Corp",
  "amount": 5000.00,
  "status": "error",
  "error_message": "Customer 'Acme Corp' not found",
  "approval_file": "APPROVAL_invoice_acme_20260306.md"
}
```

### Step 8: Move Files to /Done/

After successful execution:

1. Move approval file from `/Approved/` to `/Done/`
2. Move source file (if any) to `/Done/`
3. Update Dashboard.md with invoice created

**Example:**
```
/Approved/APPROVAL_invoice_acme_20260306.md → /Done/APPROVAL_invoice_acme_20260306.md
/In_Progress/WHATSAPP_20260306_120000.md → /Done/WHATSAPP_20260306_120000.md
```

### Step 9: Complete

Output: `<promise>TASK_COMPLETE</promise>`

---

## Approval Request Templates

### Template 1: Standard Invoice

```markdown
---
type: invoice_approval
customer_name: {customer_name}
amount: {amount}
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_file}
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

### Template 2: New Customer Invoice

```markdown
---
type: invoice_approval
customer_name: {customer_name}
amount: {amount}
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_file}
new_customer: true
---

# Invoice Approval: {Customer Name} (New Customer)

## Invoice Details
**Customer:** {customer_name} ⚠️ NEW CUSTOMER
**Amount:** ${amount}
**Description:** {description}

## Customer Information
**Email:** {email}
**Phone:** {phone}
**Status:** Will be created in Odoo before invoice

## Action
This will:
1. Create new customer in Odoo
2. Create and post invoice

The invoice will be:
- Officially recorded in accounting system
- Visible to customer in their portal
- Included in financial reports

## To Approve
Move this file to /Approved folder to create customer and invoice.

## To Reject
Move this file to /Rejected folder to cancel.

---
*Awaiting human approval before creating customer and invoice*
```

### Template 3: High-Value Invoice

```markdown
---
type: invoice_approval
customer_name: {customer_name}
amount: {amount}
created: {iso_timestamp}
status: awaiting_approval
source_file: {source_file}
high_value: true
---

# ⚠️ HIGH-VALUE Invoice Approval: {Customer Name}

## Invoice Details
**Customer:** {customer_name}
**Amount:** ${amount} ⚠️ HIGH VALUE
**Description:** {description}

## Customer Information
**Email:** {email}
**Phone:** {phone}
**Odoo ID:** {customer_id}
**Previous Invoices:** {count} invoices, ${total_amount} total

## Financial Impact
**Revenue:** +${amount}
**Outstanding Receivables:** +${amount} (until paid)
**Percentage of Monthly Target:** {percentage}%

## Action
This will create and post a high-value invoice in Odoo. The invoice will be:
- Officially recorded in accounting system
- Visible to customer in their portal
- Included in financial reports

## Verification Checklist
- [ ] Customer details verified
- [ ] Amount confirmed with contract/agreement
- [ ] Description accurate
- [ ] Payment terms agreed

## To Approve
Move this file to /Approved folder to create invoice.

## To Reject
Move this file to /Rejected folder to cancel.

---
**⚠️ HIGH-VALUE INVOICE: Please verify all details before approving**
```

---

## Error Handling

### Error: Customer Not Found

**Scenario:** create_invoice returns "Customer 'Acme Corp' not found"

**Action:**
1. This should not happen if Step 2 was followed correctly
2. Call get_customers to verify
3. If customer truly doesn't exist, call create_customer
4. Retry create_invoice
5. If still fails, escalate to human

### Error: Authentication Failed

**Scenario:** "Odoo authentication failed. Check credentials."

**Action:**
1. Do NOT retry
2. Log error
3. Move approval file back to /Pending_Approval/ with error note
4. Escalate to human to check ODOO credentials in .env

### Error: DRY_RUN Active

**Scenario:** Response is "[DRY RUN] Would call Odoo tool: create_invoice"

**Action:**
1. This is NOT an error — it's expected behavior in DRY_RUN mode
2. Log simulation
3. Move files to /Done/ as if successful
4. Do NOT wait for actual invoice creation

---

## Rejection Handling

**When file appears in `/Rejected/`:**

1. Read rejection file (may have human notes)
2. Cancel invoice creation (do NOT call create_invoice)
3. Log rejection to /Vault/Logs/
4. Move rejection file to /Done/
5. Notify user of cancellation

**Rejection log:**
```json
{
  "timestamp": "2026-03-06T14:35:00Z",
  "action_type": "odoo_invoice_rejected",
  "customer_name": "Acme Corp",
  "amount": 5000.00,
  "reason": "human_rejected",
  "approval_file": "APPROVAL_invoice_acme_20260306.md"
}
```

---

## Integration with Other Skills

### WhatsApp Triage → Odoo Accounting

```
WHATSAPP_*.md in /Needs_Action/
    ↓
whatsapp-triage detects "invoice" keyword
    ↓
Creates PLAN_WHATSAPP_invoice.md
    ↓
Plan executes: Load odoo-accounting skill
    ↓
odoo-accounting creates approval request
    ↓
Human approves
    ↓
Invoice created in Odoo
```

### Email Triage → Odoo Accounting

```
EMAIL_*.md in /Needs_Action/
    ↓
gmail-triage detects invoice request
    ↓
Creates PLAN_EMAIL_invoice.md
    ↓
Plan executes: Load odoo-accounting skill
    ↓
odoo-accounting creates approval request
    ↓
Human approves
    ↓
Invoice created in Odoo
```

### Daily Briefing → Odoo Accounting

```
PROMPT_daily_briefing.md in /Plans/
    ↓
daily-briefing skill triggers
    ↓
Calls odoo-accounting for revenue summary
    ↓
odoo-accounting calls get_accounting_summary
    ↓
Returns revenue data
    ↓
daily-briefing adds to briefing report
```

---

## Best Practices

1. **Always verify customer exists** before creating invoice
2. **Always create approval request** — never call create_invoice directly
3. **Always log actions** to /Vault/Logs/
4. **Always respect DRY_RUN mode** — check before executing
5. **Always move files to /Done/** after completion
6. **Never retry failed operations** without human intervention
7. **Never store credentials in code** — use .env only

---

## Quick Reference

**Customer verification:**
```python
result = mcp_call("get_customers", {"search": customer_name})
customer_exists = "No customers found" not in result
```

**Create customer:**
```python
mcp_call("create_customer", {
    "name": customer_name,
    "email": email,
    "phone": phone
})
```

**Create invoice (after approval):**
```python
mcp_call("create_invoice", {
    "customer_name": customer_name,
    "description": description,
    "amount": amount
})
```

**Get accounting summary:**
```python
mcp_call("get_accounting_summary", {
    "period": "this_month"
})
```
