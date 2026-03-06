# Odoo MCP Tools Reference

Complete documentation for all Odoo MCP tools available via `mcp_servers/odoo_mcp.py`.

## Connection Details

**MCP Server:** `mcp_servers/odoo_mcp.py`  
**Protocol:** JSON-RPC (xmlrpc) to Odoo 19  
**Authentication:** Via environment variables (ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD)  
**DRY_RUN:** Respects `DRY_RUN=true` in `.env` — returns simulation messages instead of executing

## Tool: create_invoice

**Purpose:** Create and post a customer invoice in Odoo

**Parameters:**
```json
{
  "customer_name": "string (required) - Customer name (must exist in Odoo)",
  "description": "string (required) - Service/product description",
  "amount": "number (required) - Invoice amount"
}
```

**Behavior:**
1. Searches for customer by name in Odoo
2. If customer not found, returns error message
3. Creates invoice with one line item
4. **Automatically posts invoice** (makes it official)
5. Returns invoice number, amount, and status

**Returns:**
```
Success:
"Invoice created successfully!
Invoice #: INV/2026/0042
Amount: 5000.0
Status: posted"

Error (customer not found):
"Customer 'Acme Corp' not found. Create customer first."

DRY_RUN:
"[DRY RUN] Would call Odoo tool: create_invoice with args: {...}"
```

**Security Warning:**
This tool automatically posts the invoice, making it official and visible to the customer. ALWAYS require human approval before calling this tool.

**Example Usage:**
```python
# WRONG - Never call directly without approval
result = mcp_call("create_invoice", {
    "customer_name": "Acme Corp",
    "description": "Web development - March 2026",
    "amount": 5000.00
})

# CORRECT - Always create approval request first
# 1. Create APPROVAL_invoice_acme_20260306.md in /Pending_Approval/
# 2. Wait for human to move to /Approved/
# 3. Then call create_invoice
```

**Implementation Details:**
- Uses `account.move` model with `move_type: "out_invoice"`
- Creates single invoice line with quantity=1, price_unit=amount
- Calls `action_post` to post invoice immediately
- Returns invoice name (number), amount_total, and state

---

## Tool: get_invoices

**Purpose:** List customer invoices from Odoo

**Parameters:**
```json
{
  "status": "string (optional) - Filter: draft, posted, paid, all (default: all)",
  "limit": "integer (optional) - Max results (default: 10)"
}
```

**Status Filters:**
- `draft` — Invoices not yet posted (still editable)
- `posted` — Posted invoices (official, sent to customer)
- `paid` — Invoices marked as paid
- `all` — All customer invoices regardless of status

**Returns:**
```
Success:
"📄 Invoices:
• INV/2026/0042 | Acme Corp | 5000.0 | posted | 2026-03-06
• INV/2026/0041 | Beta Inc | 3000.0 | paid | 2026-03-05
• INV/2026/0040 | Gamma LLC | 2000.0 | posted | 2026-03-04"

No results:
"No invoices found."

DRY_RUN:
"[DRY RUN] Would call Odoo tool: get_invoices with args: {...}"
```

**Example Usage:**
```python
# Get all posted invoices
result = mcp_call("get_invoices", {
    "status": "posted",
    "limit": 10
})

# Get paid invoices only
result = mcp_call("get_invoices", {
    "status": "paid",
    "limit": 5
})

# Get all invoices (default)
result = mcp_call("get_invoices", {})
```

**Use Cases:**
- Check recent invoices for CEO briefing
- Verify invoice was created successfully
- Find unpaid invoices for follow-up
- Audit invoice history

**Implementation Details:**
- Filters by `move_type: "out_invoice"` (customer invoices only)
- Returns fields: name, partner_id, amount_total, state, payment_state, invoice_date
- Sorted by date (most recent first)

---

## Tool: create_customer

**Purpose:** Create a new customer in Odoo

**Parameters:**
```json
{
  "name": "string (required) - Customer full name",
  "email": "string (optional) - Customer email address",
  "phone": "string (optional) - Customer phone number"
}
```

**Behavior:**
1. Creates new partner (customer) in Odoo
2. Sets `customer_rank: 1` to mark as customer
3. Optionally adds email and phone if provided
4. Returns customer name and Odoo ID

**Returns:**
```
Success:
"Customer created successfully!
Name: Acme Corp
ID: 42"

DRY_RUN:
"[DRY RUN] Would call Odoo tool: create_customer with args: {...}"
```

**Example Usage:**
```python
# Create customer with full details
result = mcp_call("create_customer", {
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "+1234567890"
})

# Create customer with name only
result = mcp_call("create_customer", {
    "name": "Beta Inc"
})
```

**Use Cases:**
- Create customer before invoice generation
- Add new client to Odoo from email/WhatsApp
- Onboard new customer from CRM

**Security:**
Customer creation does NOT require approval (non-destructive, can be edited later).

**Implementation Details:**
- Uses `res.partner` model
- Sets `customer_rank: 1` to mark as customer (not just contact)
- Email and phone are optional fields
- Returns partner_id for reference

---

## Tool: get_customers

**Purpose:** Search customers in Odoo

**Parameters:**
```json
{
  "search": "string (optional) - Search by name or email (empty for all)",
  "limit": "integer (optional) - Max results (default: 10)"
}
```

