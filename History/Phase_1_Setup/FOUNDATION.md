# Phase 1: Foundation & Core Agents 🏗️

**Timeline**: Start of project to basic prototype.
**Focus**: Setting up the "Brain" (Gemini) and the "Body" (FastAPI/Next.js).

## 1. The Stack
- **Backend**: Python FastAPI. Lightweight, fast, async-native.
- **Frontend**: Next.js 14 + Tailwind. React-based for dynamic chat UI.
- **AI**: Google Gemini (via `google-generativeai` SDK).

## 2. Core Agent Design
The system uses a "Tool-Use" architecture.
- **ChatAgent**: The orchestrator. It receives user text, decides which tool to call.
- **Tools**: initialized in `__init__` and passed to Gemini as function declarations.

### Implementation Details
- `src/agents/main_agent.py`: Background worker that triggers periodic checks.
- `src/agents/chat_agent.py`: Real-time session handler. Supports streaming responses.

## 3. Initial Challenges
- **Startup Errors**: Path resolution issues in `start.bat`. Fixed by using absolute/relative path handling correctly.
- **UI**: Initial UI was basic HTML. Upgraded to Next.js in this phase.
