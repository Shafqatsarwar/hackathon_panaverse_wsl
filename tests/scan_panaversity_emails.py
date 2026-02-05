"""
Gmail Scanner for Panaversity/PIAIC Announcements
Scans January 2026 emails for batch announcements and sends summary
"""
import sys
import os
import logging
from datetime import datetime
from typing import List, Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from src.utils.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PanaversityEmailScanner")

def send_summary_email(summary_html: str, recipient: str) -> bool:
    """Send summary email via SMTP"""
    try:
        logger.info(f"Sending summary email to {recipient}...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = recipient
        msg['Subject'] = f"Panaversity/PIAIC January 2026 Announcements Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Create HTML part
        html_part = MIMEText(summary_html, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info("Summary email sent successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

def create_html_summary(emails: List[Dict[str, Any]]) -> str:
    """Create HTML summary of emails"""
    
    # Group by batch
    batch_47 = []
    batch_82 = []
    batch_77 = []
    general = []
    
    for email in emails:
        subject = email.get('subject', '').lower()
        snippet = email.get('snippet', '').lower()
        combined = subject + ' ' + snippet
        
        if 'batch 47' in combined or 'batch47' in combined:
            batch_47.append(email)
        elif 'batch 82' in combined or 'batch82' in combined:
            batch_82.append(email)
        elif 'batch 77' in combined or 'batch77' in combined:
            batch_77.append(email)
        else:
            general.append(email)
    
    # Create HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #2980b9;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 10px;
            }}
            .email-item {{
                background: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }}
            .email-subject {{
                font-weight: bold;
                color: #2c3e50;
                font-size: 16px;
                margin-bottom: 8px;
            }}
            .email-from {{
                color: #7f8c8d;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .email-date {{
                color: #95a5a6;
                font-size: 13px;
                margin-bottom: 10px;
            }}
            .email-snippet {{
                color: #555;
                font-size: 14px;
                line-height: 1.5;
            }}
            .stats {{
                background: #e8f4f8;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .stat-item {{
                display: inline-block;
                margin-right: 20px;
                font-weight: bold;
            }}
            .badge {{
                background: #3498db;
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 12px;
                margin-left: 5px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ecf0f1;
                color: #7f8c8d;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <h1>📧 Panaversity/PIAIC January 2026 Announcements</h1>
        
        <div class="stats">
            <div class="stat-item">Total Emails: <span class="badge">{len(emails)}</span></div>
            <div class="stat-item">Batch 47: <span class="badge">{len(batch_47)}</span></div>
            <div class="stat-item">Batch 82: <span class="badge">{len(batch_82)}</span></div>
            <div class="stat-item">Batch 77: <span class="badge">{len(batch_77)}</span></div>
            <div class="stat-item">General: <span class="badge">{len(general)}</span></div>
        </div>
    """
    
    # Add Batch 47 section
    if batch_47:
        html += f"""
        <h2>🎓 Batch 47 Announcements ({len(batch_47)})</h2>
        """
        for email in batch_47:
            html += f"""
            <div class="email-item">
                <div class="email-subject">{email.get('subject', 'No Subject')}</div>
                <div class="email-from">From: {email.get('sender', 'Unknown')}</div>
                <div class="email-date">Date: {email.get('date', 'Unknown')}</div>
                <div class="email-snippet">{email.get('snippet', 'No preview available')}</div>
            </div>
            """
    
    # Add Batch 82 section
    if batch_82:
        html += f"""
        <h2>🎓 Batch 82 Announcements ({len(batch_82)})</h2>
        """
        for email in batch_82:
            html += f"""
            <div class="email-item">
                <div class="email-subject">{email.get('subject', 'No Subject')}</div>
                <div class="email-from">From: {email.get('sender', 'Unknown')}</div>
                <div class="email-date">Date: {email.get('date', 'Unknown')}</div>
                <div class="email-snippet">{email.get('snippet', 'No preview available')}</div>
            </div>
            """
    
    # Add Batch 77 section
    if batch_77:
        html += f"""
        <h2>🎓 Batch 77 Announcements ({len(batch_77)})</h2>
        """
        for email in batch_77:
            html += f"""
            <div class="email-item">
                <div class="email-subject">{email.get('subject', 'No Subject')}</div>
                <div class="email-from">From: {email.get('sender', 'Unknown')}</div>
                <div class="email-date">Date: {email.get('date', 'Unknown')}</div>
                <div class="email-snippet">{email.get('snippet', 'No preview available')}</div>
            </div>
            """
    
    # Add General section
    if general:
        html += f"""
        <h2>📢 General Panaversity Announcements ({len(general)})</h2>
        """
        for email in general:
            html += f"""
            <div class="email-item">
                <div class="email-subject">{email.get('subject', 'No Subject')}</div>
                <div class="email-from">From: {email.get('sender', 'Unknown')}</div>
                <div class="email-date">Date: {email.get('date', 'Unknown')}</div>
                <div class="email-snippet">{email.get('snippet', 'No preview available')}</div>
            </div>
            """
    
    html += f"""
        <div class="footer">
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Source:</strong> {Config.GMAIL_ADDRESS}</p>
            <p><strong>Powered by:</strong> Panaversity Student Assistant AI</p>
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    logger.info("="*70)
    logger.info("Panaversity/PIAIC Email Scanner - January 2026")
    logger.info("="*70)
    
    # Initialize Gmail monitor
    logger.info("\n[1/3] Initializing Gmail Monitor...")
    
    keywords = [
        "Panaversity", "PIAIC", "Panaverse",
        "batch 47", "batch47", "batch 82", "batch82", "batch 77", "batch77",
        "announcement", "quiz", "assignment", "exam", "deadline"
    ]
    
    gmail = GmailMonitoringSkill(
        credentials_path=Config.GMAIL_CREDENTIALS_PATH,
        token_path=Config.GMAIL_TOKEN_PATH,
        keywords=keywords
    )
    
    # Authenticate
    if not gmail.authenticate():
        logger.error("Failed to authenticate with Gmail")
        logger.error("Please ensure credentials.json and token.json are configured")
        return {
            'emails_found': 0,
            'email_sent': False,
            'recipient': "khansarwar1@hotmail.com"
        }
    
    # Search for January 2026 emails
    logger.info("[2/3] Searching for Panaversity/PIAIC emails in January 2026...")
    
    # Fetch unread emails (we'll filter for January manually)
    all_emails = gmail.fetch_unread_emails(max_results=100)
    
    # Filter for January 2026
    january_emails = []
    for email in all_emails:
        date_str = email.get('date', '')
        if '2026-01' in date_str or 'Jan 2026' in date_str:
            january_emails.append(email)
    
    if not january_emails:
        logger.warning("No emails found matching the criteria")
        logger.info("\nNote: This searches unread emails only")
        logger.info("If you've already read January emails, they won't appear")
        return {
            'emails_found': 0,
            'email_sent': False,
            'recipient': "khansarwar1@hotmail.com"
        }
    
    logger.info(f"\nFound {len(january_emails)} emails!")
    
    # Display summary
    logger.info("\nEmail Summary:")
    for idx, email in enumerate(january_emails[:10], 1):
        logger.info(f"\n{idx}. {email.get('subject', 'No Subject')}")
        logger.info(f"   From: {email.get('sender', 'Unknown')}")
        logger.info(f"   Date: {email.get('date', 'Unknown')}")
        logger.info(f"   Preview: {email.get('snippet', '')[:100]}...")
    
    if len(january_emails) > 10:
        logger.info(f"\n... and {len(january_emails) - 10} more emails")
    
    # Create HTML summary
    logger.info("\n[3/3] Creating and sending summary email...")
    html_summary = create_html_summary(january_emails)
    
    # Send email
    recipient = "khansarwar1@hotmail.com"
    success = send_summary_email(html_summary, recipient)
    
    if success:
        logger.info("\n" + "="*70)
        logger.info("SUCCESS! Summary email sent!")
        logger.info("="*70)
        logger.info(f"\nSummary sent to: {recipient}")
        logger.info(f"Total emails found: {len(january_emails)}")
        logger.info(f"Date range: January 2026")
    else:
        logger.error("\nFailed to send summary email")
        logger.info("\nYou can still view the emails in the logs above")
    
    return {
        'emails_found': len(january_emails),
        'email_sent': success,
        'recipient': recipient
    }

if __name__ == "__main__":
    try:
        result = main()
        
        print("\n" + "="*70)
        print("FINAL RESULT:")
        print("="*70)
        print(f"Emails found: {result['emails_found']}")
        print(f"Summary sent: {'YES' if result['email_sent'] else 'NO'}")
        print(f"Recipient: {result['recipient']}")
        print("="*70)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
