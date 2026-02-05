#!/usr/bin/env python3
"""
Comprehensive Skills Test Script
Tests: Gmail, WhatsApp (Baileys), Odoo, LinkedIn
Sends summary email of all results
"""
import sys
import os
import requests
from datetime import datetime

# Add project root to path
sys.path.insert(0, '/home/shafqatsarwar/Projects/hackathon_panaverse')

# Results storage
test_results = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S PKT"),
    "whatsapp": {"status": "❌", "data": None},
    "gmail": {"status": "❌", "data": None},
    "odoo": {"status": "❌", "data": None},
    "linkedin": {"status": "❌", "data": None}
}

print("=" * 60)
print("🧪 PANAVERSITY SKILLS COMPREHENSIVE TEST")
print(f"📅 {test_results['timestamp']}")
print("=" * 60)

# ===========================================
# TEST 1: WhatsApp (Baileys)
# ===========================================
print("\n🟢 TEST 1: WhatsApp Baileys...")
try:
    status_resp = requests.get("http://localhost:3001/api/status", timeout=10)
    status = status_resp.json()
    
    if status.get("connected"):
        chats_resp = requests.get("http://localhost:3001/api/chats?limit=5", timeout=10)
        chats = chats_resp.json()
        
        test_results["whatsapp"]["status"] = "✅ Connected"
        test_results["whatsapp"]["data"] = {
            "connected": True,
            "chats_count": len(chats.get("chats", [])),
            "sample_chats": [c.get("name", "Unknown") for c in chats.get("chats", [])[:5]]
        }
        print(f"   ✅ Connected! Found {len(chats.get('chats', []))} groups/chats")
    else:
        test_results["whatsapp"]["status"] = "⚠️ Not Connected"
        test_results["whatsapp"]["data"] = {"connected": False}
        print("   ⚠️ Not connected (need QR scan)")
except Exception as e:
    test_results["whatsapp"]["status"] = f"❌ Error: {str(e)[:50]}"
    print(f"   ❌ Error: {e}")

# ===========================================
# TEST 2: Gmail Monitoring
# ===========================================
print("\n🟢 TEST 2: Gmail Monitoring...")
try:
    from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
    from src.utils.config import Config
    
    gmail = GmailMonitoringSkill(
        credentials_path=Config.GMAIL_CREDENTIALS_PATH,
        token_path=Config.GMAIL_TOKEN_PATH,
        keywords=["panaversity", "assignment", "deadline", "urgent"]
    )
    
    if gmail.authenticate():
        emails = gmail.fetch_unread_emails(max_results=5)
        test_results["gmail"]["status"] = "✅ Authenticated"
        test_results["gmail"]["data"] = {
            "authenticated": True,
            "unread_count": len(emails),
            "sample_subjects": [e.get("subject", "No Subject")[:40] for e in emails[:3]]
        }
        print(f"   ✅ Authenticated! Found {len(emails)} unread emails")
    else:
        test_results["gmail"]["status"] = "⚠️ Auth Failed"
        test_results["gmail"]["data"] = {"authenticated": False}
        print("   ⚠️ Authentication failed")
except Exception as e:
    test_results["gmail"]["status"] = f"❌ Error: {str(e)[:50]}"
    print(f"   ❌ Error: {e}")

# ===========================================
# TEST 3: Odoo CRM
# ===========================================
print("\n🟢 TEST 3: Odoo CRM...")
try:
    from skills.odoo_skill.skill import OdooSkill
    
    odoo = OdooSkill()
    
    if odoo.authenticate():
        leads = odoo.get_leads(limit=5)
        test_results["odoo"]["status"] = "✅ Connected"
        test_results["odoo"]["data"] = {
            "authenticated": True,
            "leads_count": len(leads),
            "sample_leads": [l.get("name", "No Name")[:40] for l in leads[:3]]
        }
        print(f"   ✅ Connected! Found {len(leads)} leads")
    else:
        test_results["odoo"]["status"] = "⚠️ Auth Failed"
        test_results["odoo"]["data"] = {"authenticated": False}
        print("   ⚠️ Authentication failed (check Odoo config)")
except Exception as e:
    test_results["odoo"]["status"] = f"❌ Error: {str(e)[:50]}"
    print(f"   ❌ Error: {e}")

# ===========================================
# TEST 4: LinkedIn
# ===========================================
print("\n🟢 TEST 4: LinkedIn Skill...")
try:
    from skills.linkedin_skill.skill import LinkedInSkill
    
    linkedin = LinkedInSkill(headless=True, enabled=True)
    # Check if session exists
    session_exists = os.path.exists("./linkedin_session/Default/Cookies")
    
    if session_exists:
        test_results["linkedin"]["status"] = "✅ Session Found"
        test_results["linkedin"]["data"] = {
            "session_exists": True,
            "note": "LinkedIn automation requires manual login first"
        }
        print("   ✅ Session found! Ready for scraping")
    else:
        test_results["linkedin"]["status"] = "⚠️ No Session"
        test_results["linkedin"]["data"] = {"session_exists": False}
        print("   ⚠️ No session found (need manual login)")
except Exception as e:
    test_results["linkedin"]["status"] = f"❌ Error: {str(e)[:50]}"
    print(f"   ❌ Error: {e}")

# ===========================================
# BUILD SUMMARY EMAIL
# ===========================================
print("\n" + "=" * 60)
print("📧 BUILDING SUMMARY EMAIL...")
print("=" * 60)

