"""
Configuration management for Panaversity Student Assistant
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class Config:
    """Application configuration"""
    
    # Gmail Configuration
    GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "exellencelinks@gmail.com")
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
    
    # Admin Notifications
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "khansarwar1@hotmail.com")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "Admin@123")
    ADMIN_WHATSAPP = os.getenv("ADMIN_WHATSAPP", "+923244279017")
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "exellencelinks@gmail.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # Feature Flags
    WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "false").lower() == "true"
    LINKEDIN_ENABLED = os.getenv("LINKEDIN_ENABLED", "false").lower() == "true"
    
    # LinkedIn Configuration
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "exellencelinks@gmail.com")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")

    # Odoo Configuration
    ODOO_URL = os.getenv("ODOO_URL", "")
    ODOO_DB = os.getenv("ODOO_DB", "")
    ODOO_USERNAME = os.getenv("ODOO_USERNAME", "")
    ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "")
    
    # Check Intervals (in minutes)
    EMAIL_CHECK_INTERVAL = int(os.getenv("EMAIL_CHECK_INTERVAL", "15"))
    WHATSAPP_CHECK_INTERVAL = int(os.getenv("WHATSAPP_CHECK_INTERVAL", "60"))
    LINKEDIN_CHECK_INTERVAL = int(os.getenv("LINKEDIN_CHECK_INTERVAL", "60"))
    
    # Keywords for filtering
    FILTER_KEYWORDS = os.getenv("FILTER_KEYWORDS", "Panversity,PIAIC,Quiz,Assignment,Exam,Deadline").split(",")
    
    # Forwarding Configuration
    WHATSAPP_FORWARD_MESSAGES = os.getenv("WHATSAPP_FORWARD_MESSAGES", "")  # WhatsApp number to forward to
    EMAIL_FORWARD_EMAIL = os.getenv("EMAIL_FORWARD_EMAIL", "")  # Email address to forward to
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if not cls.GMAIL_ADDRESS:
            errors.append("GMAIL_ADDRESS is required")
        
        if not cls.ADMIN_EMAIL:
            errors.append("ADMIN_EMAIL is required")
        
        if not cls.SMTP_PASSWORD:
            errors.append("SMTP_PASSWORD is required for email notifications")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Print current configuration (hiding sensitive data)"""
        print("=" * 50)
        print("Panaversity Student Assistant Configuration")
        print("=" * 50)
        print(f"Gmail Address: {cls.GMAIL_ADDRESS}")
        print(f"Admin Email: {cls.ADMIN_EMAIL}")
        print(f"Admin WhatsApp: {cls.ADMIN_WHATSAPP}")
        print(f"WhatsApp Enabled: {cls.WHATSAPP_ENABLED}")
        print(f"LinkedIn Enabled: {cls.LINKEDIN_ENABLED}")
        print(f"Email Check Interval: {cls.EMAIL_CHECK_INTERVAL} minutes")
        print(f"Filter Keywords: {', '.join(cls.FILTER_KEYWORDS)}")
        print(f"SMTP Configured: {'Yes' if cls.SMTP_PASSWORD else 'No'}")
        print("=" * 50)
