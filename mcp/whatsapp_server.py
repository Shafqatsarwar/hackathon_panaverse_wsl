"""
WhatsApp MCP Server for Panaversity Student Assistant
Provides WhatsApp messaging tools via Model Context Protocol
"""
import os
import logging
from typing import Any, Dict, List
from src.utils.config import Config
from skills.whatsapp_skill.skill import WhatsAppSkill

logger = logging.getLogger(__name__)

class WhatsAppMCPServer:
    """MCP Server for WhatsApp operations"""
    
    def __init__(self):
        self.name = "whatsapp"
        self.version = "2.0.0"
        session_path = os.path.abspath("./whatsapp_session")
        logger.info(f"MCP Server: Using WhatsApp Session at {session_path}")
        
        self.skill = WhatsAppSkill(
            enabled=Config.WHATSAPP_ENABLED,
            headless=True,  # Force Headed to match persisted session type
            session_dir=session_path
        )
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available WhatsApp tools"""
        return [
            {
                "name": "send_message",
                "description": "Send a WhatsApp message to a specific number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "string",
                            "description": "Phone number with country code (e.g., +923001234567)"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message content"
                        }
                    },
                    "required": ["number", "message"]
                }
            },
            {
                "name": "check_messages",
                "description": "Check WhatsApp messages, optionally filtered by keywords",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional keywords to filter messages"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to check (default: 20)"
                        }
                    }
                }
            },
            {
                "name": "check_status",
                "description": "Check status of WhatsApp connection",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        if name == "send_message":
            return self._send_message(arguments["number"], arguments["message"])
        elif name == "check_messages":
            keywords = arguments.get("keywords", None)
            limit = arguments.get("limit", 20)
            return self._check_messages(keywords, limit)
        elif name == "check_status":
            return self._check_status()
        else:
            return {"error": f"Unknown tool: {name}"}
            
    def _send_message(self, number: str, message: str) -> Dict[str, Any]:
        """Send WhatsApp message using the actual skill"""
        if not Config.WHATSAPP_ENABLED:
             return {"success": False, "error": "WhatsApp integration is disabled in .env. Set WHATSAPP_ENABLED=true"}
             
        logger.info(f"MCP Server: Sending WhatsApp to {number}: {message}")
        
        try:
            result = self.skill.send_message(number, message)
            logger.info(f"MCP Server: WhatsApp result: {result}")
            return result
        except Exception as e:
            logger.error(f"MCP Server: WhatsApp error: {e}")
            return {"success": False, "error": str(e)}
    
    def _check_messages(self, keywords: List[str] = None, limit: int = 20) -> Dict[str, Any]:
        """Check WhatsApp messages using the actual skill"""
        if not Config.WHATSAPP_ENABLED:
            return {"error": "WhatsApp integration is disabled in .env. Set WHATSAPP_ENABLED=true"}
        
        logger.info(f"MCP Server: Checking WhatsApp messages with keywords: {keywords}")
        
        try:
            messages = self.skill.check_messages(keywords=keywords, limit=limit)
            logger.info(f"MCP Server: Found {len(messages)} messages")
            return {"success": True, "messages": messages, "count": len(messages)}
        except Exception as e:
            logger.error(f"MCP Server: WhatsApp check error: {e}")
            return {"success": False, "error": str(e)}
        
    def _check_status(self) -> Dict[str, Any]:
        return {
            "enabled": Config.WHATSAPP_ENABLED,
            "admin_number": Config.ADMIN_WHATSAPP,
            "skill_enabled": self.skill.enabled
        }

if __name__ == "__main__":
    server = WhatsAppMCPServer()
    logger.info(f"WhatsApp MCP Server v{server.version} started")
