# Phase 2: The "Trinity" Integrations 🔗

**Focus**: Integrating Gmail, WhatsApp, and LinkedIn.

## 1. Gmail (The Reliable One)
- **Protocol**: IMAP (Read) / SMTP (Send).
- **Logic**: Filters emails by subject (e.g., "Assignment").
- **Agent**: `src/agents/email_agent.py`.
- **Status**: Stable. Works via App Passwords.

## 2. WhatsApp (The Challenging One)
- **Protocol**: **None** (Official API is restrictive).
- **Solution**: **Browser Automation** (Playwright).
- **Logic**:
    - Launches Headless Chrome.
    - Saves user session to `./whatsapp_session`.
    - Scrapes DOM for unread badges.
    - Filters message text for keywords.
- **Agent**: `src/agents/whatsapp_agent.py`.

## 3. LinkedIn (The Social One)
- **Protocol**: Browser Automation.
- **Logic**: Similar to WhatsApp. Navigates to `/notifications` and scrapes text.
- **Agent**: `src/agents/linkedin_agent.py`.

## Key Breakthrough
Realizing that "Serverless" hosting wouldn't support these browser-based agents led to the pivot to Local/VPS hosting (See Phase 9).
