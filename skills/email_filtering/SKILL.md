---
name: Email Filtering
description: Filter and categorize emails based on keywords and priority
version: 1.0.0
category: utility
---

# Email Filtering Skill

## Overview

This skill provides intelligent email filtering and categorization based on keywords, priority detection, and content analysis.

## Capabilities

- **Keyword Matching**: Filter emails by configurable keywords
- **Priority Detection**: Categorize as High/Medium/Low priority
- **Quiz Detection**: Identify quiz and exam announcements
- **Deadline Detection**: Detect deadline-related emails
- **Smart Categorization**: Comprehensive email analysis

## Usage

```python
from skills.email_filtering import EmailFilteringSkill

skill = EmailFilteringSkill(
    keywords=["Panaversity", "PIAIC", "Quiz"]
)

# Check if email is relevant
is_relevant = skill.is_relevant(
    subject="PIAIC Quiz Tomorrow",
    body="Don't forget the quiz"
)

# Categorize email
category = skill.categorize_email(
    subject="Urgent: Assignment Due",
    body="Submit by Friday"
)

print(category)
# {
#     'is_relevant': True,
#     'keywords': ['assignment'],
#     'is_quiz': False,
#     'has_deadline': True,
#     'priority': 'high'
# }
```

## API Reference

### Methods

#### `is_relevant(subject: str, body: str = "") -> bool`
Check if email contains filter keywords

#### `extract_keywords(subject: str, body: str = "") -> List[str]`
Extract matching keywords from email

#### `detect_quiz_alert(subject: str, body: str = "") -> bool`
Detect if email is about quiz/exam

#### `detect_deadline(subject: str, body: str = "") -> bool`
Detect if email mentions deadline

#### `categorize_email(subject: str, body: str = "") -> Dict`
Comprehensive email categorization

**Returns:**
```python
{
    'is_relevant': bool,
    'keywords': List[str],
    'is_quiz': bool,
    'has_deadline': bool,
    'priority': str  # 'high', 'medium', or 'low'
}
```

## Priority Rules

### High Priority
- Contains: urgent, quiz, exam, deadline, today, tomorrow

### Medium Priority
- Contains: assignment, submission, meeting

### Low Priority
- Everything else

## Dependencies

None (pure Python)
