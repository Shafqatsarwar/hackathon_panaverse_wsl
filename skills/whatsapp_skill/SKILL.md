---
name: whatsapp_skill
description: Skill for sending and receiving WhatsApp messages using Playwright browser automation
version: 3.0.0
---

# WhatsApp Skill V3.0

This skill handles interaction with WhatsApp Web via Playwright browser automation, allowing agents to send notifications and check for messages.

## 🚀 What's New in V3.0

- **Fully Async Architecture**: Native async/await support
- **Dual Interface**: Both async and sync methods available
- **Better Error Handling**: Comprehensive error messages
- **Windows Compatible**: Proper event loop handling for Windows
- **Session Persistence**: QR code scan only once
- **Archived Chat Support**: Checks both main and archived chats

## 📋 Capabilities

- ✅ Send text messages to specified numbers
- ✅ Check for new messages (with keyword filtering)
- ✅ Scan archived chats
- ✅ Session persistence (login once)
- ✅ Async and sync interfaces
- ✅ Windows event loop handling

## 🔧 Setup

### 1. Install Playwright
```bash
pip install playwright
playwright install chromium
```

### 2. Enable in .env
```bash
WHATSAPP_ENABLED=true
ADMIN_WHATSAPP=+923244279017  # Your number with country code
```

### 3. First Login (QR Code)
```bash
python tests/verify_whatsapp.py
```
- Browser opens to WhatsApp Web
- Scan QR code with your phone
- Session saves to `./whatsapp_session`
- You only need to do this ONCE

## 💻 Usage

### Async Interface (Recommended for async code)

```python
from skills.whatsapp_skill.skill import WhatsAppSkill
import asyncio

async def main():
    skill = WhatsAppSkill(headless=True)
    
    # Send message
    result = await skill.send_message_async("+923001234567", "Hello from AI! 🤖")
    print(result)  # {"success": True, "status": "sent"}
    
    # Check messages
    messages = await skill.check_messages_async(
        keywords=["PIAIC", "Panaversity", "Batch 47"],
        check_archived=True,
        limit=20
    )
    for msg in messages:
        print(f"From: {msg['title']}")
        print(f"Message: {msg['last_message']}")
        print(f"Unread: {msg['unread']}")

asyncio.run(main())
```

### Sync Interface (For non-async code)

```python
from skills.whatsapp_skill.skill import WhatsAppSkill

skill = WhatsAppSkill(headless=True)

# Send message
result = skill.send_message("+923001234567", "Hello from AI! 🤖")
print(result)

# Check messages
messages = skill.check_messages(keywords=["PIAIC", "Panaversity"])
for msg in messages:
    print(f"Found: {msg['title']} -> {msg['last_message']}")
```

### From Watchers (Async Context)

```python
# In watchers.py or other async code
async def poll_whatsapp(self):
    # Use async interface directly
    msgs = await self.whatsapp_skill.check_messages_async(
        keywords=["Urgent", "Help"],
        limit=20
    )
    # Process messages...
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  WhatsAppSkill                      │
├─────────────────────────────────────┤
│  Async Methods (Primary):          │
│  - send_message_async()             │
│  - check_messages_async()           │
│                                     │
│  Sync Wrappers (Compatibility):    │
│  - send_message()                   │
│  - check_messages()                 │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Playwright Browser Automation      │
│  - Chromium persistent context      │
│  - Session in ./whatsapp_session    │
│  - WhatsApp Web interface           │
└─────────────────────────────────────┘
```

## 📊 Return Values

### send_message() / send_message_async()
```python
# Success
{"success": True, "status": "sent"}

# Failure
{"success": False, "error": "Invalid WhatsApp number."}
{"success": False, "error": "WhatsApp skill is disabled"}
```

### check_messages() / check_messages_async()
```python
# Success
[
    {
        "title": "John Doe",
        "last_message": "Hey, about the PIAIC assignment...",
        "unread": "3",
        "matched_keyword": "PIAIC"
    },
    {
        "title": "Panaversity Group",
        "last_message": "New quiz posted!",
        "unread": "0",
        "source": "archived",  # If from archived
        "matched_keyword": "quiz"
    }
]

# Error
[{"error": "Failed to initialize browser or login"}]
```

## 🐛 Troubleshooting

### Issue: "NotImplementedError" on Windows
**Fixed in V3.0** - Proper Windows event loop policy handling

### Issue: "Login timeout"
```bash
# Delete session and re-scan QR code
Remove-Item -Recurse -Force whatsapp_session
python tests/verify_whatsapp.py
```

### Issue: "WhatsApp skill is disabled"
Check `.env` file:
```bash
WHATSAPP_ENABLED=true
```

### Issue: Messages not sending
- Verify phone number format: `+923001234567` (country code + number, no spaces)
- Check browser is not blocked by firewall
- Verify session is still valid

### Issue: No messages found
- Check `FILTER_KEYWORDS` in `.env`
- Verify keywords match message content
- Try without keywords to see all messages

## 🧪 Testing

```bash
# Test 1: Verify login
python tests/verify_whatsapp.py

# Test 2: Send message
python tests/test_wa_send.py

# Test 3: Check messages
python tests/test_whatsapp.py

# Test 4: Full skill suite
python tests/test_skills.py
```

## ⚙️ Configuration Options

```python
skill = WhatsAppSkill(
    enabled=True,              # Enable/disable skill
    headless=False,            # Show browser (False) or hide (True)
    session_dir="./whatsapp_session"  # Where to store session
)
```

## 🔒 Security Notes

- Session data stored in `./whatsapp_session` folder
- Add `whatsapp_session/` to `.gitignore`
- Never commit session data to version control
- QR code scan required on first use only
- Session persists until you log out on phone

## 📝 Version History

- **V3.0** (2026-01-28): Full async refactor, dual interface, better error handling
- **V2.1** (2026-01-25): Windows event loop fixes, archived chat support
- **V2.0** (2026-01-24): Playwright implementation
- **V1.0** (2026-01-22): Initial mock implementation

---

*Last updated: 2026-01-28*
*Maintained by: Panaversity AI Team*
