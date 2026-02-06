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
 *** Stop the background backend and frontend I started
pkill -f "python3 src/api/chat_api.py"
pkill -f "next dev"
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
**☁️ Oracle Cloud Deployment:**
To zip and deploy the latest code to your server:

**Option 1: Using Python Directly**
```bash
python create_deploy_package.py
scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@YOUR_IP:~/
# (scp -i <KEY_PATH> <ZIP_NAME> <USER>@<SERVER_IP>:~/)
ssh -i oracle/oracle_key.key ubuntu@YOUR_IP "cd ~/panaverse && sudo docker-compose up --build -d"
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP> "cd <DEPLOY_DIR> && sudo docker-compose up --build -d")
```
## 📅 11. Daily Health Check Routine

Run these commands daily to ensure your agent is healthy:

```bash
# 1. SSH into server
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)

# 2. Check containers
sudo docker ps

# 3. Check WhatsApp
curl -s http://localhost:3001/api/status

# 4. Check recent watcher activity
sudo docker logs --since 1h panaversity_watcher | head -50

# 5. Exit
exit
```

---

## 🔄 12. Quick Redeploy (One-Liner)

From local WSL terminal:
```bash
cd /home/shafqatsarwar/Projects/hackathon_panaverse_wsl && source .venv/bin/activate && python3 create_deploy_package.py && scp -i oracle_cloud/oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/ && ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && cd ~ && unzip -o panaverse_full_project.zip -d panaverse && cd panaverse && sudo docker-compose up --build -d && sudo docker logs -f panaversity_whatsapp"
# (cd <LOCAL_DIR> && source <VENV_ACTIVATE> && python3 create_deploy_package.py && scp -i <KEY_PATH> <ZIP_NAME> <USER>@<SERVER_IP>:~/ && ssh -i <KEY_PATH> <USER>@<SERVER_IP> "cd <DEPLOY_DIR> && sudo docker-compose down && cd ~ && unzip -o <ZIP_NAME> -d <DEPLOY_DIR> && cd <DEPLOY_DIR> && sudo docker-compose up --build -d && sudo docker logs -f <CONTAINER_NAME>")
```


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
cd /home/shafqatsarwar/Projects/hackathon_panaverse_wsl
source .venv/bin/activate
python3 create_deploy_package.py
```

### 📤 Step 2: Upload to Server
```bash
scp -i oracle_cloud/oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/
# (scp -i <KEY_PATH> <ZIP_NAME> <USER>@<SERVER_IP>:~/)
```

### 🔧 Step 3: Deploy on Server
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)
cd ~
unzip -o panaverse_full_project.zip -d panaverse
cd panaverse
sudo docker-compose up --build -d
```

### 📱 Step 4: WhatsApp QR Code Scan
```bash
sudo docker logs -f panaversity_whatsapp
```

---

## 🤖 7. Autonomous Agent - What It Does (24/7)

Your AI Employee is now running automatically and will:

| Feature | Interval | Action |
|---------|----------|--------|
| **Gmail Monitoring** | Every 15 mins | Scans for keywords (Panaversity, PIAIC, Assignment, etc.) |
| **Email Forwarding** | On detection | Forwards relevant emails to `khansarwar1@hotmail.com` |
| **WhatsApp Alerts** | On detection | Sends WhatsApp notification to `+923244279017` |
| **Odoo CRM** | On new lead | Creates lead from LinkedIn/Gmail contacts |
| **LinkedIn** | Daily (if session valid) | Checks notifications and connections |

### 🔑 Keywords Being Monitored:
- Panaversity, PIAIC, Panaverse
- Quiz, Assignment, Exam, Deadline
- Lahore, Batch, Batch47, UMT

---

## 📊 8. Monitoring & Verification Commands

### SSH into Server First:
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)
```

### Check All Containers Running:
```bash
sudo docker ps
```
**Expected:** Both `panaversity_whatsapp` and `panaversity_watcher` should show "Up"

### Check WhatsApp Connection:
```bash
curl -s http://localhost:3001/api/status
```
**Expected:** `{"connected":true,"hasQR":false}`

### View Live Watcher Logs:
```bash
sudo docker logs -f panaversity_watcher
```
Shows Gmail checks, email processing, and alerts being sent.

### View WhatsApp Logs:
```bash
sudo docker logs -f panaversity_whatsapp
```
Shows messages sent/received.

### View Last 100 Lines of Logs:
```bash
sudo docker logs --tail 100 panaversity_watcher
sudo docker logs --tail 100 panaversity_whatsapp
```

### Check Watcher Activity (Last Hour):
```bash
sudo docker logs --since 1h panaversity_watcher
```

---

## 🧪 9. Manual Testing Commands

### Send Test WhatsApp Message:
```bash
curl -X POST http://localhost:3001/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "+923244279017", "message": "🧪 Test from Oracle Cloud!"}'
```

### Get WhatsApp Chats:
```bash
curl -s http://localhost:3001/api/chats
```

### Force Restart Services:
```bash
cd ~/panaverse
sudo docker-compose restart
```

### Full Rebuild (After Code Changes):
```bash
cd ~/panaverse
sudo docker-compose down
sudo docker-compose up --build -d
```

---

## 🔧 10. Troubleshooting (Oracle Cloud)

### 📱 WhatsApp Session Expired / Re-Login

When WhatsApp session expires or signs out, follow these steps:

#### Step 1: SSH into Server (from local WSL)
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)
```