html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #4285f4 0%, #34a853 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .section {{ padding: 20px 30px; border-bottom: 1px solid #eee; }}
        .section:last-child {{ border-bottom: none; }}
        .section h2 {{ color: #333; margin: 0 0 15px 0; font-size: 20px; display: flex; align-items: center; gap: 10px; }}
        .status {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold; }}
        .status.success {{ background: #e6f4ea; color: #1e8e3e; }}
        .status.warning {{ background: #fef7e0; color: #f9a825; }}
        .status.error {{ background: #fce8e6; color: #d93025; }}
        .data-box {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px; }}
        .data-box ul {{ margin: 0; padding-left: 20px; }}
        .data-box li {{ margin: 5px 0; color: #555; }}
        .footer {{ background: #f8f9fa; padding: 20px 30px; text-align: center; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Panaversity Skills Test Report</h1>
            <p>Generated: {test_results['timestamp']}</p>
        </div>
        
        <div class="section">
            <h2>📱 WhatsApp (Baileys)</h2>
            <span class="status {'success' if '✅' in test_results['whatsapp']['status'] else 'warning' if '⚠️' in test_results['whatsapp']['status'] else 'error'}">{test_results['whatsapp']['status']}</span>
            <div class="data-box">
                <ul>
"""

# Add WhatsApp data
wa_data = test_results["whatsapp"].get("data") or {}
if wa_data.get("connected"):
    html_body += f"<li>Chats/Groups found: {wa_data.get('chats_count', 0)}</li>"
    for chat in wa_data.get("sample_chats", []):
        html_body += f"<li>• {chat}</li>"
else:
    html_body += "<li>Not connected - QR scan required</li>"

html_body += f"""
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>📧 Gmail Monitoring</h2>
            <span class="status {'success' if '✅' in test_results['gmail']['status'] else 'warning' if '⚠️' in test_results['gmail']['status'] else 'error'}">{test_results['gmail']['status']}</span>
            <div class="data-box">
                <ul>
"""

# Add Gmail data
gmail_data = test_results["gmail"].get("data") or {}
if gmail_data.get("authenticated"):
    html_body += f"<li>Unread emails: {gmail_data.get('unread_count', 0)}</li>"
    for subj in gmail_data.get("sample_subjects", []):
        html_body += f"<li>• {subj}</li>"
else:
    html_body += "<li>Not authenticated - check credentials</li>"

html_body += f"""
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🏢 Odoo CRM Leads</h2>
            <span class="status {'success' if '✅' in test_results['odoo']['status'] else 'warning' if '⚠️' in test_results['odoo']['status'] else 'error'}">{test_results['odoo']['status']}</span>
            <div class="data-box">
                <ul>
"""

# Add Odoo data
odoo_data = test_results["odoo"].get("data") or {}
if odoo_data.get("authenticated"):
    html_body += f"<li>Total leads: {odoo_data.get('leads_count', 0)}</li>"
    for lead in odoo_data.get("sample_leads", []):
        html_body += f"<li>• {lead}</li>"
else:
    html_body += "<li>Not connected - check Odoo configuration</li>"

html_body += f"""
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>💼 LinkedIn</h2>
            <span class="status {'success' if '✅' in test_results['linkedin']['status'] else 'warning' if '⚠️' in test_results['linkedin']['status'] else 'error'}">{test_results['linkedin']['status']}</span>
            <div class="data-box">
                <ul>
"""

# Add LinkedIn data
linkedin_data = test_results["linkedin"].get("data") or {}
if linkedin_data.get("session_exists"):
    html_body += "<li>Session exists - ready for automation</li>"
else:
    html_body += "<li>No session - manual login required</li>"

html_body += """
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>🚀 Panaversity Student Assistant | Baileys WhatsApp Integration</p>
            <p>This report was generated automatically</p>
        </div>
    </div>
</body>
</html>
"""

# ===========================================
# SEND EMAIL
# ===========================================
print("\n📤 Sending summary email...")
try:
    from skills.email_notifications.email_notifications import EmailNotificationSkill
    from src.utils.config import Config
    
    email_skill = EmailNotificationSkill(
        smtp_server=Config.SMTP_SERVER,
        smtp_port=Config.SMTP_PORT,
        smtp_username=Config.SMTP_USERNAME,
        smtp_password=Config.SMTP_PASSWORD
    )
    
    subject = f"🎯 Panaversity Skills Test Report - {test_results['timestamp']}"
    result = email_skill.send_email_notification(
        to_email=Config.ADMIN_EMAIL,
        subject=subject,
        body=html_body,
        html=True
    )
    
    if result:
        print(f"   ✅ Email sent to {Config.ADMIN_EMAIL}!")
    else:
        print("   ❌ Email sending failed")
except Exception as e:
    print(f"   ❌ Email error: {e}")

# ===========================================
# FINAL SUMMARY
# ===========================================
print("\n" + "=" * 60)
print("📊 FINAL TEST RESULTS")
print("=" * 60)
print(f"  WhatsApp: {test_results['whatsapp']['status']}")
print(f"  Gmail:    {test_results['gmail']['status']}")
print(f"  Odoo:     {test_results['odoo']['status']}")
print(f"  LinkedIn: {test_results['linkedin']['status']}")
print("=" * 60)
