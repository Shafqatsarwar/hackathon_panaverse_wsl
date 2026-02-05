# Tasks

This folder contains task definitions for the assistant.

## Task Structure

Each task is a JSON file defining:
- Task name
- Description
- Schedule
- Agent assignments
- Success criteria

## Example Task

```json
{
  "name": "email_monitoring",
  "description": "Monitor Gmail for Panaversity emails",
  "schedule": "every 15 minutes",
  "agents": ["EmailAgent", "NotificationAgent"],
  "success_criteria": {
    "emails_checked": true,
    "notifications_sent": true
  }
}
```

## Current Tasks

- `email_monitoring.json`: Monitor and notify about emails
- (More tasks coming in Phase 2 & 3)
