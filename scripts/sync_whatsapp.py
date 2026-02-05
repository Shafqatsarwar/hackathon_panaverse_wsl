
import logging
import sys
import os

# Adjust path to import skill
sys.path.append(os.getcwd())
from skills.whatsapp_skill.skill import WhatsAppSkill

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsAppSync")

def sync_panaverse_messages():
    skill = WhatsAppSkill(enabled=True, headless=True) # Run headless=True for cloud compatibility
    
    logger.info("Starting WhatsApp Sync for Panaverse/PIAIC...")
    
    # Keywords to look for
    keywords = ["Panaversity", "PIAIC", "Panaverse"]
    
    # This will open browser, scan main list + archived, and return results
    messages = skill.check_messages(keywords=keywords, check_archived=True)
    
    logger.info("--- SYNC RESULTS ---")
    if messages:
        for msg in messages:
            if "error" in msg:
                 logger.error(f"Error: {msg['error']}")
            else:
                 logger.info(f"Chat Found: {msg['title']} (Unread: {msg['unread']})")
                 logger.info(f"Last Preview: {msg['last_message']}")
                 if 'source' in msg:
                     logger.info(f"Source: {msg['source']}")
                 logger.info("-" * 20)
    else:
        logger.info("No matching chats found.")

if __name__ == "__main__":
    sync_panaverse_messages()
