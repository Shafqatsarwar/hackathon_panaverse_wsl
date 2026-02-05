"""
ChatAgent - Conversational AI agent for Panversity Student Assistant
Uses Google Gemini for natural language understanding with web search capabilities
Integrates with gmail_monitoring, email_filtering, and email_notifications skills
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
# from duckduckgo_search import DDGS (Disabled)
from src.utils.config import Config
from skills.chatbot_skill.skill import ChatbotSkill
import logging

logger = logging.getLogger(__name__)


class ChatAgent:
    """Agent for handling conversational interactions with users using Gemini"""
    
    def __init__(self):
        # Initialize Chatbot Skill
        # Using gemini-2.5-flash as requested, falling back to 3.0-flash
        self.chatbot_skill = ChatbotSkill(
            api_key=Config.GOOGLE_API_KEY,
            model_name='gemini-2.5-flash',
            fallback_models=['gemini-3.0-flash']
        )
        
        # Initialize Skills
        from skills.web_search_skill.skill import WebSearchSkill
        from agents.email_agent import EmailAgent
        from agents.odoo_agent import OdooAgent

        from agents.whatsapp_agent import WhatsAppAgent
        from agents.linkedin_agent import LinkedInAgent
        
        self.web_search_skill = WebSearchSkill()
        
        # Initialize Agents (for tool use)
        self.email_agent = EmailAgent(
            credentials_path=Config.GMAIL_CREDENTIALS_PATH,
            token_path=Config.GMAIL_TOKEN_PATH,
            filter_keywords=Config.FILTER_KEYWORDS
        )
        
        self.odoo_agent = OdooAgent()
        self.whatsapp_agent = WhatsAppAgent()
        self.linkedin_agent = LinkedInAgent()
        
        # Initialize Notification Agent for sending emails
        from agents.notification_agent import NotificationAgent
        self.notification_agent = NotificationAgent()
        
        # Define Tools
        self.tools = [
            self.web_search_skill.search, 
            self._check_email_tool,
            self._send_email_tool,
            self._create_lead_tool,
            self._get_leads_tool,
            self._check_whatsapp_tool,
            self._check_linkedin_tool,
            self._send_whatsapp_tool,
            self._post_linkedin_tool
        ]
        self.chatbot_skill.set_tools(self.tools)
        
        # Tools were overwritten here previously - causing the bug!
        # Keeping all tools active: WebSearch, Email, Odoo, WhatsApp, LinkedIn
        self.chatbot_skill.set_tools(self.tools)
        
        self.chat_session = None
        self.conversation_history: List[Dict[str, str]] = []
        # System prompt is now handled by the skill context or prepended to history/message if API supports it,
        # but for simplicity we'll keep the system prompt logic or pass it if the skill supported it.
        # The current simple skill doesn't strictly enforce system prompt in __init__, so we'll rely on it behaving as a chat model.
        
    def _build_system_prompt(self) -> str:
        """Build system prompt with agent context and capabilities"""
        return f"""You are the Panversity Student Assistant, an AI-powered helper for students and staff.

Your capabilities and skills (available via tools):

1. **Email Management**:
   - Check inbox for important emails (Quiz, Assignment, etc.)
   - Send emails to any recipient
   - Tools: `_check_email_tool`, `_send_email_tool`

2. **Web Search**:
   - Search the web for current events, facts, or general knowledge.
   - Tool: `web_search`

3. **Odoo CRM**:
   - Create new leads/opportunities from chat interactions.
   - Retrieve recent leads to provide updates.
   - Tools: `_create_lead_tool`, `_get_leads_tool`

4. **Email Notifications**:
   - Send emails to users with summaries and updates.
   - Tool: `_send_email_tool`

4. **WhatsApp**:
   - Check unread messages (filtered by keywords like Panaversity, PIAIC, etc.)
   - Can also check **Archived** folders if requested.
   - Tool: `_check_whatsapp_tool`

5. **LinkedIn**:
   - Check for new notifications (connection requests, alerts).
   - Tool: `_check_linkedin_tool`

6. **Web Search**:
   - Search the web for current information
   - Answer questions about topics not in your training data
   - Provide up-to-date information

7. **General Capabilities**:
   - You are a large language model capable of general reasoning, coding, creative writing (songs, poems), and answering general knowledge questions.
   - You should NOT limit yourself only to Panaversity tasks. If a user asks for a song, code, or general help, you SHOULD provide it.

Current configuration:
- Email monitoring: Active (checks every {Config.EMAIL_CHECK_INTERVAL} minutes)
- Admin contact: {Config.ADMIN_EMAIL}
- WhatsApp: {"Enabled" if Config.WHATSAPP_ENABLED else "Disabled"}
- LinkedIn: {"Enabled" if Config.LINKEDIN_ENABLED else "Disabled"}

