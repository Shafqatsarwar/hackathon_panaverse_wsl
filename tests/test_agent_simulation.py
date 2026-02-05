
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from agents.whatsapp_agent import WhatsAppAgent
from agents.notification_agent import NotificationAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestAgents")

def test_whatsapp_agent():
    logger.info("--- Testing WhatsApp Agent ---")
    
    # Initialize Agent
    agent = WhatsAppAgent()
    target_number = os.getenv("WHATSAPP_FORWARD_MESSAGES", "+46764305834")
    
    # Test checking messages (Read Mode)
    logger.info("Agent: Checking messages...")
    try:
        messages = agent.get_unread_messages(limit=5, check_archived=True)
        logger.info(f"Agent found {len(messages)} messages.")
    except Exception as e:
        logger.error(f"Agent check failed: {e}")

    # Sending 3 messages
    for i in range(1, 4):
        msg = f"Test Message Agent {i}/3 - Verification"
        logger.info(f"Agent Sending: {msg}")
        try:
            result = agent.send_message(target_number, msg)
            logger.info(f"Result: {result}")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Agent send failed {i}: {e}")

def test_notification_agent():
    logger.info("--- Testing Notification Agent (Email) ---")
    
    # Initialize Agent
    agent = NotificationAgent()
    target_email = os.getenv("EMAIL_FORWARD_EMAIL", "khansarwar1@hotmail.com")
    
    # Sending 3 emails
    for i in range(1, 4):
        subject = f"Test Email Agent {i}/3"
        body = f"This is a verification email {i}/3 sent via NotificationAgent."
        logger.info(f"Agent Sending Email: {subject}")
        try:
            result = agent.send_email(target_email, subject, body)
            logger.info(f"Result: {result}")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Agent email failed {i}: {e}")

if __name__ == "__main__":
    test_whatsapp_agent()
    test_notification_agent()
