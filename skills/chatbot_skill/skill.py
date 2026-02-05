"""
Chatbot Skill (Gemini Integration)
"""
import logging
import time
import google.generativeai as genai
# import nest_asyncio
from typing import Dict, Any, Generator

logger = logging.getLogger(__name__)

class ChatbotSkill:
    """Skill for AI generation using Gemini"""
    
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash', fallback_models: list = ['gemini-3.0-flash']):
        if not api_key:
            logger.warning("ChatbotSkill: No API Key provided")
            self.model = None
            self.model_name = None
        else:
            genai.configure(api_key=api_key)
            self.models_to_try = [model_name] + (fallback_models or [])
            self.current_model_index = 0
            self.tools = None
            self._initialize_model()

    def set_tools(self, tools: list):
        """Set tools for function calling"""
        self.tools = tools
        self._initialize_model()  # Re-init model with tools

    def _initialize_model(self):
        """Initialize the current model"""
        if self.current_model_index < len(self.models_to_try):
            model_name = self.models_to_try[self.current_model_index]
            logger.info(f"ChatbotSkill: Initializing model: {model_name} with tools: {bool(self.tools)}")
            self.model = genai.GenerativeModel(model_name=model_name, tools=self.tools)
            self.model_name = model_name
        else:
            logger.error("ChatbotSkill: All models failed to initialize or valid models exhausted.")
            self.model = None

    def _switch_to_fallback(self):
        """Switch to next available fallback model"""
        self.current_model_index += 1
        if self.current_model_index < len(self.models_to_try):
            logger.warning(f"ChatbotSkill: Switching to fallback model: {self.models_to_try[self.current_model_index]}")
            self._initialize_model()
            return True
        return False
    
    def start_chat(self, history: list = None):
        """Start a new chat session"""
        if not self.model:
            raise ValueError("Gemini not configured")
        # Ensure automatic function calling is enabled if tools present
        return self.model.start_chat(history=history or [], enable_automatic_function_calling=True if self.tools else False)
        
    def generate_response(self, chat_session, message: str, retries: int = 3) -> str:
        """Generate a response with retry logic"""
        if not self.model:
            return "Error: AI not configured."
            
        for attempt in range(retries):
            try:
                response = chat_session.send_message(message)
                return response.text
            except Exception as e:
                error_str = str(e)
                # Check for 404 (Not Found / Invalid Model) or 400 (Bad Request - typically model related if others work)
                if "404" in error_str or "not found" in error_str.lower() or "400" in error_str:
                     logger.warning(f"Model {self.model_name} failed with fatal error: {error_str}")
                     if self._switch_to_fallback():
                         # We need to restart the chat session with the new model
                         # Note: History preservation is complex here as 'chat_session' object is tied to model.
                         # SImple fallback: Start new session (or if caller handles session, this might be tricky).
                         # For this skill: We rely on the caller to handle session management usually, 
                         # but since we pass 'chat_session' in, we can't easily swap 'chat_session' IN PLACE.
                         # Workaround for Phase 6: We inform error, but if we init checks passed...
                         # Actually for 404, it usually happens on first call.
                         # Let's try to notify user or handle it. 
                         # Since this is a simple skill, we'll return error asking for retry which might trigger re-init?
                         # Better: Re-raise or return specific error?
                         return f"Error: Model {self.model_name} failed. Switched to fallback. Please retry."
                
                if "429" in error_str and attempt < retries - 1:
                    # Attempt to extract suggested wait time from error message
                    import re
                    wait_time = (attempt + 1) * 5 # Base wait
                    match = re.search(r"retry in (\d+\.?\d*)s", error_str)
                    if match:
                        wait_time = float(match.group(1)) + 1
                    
                    logger.warning(f"Rate limit hit, retrying in {wait_time}s... (Attempt {attempt+1}/{retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Generate Response Error: {error_str}")
                    return f"Error: {error_str}"
        return "Error: Failed after retries"
        
    def stream_response(self, chat_session, message: str, retries: int = 3) -> Generator[str, None, None]:
        """Stream a response with retry logic"""
        if not self.model:
            yield "Error: AI not configured."
            return
            
        for attempt in range(retries):
            try:
                # Disable streaming if tools are present to avoid SDK error
                do_stream = True if not self.tools else False
                
                response = chat_session.send_message(message, stream=do_stream)
                
                if do_stream:
                    for chunk in response:
                        if hasattr(chunk, 'text') and chunk.text:
                            yield chunk.text
                else:
                    # If not streaming, yield the full text at once
                    if response.text:
                        yield response.text
                return
            except Exception as e:
                if "429" in str(e) and attempt < retries - 1:
                    import re
                    wait_time = (attempt + 1) * 5
                    match = re.search(r"retry in (\d+\.?\d*)s", str(e))
                    if match:
                        wait_time = float(match.group(1)) + 1
                        
                    logger.warning(f"Rate limit hit, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    error_msg = str(e) or type(e).__name__
                    logger.error(f"ChatbotSkill Stream Error: {error_msg}")
                    yield f"Error: {error_msg}"
                    return
        yield "Error: Failed after retries"