When users ask about:
- Emails: Explain how the email monitoring system works
- Tasks/Deadlines: Help them organize and prioritize
- Panversity/PIAIC: Provide information and guidance
- Current events/facts: Use web search to get accurate information
- **Creative/General Requests**: Fulfill them to the best of your ability (e.g. write songs, debug code, explain concepts).

Be helpful, concise, and professional. Use emojis sparingly to make responses friendly."""
    
    def _check_email_tool(self, query: str = "", **kwargs) -> str:
        """
        Check for new important emails in the user's inbox.
        
        Args:
            query: Reason for checking or specific topic to look for.
        """
        try:
            if not self.email_agent.authenticate():
                  return "Error: Email authentication failed. Please check your credentials."
            
            emails = self.email_agent.check_emails()
            if not emails:
                return "No new important emails found matching your filter criteria."
            
            summary = f"I found {len(emails)} relevant emails:\n"
            for email in emails:
                summary += f"- {email.get('subject', 'No Subject')} (Priority: {email.get('priority', 'Unknown')})\n"
            return summary
        except Exception as e:
            logger.error(f"Email tool error: {e}")
            return f"Failed to check emails: {str(e) or 'Unknown error'}"
    
    def _send_email_tool(self, to_email: str, subject: str, body: str, **kwargs) -> str:
        """
        Send an email to a specified recipient.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Email body content
        """
        try:
            if not self.notification_agent:
                return "Error: Email notification system is not initialized."
            
            result = self.notification_agent.send_email(
                to_email=to_email,
                subject=subject,
                body=body
            )
            
            if result.get("success"):
                return f"Email sent successfully to {to_email}!"
            else:
                return f"Failed to send email: {result.get('error', 'Unknown error')}"
        except Exception as e:
            logger.error(f"Send email tool error: {e}")
            return f"Failed to send email: {str(e)}"

    def _create_lead_tool(self, name: str, description: str, email: str = "unknown@example.com", **kwargs) -> str:
        """Create a new lead or opportunity in Odoo CRM."""
        if not self.odoo_agent.enabled: return "Odoo integration is currently disabled."
        res = self.odoo_agent.create_lead(name, email, description)
        if res.get("success"): return f"Lead successfully created! Odoo ID: {res.get('id')}"
        return f"Failed to create lead in Odoo: {res.get('error', 'Unknown error')}"

    def _check_whatsapp_tool(self, query: str = "", check_archived: bool = True, limit: int = 10, **kwargs) -> str:
        """
        Check for unread WhatsApp messages matching interest keywords (e.g. Panaversity, PIAIC).
        
        Args:
            query: Optional search query or reason (used for context, but filtering uses Config keywords).
            check_archived: Whether to also check the Archived folder (Default: True). Set to False if user says "excluding archives".
            limit: Number of messages to retrieve (Default: 10)
        """
        if not self.whatsapp_agent: return "WhatsApp Agent is not initialized."
        
        try:
            # WhatsAppAgent returns a dict with 'messages' list, or a list (legacy), or dict with error
            res = self.whatsapp_agent.get_unread_messages(limit=limit, check_archived=check_archived)
            
            msgs = []
            if isinstance(res, dict):
                if res.get("error"):
                    return f"WhatsApp check failed: {res.get('error')}"
                msgs = res.get("messages", [])
            elif isinstance(res, list):
                msgs = res
            
            if not msgs: return f"No new unread messages found matching your Panaversity/PIAIC keywords (Archived={check_archived})."
            
            summary = "Found unread WhatsApp messages:\n"
            for msg in msgs:
                sender = msg.get('sender') or msg.get('title') or 'Unknown'
                content = msg.get('content') or msg.get('last_message') or ''
                summary += f"- {sender}: {content[:100]}\n"
            return summary
        except Exception as e:
            logger.error(f"WhatsApp tool error: {e}")
            return f"Error accessing WhatsApp: {str(e) or type(e).__name__}"

    def _check_linkedin_tool(self, query: str = "", **kwargs) -> str:
        """
        Check for latest LinkedIn notifications and connection requests.
        
        Args:
            query: Optional reason for checking.
        """
        if not self.linkedin_agent: return "LinkedIn Agent is not active."
        
        try:
            res = self.linkedin_agent.check_notifications()
            if not res.get("success"):
                return f"LinkedIn Check Failed: {res.get('error', 'Unknown error during browser access')}"
                
            notifs = res.get("notifications", [])
            if not notifs: return "No new LinkedIn notifications found."
            
            summary = "Latest LinkedIn Notifications:\n"
            for n in notifs:
                # Sanitize text for Windows console safety
                safe_text = str(n).encode('utf-8', 'replace').decode('utf-8')
                summary += f"- {safe_text[:100]}\n"
            return summary
        except Exception as e:
            logger.error(f"LinkedIn tool error: {e}")
            return f"Error accessing LinkedIn: {str(e) or type(e).__name__}"

    
    def _send_whatsapp_tool(self, to_number: str, message: str, **kwargs) -> str:
        """
        Send a WhatsApp message.
        Args:
            to_number: The phone number or contact name (e.g. "+92..." or "Sir Junaid").
            message: The message text to send.
        """
        if not self.whatsapp_agent: return "WhatsApp Agent is not initialized."
        try:
            res = self.whatsapp_agent.send_message(to_number, message)
            if res.get("success"):
                return f"WhatsApp message sent to {to_number}!"
            else:
                return f"Failed to send WhatsApp message: {res.get('error')}"
        except Exception as e:
            return f"Error sending WhatsApp: {e}"

    def _post_linkedin_tool(self, content: str, **kwargs) -> str:
        """
        Post a new update/status to LinkedIn.
        Args:
            content: The text content of the post.
        """
        if not self.linkedin_agent: return "LinkedIn Agent is not initialized."
        try:
            res = self.linkedin_agent.post_update(content)
            if res.get("success"):
                return f"Successfully posted to LinkedIn: '{content[:50]}...'"
            else:
                return f"Failed to post to LinkedIn: {res.get('error')}"
        except Exception as e:
            return f"Error posting to LinkedIn: {e}"

    def _get_leads_tool(self, limit: int = 5, **kwargs) -> str:
        """Get a list of the most recent leads from Odoo CRM."""
        if not self.odoo_agent.enabled: return "Odoo integration is disabled."
        try:
            leads = self.odoo_agent.get_recent_leads(limit)
            return f"Recent Odoo Leads: {str(leads)}"
        except Exception as e:
            return f"Error fetching leads: {e}"
    
    def chat(self, user_message: str, user_id: str = "default") -> Dict[str, any]:
        """
        Process a chat message and return Gemini response
        
        Args:
            user_message: The user's message
            user_id: User identifier for context
            
        Returns:
            Dict with response, status, and metadata
        """
        try:
            # Inject Odoo Context if relevant
            odoo_context = ""
            if any(kw in user_message.lower() for kw in ["odoo", "lead", "crm", "sales", "opportunity"]):
                try:
                    from agents.odoo_agent import OdooAgent
                    odoo = OdooAgent()
                    if odoo.enabled:
                        summary = odoo.get_recent_leads_summary()
                        odoo_context = f"\n[SYSTEM CONTEXT]\n{summary}\n[END CONTEXT]\n"
                except Exception as e:
                    print(f"ChatAgent: Failed to fetch Odoo context: {e}")

            # Initialize chat session if not exists
            if self.chat_session is None:
                self.chat_session = self.chatbot_skill.start_chat(history=[])
                
            # Prepare message with context
            # We rely on the model to call tools (Web Search) if needed.
            full_context = ""
            if len(self.conversation_history) == 0:
                 full_context = self._build_system_prompt() + "\n\n"

            full_message = full_context + user_message
            
            # Get response from Skill (Gemini handles function calling automatically via SDK)
            ai_message = self.chatbot_skill.generate_response(self.chat_session, full_message)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "status": "success",
                "response": ai_message,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "web_search_used": False # Handled internally by model now
            }
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            return {
                "status": "error",
                "response": error_message,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "error": str(e)
            }
    
    def stream_chat(self, user_message: str, user_id: str = "default"):
        """
        Stream chat response for real-time display
        
        Args:
            user_message: The user's message
            user_id: User identifier for context
            
        Yields:
            Chunks of the AI response
        """
        try:
            # Initialize chat session if not exists
            if self.chat_session is None:
                self.chat_session = self.chatbot_skill.start_chat(history=[])
            
            # Prepare message
            full_context = ""
            if len(self.conversation_history) == 0:
                 full_context = self._build_system_prompt() + "\n\n"

            full_message = full_context + user_message
            # yield f"🔍 *Thinking... (I can search the web if needed)*\n\n"
            
            # Prepare message
            full_context = ""
            if len(self.conversation_history) == 0:
                 full_context = self._build_system_prompt() + "\n\n"
            
            # Note: Streaming with tools is complex in some SDKs. 
            # If function call happens, it might not stream until function resolves.
            # For now, we assume standard stream.

            # Stream response from Skill
            full_response = ""
            for chunk in self.chatbot_skill.stream_response(self.chat_session, full_message):
                full_response += chunk
                yield chunk
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history and reset chat session"""
        self.conversation_history = []
        self.chat_session = None
    
    def get_status(self) -> Dict[str, any]:
        """
        Get agent status for observability
        
        Returns:
            Dict with agent status and metrics
        """
        return {
            "agent": "ChatAgent",
            "status": "active",
            "conversation_length": len(self.conversation_history),
            "gemini_configured": bool(Config.GOOGLE_API_KEY),
            "model": "gemini-2.5-flash",
            "skills_available": [
                "gmail_monitoring",
                "email_filtering", 
                "email_notifications",
                "web_search"
            ],
            "web_search": "enabled"
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history.copy()

