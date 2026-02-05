
import logging
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(os.getcwd())

from skills.whatsapp_skill.skill import WhatsAppSkill
from src.utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FilterTask")

def process():
    logger.info("--- Starting WhatsApp Keyword Filter ---")
    
    # 1. Define Keywords
    keywords = ["PIAIC", "Panaversity", "Batch 47"]
    logger.info(f"Filtering for: {keywords}")
    
    # 2. Scan WhatsApp
    skill = WhatsAppSkill(enabled=True, headless=True)
    msgs = skill.check_messages(keywords=keywords, check_archived=True)
    
    if not msgs or ("error" in msgs[0]):
        logger.info("No messages found or error occurred.")
        return

    # 3. Compile Report
    report_lines = ["<h3>WhatsApp Scan Report</h3><ul>"]
    found_any = False
    
    for msg in msgs:
        if "error" in msg: continue
        found_any = True
        line = f"<li><strong>{msg.get('title')}</strong>: {msg.get('last_message')} <br><em>(Match: {msg.get('matched_keyword')})</em></li>"
        report_lines.append(line)
        logger.info(f"Match: {msg.get('title')}")
        
    report_lines.append("</ul>")
    
    if not found_any:
        logger.info("No matches for specified keywords.")
        return

    # 4. Send Email
    sender_email = Config.ADMIN_EMAIL # reusing config
    receiver_email = "khansarwar1@hotmail.com" # Requested email
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Important Updates: PIAIC & Panaversity (Batch 47)"
    
    body = "".join(report_lines)
    msg.attach(MIMEText(body, 'html'))
    
    try:
        if Config.SMTP_SERVER and Config.SMTP_PORT:
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {receiver_email}")
        else:
            logger.error("SMTP Config missing. Printing report instead:")
            print(body)
            
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

if __name__ == "__main__":
    process()
