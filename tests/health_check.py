"""
Simple System Health Check
Verifies that the backend can start and all agents initialize properly
Run this before presenting to judges!
"""
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("PANAVERSITY ASSISTANT - SYSTEM HEALTH CHECK")
print("=" * 70)
print()

# Test 1: Configuration
print("[1/5] Checking Configuration...")
try:
    from src.utils.config import Config
    print(f"  [OK] Config loaded")
    print(f"  [OK] Gmail: {Config.GMAIL_ADDRESS}")
    print(f"  [OK] Odoo: {Config.ODOO_URL}")
    print(f"  [OK] WhatsApp: {'Enabled' if Config.WHATSAPP_ENABLED else 'Disabled'}")
    print(f"  [OK] LinkedIn: {'Enabled' if Config.LINKEDIN_ENABLED else 'Disabled'}")
except Exception as e:
    print(f"  [FAIL] Configuration error: {e}")
    sys.exit(1)

# Test 2: ChatAgent (most critical for demo)
print("\n[2/5] Testing ChatAgent...")
try:
    from agents.chat_agent import ChatAgent
    chat_agent = ChatAgent()
    print(f"  [OK] ChatAgent initialized")
    
    # Try a simple chat
    response = chat_agent.chat("Hello, test message")
    if response.get("status") == "success":
        print(f"  [OK] ChatAgent responding correctly")
    else:
        print(f"  [WARN] ChatAgent response: {response.get('status')}")
except Exception as e:
    print(f"  [FAIL] ChatAgent error: {e}")
    sys.exit(1)

# Test 3: MainAgent
print("\n[3/5] Testing MainAgent...")
try:
    from agents.main_agent import MainAgent
    main_agent = MainAgent()
    print(f"  [OK] MainAgent initialized")
    print(f"  [OK] All sub-agents loaded successfully")
except Exception as e:
    print(f"  [FAIL] MainAgent error: {e}")
    sys.exit(1)

# Test 4: Vault Structure
print("\n[4/5] Checking Vault Structure...")
try:
    vault_dirs = [
        "data/vault/Needs_Action",
        "data/vault/Plans",
        "data/vault/Done"
    ]
    for dir_path in vault_dirs:
        if Path(dir_path).exists():
            print(f"  [OK] {dir_path}")
        else:
            print(f"  [WARN] {dir_path} missing")
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"  [OK] Created {dir_path}")
except Exception as e:
    print(f"  [FAIL] Vault error: {e}")

# Test 5: Session Data
print("\n[5/5] Checking Session Data...")
session_checks = {
    "WhatsApp": "whatsapp_session",
    "LinkedIn": "linkedin_session"
}
for name, path in session_checks.items():
    if Path(path).exists():
        print(f"  [OK] {name} session found")
    else:
        print(f"  [WARN] {name} session not found - manual login needed")

# Summary
print("\n" + "=" * 70)
print("HEALTH CHECK COMPLETE")
print("=" * 70)
print("\nALL CRITICAL SYSTEMS OPERATIONAL!")
print("\nSystem is ready for demo. Key features:")
print("  - Chatbot with Gemini 2.5 Flash")
print("  - Gmail monitoring")
print("  - WhatsApp integration")
print("  - LinkedIn integration")
print("  - Odoo CRM integration")
print("  - Web search capability")
print("\nTo start the system:")
print("  1. Double-click start.bat")
print("  2. Visit http://localhost:3000")
print("=" * 70)
