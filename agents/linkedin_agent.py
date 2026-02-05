"""
LinkedIn Agent - Connects LinkedIn Skill to Odoo
"""
import logging
from typing import Dict, Any, List, Optional
from skills.linkedin_skill.skill import LinkedInSkill
from src.utils.config import Config
# Avoid circular import if possible, but typing is fine
# from agents.odoo_agent import OdooAgent 

logger = logging.getLogger(__name__)

class LinkedInAgent:
    """Agent for LinkedIn interaction and Sync"""
    
    def __init__(self):
        self.skill = LinkedInSkill(enabled=Config.LINKEDIN_ENABLED, headless=True)
        
    def post_update(self, message: str) -> Dict[str, Any]:
        """Post a status update"""
        return self.skill.post_update(message)
    
    def check_notifications(self) -> Dict[str, Any]:
        """Check notifications"""
        return self.skill.check_notifications()

    def sync_leads_to_odoo(self, odoo_agent) -> Dict[str, Any]:
        """
        Scrape LinkedIn messages and sync them to Odoo as leads.
        Args:
            odoo_agent: Instance of OdooAgent
        """
        if not self.skill.enabled:
            return {"success": False, "error": "LinkedIn disabled"}
            
        logger.info("LinkedInAgent: Starting Lead Sync...")
        
        # 1. Scrape
        results = self.skill.scrape_leads()
        if "error" in results:
            return {"success": False, "error": results["error"]}
            
        messages = results.get("messages", [])
        logger.info(f"LinkedInAgent: Found {len(messages)} messages.")
        
        created_count = 0
        errors = []
        
        # 2. Sync to Odoo
        for msg in messages:
            if odoo_agent and odoo_agent.enabled:
                res = odoo_agent.create_lead_from_linkedin(msg)
                if res.get("success"):
                    created_count += 1
                else:
                    errors.append(f"Failed to create lead for {msg.get('sender')}: {res.get('error')}")
            else:
                 logger.warning("LinkedInAgent: Odoo Agent not available/enabled. Skipping sync.")
        
        return {
            "success": True,
            "leads_found": len(messages),
            "leads_synced": created_count,
            "errors": errors
        }
        
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "LinkedInAgent",
            "enabled": self.skill.enabled
        }
