---
type: plan
created: 2026-03-09T09:31:56Z
source_file: WHATSAPP_20260309_093156_346480.md
source_type: whatsapp
priority: high
status: pending
---

# Plan: WhatsApp — Invoice Request

## Context
**Received:** 2026-03-09 09:31:56
**Priority:** High
**Matched Keywords:** urgent, invoice, asap
**Phone:** +92 323 8293672

## Objective
Generate and send invoice for AI automation services to client who requested via WhatsApp.

## Steps
- [ ] Gather missing invoice details (customer name, email, amount, service description)
- [ ] Verify customer exists in Odoo using odoo-accounting skill
- [ ] Create customer in Odoo if not found
- [ ] Create invoice approval request in /Pending_Approval/
- [ ] Wait for human to provide missing details and approve
- [ ] Generate invoice in Odoo after approval
- [ ] Send invoice to customer email
- [ ] Send WhatsApp confirmation to +92 323 8293672
- [ ] Log all actions to /Vault/Logs/

## Required Resources
- Skills: odoo-accounting, whatsapp-sender
- MCPs: create_customer, create_invoice, send_whatsapp
- Vault files: Company_Handbook.md, Business_Goals.md

## Missing Information
- Customer name (required for Odoo)
- Customer email (required for invoice delivery)
- Invoice amount (required)
- Detailed service description (optional but recommended)

## Completion Rule
Move this file and source WHATSAPP_*.md to /Done/ when invoice is created in Odoo and confirmation sent to customer.
