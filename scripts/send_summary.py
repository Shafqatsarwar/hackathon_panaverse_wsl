import os
import sys
import asyncio
import logging
from datetime import datetime
import io

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Force UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.utils.config import Config
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from skills.whatsapp_skill.skill import WhatsAppSkill
from skills.linkedin_skill.skill import LinkedInSkill
from skills.odoo_skill.skill import OdooSkill
from src.utils.notifications import NotificationService

# Setup logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("summary_debug.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SummaryReport")

async def gather_data():
    summary_report = f"PANAVERSITY AI EMPLOYEE - ACTIVITY SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
    summary_report += "="*80 + "\n\n"

    # 1. GMAIL
    summary_report += "[1] GMAIL UPDATES\n"
    summary_report += "-"*20 + "\n"
    try:
        gmail = GmailMonitoringSkill(
            credentials_path=Config.GMAIL_CREDENTIALS_PATH,
            token_path=Config.GMAIL_TOKEN_PATH,
            keywords=Config.FILTER_KEYWORDS
        )
        if gmail.authenticate():
            emails = gmail.fetch_unread_emails(max_results=5)
            if emails:
                for email in emails:
                    summary_report += f"- FROM: {email.get('sender')} | SUBJECT: {email.get('subject')}\n"
            else:
                summary_report += "No new relevant emails found.\n"
        else:
            summary_report += "Gmail Authentication Failed.\n"
    except Exception as e:
        summary_report += f"Gmail Error: {str(e)}\n"
    summary_report += "\n"

    # 2. WHATSAPP
    summary_report += "[2] WHATSAPP UPDATES\n"
    summary_report += "-"*20 + "\n"
    try:
        wa = WhatsAppSkill(enabled=True, headless=True)
        wa_data = await wa.check_messages_async(keywords=Config.FILTER_KEYWORDS, limit=10)
        if wa_data.get("success"):
            msgs = wa_data.get("messages", [])
            if msgs:
                for m in msgs:
                    summary_report += f"- [{m.get('title')}] Last: {m.get('last_message')[:50]}... ({m.get('unread', '0')} unread)\n"
            else:
                summary_report += "No new relevant WhatsApp messages.\n"
        else:
            summary_report += f"WhatsApp Check Failed: {wa_data.get('error')}\n"
    except Exception as e:
        summary_report += f"WhatsApp Error: {str(e)}\n"
    summary_report += "\n"

    # 3. ODOO CRM LEADS
    summary_report += "[3] ODOO CRM LEADS\n"
    summary_report += "-"*20 + "\n"
    try:
        odoo = OdooSkill()
        leads = odoo.get_leads(limit=5)
        if leads:
            for L in leads:
                summary_report += f"- ID: {L.get('id')} | NAME: {L.get('name')} | EMAIL: {L.get('email_from')}\n"
        else:
            summary_report += "No recent leads found in Odoo (or connection failed).\n"
    except Exception as e:
        summary_report += f"Odoo Exception: {str(e)}\n"
    summary_report += "\n"

    # 4. LINKEDIN
    summary_report += "[4] LINKEDIN NOTIFICATIONS & MESSAGES\n"
    summary_report += "-"*20 + "\n"
    try:
        li = LinkedInSkill(enabled=True, headless=True)
        li_data = li.scrape_leads() 
        if li_data.get("success"):
            notifs = li_data.get("notifications", [])
            if notifs:
                summary_report += "Notifications:\n"
                for n in notifs[:3]:
                    summary_report += f"  - {n[:100]}...\n"
            
            msgs = li_data.get("messages", [])
            if msgs:
                summary_report += "Messages:\n"
                for m in msgs:
                    summary_report += f"  - FROM: {m.get('sender')} | TEXT: {m.get('content')[:50]}...\n"
            
            if not notifs and not msgs:
                 summary_report += "No new LinkedIn notifications or messages.\n"
        else:
            summary_report += f"LinkedIn Error: {li_data.get('error')}\n"
    except Exception as e:
        summary_report += f"LinkedIn Exception: {str(e)}\n"
    
    summary_report += "\n" + "="*80 + "\n"
    summary_report += "End of Report"
    
    return summary_report

async def main():
    logger.info("Gathering data for summary report...")
    report = await gather_data()
    
    # Save report locally for backup
    with open("LAST_SUMMARY_REPORT.txt", "w", encoding='utf-8') as f:
        f.write(report)
        
    print("\nREPORT PREVIEW:")
    print("-" * 40)
    print(report)
    print("-" * 40)
    
    # Send via Email
    target_email = Config.EMAIL_FORWARD_EMAIL or Config.ADMIN_EMAIL
    logger.info(f"Sending summary email to {target_email}...")
    try:
        notifier = NotificationService(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            smtp_username=Config.SMTP_USERNAME,
            smtp_password=Config.SMTP_PASSWORD
        )
        
        success = notifier.send_email_notification(
            to_email=target_email,
            subject=f"Panaversity AI - Activity Summary {datetime.now().strftime('%Y-%m-%d')}",
            body=report
        )
        
        if success:
            logger.info("Summary email sent successfully!")
        else:
            logger.error("Failed to send summary email.")
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")

    # Send via WhatsApp (NEW)
    target_number = Config.WHATSAPP_FORWARD_MESSAGES or Config.ADMIN_WHATSAPP
    logger.info(f"Sending summary to WhatsApp {target_number}...")
    try:
        wa = WhatsAppSkill(enabled=True, headless=True)
        # We use the existing WhatsApp session
        wa_result = await wa.send_message_async(target_number, f"*ACTIVITY SUMMARY*\n{report[:1000]}...") # Truncate if too long
        
        if wa_result.get("success"):
            logger.info("Summary WhatsApp sent successfully!")
        else:
            logger.error(f"Failed to send summary WhatsApp: {wa_result.get('error')}")
    except Exception as e:
        logger.error(f"Error sending WhatsApp: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
