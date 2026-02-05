# Project Overview 🌟

**Project Name**: Panaversity Student Assistant
**Hackathon**: Agents v3.0
**Core Goal**: A Unified AI Assistant for Students & Admin.

## What it does
It connects the communication channels students use most (WhatsApp, Email) with the business data they need (Odoo LMS/CRM), mediated by an intelligent AI (Gemini).

## Key Components
1.  **Dual-Interface**: 
    - **Web UI**: Modern chat interface for direct interaction.
    - **Background Service**: "Always-on" monitoring of WhatsApp/Email.
2.  **Tools**:
    - `EmailAgent`: Reads/Sends via SMTP/IMAP.
    - `WhatsAppAgent`: Automates WhatsApp Web via Playwright.
    - `OdooAgent`: Syncs data via XML-RPC.
    - `WebSearch`: Live internet access.

## Target Audience
- **Students**: "When is my exam?", "Do I have new assignments?"
- **Admin**: "Create a lead for this student", "Check pending tasks."
