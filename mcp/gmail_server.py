"""
Gmail MCP Server for Panaversity Student Assistant
Provides Gmail tools via Model Context Protocol
"""
import os
import sys
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class GmailMCPServer:
    """MCP Server for Gmail operations"""
    
    def __init__(self):
        self.name = "gmail"
        self.version = "1.0.0"
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available Gmail tools"""
        return [
            {
                "name": "check_emails",
                "description": "Check for new Panaversity-related emails",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "max_results": {
                            "type": "number",
                            "description": "Maximum number of emails to fetch",
                            "default": 10
                        }
                    }
                }
            },
            {
                "name": "send_notification",
                "description": "Send email notification to admin",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body"
                        }
                    },
                    "required": ["subject", "body"]
                }
            }
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        if name == "check_emails":
            return self._check_emails(arguments.get("max_results", 10))
        elif name == "send_notification":
            return self._send_notification(
                arguments["subject"],
                arguments["body"]
            )
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def _check_emails(self, max_results: int) -> Dict[str, Any]:
        """Check for new emails"""
        try:
            from agents.email_agent import EmailAgent
            from src.utils.config import Config
            
            agent = EmailAgent(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH,
                filter_keywords=Config.FILTER_KEYWORDS
            )
            
            if not agent.authenticate():
                return {"error": "Failed to authenticate with Gmail"}
            
            emails = agent.check_emails()
            
            return {
                "success": True,
                "count": len(emails),
                "emails": emails
            }
        
        except Exception as e:
            logger.error(f"Error checking emails: {str(e)}")
            return {"error": str(e)}
    
    def _send_notification(self, subject: str, body: str) -> Dict[str, Any]:
        """Send notification email"""
        try:
            from src.utils.notifications import NotificationService
            from src.utils.config import Config
            
            service = NotificationService(
                smtp_server=Config.SMTP_SERVER,
                smtp_port=Config.SMTP_PORT,
                smtp_username=Config.SMTP_USERNAME,
                smtp_password=Config.SMTP_PASSWORD
            )
            
            success = service.send_email_notification(
                to_email=Config.ADMIN_EMAIL,
                subject=subject,
                body=body
            )
            
            return {"success": success}
        
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return {"error": str(e)}

if __name__ == "__main__":
    # MCP server entry point
    server = GmailMCPServer()
    logger.info(f"Gmail MCP Server v{server.version} started")
