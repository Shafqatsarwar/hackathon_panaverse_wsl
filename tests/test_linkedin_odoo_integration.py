"""
LinkedIn to Odoo CRM Integration + Project Post
1. Extract LinkedIn contacts/connections
2. Save as leads in Odoo CRM
3. Post about the project on LinkedIn with GitHub URL
"""
import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.linkedin_skill.skill import LinkedInSkill
from skills.odoo_skill.odoo_skill import OdooSkill
from playwright.async_api import async_playwright

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("LinkedInOdooIntegration")

async def get_linkedin_connections(linkedin_skill: LinkedInSkill) -> List[Dict[str, Any]]:
    """
    Get LinkedIn connections using Playwright
    This will navigate to My Network and extract connections
    """
    logger.info("Extracting LinkedIn connections...")
    
    playwright = await async_playwright().start()
    
    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=linkedin_skill.session_dir,
            headless=linkedin_skill.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--window-size=1280,800"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Navigate to connections page
        logger.info("Navigating to My Network...")
        await page.goto("https://www.linkedin.com/mynetwork/invite-connect/connections/", 
                       wait_until="domcontentloaded")
        
        # Wait for login if needed
        try:
            await page.wait_for_selector('#global-nav', timeout=10000)
        except:
            logger.warning("Not logged in to LinkedIn. Please log in manually.")
            await context.close()
            await playwright.stop()
            return []
        
        # Wait for connections to load
        await page.wait_for_timeout(3000)
        
        # Extract connections
        connections = []
        try:
            # Scroll to load more connections
            for i in range(3):  # Scroll 3 times
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
            
            # Get connection cards
            connection_cards = await page.locator('li.mn-connection-card').all()
            
            logger.info(f"Found {len(connection_cards)} connection cards")
            
            for card in connection_cards[:50]:  # Limit to first 50
                try:
                    # Extract name
                    name_el = card.locator('.mn-connection-card__name')
                    name = await name_el.text_content() if await name_el.count() > 0 else "Unknown"
                    
                    # Extract occupation/headline
                    occupation_el = card.locator('.mn-connection-card__occupation')
                    occupation = await occupation_el.text_content() if await occupation_el.count() > 0 else ""
                    
                    # Try to get profile link for email extraction (if visible)
                    link_el = card.locator('a[href*="/in/"]')
                    profile_url = await link_el.get_attribute('href') if await link_el.count() > 0 else ""
                    
                    connections.append({
                        'name': name.strip(),
                        'occupation': occupation.strip(),
                        'profile_url': profile_url,
                        'source': 'LinkedIn Connections'
                    })
                except Exception as e:
                    logger.debug(f"Error extracting connection: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting connections: {e}")
        
        await context.close()
        await playwright.stop()
        
        return connections
        
    except Exception as e:
        logger.error(f"LinkedIn connection extraction error: {e}")
        await playwright.stop()
        return []

async def post_to_linkedin(linkedin_skill: LinkedInSkill, post_content: str) -> bool:
    """
    Post content to LinkedIn feed
    """
    logger.info("Posting to LinkedIn...")
    
    playwright = await async_playwright().start()
    
    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=linkedin_skill.session_dir,
            headless=linkedin_skill.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--window-size=1280,800"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Navigate to feed
        logger.info("Navigating to LinkedIn feed...")
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        
        # Wait for login
        try:
            await page.wait_for_selector('#global-nav', timeout=10000)
        except:
            logger.error("Not logged in to LinkedIn")
            await context.close()
            await playwright.stop()
            return False
        
        # Click "Start a post" button
        logger.info("Clicking 'Start a post' button...")
        try:
            start_post_btn = page.locator('button[aria-label*="Start a post"], button:has-text("Start a post")')
            await start_post_btn.first.click()
            await page.wait_for_timeout(2000)
            
            # Find the text editor
            editor = page.locator('div[contenteditable="true"][role="textbox"]')
            await editor.first.click()
            await page.wait_for_timeout(1000)
            
            # Type the post content
            logger.info("Typing post content...")
            await editor.first.fill(post_content)
            await page.wait_for_timeout(2000)
            
            # Click Post button
            logger.info("Clicking Post button...")
            post_btn = page.locator('button[aria-label*="Post"], button:has-text("Post")')
            await post_btn.first.click()
            await page.wait_for_timeout(3000)
            
            logger.info("Post published successfully!")
            
            await context.close()
            await playwright.stop()
            return True
            
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            # Take screenshot for debugging
            try:
                await page.screenshot(path="linkedin_post_error.png")
            except:
                pass
            await context.close()
            await playwright.stop()
            return False
        
    except Exception as e:
        logger.error(f"LinkedIn posting error: {e}")
        await playwright.stop()
        return False

