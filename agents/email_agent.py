"""
Email Agent - Uses Gmail and Email Filtering Skills
"""
import logging
from typing import List, Dict, Any
from datetime import datetime
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from skills.email_filtering import EmailFilteringSkill

logger = logging.getLogger(__name__)

class EmailAgent:
    """Agent that monitors Gmail using skills"""
    
    def __init__(self, credentials_path: str, token_path: str, filter_keywords: List[str]):
        # Initialize skills
        self.gmail_skill = GmailMonitoringSkill(
            credentials_path=credentials_path,
            token_path=token_path,
            keywords=filter_keywords
        )
        self.filter_skill = EmailFilteringSkill(keywords=filter_keywords)
        self.last_check_time = None
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail"""
        return self.gmail_skill.authenticate()
    
    def check_emails(self, mark_read: bool = False) -> List[Dict[str, Any]]:
        """Check for new relevant emails"""
        logger.info("Email Agent: Checking for new emails...")
        
        # Use Gmail skill to fetch and filter
        relevant_emails = self.gmail_skill.check_emails(mark_read=mark_read)
        
        self.last_check_time = datetime.now()
        logger.info(f"Email Agent: Found {len(relevant_emails)} relevant emails")
        
        return relevant_emails
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": "EmailAgent",
            "last_check": self.last_check_time.isoformat() if self.last_check_time else None,
            "authenticated": self.gmail_skill.service is not None
        }
