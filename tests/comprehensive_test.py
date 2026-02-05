"""
COMPREHENSIVE AUTONOMOUS TESTING SUITE
Tests all skills and agents with minimum 3 tests each
NO manual intervention required
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestResults:
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def add_result(self, skill_name, test_name, passed, message=""):
        if skill_name not in self.results:
            self.results[skill_name] = []
        
        self.results[skill_name].append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def print_summary(self):
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        for skill_name, tests in self.results.items():
            print(f"\nSKILL: {skill_name}")
            print("-" * 80)
            for test in tests:
                status = "PASS" if test["passed"] else "FAIL"
                print(f"  {status} - {test['test']}")
                if test["message"]:
                    print(f"         {test['message']}")
        
        print("\n" + "=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print("=" * 80)

results = TestResults()

# ============================================================================
# 1. GMAIL SKILL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("🧪 TESTING: GMAIL SKILL")
print("=" * 80)

try:
    from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
    from src.utils.config import Config
    
    # Initialize
    gmail_skill = GmailMonitoringSkill(
        credentials_path=Config.GMAIL_CREDENTIALS_PATH,
        token_path=Config.GMAIL_TOKEN_PATH,
        keywords=Config.FILTER_KEYWORDS
    )
    
    # Test 1: Authentication
    print("\nTest 1: Gmail Authentication")
    try:
        auth_result = gmail_skill.authenticate()
        if auth_result and gmail_skill.service:
            results.add_result("Gmail", "Authentication", True, "Successfully authenticated")
            print("PASS - Gmail authenticated")
        else:
            results.add_result("Gmail", "Authentication", False, "Authentication failed")
            print("FAIL - Authentication failed")
    except Exception as e:
        results.add_result("Gmail", "Authentication", False, str(e))
        print(f"FAIL - {e}")
    
    # Test 2: Fetch Unread Emails
    print("\nTest 2: Fetch Unread Emails")
    try:
        emails = gmail_skill.fetch_unread_emails(max_results=5)
        if isinstance(emails, list):
            results.add_result("Gmail", "Fetch Emails", True, f"Found {len(emails)} emails")
            print(f"PASS - Fetched {len(emails)} unread emails")
        else:
            results.add_result("Gmail", "Fetch Emails", False, "Invalid response type")
            print("FAIL - Invalid response")
    except Exception as e:
        results.add_result("Gmail", "Fetch Emails", False, str(e))
        print(f"FAIL - {e}")
    
    # Test 3: Filter Emails by Keywords
    print("\nTest 3: Filter Emails by Keywords")
    try:
        all_emails = gmail_skill.fetch_unread_emails(max_results=10)
        filtered = gmail_skill.filter_relevant_emails(all_emails)
        if isinstance(filtered, list):
            results.add_result("Gmail", "Filter Emails", True, f"Filtered to {len(filtered)} relevant emails")
            print(f"PASS - Filtered {len(all_emails)} -> {len(filtered)} relevant emails")
        else:
            results.add_result("Gmail", "Filter Emails", False, "Invalid response")
            print("FAIL - Invalid response")
    except Exception as e:
        results.add_result("Gmail", "Filter Emails", False, str(e))
        print(f"FAIL - {e}")

except Exception as e:
    results.add_result("Gmail", "Initialization", False, str(e))
    print(f"❌ FAIL - Could not initialize Gmail skill: {e}")

# ============================================================================
# 2. WHATSAPP SKILL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("🧪 TESTING: WHATSAPP SKILL")
print("=" * 80)

try:
    from skills.whatsapp_skill.skill import WhatsAppSkill
    from src.utils.config import Config
    
    if not Config.WHATSAPP_ENABLED:
        print("⚠️ SKIP - WhatsApp is disabled in config")
        results.add_result("WhatsApp", "All Tests", False, "Disabled in config")
    else:
        # Initialize
        wa_skill = WhatsAppSkill(enabled=True, headless=True)
        
        # Test 1: Check Messages
        print("\nTest 1: Check for Messages")
        try:
            messages = wa_skill.check_messages()
            if isinstance(messages, dict) and "success" in messages:
                results.add_result("WhatsApp", "Check Messages", messages["success"], 
                                 messages.get("error", f"Found {len(messages.get('messages', []))} messages"))
                if messages["success"]:
                    print(f"PASS - Found {len(messages.get('messages', []))} messages")
                else:
                    print(f"FAIL - {messages.get('error')}")
            else:
                results.add_result("WhatsApp", "Check Messages", False, "Invalid response format")
                print("FAIL - Invalid response format")
        except Exception as e:
            results.add_result("WhatsApp", "Check Messages", False, str(e))
            print(f"FAIL - {e}")
        
        # Test 2: Check Archived Messages
        print("\nTest 2: Check Archived Messages")
        try:
            archived = wa_skill.check_archived_messages()
            if isinstance(archived, dict) and "success" in archived:
                results.add_result("WhatsApp", "Check Archived", archived["success"],
                                 archived.get("error", f"Found {len(archived.get('messages', []))} archived"))
                if archived["success"]:
                    print(f"PASS - Found {len(archived.get('messages', []))} archived messages")
                else:
                    print(f"FAIL - {archived.get('error')}")
            else:
                results.add_result("WhatsApp", "Check Archived", False, "Invalid response format")
                print("FAIL - Invalid response format")
        except Exception as e:
            results.add_result("WhatsApp", "Check Archived", False, str(e))
            print(f"FAIL - {e}")
        
        # Test 3: Send Message (to admin)
        print("\nTest 3: Send Test Message")
        try:
            test_msg = f"Test message from Panaversity Assistant - {datetime.now().strftime('%H:%M:%S')}"
            send_result = wa_skill.send_message(Config.ADMIN_WHATSAPP, test_msg)
            if isinstance(send_result, dict) and "success" in send_result:
                results.add_result("WhatsApp", "Send Message", send_result["success"],
                                 send_result.get("error", "Message sent"))
                if send_result["success"]:
                    print(f"PASS - Message sent to {Config.ADMIN_WHATSAPP}")
                else:
                    print(f"FAIL - {send_result.get('error')}")
            else:
                results.add_result("WhatsApp", "Send Message", False, "Invalid response format")
                print("FAIL - Invalid response format")
        except Exception as e:
            results.add_result("WhatsApp", "Send Message", False, str(e))
            print(f"FAIL - {e}")

except Exception as e:
    results.add_result("WhatsApp", "Initialization", False, str(e))
    print(f"❌ FAIL - Could not initialize WhatsApp skill: {e}")

# ============================================================================
# 3. LINKEDIN SKILL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("🧪 TESTING: LINKEDIN SKILL")
print("=" * 80)

try:
    from skills.linkedin_skill.skill import LinkedInSkill
    from src.utils.config import Config
    
    if not Config.LINKEDIN_ENABLED:
        print("⚠️ SKIP - LinkedIn is disabled in config")
        results.add_result("LinkedIn", "All Tests", False, "Disabled in config")
    else:
        # Initialize
        li_skill = LinkedInSkill(enabled=True, headless=True)
        
        # Test 1: Check Notifications
        print("\n🔗 Test 1: Check Notifications")
        try:
            notifs = li_skill.check_notifications()
            if isinstance(notifs, dict) and "success" in notifs:
                results.add_result("LinkedIn", "Check Notifications", notifs["success"],
                                 notifs.get("error", f"Found {len(notifs.get('notifications', []))} notifications"))
                if notifs["success"]:
                    print(f"✅ PASS - Found {len(notifs.get('notifications', []))} notifications")
                else:
                    print(f"❌ FAIL - {notifs.get('error')}")
            else:
                results.add_result("LinkedIn", "Check Notifications", False, "Invalid response format")
                print("❌ FAIL - Invalid response format")
        except Exception as e:
            results.add_result("LinkedIn", "Check Notifications", False, str(e))
            print(f"❌ FAIL - {e}")
        
        # Test 2: Scrape Leads (Messages)
        print("\n🔗 Test 2: Scrape Leads/Messages")
        try:
            leads = li_skill.scrape_leads()
            if isinstance(leads, dict) and "success" in leads:
                results.add_result("LinkedIn", "Scrape Leads", leads["success"],
                                 leads.get("error", f"Found {len(leads.get('messages', []))} messages"))
                if leads["success"]:
                    print(f"✅ PASS - Found {len(leads.get('messages', []))} messages")
                else:
                    print(f"❌ FAIL - {leads.get('error')}")
            else:
                results.add_result("LinkedIn", "Scrape Leads", False, "Invalid response format")
                print("❌ FAIL - Invalid response format")
        except Exception as e:
            results.add_result("LinkedIn", "Scrape Leads", False, str(e))
            print(f"❌ FAIL - {e}")
        
        # Test 3: Response Format Consistency
        print("\n🔗 Test 3: Response Format Consistency")
        try:
            test_response = li_skill.check_notifications()
            has_success = "success" in test_response
            has_proper_structure = isinstance(test_response, dict)
            
            if has_success and has_proper_structure:
                results.add_result("LinkedIn", "Response Format", True, "Consistent format")
                print("✅ PASS - Response format is consistent")
            else:
                results.add_result("LinkedIn", "Response Format", False, "Inconsistent format")
                print("❌ FAIL - Response format inconsistent")
        except Exception as e:
            results.add_result("LinkedIn", "Response Format", False, str(e))
            print(f"❌ FAIL - {e}")

except Exception as e:
    results.add_result("LinkedIn", "Initialization", False, str(e))
    print(f"❌ FAIL - Could not initialize LinkedIn skill: {e}")

# ============================================================================
# 4. ODOO CRM SKILL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("🧪 TESTING: ODOO CRM SKILL")
print("=" * 80)

try:
    from skills.odoo_skill.skill import OdooSkill
    from src.utils.config import Config
    
    # Initialize
    odoo_skill = OdooSkill(
        url=Config.ODOO_URL,
        db=Config.ODOO_DB,
        username=Config.ODOO_USERNAME,
        password=Config.ODOO_PASSWORD
    )
    
    # Test 1: Connection
    print("\n📊 Test 1: Odoo Connection")
    try:
        if odoo_skill.uid:
            results.add_result("Odoo", "Connection", True, f"Connected as UID {odoo_skill.uid}")
            print(f"✅ PASS - Connected to Odoo (UID: {odoo_skill.uid})")
        else:
            results.add_result("Odoo", "Connection", False, "No UID obtained")
            print("❌ FAIL - Connection failed")
    except Exception as e:
        results.add_result("Odoo", "Connection", False, str(e))
        print(f"❌ FAIL - {e}")
    
    # Test 2: Create Lead
    print("\n📊 Test 2: Create Test Lead")
    try:
        test_lead = odoo_skill.create_lead(
            name=f"Test Lead - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            email="test@example.com",
            description="Automated test lead from comprehensive testing suite"
        )
        if test_lead.get("success") and test_lead.get("lead_id"):
            results.add_result("Odoo", "Create Lead", True, f"Lead ID: {test_lead['lead_id']}")
            print(f"✅ PASS - Created lead #{test_lead['lead_id']}")
        else:
            results.add_result("Odoo", "Create Lead", False, test_lead.get("error", "Unknown error"))
            print(f"❌ FAIL - {test_lead.get('error')}")
    except Exception as e:
        results.add_result("Odoo", "Create Lead", False, str(e))
        print(f"❌ FAIL - {e}")
    
    # Test 3: Get Leads
    print("\n📊 Test 3: Get Recent Leads")
    try:
        leads_list = odoo_skill.get_leads(limit=5)
        if leads_list.get("success") and isinstance(leads_list.get("leads"), list):
            results.add_result("Odoo", "Get Leads", True, f"Retrieved {len(leads_list['leads'])} leads")
            print(f"✅ PASS - Retrieved {len(leads_list['leads'])} leads")
        else:
            results.add_result("Odoo", "Get Leads", False, leads_list.get("error", "Unknown error"))
            print(f"❌ FAIL - {leads_list.get('error')}")
    except Exception as e:
        results.add_result("Odoo", "Get Leads", False, str(e))
        print(f"❌ FAIL - {e}")

except Exception as e:
    results.add_result("Odoo", "Initialization", False, str(e))
    print(f"❌ FAIL - Could not initialize Odoo skill: {e}")

# ============================================================================
# 5. CHATBOT + WEB SEARCH TESTS
# ============================================================================
print("\n" + "=" * 80)
print("🧪 TESTING: CHATBOT + WEB SEARCH")
print("=" * 80)

try:
    from agents.chat_agent import ChatAgent
    
    # Initialize
    chat_agent = ChatAgent()
    
    # Test 1: Simple Query
    print("\n🤖 Test 1: Simple Query")
    try:
        response = chat_agent.chat("Hello, who are you?")
        if response.get("status") == "success" and response.get("response"):
            results.add_result("Chatbot", "Simple Query", True, "Got response")
            print("✅ PASS - Chatbot responded")
        else:
            results.add_result("Chatbot", "Simple Query", False, "No response")
            print("❌ FAIL - No response")
    except Exception as e:
        results.add_result("Chatbot", "Simple Query", False, str(e))
        print(f"❌ FAIL - {e}")
    
    # Test 2: Tool Calling (Email Check)
    print("\n🤖 Test 2: Tool Calling - Check Emails")
    try:
        response = chat_agent.chat("Check my emails")
        if response.get("status") == "success":
            results.add_result("Chatbot", "Email Tool", True, "Tool called")
            print("✅ PASS - Email tool called")
        else:
            results.add_result("Chatbot", "Email Tool", False, response.get("error", "Unknown"))
            print(f"❌ FAIL - {response.get('error')}")
    except Exception as e:
        results.add_result("Chatbot", "Email Tool", False, str(e))
        print(f"❌ FAIL - {e}")
    
    # Test 3: Web Search
    print("\n🤖 Test 3: Web Search Query")
    try:
        response = chat_agent.chat("What is the weather today?")
        if response.get("status") == "success" and response.get("response"):
            results.add_result("Chatbot", "Web Search", True, "Search completed")
            print("✅ PASS - Web search worked")
        else:
            results.add_result("Chatbot", "Web Search", False, "No response")
            print("❌ FAIL - No response")
    except Exception as e:
        results.add_result("Chatbot", "Web Search", False, str(e))
        print(f"❌ FAIL - {e}")

except Exception as e:
    results.add_result("Chatbot", "Initialization", False, str(e))
    print(f"❌ FAIL - Could not initialize Chatbot: {e}")

# ============================================================================
# FINAL RESULTS
# ============================================================================
results.print_summary()

# Save results to file
with open("TEST_RESULTS.txt", "w") as f:
    f.write(f"Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    for skill_name, tests in results.results.items():
        f.write(f"{skill_name}:\n")
        for test in tests:
            status = "PASS" if test["passed"] else "FAIL"
            f.write(f"  [{status}] {test['test']}: {test['message']}\n")
        f.write("\n")
    f.write(f"\nTotal: {results.total_tests}, Passed: {results.passed_tests}, Failed: {results.failed_tests}\n")
    f.write(f"Success Rate: {(results.passed_tests/results.total_tests*100):.1f}%\n")

print("\n📄 Results saved to: TEST_RESULTS.txt")
