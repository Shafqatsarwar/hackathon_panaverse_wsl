# Architecture Decision Records (ADR) 🏛️

This folder documents the significant architectural decisions made during the project.

## ADR-001: Headless Browser for Messaging
- **Context**: Need free programmatic access to WhatsApp & LinkedIn.
- **Decision**: Use **Playwright** (Chromium).
- **Justification**: Official APIs are paid/business-only. Scraping the Web UI provides full read/write access for free.
- **Trade-off**: Requires higher RAM (500MB+) and session maintenance (QR codes).

## ADR-002: NestAsyncio for Event Loops
- **Context**: `ChatAgent` executes in FastAPI's async loop. Playwright also needs an async loop. Calling `asyncio.run()` (new loop) from inside FastAPI (existing loop) crashes Python.
- **Decision**: Use `nest_asyncio` library.
- **Justification**: Allows re-entrant event loops, enabling synchronous tool wrappers to call async automation code cleanly.

## ADR-003: Hybrid Deployment (Docker)
- **Context**: Vercel (Serverless) has 50MB limits and no persistent filesystem (needed for WhatsApp session files).
- **Decision**: Docker Container on VPS (Virtual Private Server).
- **Justification**: "Always-on" requirements and filesystem persistence for session cookies make Serverless non-viable.

## ADR-004: Odoo via XML-RPC
- **Context**: Need to talk to Odoo ERP.
- **Decision**: Native `xmlrpc` library.
- **Justification**: Standard Odoo protocol. Avoids third-party wrapper dependencies that might be outdated.
