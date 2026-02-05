# 🧭 Panaversity AI Employee - Developer Guide

Welcome to the **Panaversity Student Assistant** development guide. This document provides a clear roadmap for running, maintaining, and scaling your digital FTE.

---

## ⚡ 1. Running the System

### 🚀 **Automatic Mode (Recommended)**
The easiest way to start the full autonomous system (Back, Front, Brain, Watchers) in separate windows.

**📂 Double-Click Method:**
- Run **`start.bat`** (or `python start_autonomous.py`) to start everything.
- Run **`stop.bat`** (or `python stop_autonomous.py`) to kill all processes.

**⚠️ Emergency Kill (If stuck):**
Run this in terminal to force-kill everything:
```cmd
taskkill /F /IM python.exe /T & taskkill /F /IM node.exe /T
```

**☁️ Oracle Cloud Deployment:**
To zip and deploy the latest code to your server:

**Option 1: Using Python Directly**
```bash
python create_deploy_package.py
scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@YOUR_IP:~/
ssh -i oracle/oracle_key.key ubuntu@YOUR_IP "cd ~/panaverse && sudo docker-compose up --build -d"
```

**💻 Terminal Method:**
```powershell
# Start everything via Python orchestrator
python start_autonomous.py

# Force stop everything
python stop_autonomous.py
```

### 🛠 **Manual / Individual Launch (Debugging)**
Use these commands to run specific components if you need to see real-time logs in your active terminal.

| Component | Command | Description |
| :--- | :--- | :--- |
| **Backend API** | `python src/api/chat_api.py` | FastAPI server on port 8000 |
| **Frontend UI** | `cd frontend && npm run dev` | Next.js 15 on port 3000 |
| **Watchers** | `python watchers.py` | Starts the "Senses" (Gmail/WA monitoring) |
| **Brain Agent** | `python agents/brain_agent.py` | Starts the "Reasoning" (Task processing) |
| **WhatsApp Baileys** | `cd skills/whatsapp_baileys && npm start` | WhatsApp service (port 3001) |
| **LinkedIn Test** | `python -m skills.linkedin_skill.skill` | Test LinkedIn Scraper |
| **Odoo Sync** | `python mcp/odoo_server.py` | Manual test for Odoo bridge |


---

## 🏗️ 2. System Architecture
The AI Employee follows a **Local-First, Watcher-Brain-Vault** architecture.

### 🔄 The "Digital FTE" Loop
1. **Watchers (Senses)**: Monitor Gmail and WhatsApp. When a "Panaverse" keyword or lead is found, they write a `.md` file to `data/vault/Needs_Action/`.
2. **Vault (Memory)**: A folder-based persistent system.
    - `/Needs_Action`: The inbox for the AI.
    - `/Plans`: AI-generated execution steps.
    - `/Done`: Completed task history.
3. **Brain (Reasoning)**: The `brain_agent.py` runs the "Ralph Wiggum Persistence Loop". It picks up tasks from the Vault, creates a plan, executes it using MCP tools (Odoo/Gmail), and moves the file to `/Done`.

### 📂 Directory Map
- `agents/`: Orchestration logic (Brain, Chat, Email).
- `skills/`: Core capabilities (Gmail, WhatsApp Baileys, Odoo, LinkedIn).
- `mcp/`: Server-side bridges for external tools.
- `frontend/app/dashboard/`: The modern Sales Command Center.
- `data/vault/`: Local markdown memory.

### 📱 WhatsApp Architecture (NEW - Baileys)
```
┌─────────────────┐     HTTP API     ┌─────────────────┐
│  Python Watcher │ ◄──────────────► │ Baileys Service │
│  (main app)     │   Port 3001      │  (Node.js)      │
└─────────────────┘                  └────────┬────────┘
                                              │ WebSocket
                                              ▼
                                     ┌─────────────────┐
                                     │    WhatsApp     │
                                     │    Servers      │
                                     └─────────────────┘
```

**Benefits:**
- ✅ No browser automation (hard to detect)
- ✅ Reliable session persistence
- ✅ Fast and lightweight (~60MB vs ~1GB)

---

## 🔑 3. Configuration (.env)
Your `.env` file must be in the root directory. Key requirements:

```ini
# Core AI
GOOGLE_API_KEY="AIzaSy..."  # Default: Gemini 2.5 Flash

# Odoo CRM
ODOO_URL="http://localhost:8069"
ODOO_DB="panaverse_crm"
ODOO_USER="admin***"
ODOO_PASS="password***"

# Gmail
GMAIL_CREDENTIALS_PATH="credentials.json"
GMAIL_TOKEN_PATH="token.json"

# WhatsApp (Baileys)
WHATSAPP_ENABLED=true
WHATSAPP_BAILEYS_URL="http://localhost:3001/api"
ADMIN_WHATSAPP="+923244279017"

# Admin Login
ADMIN_EMAIL="kh*********@mail.com"
ADMIN_PASS="A********@123"
```

---

## 🛠️ 4. Troubleshooting

### ❌ Port 8000/3000/3001 in Use
If the system fails to start due to port conflicts:
```powershell
# Kill all Python/Node processes hanging in background
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
```

### ❌ WhatsApp Not Connecting (Baileys)
1. Navigate to `skills/whatsapp_baileys/`
2. Delete the `sessions/` folder
3. Run `npm start`
4. Scan the QR code when it appears

### ❌ LinkedIn No Session
LinkedIn requires a one-time manual login:
```bash
python -c "from skills.linkedin_skill.skill import LinkedInSkill; LinkedInSkill(headless=False).scrape_leads()"
```
Login when the browser opens. Session will be saved.

### ❌ Odoo Connection Failure
Verify Odoo is running locally or your Docker instance is up. Check `xmlrpc.client` is working in Python.

---

## 🧪 5. Testing & Verification
Run the comprehensive test to verify all skills:
```bash
python test_all_skills.py
```
This tests WhatsApp (Baileys), Gmail, Odoo, and LinkedIn.

---

## ☁️ 6. Oracle Cloud Deployment Commands

### 📦 Step 1: Create Deploy Package (Local)
```bash
# Create zip without sensitive files
python create_deploy_package.py
mv panaverse_full_project.zip panaverse_deploy.zip
```

### 📤 Step 2: Upload to Server
```bash
# Upload zip file to Oracle Cloud
scp -i oracle/oracle_key.key panaverse_deploy.zip ubuntu@141.147.83.137:~/
```

### 🔧 Step 3: Deploy on Server
```bash
# SSH into server
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137

# On the server - extract and deploy
cd ~
unzip -o panaverse_deploy.zip -d panaverse
cd panaverse
sudo docker-compose up --build -d
```

### 📱 Step 4: WhatsApp QR Code Scan
```bash
# Watch WhatsApp logs and scan QR when it appears
sudo docker logs -f panaversity_whatsapp

# Or get QR as image
curl http://localhost:3001/api/qr | python3 -c "import sys,json; print(json.load(sys.stdin).get('qr','No QR'))"
```

### 🔍 Step 5: Monitor Logs
```bash
# View all container logs
sudo docker-compose logs -f

# View specific service
sudo docker logs -f panaversity_watcher
sudo docker logs -f panaversity_whatsapp
```

### 🔄 Quick Redeploy Commands
```bash
# Full redeploy from local machine (one-liner)
python create_deploy_package.py && scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/ && ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && unzip -o ~/panaverse_full_project.zip -d ~/panaverse && sudo docker-compose up --build -d"

# Restart containers only (no rebuild)
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose restart"
```

---
*Maintained by Team AI Force - Platinum Tier Hackathon Project (2026)*
