"""
LinkedIn to Odoo CRM Sync (Interactive Version)
Extracts LinkedIn connections and saves them as leads in Odoo CRM
Browser stays open so you can see the process
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath('.'))

from playwright.async_api import async_playwright
from agents.odoo_agent import OdooAgent
from src.utils.config import Config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scrape_linkedin_connections():
    """Scrape LinkedIn connections with browser visible"""
    print("\n🌐 Opening LinkedIn in browser...")
    
    playwright = await async_playwright().start()
    
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="./linkedin_session",
        headless=False,  # Keep browser visible
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--window-size=1280,800"
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    page = context.pages[0] if context.pages else await context.new_page()
    
    results = {"notifications": [], "messages": [], "connections": []}
    
    try:
        # 1. Check login
        print("🔐 Checking login status...")
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        
        try:
            await page.wait_for_selector('#global-nav', timeout=10000)
            print("✅ Logged in successfully!")
        except:
            print("❌ Not logged in. Please log in manually in the browser window.")
            print("Waiting 60 seconds for you to log in...")
            await asyncio.sleep(60)
            
            try:
                await page.wait_for_selector('#global-nav', timeout=5000)
                print("✅ Login detected!")
            except:
                print("❌ Still not logged in. Aborting.")
                await context.close()
                await playwright.stop()
                return {"success": False, "error": "Login required"}
        
        # 2. Get My Network / Connections
        print("\n👥 Fetching connections from My Network...")
        await page.goto("https://www.linkedin.com/mynetwork/invite-connect/connections/", wait_until="domcontentloaded")
        await asyncio.sleep(3)  # Wait for page to load
        
        try:
            # Scroll to load more connections
            for i in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)
            
            # Extract connections
            connection_cards = await page.locator('li.mn-connection-card').all()
            
            print(f"📊 Found {len(connection_cards)} connections")
            
            for card in connection_cards[:20]:  # Limit to first 20
                try:
                    name_el = card.locator('.mn-connection-card__name')
                    name = await name_el.text_content() if await name_el.count() else "Unknown"
                    
                    occupation_el = card.locator('.mn-connection-card__occupation')
                    occupation = await occupation_el.text_content() if await occupation_el.count() else ""
                    
                    results["connections"].append({
                        "name": name.strip(),
                        "occupation": occupation.strip(),
                        "type": "connection"
                    })
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Could not fetch connections: {e}")
        
        # 3. Get Messages
        print("\n💬 Fetching recent messages...")
        await page.goto("https://www.linkedin.com/messaging/", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        try:
            conversations = await page.locator('div[class*="msg-conversation-card"]').all()
            
            print(f"📊 Found {len(conversations)} conversations")
            
            for conv in conversations[:10]:  # Limit to first 10
                try:
                    sender_el = conv.locator('h3, .msg-conversation-listitem__participant-names')
                    sender = await sender_el.first.text_content() if await sender_el.count() else "Unknown"
                    
                    preview_el = conv.locator('p, .msg-conversation-card__message-snippet')
                    preview = await preview_el.first.text_content() if await preview_el.count() else ""
                    
                    results["messages"].append({
                        "sender": sender.strip(),
                        "content": preview.strip(),
                        "type": "message"
                    })
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Could not fetch messages: {e}")
        
        print("\n✅ LinkedIn data extracted successfully!")
        print(f"   - Connections: {len(results['connections'])}")
        print(f"   - Messages: {len(results['messages'])}")
        
        await context.close()
        await playwright.stop()
        
        results["success"] = True
        return results
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await context.close()
        await playwright.stop()
        return {"success": False, "error": str(e)}

def main():
    print("🔗 LinkedIn to Odoo CRM Sync (Interactive)")
    print("=" * 60)
    
    # Set Windows event loop policy
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Initialize Odoo
    print("\n📋 Initializing Odoo CRM Agent...")
    odoo_agent = OdooAgent()
    
    if not odoo_agent.enabled:
        print("❌ Error: Odoo CRM is not enabled!")
        print("Please check your .env file and ensure Odoo credentials are set.")
        return
    
    print(f"✅ Connected to: {Config.ODOO_URL}")
    
    # Scrape LinkedIn
    result = asyncio.run(scrape_linkedin_connections())
    
    if not result.get("success"):
        print(f"\n❌ Error: {result.get('error')}")
        return
    
    # Combine connections and messages
    all_leads = result.get("connections", []) + result.get("messages", [])
    
    if not all_leads:
        print("\n⚠️ No LinkedIn data found to sync.")
        return
    
    print(f"\n📤 Syncing {len(all_leads)} items to Odoo CRM...")
    print("-" * 60)
    
    created_count = 0
    errors = []
    
    for i, lead_data in enumerate(all_leads, 1):
        name = lead_data.get("sender") or lead_data.get("name", "Unknown")
        content = lead_data.get("content") or lead_data.get("occupation", "")
        lead_type = lead_data.get("type", "unknown")
        
        print(f"\n[{i}/{len(all_leads)}] {name}")
        print(f"    Type: {lead_type}")
        print(f"    Info: {content[:60]}...")
        
        try:
            # Create lead in Odoo
            if lead_type == "message":
                res = odoo_agent.create_lead_from_linkedin(lead_data)
            else:
                # For connections, create a generic lead
                res = odoo_agent.create_lead(
                    name=f"LinkedIn Connection: {name}",
                    description=f"LinkedIn Connection\n\nOccupation: {content}",
                    email="linkedin@placeholder.com"
                )
            
            if res.get("success"):
                lead_id = res.get("lead_id")
                print(f"    ✅ Created lead #{lead_id}")
                created_count += 1
            else:
                error_msg = res.get("error", "Unknown error")
                print(f"    ❌ Failed: {error_msg}")
                errors.append(f"{name}: {error_msg}")
        except Exception as e:
            print(f"    ❌ Exception: {str(e)}")
            errors.append(f"{name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 SYNC SUMMARY")
    print("=" * 60)
    print(f"Total Items: {len(all_leads)}")
    print(f"Successfully Created Leads: {created_count}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\n❌ Error Details:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"  - {error}")
    
    print("\n✅ Sync completed!")
    print(f"\n🌐 View your leads: {Config.ODOO_URL}/web#action=crm.crm_lead_all_leads")

if __name__ == "__main__":
    main()
