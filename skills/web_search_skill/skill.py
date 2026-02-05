"""
Web Search Skill using a simple requests-based approach.
No asyncio conflicts. Works on Windows.
"""
import logging
import requests
from typing import List, Dict
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

class WebSearchSkill:
    """Skill for performing web searches using a simple HTTP approach."""
    
    def __init__(self):
        self.enabled = True
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform a web search using DuckDuckGo Instant Answer API.
        This is a simple, free, and Windows-compatible approach.
        """
        try:
            logger.info(f"WebSearchSkill: Searching for '{query}'")
            
            # Use DuckDuckGo Instant Answer API (free, no auth required)
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1"
            
            response = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Abstract (main answer)
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Answer"),
                    "body": data.get("Abstract"),
                    "href": data.get("AbstractURL", "#")
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results-1]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text", "")[:80],
                        "body": topic.get("Text", ""),
                        "href": topic.get("FirstURL", "#")
                    })
            
            # Fallback if no results
            if not results:
                results.append({
                    "title": f"Search results for: {query}",
                    "body": f"No instant answers found for '{query}'. The user may need to search manually or try a more specific query.",
                    "href": f"https://duckduckgo.com/?q={quote_plus(query)}"
                })
            
            logger.info(f"WebSearchSkill: Found {len(results)} results")
            return results[:max_results]
            
        except requests.RequestException as e:
            logger.error(f"WebSearchSkill: Network error: {e}")
            return [{
                "title": "Search Error",
                "body": f"Could not perform search due to network error: {str(e)}",
                "href": "#"
            }]
        except Exception as e:
            logger.error(f"WebSearchSkill: Error: {e}")
            return [{
                "title": "Search Error",
                "body": f"Search failed: {str(e)}",
                "href": "#"
            }]

    def get_tool_definition(self):
        """Return the Gemini tool definition"""
        return {
            "function_declarations": [
                {
                    "name": "web_search",
                    "description": "Search the web for information. Use this for general knowledge, current events, weather, news, or looking up facts.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query."
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
