---
name: chatbot_skill
description: Skill for Generative AI interactions (wrapping Google Gemini)
---

# Chatbot Skill

This skill allows agents to generate text and responses using Google's Gemini models.

## Capabilities

- Generate content (chat)
- Stream content
- Manage chat sessions

## Usage

```python
from skills.chatbot_skill.skill import ChatbotSkill

skill = ChatbotSkill(api_key="...")
response = skill.generate_response("Hello!")
```

## Configuration

Requires `GOOGLE_API_KEY` in `.env`.
