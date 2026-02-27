"""
Odoo MCP Server - Gold Tier
Proper MCP implementation using the mcp library.
Connects to Odoo 19 via JSON-RPC (xmlrpc) API.
"""
import asyncio
import os
import xmlrpc.client
from datetime import datetime
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

if not all([ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD]):
    raise RuntimeError("Missing Odoo credentials. Check your .env file: ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD")

server = Server("odoo")


def _get_uid():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise RuntimeError("Odoo authentication failed. Check credentials.")
    return uid


def _get_models():
    return xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="create_invoice",
            description="Create a new customer invoice in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer name (must exist in Odoo)"},
                    "description": {"type": "string", "description": "Service/product description"},
                    "amount": {"type": "number", "description": "Invoice amount"},
                },
                "required": ["customer_name", "description", "amount"],
            },
        ),
        types.Tool(
            name="get_invoices",
            description="List customer invoices from Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status: draft, posted, paid, all",
                        "default": "all",
                    },
                    "limit": {"type": "integer", "description": "Max number of invoices to return", "default": 10},
                },
            },
        ),
        types.Tool(
            name="create_customer",
            description="Create a new customer in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Customer full name"},
                    "email": {"type": "string", "description": "Customer email address"},
                    "phone": {"type": "string", "description": "Customer phone number"},
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="get_customers",
            description="Search customers in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {"type": "string", "description": "Search by name or email (leave empty for all)"},
                    "limit": {"type": "integer", "description": "Max number of customers to return", "default": 10},
                },
            },
        ),
        types.Tool(
            name="get_accounting_summary",
            description="Get accounting summary for CEO briefing - total revenue, paid and unpaid invoices",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "description": "Period: this_month, last_month, all",
                        "default": "this_month",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would call Odoo tool: {name} with args: {arguments}")]

    try:
        if name == "create_invoice":
            return await _create_invoice(arguments)
        elif name == "get_invoices":
            return await _get_invoices(arguments)
        elif name == "create_customer":
            return await _create_customer(arguments)
        elif name == "get_customers":
            return await _get_customers(arguments)
        elif name == "get_accounting_summary":
            return await _get_accounting_summary(arguments)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def _create_invoice(args: dict) -> list[types.TextContent]:
    uid = _get_uid()
    models = _get_models()

    partner_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "res.partner", "search",
        [[["name", "ilike", args["customer_name"]], ["customer_rank", ">", 0]]],
    )

    if not partner_ids:
        return [types.TextContent(type="text", text=f"Customer '{args['customer_name']}' not found. Create customer first.")]

    invoice_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "account.move", "create",
        [{
            "move_type": "out_invoice",
            "partner_id": partner_ids[0],
            "invoice_line_ids": [(0, 0, {
                "name": args["description"],
                "quantity": 1,
                "price_unit": args["amount"],
            })],
        }],
    )

    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "account.move", "action_post",
        [[invoice_id]],
    )

    invoice = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "account.move", "read",
        [[invoice_id]],
        {"fields": ["name", "amount_total", "state"]},
    )[0]

    return [types.TextContent(
        type="text",
        text=f"Invoice created successfully!\nInvoice #: {invoice['name']}\nAmount: {invoice['amount_total']}\nStatus: {invoice['state']}",
    )]


async def _get_invoices(args: dict) -> list[types.TextContent]:
    uid = _get_uid()
    models = _get_models()

    status = args.get("status", "all")
    limit = args.get("limit", 10)

    domain = [["move_type", "=", "out_invoice"]]
    if status == "draft":
        domain.append(["state", "=", "draft"])
    elif status == "posted":
        domain.append(["state", "=", "posted"])
    elif status == "paid":
        domain.append(["payment_state", "=", "paid"])

    invoices = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "account.move", "search_read",
        [domain],
        {"fields": ["name", "partner_id", "amount_total", "state", "payment_state", "invoice_date"], "limit": limit},
    )

    if not invoices:
        return [types.TextContent(type="text", text="No invoices found.")]

    lines = ["📄 Invoices:\n"]
    for inv in invoices:
        customer = inv["partner_id"][1] if inv["partner_id"] else "Unknown"
        lines.append(
            f"• {inv['name']} | {customer} | {inv['amount_total']} | {inv['state']} | {inv.get('invoice_date', 'N/A')}"
        )

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _create_customer(args: dict) -> list[types.TextContent]:
    uid = _get_uid()
    models = _get_models()

    vals = {
        "name": args["name"],
        "customer_rank": 1,
    }
    if args.get("email"):
        vals["email"] = args["email"]
    if args.get("phone"):
        vals["phone"] = args["phone"]

    partner_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "res.partner", "create",
        [vals],
    )

    return [types.TextContent(
        type="text",
        text=f"Customer created successfully!\nName: {args['name']}\nID: {partner_id}",
    )]


async def _get_customers(args: dict) -> list[types.TextContent]:
    uid = _get_uid()
    models = _get_models()

    search = args.get("search", "")
    limit = args.get("limit", 10)

    domain = [["customer_rank", ">", 0]]
    if search:
        domain.append(["name", "ilike", search])

    customers = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "res.partner", "search_read",
        [domain],
        {"fields": ["name", "email", "phone"], "limit": limit},
    )

    if not customers:
        return [types.TextContent(type="text", text="No customers found.")]

    lines = ["👥 Customers:\n"]
    for c in customers:
        lines.append(f"• {c['name']} | {c.get('email', 'N/A')} | {c.get('phone', 'N/A')}")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _get_accounting_summary(args: dict) -> list[types.TextContent]:
    uid = _get_uid()
    models = _get_models()

    period = args.get("period", "this_month")
    now = datetime.now()

    domain = [["move_type", "=", "out_invoice"], ["state", "=", "posted"]]

    if period == "this_month":
        domain.append(["invoice_date", ">=", f"{now.year}-{now.month:02d}-01"])
    elif period == "last_month":
        if now.month == 1:
            domain.append(["invoice_date", ">=", f"{now.year - 1}-12-01"])
            domain.append(["invoice_date", "<=", f"{now.year - 1}-12-31"])
        else:
            domain.append(["invoice_date", ">=", f"{now.year}-{now.month - 1:02d}-01"])
            domain.append(["invoice_date", "<", f"{now.year}-{now.month:02d}-01"])

    invoices = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        "account.move", "search_read",
        [domain],
        {"fields": ["name", "amount_total", "payment_state", "partner_id"]},
    )

    total = sum(inv["amount_total"] for inv in invoices)
    paid = sum(inv["amount_total"] for inv in invoices if inv["payment_state"] == "paid")
    unpaid = total - paid

    summary = f"""📊 Accounting Summary ({period})
━━━━━━━━━━━━━━━━━━━━━━
Total Invoiced : {total:,.2f}
Paid           : {paid:,.2f}
Unpaid         : {unpaid:,.2f}
Total Invoices : {len(invoices)}
━━━━━━━━━━━━━━━━━━━━━━"""

    return [types.TextContent(type="text", text=summary)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())