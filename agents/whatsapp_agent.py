"""
WhatsApp Agent - Using Baileys (No Browser Automation)
"""
import logging
from typing import Dict, Any, List
from skills.whatsapp_baileys.skill import WhatsAppBaileysSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class WhatsAppAgent:
    """Agent for WhatsApp communication using Baileys microservice"""
    
    def __init__(self):
        self.skill = WhatsAppBaileysSkill(
            base_url=Config.WHATSAPP_BAILEYS_URL if hasattr(Config, 'WHATSAPP_BAILEYS_URL') else "http://localhost:3001/api"
        )
        
    def send_alert(self, message: str) -> Dict[str, Any]:
        """Send an alert to the admin"""
        admin_number = Config.ADMIN_WHATSAPP
        return self.skill.send_message(admin_number, message)

    def send_message(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send a message to any number"""
        return self.skill.send_message(to_number, message)
        
    def get_unread_messages(self, limit: int = 5, check_archived: bool = False) -> List[Dict]:
        """Get recent chats"""
        try:
            chats = self.skill.get_chats(limit=limit)
            return chats.get("chats", [])
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        """Get WhatsApp connection status"""
        try:
            status = self.skill.get_status()
            return {
                "name": "WhatsAppAgent (Baileys)",
                "connected": status.get("connected", False),
                "enabled": True
            }
        except Exception as e:
            return {
                "name": "WhatsAppAgent (Baileys)",
                "connected": False,
                "enabled": True,
                "error": str(e)
            }
    
    def is_connected(self) -> bool:
        """Check if WhatsApp is connected"""
        return self.skill.is_connected()
