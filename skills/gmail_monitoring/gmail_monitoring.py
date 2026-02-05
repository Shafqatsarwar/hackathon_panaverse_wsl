"""
Gmail Monitoring Skill
Provides Gmail API integration for email monitoring
"""
import os
import pickle
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.utils import parsedate_to_datetime

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailMonitoringSkill:
    """Gmail monitoring skill for fetching and filtering emails"""
    
    def __init__(self, credentials_path: str, token_path: str, keywords: List[str]):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.keywords = [k.lower().strip() for k in keywords]
        self.service = None
        self.last_check_time = None
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail API"""
        try:
            creds = None
            
            if os.path.exists(self.token_path):
                try:
                    with open(self.token_path, 'rb') as token:
                        creds = pickle.load(token)
                except Exception as e:
                    logger.warning(f"Failed to load token: {e}")
                    creds = None
            
            # If creds exist but are invalid, try to refresh
            if creds and not creds.valid:
                if creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        logger.warning(f"Token refresh failed: {e}. Re-authenticating...")
                        creds = None
                else:
                    creds = None

            # If no valid creds (either didn't exist, load failed, or refresh failed)
            if not creds:
                if not os.path.exists(self.credentials_path):
                    logger.error(f"Credentials file not found: {self.credentials_path}")
                    return False
                
                # Run local server for initial auth
                print("Initiating Gmail Authentication... Check your browser.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the new credentials
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail authentication successful")
            return True
        
        except Exception as e:
            logger.error(f"Gmail authentication failed: {str(e)}")
            return False
    
    def fetch_unread_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Fetch unread emails from Gmail"""
        if not self.service:
            logger.error("Gmail service not initialized")
            return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return []
            
            emails = []
            for msg in messages:
                email_data = self._get_email_details(msg['id'])
                if email_data:
                    emails.append(email_data)
            
            logger.info(f"Fetched {len(emails)} unread emails")
            return emails
        
        except HttpError as error:
            logger.error(f"Failed to fetch emails: {error}")
            return []
    
    def _get_email_details(self, msg_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
            date_str = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
            
            try:
                date = parsedate_to_datetime(date_str).strftime('%Y-%m-%d %H:%M:%S') if date_str else 'Unknown Date'
            except:
                date = date_str or 'Unknown Date'
            
            snippet = message.get('snippet', '')
            body = self._get_email_body(message)
            
            return {
                'id': msg_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'snippet': snippet,
                'body': body
            }
        
        except Exception as e:
            logger.error(f"Failed to get email details: {str(e)}")
            return None
    
    def _get_email_body(self, message: Dict) -> str:
        """Extract email body from message"""
        try:
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            else:
                data = message['payload']['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to extract email body: {str(e)}")
        
        return ""
    
    def filter_relevant_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter emails based on keywords"""
        from skills.email_filtering import EmailFilteringSkill
        
        filter_skill = EmailFilteringSkill(self.keywords)
        relevant_emails = []
        
        for email in emails:
            subject = email.get('subject', '')
            body = email.get('body', '')
            
            if filter_skill.is_relevant(subject, body):
                category = filter_skill.categorize_email(subject, body)
                email.update(category)
                relevant_emails.append(email)
        
        logger.info(f"Found {len(relevant_emails)} relevant emails")
        return relevant_emails
    
    def check_emails(self, mark_read: bool = False) -> List[Dict[str, Any]]:
        """
        Main method to check for new relevant emails.
        
        Args:
            mark_read: If True, marks fetched emails as read to prevent re-processing.
                       Defaults to False (safe mode).
        """
        logger.info("Checking for new emails...")
        
        emails = self.fetch_unread_emails()
        
        if not emails:
            return []
        
        relevant_emails = self.filter_relevant_emails(emails)
        self.last_check_time = datetime.now()
        
        # Optional: Mark as read if requested
        if mark_read and self.service:
            try:
                batch = self.service.new_batch_http_request()
                for email in emails: # Mark ALL fetched unread emails as read, or just relevant?
                    # Usually better to mark all as read so we don't get stuck on irrelevant spam,
                    # BUT that might be dangerous if the user misses non-relevant but personal emails.
                    # Safest: Mark ONLY relevant emails as read.
                    if email in relevant_emails:
                         self.service.users().messages().modify(
                            userId='me',
                            id=email['id'],
                            body={'removeLabelIds': ['UNREAD']}
                        ).execute()
            except Exception as e:
                logger.error(f"Failed to mark emails as read: {e}")

        return relevant_emails

    def mark_email_as_read(self, msg_id: str) -> bool:
        """Mark a single email as read"""
        try:
             self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
             return True
        except Exception as e:
            logger.error(f"Failed to mark email {msg_id} as read: {e}")
            return False

