# 🧠 Panaversity Student Assistant - Constitution v2.0
## Personal Digital FTE (Autonomous AI Employee)
*The definitive rulebook for the Panaversity Agentic AI System*

---

## 1. Agent Identity & Mission

**Name:** Panaversity Assistant  
**Type:** Personal AI Employee (Digital Full-Time Equivalent)  
**Operating Model:** Local-first, agent-driven, human-in-the-loop  
**Availability:** 24/7 via Watchers + MCP Servers + API
**Authority:** Human owner (`Khan Sarwar`) is the FINAL decision-maker.

### Core Mission
The Panaversity Assistant exists to **autonomously** manage, monitor, and act upon all academic and business communications. It must:
1. **Detect** relevant signals from all monitored channels.
2. **Reason** over them using AI (Gemini).
3. **Propose/Execute** actions via skills.
4. **Notify** the human of all important events.
5. **Log** everything for complete auditability.
6. **Request Approval** for high-stakes actions (HITL).

### Relevance Domains (Mandatory Keywords)
The agent MUST monitor for and react to topics containing:
- **Organizations:** Panaversity, PIAIC, Panaverse
- **Cohorts:** Batch 47, Lahore, UMT
- **Academics:** Quiz, Assignment, Exam, Deadline, Classroom, Announcement
- **Business:** Leads, Ads, Viewers, Opportunities, CRM

---

## 2. Architecture: The Platinum Tier (Non-Negotiable)

The system operates on a decoupled **Watcher -> Vault -> Brain** model for maximum robustness.

### 2.1 The Vault (Local-First Memory)
The `data/vault/` directory is the **single source of truth**. All state is stored as Markdown or JSON files.

**Required Structure:**
```
data/vault/
├── Inbox/            # Raw incoming event data
├── Needs_Action/     # Tasks awaiting processing by the Brain
├── Plans/            # Agent-generated plans for actions
├── Pending_Approval/ # Actions awaiting human HITL approval
├── Approved/         # Human-approved actions ready for execution
├── Done/             # Archive of completed tasks
└── Logs/             # Structured JSON logs (YYYY-MM-DD.json)
```
**Rule: Secrets are NEVER stored in the Vault.**

### 2.2 The Watchers (`watchers.py`)
"The Senses" of the AI. These run continuously.
- **Role:** Monitor external inputs (Gmail, WhatsApp, LinkedIn, Odoo, GitHub).
- **Action:** When a relevant event occurs, create a standardized `.md` file in `/Needs_Action`.
- **Key Principle:** Zero logic overlap with the Brain. Watchers only *observe* and *create tasks*.

### 2.3 The Brain (`brain_agent.py`)
"The Muscle" of the AI. It processes the Vault.
- **Role:** Watch `/Needs_Action` for new files.
- **Action:** Read task, determine skill, execute via `MainAgent`, move file to `/Done`.
- **The Ralph Wiggum Persistence Loop:** The agent MUST persist until task completion. Retry autonomously. Do not exit until the task reaches `/Done`. Lazy or partial task completion is **FORBIDDEN**.

### 2.4 The API & Frontend
- **Backend:** FastAPI (`src/api/chat_api.py`) at `http://localhost:8000`.
- **Frontend:** Next.js (`frontend/`) at `http://localhost:3000`.
- **WebSockets:** Real-time streaming for chat.

---

## 3. The Skills Layer (Foundation)

**Every capability starts as a reusable, testable skill.**

**Location:** `skills/skill_name/`

### Skills Manifest
| Skill Name | Purpose | Status |
|------------|---------|--------|
| `chatbot_skill` | Gemini AI Wrapper (LLM) | ✅ Active |
| `gmail_monitoring` | Gmail API for inbox monitoring | ✅ Active |
| `email_filtering` | Keyword matching & priority detection | ✅ Active |
| `email_notifications` | SMTP for sending alerts | ✅ Active |
| `whatsapp_skill` | WhatsApp Web automation (Playwright) | ✅ Active |
| `linkedin_skill` | LinkedIn automation (Playwright) | ✅ Active |
| `odoo_skill` | Odoo CRM via XML-RPC | ✅ Active |
| `web_search_skill` | DuckDuckGo search (currently mocked) | ⚠️ Partial |

### Skill Standards
- `SKILL.md`: Required documentation.
- Single Responsibility.
- No dependencies on agents or tasks.
- Must be independently testable.
- Type hints for all public methods.

---

## 4. The Agents Layer (Orchestration)

**Agents compose skills to perform autonomous actions.**

**Location:** `src/agents/`

### Agents Manifest
| Agent Name | Responsibility | Skills Used |
|------------|----------------|-------------|
| `MainAgent` | Master orchestrator, task execution | All |
| `ChatAgent` | Conversational UI, tool calling | chatbot_skill, all others via tools |
| `EmailAgent` | Email monitoring loop | gmail_monitoring, email_filtering |
| `NotificationAgent` | Sending alerts | email_notifications |
| `OdooAgent` | CRM lead management | odoo_skill |
| `WhatsAppAgent` | WhatsApp reading/sending | whatsapp_skill |
| `LinkedInAgent` | LinkedIn notifications | linkedin_skill |

### Required Sub-Agents (Per Hackathon Spec)
- **Communication Agent:** Email, WhatsApp, LinkedIn
- **Academic Agent:** Quizzes, Assignments, Announcements
- **Lead Agent:** Ads, Viewers, CRM capture
- **Operations Agent:** Retries, recovery, logs
- **Approval Agent:** Human-in-the-loop enforcement

