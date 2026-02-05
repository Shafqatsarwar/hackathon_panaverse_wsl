"""
LinkedIn MCP Server for Panaversity Student Assistant
Provides LinkedIn tools via Model Context Protocol
"""
from skills.linkedin_skill.skill import LinkedInSkill
import logging
from typing import Any, Dict, List
from src.utils.config import Config

logger = logging.getLogger(__name__)

class LinkedInMCPServer:
    """MCP Server for LinkedIn operations"""
    
    def __init__(self):
        self.name = "linkedin"
        self.version = "1.0.0"
        self.skill = LinkedInSkill(enabled=Config.LINKEDIN_ENABLED, headless=True)
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available LinkedIn tools"""
        return [
            {
                "name": "post_update",
                "description": "Post a status update to LinkedIn",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Text content of the post"
                        }
                    },
                    "required": ["content"]
                }
            },
            {
                "name": "check_notifications",
                "description": "Check recent LinkedIn notifications",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "number",
                            "default": 5
                        }
                    }
                }
            }
        ]
        
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        if name == "post_update":
            return self._post_update(arguments["content"])
        elif name == "check_notifications":
            return self._check_notifications(arguments.get("limit", 5))
        else:
            return {"error": f"Unknown tool: {name}"}
            
    def _post_update(self, content: str) -> Dict[str, Any]:
        """Post update logic"""
        if not self.skill.enabled:
            return {"success": False, "error": "LinkedIn integration is disabled"}
            
        logger.info(f"Posting to LinkedIn: {content[:50]}...")
        return self.skill.post_update(content)
        
    def _check_notifications(self, limit: int) -> Dict[str, Any]:
        """Check notifications logic"""
        if not self.skill.enabled:
            return {"success": False, "error": "LinkedIn integration is disabled"}
            
        # LinkedInSkill.check_notifications returns the scraping result
        return self.skill.check_notifications()

if __name__ == "__main__":
    server = LinkedInMCPServer()
    logger.info(f"LinkedIn MCP Server v{server.version} started")