#### Step 2: Check Current WhatsApp Status
```bash
curl -s http://localhost:3001/api/status
```
**If you see:** `{"connected":false}` or `{"hasQR":true}` → Session expired

#### Step 3: Delete Old Session & Restart WhatsApp
```bash
cd ~/panaverse
sudo docker-compose stop whatsapp
sudo rm -rf whatsapp_baileys_session/*
sudo docker-compose start whatsapp
```

#### Step 4: Watch Logs for New QR Code
```bash
sudo docker logs -f panaversity_whatsapp
```
**Wait for the QR code to appear in terminal**

#### Step 5: Scan QR Code
1. Open **WhatsApp** on your phone
2. Go to **Settings** → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code shown in terminal

#### Step 6: Verify Connection
```bash
# Press Ctrl+C to exit logs
# Then check status:
curl -s http://localhost:3001/api/status
```
**Expected:** `{"connected":true,"hasQR":false}`

#### Step 7: Send Test Message
```bash
curl -X POST http://localhost:3001/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "+923244279017", "message": "✅ WhatsApp Re-Connected!"}'
```

#### Step 8: Exit Server
```bash
exit
```

---

### 🔄 Quick WhatsApp Re-Login (One-Liner)

SSH and restart in one command:
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose stop whatsapp && sudo rm -rf whatsapp_baileys_session/* && sudo docker-compose start whatsapp && sudo docker logs -f panaversity_whatsapp"
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP> "cd <DEPLOY_DIR> && sudo docker-compose stop whatsapp && sudo rm -rf <SESSION_DIR> && sudo docker-compose start whatsapp && sudo docker logs -f <CONTAINER_NAME>")
```
Then scan QR when it appears.

---

### ❌ WhatsApp Still Not Connecting?

Try full container rebuild:
```bash
cd ~/panaverse
sudo docker-compose down
sudo rm -rf whatsapp_baileys_session/*
sudo docker-compose up --build -d
sudo docker logs -f panaversity_whatsapp
```

### ❌ Watcher Not Processing Emails
```bash
# Check logs for errors
sudo docker logs --tail 50 panaversity_watcher

# Restart watcher
sudo docker-compose restart watcher
```

### ❌ Container Keeps Crashing
```bash
# Check detailed logs
sudo docker logs panaversity_watcher 2>&1 | tail -100

# Check container health
sudo docker inspect panaversity_watcher | grep -A 10 "State"
```

### ❌ Disk Space Issues
```bash
# Check disk space
df -h

# Clean Docker resources
sudo docker system prune -a
```

### ❌ Memory Issues
```bash
# Check memory
free -h

# Restart Docker
sudo systemctl restart docker
cd ~/panaverse
sudo docker-compose up -d
```

---

### 🔑 Google API Key Revoked / Quota Exceeded

If Google revokes your API key or quota ends, follow these steps:

#### Step 1: Generate New API Key
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** → **API Key**
3. Copy the new key (starts with `AIzaSy...`)
4. (Optional) Restrict key to **Generative Language API** for security

#### Step 2: Update Local .env File (WSL)
```bash
cd /home/shafqatsarwar/Projects/hackathon_panaverse_wsl
nano .env
```
Find and update these lines:
```ini
GOOGLE_API_KEY=AIzaSyYOUR_NEW_KEY_HERE
GEMINI_API_KEY=AIzaSyYOUR_NEW_KEY_HERE
```
Save: `Ctrl+O`, Enter, `Ctrl+X`

#### Step 3: Redeploy to Oracle Cloud
```bash
python3 create_deploy_package.py
scp -i oracle_cloud/oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/
# (scp -i <KEY_PATH> <ZIP_NAME> <USER>@<SERVER_IP>:~/)
```

#### Step 4: Update on Server
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)
cd ~
unzip -o panaverse_full_project.zip -d panaverse
cd panaverse
sudo docker-compose down
sudo docker-compose up --build -d
```

#### Step 5: Verify New Key Works
```bash
sudo docker logs --tail 20 panaversity_watcher
```
Look for successful API calls (no "quota exceeded" or "invalid key" errors).

---

### 🔑 Quick API Key Update (Server Only - Temporary)

If you just need to update the key on the server without redeploying:

```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
# (ssh -i <KEY_PATH> <USER>@<SERVER_IP>)
cd ~/panaverse
nano .env
# Update GOOGLE_API_KEY and GEMINI_API_KEY
# Save: Ctrl+O, Enter, Ctrl+X

sudo docker-compose restart watcher
sudo docker logs -f panaversity_watcher
```

**Note:** This is temporary. Always update local .env and redeploy for permanent changes.

---


---
*Panaversity AI Employee - Running 24/7 on Oracle Cloud (2026)*
*Maintained by Team AI Force - Platinum Tier Hackathon Project*
