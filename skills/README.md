# Skills

This folder contains reusable skills that agents can use to perform specific tasks.

## Skill Structure

Each skill has:
- `SKILL.md`: Documentation with usage examples
- `skill_name.py`: Implementation
- Dependencies and configuration

## Available Skills

### 1. Gmail Monitoring (`gmail_monitoring/`)
- **Purpose**: Monitor Gmail inbox via API
- **Capabilities**: Fetch emails, authenticate, filter by keywords
- **Used by**: EmailAgent

### 2. Email Filtering (`email_filtering/`)
- **Purpose**: Filter and categorize emails
- **Capabilities**: Keyword matching, priority detection, quiz/deadline detection
- **Used by**: EmailAgent

### 3. Email Notifications (`email_notifications/`)
- **Purpose**: Send email notifications via SMTP
- **Capabilities**: HTML emails, plain text fallback, priority badges
- **Used by**: NotificationAgent

## Creating New Skills

1. Create folder: `skills/skill_name/`
2. Add `SKILL.md` with documentation
3. Add `skill_name.py` with implementation
4. Update this README

## Skill Guidelines

- **Single Responsibility**: Each skill does one thing well
- **Reusable**: Can be used by multiple agents
- **Well-Documented**: Clear SKILL.md with examples
- **Testable**: Easy to test independently
