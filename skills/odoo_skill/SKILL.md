---
name: odoo_skill
description: Interact with Odoo ERP via XML-RPC (Leads, Contacts, CRM)
---

# Odoo Skill

This skill allows the agent to read and write data to an Odoo instance using its XML-RPC external API.

## Capabilities

-   **CRM**: Create and search Leads/Opportunities.
-   **Contacts**: Search and create Partners (res.partner).
-   **Generic**: Read/Write to any Odoo model.

## Configuration

Requires the following `.env` variables:
-   `ODOO_URL`: URL of the instance (e.g., https://my-db.odoo.com)
-   `ODOO_DB`: Database name
-   `ODOO_USERNAME`: User email
-   `ODOO_PASSWORD`: API Key or Password

## Usage

```python
from skills.odoo_skill.odoo_skill import OdooSkill

skill = OdooSkill()
if skill.authenticate():
    leads = skill.search_leads([['type', '=', 'opportunity']])
```
