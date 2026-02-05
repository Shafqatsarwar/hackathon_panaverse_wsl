---
name: Email Notifications
description: Send email notifications via SMTP with HTML formatting
version: 1.0.0
category: communication
---

# Email Notifications Skill

## Overview

Send formatted email notifications via SMTP with support for both HTML and plain text.

## Capabilities

- **SMTP Email Sending**: Send emails via SMTP
- **HTML Templates**: Beautiful HTML email formatting
- **Plain Text Fallback**: Plain text alternative
- **Priority Badges**: Color-coded priority indicators
- **Error Handling**: Robust error handling and logging

## Configuration

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=exellencelinks@gmail.com
SMTP_PASSWORD=your_app_password_here
```

## Usage

```python
from skills.email_notifications import EmailNotificationSkill

skill = EmailNotificationSkill(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_username="exellencelinks@gmail.com",
    smtp_password="your_app_password"
)

# Send notification
email_data = {
    'subject': 'PIAIC Quiz Tomorrow',
    'sender': 'instructor@piaic.org',
    'date': '2026-01-23',
    'snippet': 'Quiz on AI fundamentals',
    'keywords': ['PIAIC', 'Quiz'],
    'priority': 'high'
}

success = skill.notify_new_email(
    admin_email="khansarwar1@hotmail.com",
    email_data=email_data
)
```

## API Reference

### Methods

#### `send_email_notification(to_email, subject, body, html=False) -> bool`
Send email notification

#### `notify_new_email(admin_email, email_data) -> bool`
Send formatted notification about new email

#### `format_email_summary(email_data) -> str`
Format email data as plain text

#### `format_email_summary_html(email_data) -> str`
Format email data as HTML

## Dependencies

- `smtplib` (built-in)
- `email` (built-in)
