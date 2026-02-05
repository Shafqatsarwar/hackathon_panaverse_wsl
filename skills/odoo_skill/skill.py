"""
Odoo Skill - XML-RPC Integration
"""
import logging
import xmlrpc.client
from typing import List, Dict, Any, Union
from src.utils.config import Config

logger = logging.getLogger(__name__)

class OdooSkill:
    """Skill to interact with Odoo ERP"""
    
    def __init__(self):
        self.url = Config.ODOO_URL
        self.db = Config.ODOO_DB
        self.username = Config.ODOO_USERNAME
        self.password = Config.ODOO_PASSWORD
        self.common = None
        self.models = None
        self.uid = None
        self.enabled = bool(self.url and self.db and self.username and self.password)

    def authenticate(self) -> bool:
        """Authenticate with Odoo"""
        if not self.enabled:
            logger.warning("Odoo Skill: Missing configuration (disabled)")
            return False
            
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                logger.info(f"Odoo Skill: Authenticated successfully (UID: {self.uid})")
                return True
            else:
                logger.error("Odoo Skill: Authentication failed (Invalid credentials)")
                return False
        except Exception as e:
            logger.error(f"Odoo Skill: Connection error: {e}")
            return False

    def create_lead(self, name: str, email_from: str, description: str) -> Dict[str, Any]:
        """Create a new CRM Lead"""
        if not self.uid:
            if not self.authenticate():
                return {"success": False, "error": "Authentication failed"}
        
        try:
            lead_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'crm.lead', 'create',
                [{
                    'name': name,
                    'email_from': email_from,
                    'description': description,
                    'type': 'lead'
                }]
            )
            logger.info(f"Odoo Skill: Created Lead ID {lead_id}")
            return {"success": True, "id": lead_id}
        except Exception as e:
            logger.error(f"Odoo Skill: Failed to create lead: {e}")
            return {"success": False, "error": str(e)}

    def get_leads(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent CRM leads"""
        if not self.uid:
            if not self.authenticate(): return []
            
        try:
            # Search for latest leads
            ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'crm.lead', 'search',
                [[]], # Empty domain = all records
                {'limit': limit, 'order': 'create_date desc'}
            )
            
            if ids:
                records = self.models.execute_kw(
                    self.db, self.uid, self.password,
                    'crm.lead', 'read',
                    [ids],
                    {'fields': ['name', 'contact_name', 'email_from', 'description', 'stage_id']}
                )
                return records
            return []
        except Exception as e:
            logger.error(f"Odoo Skill: Failed to get leads: {e}")
            return []
