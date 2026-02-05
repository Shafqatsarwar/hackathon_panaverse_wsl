# Odoo Integration Deep Dive 📊

**Role**: The "Business Memory" of the assistant.

## Architecture
- **Protocol**: XML-RPC (Standard Odoo API).
- **Endpoint**: `/xmlrpc/2/object` (for executing model methods).
- **Authentication**: UID retrieved via `/xmlrpc/2/common`.

## Capabilities

### 1. Leads (CRM)
- **Model**: `crm.lead`
- **Actions**:
    - `create`: New leads from Chat or Emails.
    - `search_read`: Checking recent leads.

### 2. Contacts (Res Partner)
- **Model**: `res.partner`
- **Actions**: Search for people/companies by name/email.
- **Use Case**: "Do we have a contact for Alice?"

### 3. Project Tasks
- **Model**: `project.task`
- **Actions**: Search for pending tasks assigned to user.
- **Use Case**: "What are my deadlines?"

## Future Scope
- **Knowledge Base**: Integrate `knowledge.article` for Q&A.
- **Calendar**: Sync meetings with `calendar.event`.
