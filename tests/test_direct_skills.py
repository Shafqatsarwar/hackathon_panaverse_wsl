
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from skills.whatsapp_skill.skill import WhatsAppSkill
from agents.email_agent import EmailAgent
from src.utils.notifications import NotificationService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestDirect")

def test_whatsapp_direct():
    logger.info("--- Testing WhatsApp Skill Direct ---")
    target_number = os.getenv("WHATSAPP_FORWARD_MESSAGES", "+46764305834")
    
    session_path = os.path.abspath("./whatsapp_session")
    skill = WhatsAppSkill(
        enabled=True,
        headless=False,
        session_dir=session_path
    )
    
    # Sending 4 messages
    for i in range(1, 5):
        msg = f"Test Message Direct {i}/4 - Verification"
        logger.info(f"Sending: {msg}")
        try:
            skill.send_message(target_number, msg)
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to send message {i}: {e}")

def test_email_direct():
    logger.info("--- Testing Email Notification Direct ---")
    target_email = os.getenv("EMAIL_FORWARD_EMAIL", "khansarwar1@hotmail.com")
    
    service = NotificationService(
        smtp_server=Config.SMTP_SERVER,
        smtp_port=Config.SMTP_PORT,
        smtp_username=Config.SMTP_USERNAME,
        smtp_password=Config.SMTP_PASSWORD
    )
    
    # Sending 4 emails
    for i in range(1, 5):
        subject = f"Test Email Direct {i}/4"
        body = f"This is a verification email {i}/4 sent directly via NotificationService."
        logger.info(f"Sending Email: {subject}")
        try:
            service.send_email_notification(target_email, subject, body)
            time.sleep(1)
        except Exception as e:
            logger.error(f"Failed to send email {i}: {e}")

if __name__ == "__main__":
    test_whatsapp_direct()
    test_email_direct()
