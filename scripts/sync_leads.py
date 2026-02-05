
import logging
import os
import sys

# Adjust path
sys.path.append(os.getcwd())

from skills.odoo_skill.odoo_skill import OdooSkill
from skills.linkedin_skill.skill import LinkedInSkill

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LeadAgent")

def run_lead_sync():
    logger.info("Initializing Agent: LinkedIn -> Odoo Lead Sync")
    
    # 1. Initialize Skills
    odoo = OdooSkill()
    linkedin = LinkedInSkill(enabled=True, headless=True) # Headless for automated run, user can switch
    
    # 2. Verify Odoo Connection
    logger.info("Step 1: Checking Odoo Connection...")
    if not odoo.authenticate():
        logger.error("Failed to connect to Odoo. Please check credentials in src/utils/config.py or .env")
        # Proceeding? No, we need Odoo.
        # But we can still scan LinkedIn to show user it works.
        odoo_available = False
    else:
        logger.info("Odoo connected successfully.")
        odoo_available = True

    # 3. Scrape LinkedIn
    logger.info("Step 2: Scraping LinkedIn for potential leads...")
    results = linkedin.scrape_leads()
    
    if "error" in results:
        logger.error(f"LinkedIn Error: {results['error']}")
        return

    messages = results.get("messages", [])
    logger.info(f"Found {len(messages)} messages.")
    
    # 4. Process Leads
    leads_created = 0
    if messages:
        for msg in messages:
            sender = msg['sender']
            content = msg['content']
            
            logger.info(f"Processing message from: {sender}")
            
            if odoo_available:
                # Basic logic: Create lead for every new message (deduplication needed in real app)
                lead_name = f"LinkedIn Inquiry: {sender}"
                description = f"Message Content:\n{content}\n\nSource: LinkedIn Automation"
                
                res = odoo.create_lead(
                    name=lead_name,
                    email_from="linkedin@placeholder.com", # LinkedIn doesn't give email easily
                    description=description
                )
                
                if res.get("success"):
                    logger.info(f"SUCCESS: Created Odoo Lead ID {res['id']}")
                    leads_created += 1
                else:
                    logger.error(f"Failed to create lead: {res.get('error')}")
            else:
                logger.info(f"[Mock] Would create lead for {sender}: {content[:30]}...")

    logger.info(f"Sync Complete. Total Leads Created: {leads_created}")

if __name__ == "__main__":
    run_lead_sync()
