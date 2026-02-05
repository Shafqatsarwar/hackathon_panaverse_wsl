"""
Odoo MCP Server
Model Context Protocol wrapper for Odoo CRM Skill
"""
import logging
from typing import Any, Dict, List
from skills.odoo_skill.skill import OdooSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class OdooMCPServer:
    """MCP Server for Odoo ERP Operations"""
    
    def __init__(self):
        self.name = "odoo"
        self.version = "1.0.0"
        self.skill = OdooSkill()
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available Odoo tools"""
        return [
            {
                "name": "create_lead",
                "description": "Create a new lead/opportunity in Odoo CRM",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name/Subject of the lead"
                        },
                        "email": {
                            "type": "string",
                            "description": "Contact email address"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description or notes"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_recent_leads",
                "description": "Get a list of recent leads from CRM",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Max number of leads to fetch",
                            "default": 5
                        }
                    }
                }
            },
            {
                "name": "search_leads",
                "description": "Search for leads by keyword",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Keyword to search in lead names"
                        }
                    },
                    "required": ["keyword"]
                }
            }
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Odoo tool"""
        if not self.skill.enabled:
            return {"success": False, "error": "Odoo integration is disabled."}

        if name == "create_lead":
            return self.skill.create_lead(
                name=arguments.get("name"),
                email_from=arguments.get("email", "unknown@example.com"),
                description=arguments.get("description", "")
            )
            
        elif name == "get_recent_leads":
            leads = self.skill.get_leads(limit=arguments.get("limit", 5))
            return {"success": True, "leads": leads}

        elif name == "search_leads":
            # Assuming get_leads supports a domain or filter, otherwise we fetch and filter in python
            # For simplicity, let's fetch more and filter here if the skill doesn't support search yet
            # Ideally update skill to support search.
            all_leads = self.skill.get_leads(limit=50) 
            keyword = arguments.get("keyword", "").lower()
            filtered = [l for l in all_leads if keyword in str(l.get('name', '')).lower()]
            return {"success": True, "leads": filtered, "count": len(filtered)}
            
        else:
            return {"error": f"Unknown tool: {name}"}

if __name__ == "__main__":
    server = OdooMCPServer()
    logger.info(f"Odoo MCP Server v{server.version} started")
