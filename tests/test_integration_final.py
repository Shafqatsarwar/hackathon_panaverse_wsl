import sys
import os
import asyncio
from pathlib import Path
import logging

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IntegrationTest")

async def test_all_systems():
    print("=" * 60)
    print("      COMPREHENSIVE INTEGRATION TEST (WhatsApp/Odoo/Email)      ")
    print("=" * 60)

    from src.utils.config import Config
    
    # 1. Test WhatsApp Skill (Directly)
    print("\n[1] Testing WhatsApp Skill (Session Persistence)...")
    try:
        from skills.whatsapp_skill.skill import WhatsAppSkill
        session_path = os.path.abspath("whatsapp_session")
        print(f"Using Session Path: {session_path}")
        
        wa_skill = WhatsAppSkill(enabled=True, headless=False, session_dir=session_path)
        
        # Test Check
        res = await wa_skill.check_messages_async(limit=3)
        if res.get("success"):
            print("   PASS - WhatsApp: Login Successful & Messages Checked")
            print(f"   INFO - Messages Found: {len(res.get('messages', []))}")
        else:
            print(f"   FAIL - WhatsApp Error: {res.get('error')}")
            
    except Exception as e:
        print(f"   CRASH - WhatsApp Crash: {e}")

    # 2. Test Odoo Agent
    print("\n[2] Testing Odoo Agent (Connection)...")
    try:
        from agents.odoo_agent import OdooAgent
        odoo = OdooAgent()
        if odoo.enabled:
            # Try a simple read
            leads = odoo.get_recent_leads(limit=1)
            print("   PASS - Odoo: Connection Successful")
            print(f"   INFO - Recent Leads: {len(leads)}")
        else:
            print("   INFO - Odoo: Disabled in Config")
    except Exception as e:
        print(f"   FAIL - Odoo Connection Failed: {e}")

    # 3. Test Email Agent
    print("\n[3] Testing Email Agent (Auth)...")
    try:
        from agents.email_agent import EmailAgent
        email = EmailAgent(
            credentials_path=Config.GMAIL_CREDENTIALS_PATH,
            token_path=Config.GMAIL_TOKEN_PATH
        )
        if email.authenticate():
             print("   PASS - Email: Authentication Successful")
        else:
             print("   FAIL - Email: Authentication Failed")
    except Exception as e:
        print(f"   CRASH - Email Agent Crash: {e}")

    print("\n" + "=" * 60)
    print("Test Complete. If all [1], [2], [3] are green/yellow,")
    print("Run > python start_autonomous.py")
    print("=" * 60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_all_systems())
