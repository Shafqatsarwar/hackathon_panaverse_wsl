"""
Notification Agent - Uses Email Notification Skill
"""
import logging
from typing import Dict, Any, Optional
from skills.email_notifications.email_notifications import EmailNotificationSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class NotificationAgent:
    """Agent that handles notifications using skills"""
    
    def __init__(self, 
                 smtp_server: Optional[str] = None, 
                 smtp_port: Optional[int] = None, 
                 smtp_username: Optional[str] = None, 
                 smtp_password: Optional[str] = None):
        # Use Config defaults if not provided
        self.notification_skill = EmailNotificationSkill(
            smtp_server=smtp_server or Config.SMTP_SERVER,
            smtp_port=smtp_port or Config.SMTP_PORT,
            smtp_username=smtp_username or Config.SMTP_USERNAME,
            smtp_password=smtp_password or Config.SMTP_PASSWORD
        )
    
    def send_email_alert(self, admin_email: str, email_data: Dict[str, Any]) -> bool:
        """Send email notification"""
        safe_subject = email_data.get('subject', '').encode('ascii', 'ignore').decode('ascii')
        logger.info(f"Notification Agent: Sending alert for '{safe_subject}'")
        
        success = self.notification_skill.notify_new_email(
            admin_email=admin_email,
            email_data=email_data
        )
        
        if success:
            logger.info("Notification Agent: Alert sent successfully")
        else:
            logger.error("Notification Agent: Failed to send alert")
        
        return success
    
    def send_email(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Send a direct email"""
        try:
            success = self.notification_skill.send_email_notification(
                to_email=to_email,
                subject=subject,
                body=body
            )
            return {"success": success}
        except Exception as e:
            logger.error(f"Notification Agent: Failed to send email: {e}")
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": "NotificationAgent",
            "smtp_configured": bool(self.notification_skill.smtp_password)
        }