async def main():
    logger.info("="*70)
    logger.info("LinkedIn to Odoo CRM Integration + Project Post")
    logger.info("="*70)
    
    # Initialize skills
    logger.info("\n[1/4] Initializing LinkedIn Skill...")
    linkedin_skill = LinkedInSkill(enabled=True, headless=False)
    
    logger.info("[2/4] Initializing Odoo CRM Skill...")
    odoo_skill = OdooSkill()
    
    # Authenticate with Odoo
    if odoo_skill.enabled:
        if odoo_skill.authenticate():
            logger.info("✓ Odoo CRM authenticated successfully")
        else:
            logger.warning("⚠ Odoo CRM authentication failed - will skip lead creation")
    else:
        logger.warning("⚠ Odoo CRM not configured - will skip lead creation")
    
    # Get LinkedIn connections
    logger.info("\n[3/4] Extracting LinkedIn connections...")
    connections = await get_linkedin_connections(linkedin_skill)
    
    logger.info(f"\nFound {len(connections)} LinkedIn connections")
    
    # Save connections to Odoo as leads
    if odoo_skill.enabled and odoo_skill.uid and len(connections) > 0:
        logger.info("\nSaving connections to Odoo CRM as leads...")
        saved_count = 0
        failed_count = 0
        
        for conn in connections:
            # Create lead in Odoo
            result = odoo_skill.create_lead(
                name=conn['name'],
                email_from=f"{conn['name'].lower().replace(' ', '.')}@linkedin.com",  # Placeholder email
                description=f"LinkedIn Connection\nOccupation: {conn['occupation']}\nProfile: {conn['profile_url']}\nSource: {conn['source']}"
            )
            
            if result.get('success'):
                saved_count += 1
                logger.info(f"  ✓ Saved: {conn['name']} (Lead ID: {result['id']})")
            else:
                failed_count += 1
                logger.warning(f"  ✗ Failed: {conn['name']}")
        
        logger.info(f"\n✓ Saved {saved_count} leads to Odoo CRM")
        if failed_count > 0:
            logger.warning(f"⚠ Failed to save {failed_count} leads")
    else:
        logger.info("\nSkipping Odoo CRM save (not configured or no connections)")
    
    # Create LinkedIn post about the project
    logger.info("\n[4/4] Creating LinkedIn post about the project...")
    
    post_content = f"""🚀 Excited to share my latest AI project: Panaversity Student Assistant!

This autonomous AI assistant helps students stay organized by:
✅ Monitoring Gmail for assignments, quizzes, and deadlines
✅ Checking WhatsApp for important PIAIC updates
✅ Tracking LinkedIn notifications
✅ Automatically creating tasks and reminders
✅ Integrating with Odoo CRM for lead management

Built with:
🔹 Python & FastAPI
🔹 Google Gemini AI
🔹 Playwright for browser automation
🔹 Next.js for the frontend
🔹 MCP (Model Context Protocol) architecture

This project showcases the power of AI agents working autonomously 24/7 to handle routine tasks, allowing students to focus on learning.

Check out the code on GitHub: https://github.com/Shafqatsarwar/hackathon_panaverse

#AI #Automation #Python #GenAI #PIAIC #Panaversity #MachineLearning #SoftwareDevelopment

What are your thoughts on AI assistants for education? 💭"""

    post_success = await post_to_linkedin(linkedin_skill, post_content)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("TASK SUMMARY")
    logger.info("="*70)
    logger.info(f"LinkedIn connections extracted: {len(connections)}")
    if odoo_skill.enabled and odoo_skill.uid:
        logger.info(f"Leads saved to Odoo CRM: {saved_count}")
    logger.info(f"LinkedIn post published: {'✓ YES' if post_success else '✗ NO'}")
    logger.info("="*70)
    
    return {
        'connections': len(connections),
        'leads_saved': saved_count if odoo_skill.enabled and odoo_skill.uid else 0,
        'post_published': post_success
    }

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    result = asyncio.run(main())
    
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print("="*70)
    print(f"Connections extracted: {result['connections']}")
    print(f"Leads saved to Odoo: {result['leads_saved']}")
    print(f"LinkedIn post: {'✓ Published' if result['post_published'] else '✗ Failed'}")
    print("="*70)