**Behavior:**
1. Searches customers by name (case-insensitive partial match)
2. Filters by `customer_rank > 0` (customers only, not all contacts)
3. Returns name, email, phone for each customer
4. Limited to specified number of results

**Returns:**
```
Success:
"👥 Customers:
• Acme Corp | contact@acme.com | +1234567890
• Acme Industries | info@acmeindustries.com | +0987654321
• Acme Solutions | N/A | N/A"

No results:
"No customers found."

DRY_RUN:
"[DRY RUN] Would call Odoo tool: get_customers with args: {...}"
```

**Example Usage:**
```python
# Search for specific customer
result = mcp_call("get_customers", {
    "search": "Acme",
    "limit": 5
})

# Get all customers
result = mcp_call("get_customers", {
    "limit": 20
})

# Check if customer exists
result = mcp_call("get_customers", {
    "search": "Acme Corp",
    "limit": 1
})
if "No customers found" in result:
    # Customer doesn't exist, create it
    pass
```

**Use Cases:**
- Verify customer exists before invoice creation
- Search for customer by partial name
- List all customers for reference
- Check for duplicate customers

**Implementation Details:**
- Uses `res.partner` model
- Filters by `customer_rank > 0` (customers only)
- Search uses `ilike` operator (case-insensitive partial match)
- Returns fields: name, email, phone

---

## Tool: get_accounting_summary

**Purpose:** Get accounting summary for CEO briefing

**Parameters:**
```json
{
  "period": "string (optional) - Period: this_month, last_month, all (default: this_month)"
}
```

**Period Options:**
- `this_month` — Current month to date
- `last_month` — Previous calendar month
- `all` — All time (all posted invoices)

**Behavior:**
1. Filters posted invoices by date range
2. Calculates total invoiced amount
3. Calculates paid amount (invoices with payment_state: paid)
4. Calculates unpaid amount (total - paid)
5. Counts total invoices

**Returns:**
```
Success:
"📊 Accounting Summary (this_month)
━━━━━━━━━━━━━━━━━━━━━━
Total Invoiced : 47,000.00
Paid           : 35,000.00
Unpaid         : 12,000.00
Total Invoices : 8
━━━━━━━━━━━━━━━━━━━━━━"

DRY_RUN:
"[DRY RUN] Would call Odoo tool: get_accounting_summary with args: {...}"
```

**Example Usage:**
```python
# Get current month summary (for CEO briefing)
result = mcp_call("get_accounting_summary", {
    "period": "this_month"
})

# Get last month summary
result = mcp_call("get_accounting_summary", {
    "period": "last_month"
})

# Get all-time summary
result = mcp_call("get_accounting_summary", {
    "period": "all"
})
```

**Use Cases:**
- Populate CEO briefing revenue section every Monday
- Check monthly revenue progress
- Audit unpaid invoices
- Financial reporting

**Parsing Response:**
```python
# Extract values from response
lines = result.split("\n")
total_line = [l for l in lines if "Total Invoiced" in l][0]
paid_line = [l for l in lines if "Paid" in l and "Unpaid" not in l][0]
unpaid_line = [l for l in lines if "Unpaid" in l][0]

total = float(total_line.split(":")[1].strip().replace(",", ""))
paid = float(paid_line.split(":")[1].strip().replace(",", ""))
unpaid = float(unpaid_line.split(":")[1].strip().replace(",", ""))
```

**Implementation Details:**
- Filters by `move_type: "out_invoice"` and `state: "posted"`
- Date filtering based on `invoice_date` field
- Sums `amount_total` for all matching invoices
- Checks `payment_state: "paid"` for paid invoices

---

## Error Handling

**Authentication Errors:**
```
Error: Odoo authentication failed. Check credentials.
```
**Action:** Escalate to human, check ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD in .env

**Customer Not Found:**
```
Customer 'Acme Corp' not found. Create customer first.
```
**Action:** Call create_customer, then retry invoice creation

**Connection Errors:**
```
Error: [connection error details]
```
**Action:** Check Odoo server is running, network connectivity, credentials

**DRY_RUN Mode:**
```
[DRY RUN] Would call Odoo tool: {tool_name} with args: {args}
```
**Action:** Log simulation, proceed as if successful, do NOT wait for real response

---

## Security Best Practices

1. **NEVER call create_invoice without approval** — it posts immediately
2. **ALWAYS verify customer exists** before invoice creation
3. **ALWAYS log Odoo actions** to /Vault/Logs/
4. **ALWAYS respect DRY_RUN mode** — check before executing
5. **NEVER store credentials in code** — use .env only

---

## Credentials Configuration

**Location:** `.env` file (never commit to git)

**Required variables:**
```bash
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database_name
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
DRY_RUN=false  # Set to true for testing
```

**Alternative:** Inject via `~/.claude/settings.json` env block (more secure)

---

## Testing with DRY_RUN

**Enable DRY_RUN mode:**
```bash
# In .env file
DRY_RUN=true
```

**Behavior:**
- All MCP calls return `[DRY RUN] Would call Odoo tool: ...`
- No actual Odoo API calls made
- Safe for testing workflows without affecting production data

**Testing workflow:**
1. Set DRY_RUN=true
2. Test invoice creation workflow
3. Verify approval files created correctly
4. Verify logging works
5. Set DRY_RUN=false for production
