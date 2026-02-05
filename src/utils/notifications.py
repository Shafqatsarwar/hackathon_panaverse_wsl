"""
Notification system for Panaversity Student Assistant
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Handle email and WhatsApp notifications"""
    
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
    
    def send_email_notification(self, to_email: str, subject: str, body: str, html: bool = False) -> bool:
        """Send email notification via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def format_email_summary(self, email_data: Dict[str, Any]) -> str:
        """Format email data into a readable summary"""
        subject = email_data.get('subject', 'No Subject')
        sender = email_data.get('sender', 'Unknown Sender')
        date = email_data.get('date', 'Unknown Date')
        snippet = email_data.get('snippet', '')
        keywords = email_data.get('keywords', [])
        priority = email_data.get('priority', 'low')
        
        summary = f"""
📧 New Panaversity Email Alert
{'=' * 50}

From: {sender}
Subject: {subject}
Date: {date}
Priority: {priority.upper()}

Keywords: {', '.join(keywords) if keywords else 'None'}

Preview:
{snippet}

{'=' * 50}
Panaversity Student Assistant
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return summary
    
    def format_email_summary_html(self, email_data: Dict[str, Any]) -> str:
        """Format email data into HTML summary"""
        subject = email_data.get('subject', 'No Subject')
        sender = email_data.get('sender', 'Unknown Sender')
        date = email_data.get('date', 'Unknown Date')
        snippet = email_data.get('snippet', '')
        keywords = email_data.get('keywords', [])
        priority = email_data.get('priority', 'low')
        
        priority_color = {
            'high': '#ff4444',
            'medium': '#ffaa00',
            'low': '#44ff44'
        }.get(priority, '#888888')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #4285f4; color: white; padding: 15px; border-radius: 5px; }}
        .content {{ background: #f5f5f5; padding: 20px; margin-top: 10px; border-radius: 5px; }}
        .priority {{ display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; background: {priority_color}; }}
        .keywords {{ color: #4285f4; font-weight: bold; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #888; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>📧 New Panaversity Email Alert</h2>
        </div>
        <div class="content">
            <p><strong>From:</strong> {sender}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Priority:</strong> <span class="priority">{priority.upper()}</span></p>
            <p><strong>Keywords:</strong> <span class="keywords">{', '.join(keywords) if keywords else 'None'}</span></p>
            <hr>
            <p><strong>Preview:</strong></p>
            <p>{snippet}</p>
        </div>
        <div class="footer">
            <p>Panaversity Student Assistant</p>
            <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def send_whatsapp_notification(self, number: str, message: str) -> bool:
        """Send WhatsApp notification (placeholder for future implementation)"""
        logger.warning("WhatsApp notifications not yet implemented")
        return False
    
    def notify_new_email(self, admin_email: str, email_data: Dict[str, Any]) -> bool:
        """Send notification about new relevant email"""
        subject = f"🎓 Panaversity Alert: {email_data.get('subject', 'New Email')}"
        
        # Send plain text version
        text_body = self.format_email_summary(email_data)
        
        # Send HTML version
        html_body = self.format_email_summary_html(email_data)
        
        return self.send_email_notification(admin_email, subject, html_body, html=True)
