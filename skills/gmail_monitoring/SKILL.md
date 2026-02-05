---
name: Gmail Email Monitoring
description: Monitor Gmail inbox for Panaversity-related emails and send notifications
version: 1.0.0
category: communication
---

# Gmail Email Monitoring Skill

## Overview

This skill provides Gmail API integration to monitor emails for specific keywords and send notifications when relevant emails are detected.

## Capabilities

- **Email Fetching**: Retrieve unread emails from Gmail
- **Keyword Filtering**: Filter emails by configurable keywords
- **Priority Detection**: Categorize emails by priority (High/Medium/Low)
- **Quiz Detection**: Identify quiz and exam announcements
- **Deadline Detection**: Detect emails with deadlines

## Configuration

### Required Environment Variables

```env
GMAIL_ADDRESS=exellencelinks@gmail.com
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.json
```

### Required Files

- `credentials.json`: OAuth 2.0 credentials from Google Cloud Console
- `token.json`: Auto-generated authentication token (created on first run)

## Usage

### Initialize Email Monitoring

```python
from skills.gmail_monitoring import GmailMonitoringSkill

skill = GmailMonitoringSkill(
    credentials_path="credentials.json",
    token_path="token.json",
    keywords=["Panaversity", "PIAIC", "Quiz"]
)

# Authenticate
skill.authenticate()

# Check for new emails
emails = skill.check_emails()
```

### Filter Relevant Emails

```python
# Get only relevant emails
relevant = skill.filter_relevant_emails(emails)

for email in relevant:
    print(f"Subject: {email['subject']}")
    print(f"Priority: {email['priority']}")
    print(f"Keywords: {email['keywords']}")
```

## API Reference

### Methods

#### `authenticate() -> bool`
Authenticate with Gmail API using OAuth 2.0

**Returns:** `True` if successful, `False` otherwise

#### `fetch_unread_emails(max_results: int = 10) -> List[Dict]`
Fetch unread emails from inbox

**Parameters:**
- `max_results`: Maximum number of emails to fetch

**Returns:** List of email dictionaries

#### `filter_relevant_emails(emails: List[Dict]) -> List[Dict]`
Filter emails by keywords

**Parameters:**
- `emails`: List of email dictionaries

**Returns:** Filtered list of relevant emails

#### `check_emails() -> List[Dict]`
Main method: fetch and filter emails in one call

**Returns:** List of relevant emails

## Examples

### Example 1: Basic Email Check

```python
skill = GmailMonitoringSkill(
    credentials_path="credentials.json",
    token_path="token.json",
    keywords=["PIAIC", "Quiz"]
)

skill.authenticate()
relevant_emails = skill.check_emails()

print(f"Found {len(relevant_emails)} relevant emails")
```

### Example 2: Priority-Based Processing

```python
emails = skill.check_emails()

high_priority = [e for e in emails if e['priority'] == 'high']
for email in high_priority:
    print(f"URGENT: {email['subject']}")
```

## Error Handling

```python
try:
    skill.authenticate()
    emails = skill.check_emails()
except Exception as e:
    print(f"Error: {str(e)}")
```

## Dependencies

- `google-auth>=2.23.0`
- `google-auth-oauthlib>=1.1.0`
- `google-api-python-client>=2.100.0`

## Notes

- First run requires browser authentication
- Token is cached for subsequent runs
- Requires Gmail API enabled in Google Cloud Console
