# Architecture Decision Records (ADR) 🏛️

## ADR-001: Use of Browser Automation for WhatsApp/LinkedIn
- **Status**: Accepted
- **Context**: Official APIs for WhatsApp Business require Meta verification/payment. LinkedIn API has strict quotas. The user requested a "Free" solution for personal/student use.
- **Decision**: Used **Playwright** (Headless Browser) to automate the Web versions of these services.
- **Consequence**:
    - **Pros**: Free, works with personal accounts, no API approval needed.
    - **Cons**: Heavier resource usage (requires Chrome), session management (QR codes) required, harder to deploy on Serverless (Vercel).

## ADR-002: NestAsyncio Patching
- **Status**: Accepted
- **Context**: The `ChatAgent` runs inside FastAPI's async event loop. Calling `asyncio.run()` (used by Playwright wrapper) inside an existing loop raises a `RuntimeError`.
- **Decision**: Installed `nest_asyncio` and created a `_run_async` helper to detect the running loop and "nest" the execution.
- **Consequence**: Allows synchronous tools (`check_whatsapp`) to call async code safely without blocking the server permanently.

## ADR-003: Deployment Target (VPS/Docker vs Serverless)
- **Status**: Accepted
- **Context**: User initially asked for Vercel (Free), but Vercel cannot run persistent browser sessions needed for ADR-001.
- **Decision**: Recommended **Docker / VPS** (e.g., Oracle Free Tier).
- **Consequence**: Ensures the "Always On" requirement for listening to messages is met.

## ADR-004: Frontend Tech Stack
- **Status**: Accepted
- **Decision**: Used **Next.js 14** (App Router) + **Tailwind CSS v4**.
- **Reason**: Performance, modern React patterns, and rapid UI development with utility classes.
