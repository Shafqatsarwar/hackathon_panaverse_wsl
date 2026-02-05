"""
Enhanced PIAIC Chat Analyzer
1. Finds PIAIC chats (including Sir Hassan)
2. Extracts links and files
3. Creates summary
4. Sends to specified WhatsApp number
"""
import sys
import os
import asyncio
import logging
import re
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.whatsapp_skill.skill import WhatsAppSkill

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PIAICAnalyzer")

async def extract_links_from_text(text: str) -> list:
    """Extract URLs from text"""
    # URL pattern
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls

async def main():
    logger.info("="*70)
    logger.info("PIAIC Chat Analyzer - Enhanced Version")
    logger.info("="*70)
    
    # Target numbers
    source_number = "+923244279017"  # Your main number
    target_number = "+46764305834"   # Your second WhatsApp number
    
    # Initialize WhatsApp skill
    logger.info("\n[1/4] Initializing WhatsApp Skill...")
    wa_skill = WhatsAppSkill(enabled=True, headless=False)
    
    # Search for all PIAIC-related chats
    logger.info("[2/4] Searching for PIAIC-related chats...")
    all_messages = await wa_skill.check_messages_async(
        keywords=["PIAIC", "Hassan", "Lahore", "General-Agents"],
        check_archived=True,
        limit=100  # Check more chats
    )
    
    if not all_messages or "error" in all_messages[0]:
        logger.error(f"Failed to retrieve chats: {all_messages}")
        return
    
    logger.info(f"\nFound {len(all_messages)} PIAIC-related chats:")
    for idx, msg in enumerate(all_messages[:10], 1):
        logger.info(f"  {idx}. {msg.get('title')}")
        logger.info(f"     Last: {msg.get('last_message', '')[:60]}...")
        logger.info(f"     Unread: {msg.get('unread', '0')}, Source: {msg.get('source', 'main')}")
    
    # Find specific chats
    general_agents_chat = None
    hassan_chat = None
    
    for msg in all_messages:
        title = msg.get('title', '').lower()
        if 'general-agents' in title and 'lahore' in title:
            general_agents_chat = msg
        if 'hassan' in title and 'piaic' in title:
            hassan_chat = msg
    
    logger.info("\n[3/4] Analyzing chats...")
    
    # Prepare summary
    summary_parts = []
    summary_parts.append("📊 PIAIC Chat Analysis Report")
    summary_parts.append("=" * 40)
    summary_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_parts.append("")
    
    # Analyze General-Agents Lahore chat
    if general_agents_chat:
        summary_parts.append("📱 PIAIC General-Agents Lahore")
        summary_parts.append(f"Status: {general_agents_chat.get('source', 'main').upper()}")
        summary_parts.append(f"Unread: {general_agents_chat.get('unread', '0')}")
        summary_parts.append(f"Latest: {general_agents_chat.get('last_message', 'N/A')[:100]}")
        
        # Extract links from last message
        links = await extract_links_from_text(general_agents_chat.get('last_message', ''))
        if links:
            summary_parts.append(f"\n🔗 Links found: {len(links)}")
            for link in links[:5]:  # First 5 links
                summary_parts.append(f"  • {link}")
        summary_parts.append("")
    else:
        summary_parts.append("⚠️ PIAIC General-Agents Lahore: NOT FOUND")
        summary_parts.append("")
    
    # Analyze Sir Hassan chat
    if hassan_chat:
        summary_parts.append("👨‍🏫 Sir Hassan Sb PIAIC")
        summary_parts.append(f"Chat: {hassan_chat.get('title')}")
        summary_parts.append(f"Status: {hassan_chat.get('source', 'main').upper()}")
        summary_parts.append(f"Unread: {hassan_chat.get('unread', '0')}")
        summary_parts.append(f"Latest: {hassan_chat.get('last_message', 'N/A')[:100]}")
        
        # Extract links
        links = await extract_links_from_text(hassan_chat.get('last_message', ''))
        if links:
            summary_parts.append(f"\n🔗 Links/Files from Sir Hassan: {len(links)}")
            for link in links[:10]:  # First 10 links
                summary_parts.append(f"  • {link}")
        summary_parts.append("")
    else:
        summary_parts.append("⚠️ Sir Hassan PIAIC Chat: NOT FOUND")
        summary_parts.append("")
    
    # Add all found PIAIC chats
    summary_parts.append("📋 All PIAIC Chats Found:")
    for idx, msg in enumerate(all_messages[:5], 1):
        summary_parts.append(f"{idx}. {msg.get('title')}")
    
    summary_parts.append("")
    summary_parts.append("---")
    summary_parts.append("Note: This is based on latest visible messages.")
    summary_parts.append("For full chat history, please check WhatsApp directly.")
    summary_parts.append("")
    summary_parts.append("Powered by AI Assistant 🤖")
    
    # Combine summary
    full_summary = "\n".join(summary_parts)
    
    logger.info("\n" + "="*70)
    logger.info("GENERATED SUMMARY:")
    logger.info("="*70)
    logger.info(full_summary)
    logger.info("="*70)
    
    # Send to second WhatsApp number
    logger.info(f"\n[4/4] Sending summary to {target_number}...")
    
    send_result = await wa_skill.send_message_async(
        target_number,
        full_summary
    )
    
    if send_result.get('success'):
        logger.info("\n" + "="*70)
        logger.info("✅ SUCCESS! Summary sent successfully!")
        logger.info("="*70)
        logger.info(f"Sent to: {target_number}")
        logger.info(f"Message length: {len(full_summary)} characters")
        logger.info(f"Chats analyzed: {len(all_messages)}")
    else:
        logger.error(f"\n❌ Failed to send: {send_result.get('error')}")
    
    logger.info("\n✅ Task completed!")
    
    # Return summary for reference
    return {
        'summary': full_summary,
        'chats_found': len(all_messages),
        'general_agents': general_agents_chat is not None,
        'hassan_chat': hassan_chat is not None,
        'sent': send_result.get('success', False)
    }

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    result = asyncio.run(main())
    
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print("="*70)
    print(f"Chats analyzed: {result['chats_found']}")
    print(f"General-Agents found: {'✅' if result['general_agents'] else '❌'}")
    print(f"Hassan chat found: {'✅' if result['hassan_chat'] else '❌'}")
    print(f"Message sent: {'✅' if result['sent'] else '❌'}")
    print("="*70)
