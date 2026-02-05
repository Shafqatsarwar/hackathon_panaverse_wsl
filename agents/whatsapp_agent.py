"""
WhatsApp Agent
"""
import logging
from typing import Dict, Any
from skills.whatsapp_skill.skill import WhatsAppSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class WhatsAppAgent:
    """Agent for WhatsApp communication"""
    
    def __init__(self):
        import os
        from pathlib import Path
        session_path = os.path.abspath("./whatsapp_session")
        self.skill = WhatsAppSkill(
            enabled=Config.WHATSAPP_ENABLED, 
            headless=True, # Must match Watcher config to share session
            session_dir=session_path
        )
        
    def send_alert(self, message: str) -> Dict[str, Any]:
        """Send an alert to the admin"""
        admin_number = Config.ADMIN_WHATSAPP
        return self.skill.send_message(admin_number, message)

    def send_message(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send a message to any number"""
        return self.skill.send_message(to_number, message)
        
    def get_unread_messages(self, limit: int = 5, check_archived: bool = False) -> list:
        """Get unread messages, optionally filtered by config keywords"""
        # User requested specific keywords: Panaversity, PIAIC, etc.
        # We'll use the ones from Config + explicit ones if needed, 
        # but for now rely on Config which user implied they updated/we should use.
        keywords = Config.FILTER_KEYWORDS
        return self.skill.check_messages(keywords=keywords, limit=limit, check_archived=check_archived)

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "WhatsAppAgent",
            "enabled": self.skill.enabled
        }
