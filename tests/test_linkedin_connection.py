import os
import sys
import logging
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.linkedin_skill.skill import LinkedInSkill

logging.basicConfig(level=logging.INFO)

async def test_li():
    try:
        li = LinkedInSkill(enabled=True, headless=True)
        results = li.scrape_leads()
        print(f"LINKEDIN SUCCESS: {results.get('success')}")
        if results.get('success'):
            print(f"NOTIFS: {len(results.get('notifications', []))}")
            print(f"MSGS: {len(results.get('messages', []))}")
        else:
            print(f"ERROR: {results.get('error')}")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    asyncio.run(test_li())
