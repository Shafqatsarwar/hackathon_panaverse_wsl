# Web Search Skill

## Purpose
Provides web search capabilities for the AI assistant to answer questions about current events, weather, news, and general knowledge.

## Usage
```python
from skills.web_search_skill.skill import WebSearchSkill

skill = WebSearchSkill()
results = skill.search("What is Panaversity?")
```

## Methods
| Method | Description |
|--------|-------------|
| `search(query, max_results=5)` | Returns list of search results with title, body, href |
| `get_tool_definition()` | Returns Gemini function calling schema |

## Integration
Used by `ChatAgent` as a tool for answering general questions.

## Notes
- Uses DuckDuckGo Instant Answer API (free, no auth required)
- Works on Windows without asyncio conflicts
- Returns structured results suitable for AI consumption
