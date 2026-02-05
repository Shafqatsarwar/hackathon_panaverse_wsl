
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from skills.odoo_skill.skill import OdooSkill
from skills.linkedin_skill.skill import LinkedInSkill
from agents.odoo_agent import OdooAgent
from agents.linkedin_agent import LinkedInAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestBusinessApps")

def test_odoo_lead_direct():
    logger.info("--- Testing Odoo Skill Direct ---")
    skill = OdooSkill()
    if not skill.enabled:
        logger.warning("Odoo Skill is disabled/not configured.")
        return

    logger.info("Direct: Creating Dummy Lead...")
    result = skill.create_lead(
        name="Test Lead for Hackathon Verification (Direct)",
        email_from="test_direct@panaverse.com",
        description="This is a test lead created directly by the Odoo Skill to verify functionality."
    )
    logger.info(f"Result: {result}")

def test_odoo_agent():
    logger.info("--- Testing Odoo Agent ---")
    agent = OdooAgent()
    if not agent.enabled:
        logger.warning("Odoo Agent is disabled.")
        return

    logger.info("Agent: Creating Dummy Lead...")
    # Simulate email data
    email_data = {
        "subject": "Test Lead for Hackathon Verification (Agent)",
        "sender": "test_agent@panaverse.com",
        "body": "This is a test lead created via the Odoo Agent to verify the email-to-lead flow."
    }
    result = agent.create_lead_from_email(email_data)
    logger.info(f"Result: {result}")
    
    logger.info("Agent: Getting Recent Leads...")
    leads = agent.get_recent_leads(3)
    logger.info(f"Recent Leads: {len(leads)}")
    for lead in leads:
        logger.info(f"- {lead.get('name')}")

def test_linkedin_post_direct():
    logger.info("--- Testing LinkedIn Skill Direct ---")
    # For testing, we might want headful mode to see it happen if user is watching, 
    # but the script will run in background.
    skill = LinkedInSkill(enabled=True, headless=False)
    
    if not skill.enabled:
        logger.warning("LinkedIn Skill is disabled/not configured.")
        return

    msg = "🚀 Achievement Unlocked: Automated testing of Panaversity AI Agent verified successfully! #GenerativeAI #Panaverse #HackathonTest"
    logger.info(f"Direct: Posting Update: '{msg}'")
    
    result = skill.post_update(msg)
    logger.info(f"Result: {result}")

def test_linkedin_agent():
    logger.info("--- Testing LinkedIn Agent ---")
    agent = LinkedInAgent()
    
    # We won't double post for now to avoid spamming too much, 
    # but we can check notifications as a read test
    logger.info("Agent: Checking Notifications...")
    result = agent.check_notifications()
    logger.info(f"Notifications found: {len(result.get('notifications', []))}")
    if result.get("success"):
         for n in result.get("notifications", [])[:3]:
             logger.info(f"- {n}")

if __name__ == "__main__":
    # 1. Odoo Tests (Fast)
    test_odoo_lead_direct()
    test_odoo_agent()
    
    # 2. LinkedIn Tests (Slower, Browser based)
    test_linkedin_post_direct()
    # Note: We run agent test after, it might reuse session or create new one.
    test_linkedin_agent()
