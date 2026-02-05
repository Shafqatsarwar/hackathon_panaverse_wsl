"""
WhatsApp Baileys Python Bridge
Connects to the Baileys Node.js microservice via REST API.

This replaces the old Playwright-based skill with a much more reliable solution.

Usage:
    skill = WhatsAppBaileysSkill()
    result = skill.send_message("+923244279017", "Hello!")
"""
import logging
import requests
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class WhatsAppBaileysSkill:
    """
    Python bridge to WhatsApp Baileys microservice.
    The Node.js microservice must be running on the specified URL.
    """
    
    def __init__(
        self, 
        base_url: str = "http://localhost:3001/api",
        timeout: int = 30,
        enabled: bool = True
    ):
        """
        Initialize the WhatsApp Baileys skill.
        
        Args:
            base_url: URL of the Baileys microservice API
            timeout: Request timeout in seconds
            enabled: Whether the skill is enabled
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.enabled = enabled
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to Baileys service."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Baileys service not running. Start it with: npm start (in skills/whatsapp_baileys)"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get connection status of WhatsApp.
        
        Returns:
            {
                "connected": bool,
                "hasQR": bool,
                "qrCode": str or None
            }
        """
        return self._request("GET", "/status")
    
    def get_qr_code(self) -> Dict[str, Any]:
        """
        Get QR code for scanning (if not connected).
        
        Returns:
            {
                "success": bool,
                "connected": bool,
                "qr": str or None (QR data string)
            }
        """
        return self._request("GET", "/qr")
    
    def send_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Send a WhatsApp message.
        
        Args:
            to: Phone number (e.g., "+923244279017") or JID
            message: Message text
            
        Returns:
            {
                "success": bool,
                "messageId": str (if success),
                "error": str (if failed)
            }
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled"}
        
        result = self._request("POST", "/send", json={"to": to, "message": message})
        
        if result.get("success"):
            logger.info(f"WhatsApp Baileys: Message sent to {to}")
        else:
            logger.warning(f"WhatsApp Baileys: Send failed - {result.get('error')}")
        
        return result
    
    def get_chats(self, limit: int = 20) -> Dict[str, Any]:
        """
        Get recent chats.
        
        Args:
            limit: Maximum number of chats to return
            
        Returns:
            {
                "success": bool,
                "chats": [{"jid": str, "name": str, "isGroup": bool}]
            }
        """
        return self._request("GET", f"/chats?limit={limit}")
    
    def check_messages(
        self, 
        keywords: List[str] = None, 
        check_archived: bool = True, 
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Check for messages (compatibility method with old skill).
        
        Note: Currently returns chat list. Full message history requires 
        additional Baileys implementation.
        """
        result = self.get_chats(limit)
        
        if result.get("success"):
            return {
                "success": True,
                "messages": result.get("chats", []),
                "count": len(result.get("chats", []))
            }
        return {"success": False, "messages": [], "error": result.get("error")}
    
    def health_check(self) -> bool:
        """
        Check if Baileys service is running.
        
        Returns:
            True if service is healthy
        """
        result = self._request("GET", "/health")
        return result.get("status") == "ok"
    
    def is_connected(self) -> bool:
        """
        Check if connected to WhatsApp.
        
        Returns:
            True if connected
        """
        status = self.get_status()
        return status.get("connected", False)
    
    def wait_for_connection(self, timeout: int = 120) -> bool:
        """
        Wait for WhatsApp connection (user needs to scan QR).
        
        Args:
            timeout: Maximum seconds to wait
            
        Returns:
            True if connected within timeout
        """
        import time
        start = time.time()
        
        while time.time() - start < timeout:
            if self.is_connected():
                logger.info("WhatsApp Baileys: Connected!")
                return True
            
            # Check for QR code
            qr = self.get_qr_code()
            if qr.get("qr"):
                logger.info("WhatsApp Baileys: QR code available. Please scan.")
            
            time.sleep(5)
        
        logger.warning("WhatsApp Baileys: Connection timeout")
        return False


# Backward compatibility alias
WhatsAppSkill = WhatsAppBaileysSkill


if __name__ == "__main__":
    # Test
    print("Testing WhatsApp Baileys Skill...")
    skill = WhatsAppBaileysSkill()
    
    print("\n1. Health check:")
    print(f"   Service healthy: {skill.health_check()}")
    
    print("\n2. Connection status:")
    print(f"   {skill.get_status()}")
    
    if skill.is_connected():
        print("\n3. Sending test message...")
        result = skill.send_message("+923244279017", "Test from Baileys! 🚀")
        print(f"   Result: {result}")
    else:
        print("\n3. Not connected - scan QR code first")
        print(f"   QR: {skill.get_qr_code()}")
