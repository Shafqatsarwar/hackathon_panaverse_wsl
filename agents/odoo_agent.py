"""
Odoo Agent
"""
import logging
from typing import Dict, Any
from skills.odoo_skill.skill import OdooSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class OdooAgent:
    """Agent for Odoo ERP interaction"""
    
    def __init__(self):
        self.skill = OdooSkill()
        self.enabled = self.skill.enabled
        
    def create_lead_from_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a CRM lead from an email"""
        if not self.enabled:
            return {"success": False, "error": "Odoo disabled"}
            
        subject = email_data.get("subject", "No Subject")
        sender = email_data.get("sender", "Unknown")
        body = email_data.get("body", "")
        
        description = f"Generated from Email.\nSender: {sender}\n\nBody:\n{body}"
        
        logger.info(f"OdooAgent: Creating Lead for '{subject}'...")
        
        return self.skill.create_lead(
            name=subject,
            email_from=sender,
            description=description
        )
        
    def create_lead_from_linkedin(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a CRM lead from a LinkedIn message"""
        if not self.enabled:
            return {"success": False, "error": "Odoo disabled"}
            
        sender = message_data.get("sender", "Unknown")
        content = message_data.get("content", "")
        
        description = f"Source: LinkedIn Message\n\nContent:\n{content}"
        
        logger.info(f"OdooAgent: Creating LinkedIn Lead from '{sender}'...")
        return self.skill.create_lead(
            name=f"LinkedIn Inquiry: {sender}",
            email_from="linkedin@placeholder.com", 
            description=description
        )
        
    def create_lead(self, name: str, email: str, description: str) -> Dict[str, Any]:
        """Create a generic lead (proxy to skill)"""
        if not self.enabled: return {"success": False, "error": "Disabled"}
        return self.skill.create_lead(name, email, description)

    def get_recent_leads(self, limit: int = 5) -> Dict[str, Any]:
        """Get recent leads (proxy to skill)"""
        if not self.enabled: return []
        return self.skill.get_leads(limit)
        """Create a generic lead (proxy to skill)"""
        if not self.enabled: return {"success": False, "error": "Disabled"}
        return self.skill.create_lead(name, email, description)

    def get_recent_leads(self, limit: int = 5) -> Dict[str, Any]:
        """Get recent leads (proxy to skill)"""
        if not self.enabled: return []
        return self.skill.get_leads(limit)

    def get_recent_leads_summary(self) -> str:
        """Get a text summary of recent leads for the chatbot"""
        if not self.enabled:
            return "Odoo Integration is disabled."
            
        leads = self.skill.get_leads(limit=5)
        if not leads:
            return "No recent leads found in Odoo."
            
        summary = "Recent Odoo CRM Leads:\n"
        for lead in leads:
            name = lead.get('name', 'N/A')
            contact = lead.get('contact_name') or lead.get('email_from') or 'Unknown'
            # stage_id is usually [id, "Stage Name"]
            stage = lead.get('stage_id')
            stage_name = stage[1] if stage and isinstance(stage, list) and len(stage) > 1 else "Unknown"
            
            summary += f"- '{name}' from {contact} (Stage: {stage_name})\n"
            
        return summary
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "OdooAgent",
            "enabled": self.enabled,
            "url": Config.ODOO_URL
        }
