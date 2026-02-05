# Project Architecture

## Overview

Panaversity Student Assistant follows a **Skills → Agents → Tasks** architecture pattern.

## Architecture Layers

### 1. Skills (Bottom Layer)
**Purpose**: Reusable capabilities that can be used by any agent

**Location**: `skills/`

**Current Skills**:
- `gmail_monitoring`: Gmail API integration
- `email_filtering`: Email categorization and keyword matching
- `email_notifications`: SMTP email sending

**Characteristics**:
- Self-contained
- Well-documented (SKILL.md)
- Testable independently
- No dependencies on agents

### 2. Agents (Middle Layer)
**Purpose**: Use skills to perform specific actions

**Location**: `src/agents/`

**Current Agents**:
- `EmailAgent`: Uses gmail_monitoring + email_filtering skills
- `NotificationAgent`: Uses email_notifications skill
- `MainAgent`: Orchestrates EmailAgent + NotificationAgent

**Characteristics**:
- Compose multiple skills
- Maintain state
- Provide status reporting
- Handle errors gracefully

### 3. Tasks (Top Layer)
**Purpose**: Define what needs to be done and coordinate agents

**Location**: `tasks/`

**Current Tasks**:
- `email_monitoring.json`: Monitor Gmail and send notifications

**Task Definition**:
```json
{
  "name": "email_monitoring",
  "agents": ["EmailAgent", "NotificationAgent"],
  "skills_required": ["gmail_monitoring", "email_filtering", "email_notifications"],
  "schedule": "every 15 minutes",
  "success_criteria": {...}
}
```

### 4. Chat History (Logging Layer)
**Purpose**: Record all activities for audit and analytics

**Location**: `chat_history/`

**Format**: Daily JSON files (`YYYY-MM-DD.json`)

**Example**:
```json
[
  {
    "timestamp": "2026-01-23T00:05:00",
    "task": "email_check",
    "data": {
      "status": "completed",
      "emails_found": 2
    }
  }
]
```

## Data Flow

```
1. MainAgent.check_emails()
   ↓
2. EmailAgent.check_emails()
   ↓
3. GmailMonitoringSkill.check_emails()
   ↓
4. EmailFilteringSkill.categorize_email()
   ↓
5. NotificationAgent.send_email_alert()
   ↓
6. EmailNotificationSkill.notify_new_email()
   ↓
7. MainAgent._log_to_chat_history()
```

## Benefits

1. **Modularity**: Skills can be reused across agents
2. **Testability**: Each layer can be tested independently
3. **Maintainability**: Clear separation of concerns
4. **Scalability**: Easy to add new skills/agents/tasks
5. **Auditability**: Complete chat history of all activities

## Adding New Capabilities

### Add a New Skill
1. Create `skills/skill_name/`
2. Add `SKILL.md` documentation
3. Add `skill_name.py` implementation
4. Update `skills/README.md`

### Add a New Agent
1. Create `src/agents/agent_name.py`
2. Import and use relevant skills
3. Implement `get_status()` method
4. Update `main_agent.py` to coordinate

### Add a New Task
1. Create `tasks/task_name.json`
2. Define agents, skills, schedule
3. Add task execution method to MainAgent
4. Update scheduler

## File Organization

```
skills/
  skill_name/
    SKILL.md          # Documentation
    skill_name.py     # Implementation

src/agents/
  agent_name.py       # Agent using skills

tasks/
  task_name.json      # Task definition

chat_history/
  YYYY-MM-DD.json     # Daily logs
```