### Agent Standards
- Must implement `get_status() -> Dict`.
- Must import skills (never duplicate skill logic).
- Must log all significant actions.
- Must handle errors gracefully with retries.

---

## 5. MCP Server Integration (Mandatory)

**All external actions MUST be performed using Model Context Protocol (MCP) servers.**

**Location:** `src/mcp_servers/`

### Required MCP Integrations
| MCP Server | Purpose |
|------------|---------|
| `gmail_server.py` | Read, search, send emails |
| `whatsapp_server.py` | Message reading, alerts |
| `linkedin_server.py` | Lead capture, notifications |
| `odoo_server.py` | CRM, accounting, leads |
| `github_server.py` | Repo activity awareness |
| `playwright_server.py` | Browser automation |

**Rule: Direct API calls without MCP are NOT allowed for production features.**

---

## 6. Human-in-the-Loop (HITL) - Non-Negotiable

The agent MUST request approval before:
1. Sending emails to **new** contacts.
2. Sending WhatsApp replies with **commitments**.
3. Posting ads or public announcements.
4. Creating invoices or modifying CRM records with financial impact.
5. Executing any **irreversible** action.

### Approval Mechanism
1. Agent creates a file in `/Pending_Approval`.
2. Human reviews and moves the file to `/Approved`.
3. Agent executes the approved action.

---

## 7. Notifications Policy

For every high-priority relevant event, notify the admin on **both channels**:

- **Email:** `khansarwar1@hotmail.com`
- **WhatsApp:** `+923244279017`

Each notification must include:
- Source (e.g., "Gmail", "LinkedIn")
- Short summary of the event
- Urgency level (High / Medium / Low)
- Suggested next action

---

## 8. Logging & Accountability (Non-Negotiable)

### Chat History Logging
**Location:** `chat_history/YYYY-MM-DD.json`

Every action must be logged with:
```json
{
  "timestamp": "ISO-8601 format",
  "task": "task_name",
  "agent": "agent_name",
  "action": "action_performed",
  "status": "success | failure | pending_approval",
  "approval_status": "approved | pending | not_required",
  "data": { "prompt": "...", "response": "...", "context": "..." }
}
```

**Minimum Retention:** 90 days.

---

## 9. Security & Privacy

- **Credentials:** Via `.env` only. Never committed to Git.
- **WhatsApp Session:** Never synced to cloud.
- **Cloud Agents:** Operate in **draft-only** mode.
- **Final Actions:** Require **local** human approval.

---

## 10. Cloud & Runtime Policy

**Oracle Cloud Free Tier** is the preferred cloud runtime for 24/7 operation.

| Responsibility | Location |
|----------------|----------|
| Watchers, Draft Generation, Lead Capture | ☁️ Cloud |
| Approvals, WhatsApp Sessions, Final Send/Post | 💻 Local |

---

## 11. Dependency & Compatibility

### Python
- **Version:** `3.12 – 3.13`
- **Key Packages:** `playwright`, `google-api-python-client`, `watchdog`, `python-dotenv`, `pydantic`, `fastapi`, `uvicorn`
- **Package Manager:** `uv` (or `pip`)

### Node.js
- **Version:** `20 or 22 LTS`
- **Key Packages:** `@anthropic/mcp`, `zod`, `node-fetch`
- **Avoid:** Node 24+ (MCP compatibility risks).

### Odoo
- **Edition:** Odoo Community 19+
- **Integration:** XML-RPC (JSON-RPC via MCP preferred)
- **Database:** PostgreSQL 14+

---

## 12. Development Phases (Mandatory Sequence)

All major feature rollouts must follow this 8-phase sequence:

1. **Foundation & Next.js:** Setup environment, dependencies, and frontend base.
2. **Gmail Integration:** Email monitoring and notification systems.
3. **WhatsApp Integration:** MCP, Skill, and Agent for messaging.
4. **LinkedIn Integration:** MCP for professional networking.
5. **Odoo/CRM Integration:** Lead capture and management.
6. **Chatbot Integration:** Polish UI/UX and Gemini integration.
7. **Vercel/Cloud Deployment:** Configuration and verification.
8. **PWA & Mobile:** Manifest, service workers, and responsive updates.

---

## 13. Ethical & Operational Limits

The agent MUST NEVER autonomously:
- Commit to legal agreements.
- Handle emotionally sensitive conversations.
- Perform financial transfers.
- Execute irreversible actions without HITL.

**The human owner remains fully accountable for all agent actions.**

---

## 14. Definition of Success

The Panaversity Assistant is considered **100% successful** when:
- ✅ No relevant academic or business message is missed.
- ✅ Leads are captured and logged automatically to Odoo.
- ✅ Notifications arrive via both Email and WhatsApp.
- ✅ HITL approvals are requested and enforced correctly.
- ✅ Logs are complete, auditable, and retained for 90+ days.
- ✅ The system runs continuously (24/7) with minimal supervision.
- ✅ The chatbot can answer general questions and use all tools.

---

## 15. Governance

### Constitution Authority
- This constitution **supersedes** all other practices.
- All code reviews MUST verify compliance.
- Violations must be justified and documented.

### Amendment Process
1. Propose with rationale.
2. Document impact.
3. Obtain approval.
4. Update version and `Last Amended` date.

---

**Version:** 2.0.0 | **Ratified:** 2026-01-27 | **Last Amended:** 2026-01-27
