---
name: linkedin_skill
description: Skill for LinkedIn interactions (posting updates, checking notifications)
---

# LinkedIn Skill

This skill handles interaction with LinkedIn.

## Capabilities

- Post status updates
- Check notifications (simulated)

## Usage

```python
from skills.linkedin_skill.skill import LinkedInSkill

skill = LinkedInSkill()
skill.post_update("Hello network!")
```

## Configuration

Requires `LINKEDIN_ENABLED=true` in `.env`.
