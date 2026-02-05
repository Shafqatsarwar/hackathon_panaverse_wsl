# ⚙️ Comprehensive Setup Instructions

This document details how to set up the **Panaversity AI Employee** from scratch, covering Credentials, Cloud Variables, Installation, and Oracle Cloud Deployment.

## 1. Prerequisites
- **OS**: Windows 10/11 (WSL2) or Linux Ubuntu 22.04
- **Python**: 3.12+ (Recommended: 3.12.1)
- **Node.js**: v20 LTS
- **Odoo**: Community v17+ (Optional, can accept mock)
- **Git**: Latest version

## 2. Installation (Step-by-Step)

### A. Clone & Prepare
```bash
git clone https://github.com/Shafqatsarwar/hackathon_penaverse_wsl-oracle-deploy.git
cd hackathon_penaverse_wsl-oracle-deploy

# Create Virtual Environment
python -m venv .venv
source .venv/bin/activate  # Linux/WSL
# .\.venv\Scripts\activate   # Windows PowerShell
```

### B. Install Dependencies
```bash
# Python
pip install -r requirements.txt
playwright install chromium  # For LinkedIn only

# Node.js (WhatsApp Baileys)
cd skills/whatsapp_baileys
npm install
cd ../..

# Node.js (Frontend)
cd frontend
npm install
cd ..
```

---

## 3. Configuration & Credentials 🔐

### A. Google Cloud (Gmail API)
To allow the AI to check emails (`watchers.py` runs every 60s), you need `credentials.json`.
1. **Create Project**: Go to [Google Cloud Console](https://console.cloud.google.com/).
2. **Enable APIs**: Search for and enable **Gmail API**.
3. **Configure Consent Screen**:
   - Go to "OAuth consent screen".
   - Select **External** (for personal testing) or Internal.
   - Add Test Users: Add your email.
4. **Create Credentials**:
   - Go to "Credentials" > "Create Credentials" > "OAuth client ID".
   - Application Type: **Desktop app**.
   - Name: "Panaversity Assistant".
   - Click **Create**.
5. **Download JSON**:
   - Click the **Download (⬇️)** button next to your new Client ID.
   - Save the file as **`credentials.json`** in the project root folder.

### B. Environment Variables (.env)
Create a `.env` file in the root. **Do NOT commit this file.**

```ini
# --- Core AI ---
GOOGLE_API_KEY="AIzaSy... (Your Gemini API Key)"

# --- Gmail settings ---
GMAIL_CREDENTIALS_PATH="credentials.json"
GMAIL_TOKEN_PATH="token.json"  # Automatically created on first login
ADMIN_EMAIL="your_email@mail.com"

# --- SMTP for sending emails ---
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"

# --- Odoo CRM (Optional) ---
ODOO_URL="http://localhost:8069" # Or your Cloud IP
ODOO_DB="panaverse_db"
ODOO_USER="admin"
ODOO_PASSWORD="admin_password"

# --- WhatsApp (Baileys - NEW) ---
WHATSAPP_ENABLED="True"
WHATSAPP_BAILEYS_URL="http://localhost:3001/api"
ADMIN_WHATSAPP="+923244279017"
```

---

## 4. Running the System

### Option 1: Docker (Recommended for Oracle Cloud)
```bash
# Build and start all services
docker-compose up --build -d

# View WhatsApp logs (scan QR code)
docker logs -f panaversity_whatsapp

# View main watcher logs
docker logs -f panaversity_watcher
```

### Option 2: Manual / Terminal
```bash
# 1. Start WhatsApp Baileys Service (separate terminal)
cd skills/whatsapp_baileys && npm start

# 2. Start Main Watcher (separate terminal)
source .venv/bin/activate
python watchers.py
```

### ⚠️ Emergency Kill (If stuck)
If processes hang:
```bash
# Linux/WSL
pkill -f node
pkill -f python

# Windows
taskkill /F /IM python.exe /T & taskkill /F /IM node.exe /T
```

---

## 5. Oracle Cloud Deployment Guide ☁️

### Step 1: Create Instance
1. Sign up for Oracle Cloud Free Tier.
2. Create **Compute Instance**:
   - **Image**: Canonical Ubuntu 22.04
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **SSH Keys**: "Generate a key pair for me" -> **Save Private Key** (e.g., `oracle_key.key`).

### Step 2: Networking (Crucial Fix)
If your instance says "Public IP: No" or you can't connect:
1. Go to **Instance Details** > **Attached VNICs** (left menu).
2. Click the VNIC Name.
3. Scroll to **IPv4 Addresses**.
4. Click **... (Actions)** > **Edit**.
5. Change "Public IP Type" to **Ephemeral Public IP**.
6. Click **Update**.
7. Copy the new IP Address (e.g., `141.147.x.x`).

### Step 3: Fast Deployment
```bash
# 1. Create deploy package (excludes sensitive files)
python create_deploy_package.py
mv panaverse_full_project.zip panaverse_deploy.zip

# 2. Upload to server
scp -i oracle/oracle_key.key panaverse_deploy.zip ubuntu@YOUR_IP:~/

# 3. SSH and deploy
ssh -i oracle/oracle_key.key ubuntu@YOUR_IP

# On the server:
cd ~
unzip -o panaverse_deploy.zip -d panaverse
cd panaverse
sudo docker-compose up --build -d

# 4. Watch WhatsApp logs and scan QR
sudo docker logs -f panaversity_whatsapp
```

---

## 6. How it Works (The logic)

### Services
| Service | Port | Technology | Purpose |
|---------|------|------------|---------|
| WhatsApp Baileys | 3001 | Node.js | WhatsApp via WebSocket (no browser!) |
| Main Watcher | - | Python | Monitors Gmail, processes tasks |
| Frontend | 3000 | Next.js | Admin dashboard |
| Backend API | 8000 | FastAPI | REST API |

### Data Flow
1. **Watchers**: Monitor Gmail/WhatsApp every 60 seconds
2. **Brain**: Analyzes inputs and routes to skills
3. **Skills**: Execute actions (send message, create lead, etc.)

---

## 7. Skill Reference

| Skill | Location | Description |
|-------|----------|-------------|
| WhatsApp (Baileys) | `skills/whatsapp_baileys/` | Send/receive WhatsApp (Node.js) |
| WhatsApp Python Bridge | `skills/whatsapp_baileys/skill.py` | Python interface to Baileys |
| Gmail Monitoring | `skills/gmail_monitoring/` | Check unread emails |
| Email Notifications | `skills/email_notifications/` | Send SMTP emails |
| LinkedIn | `skills/linkedin_skill/` | Scrape notifications (Playwright) |
| Odoo CRM | `skills/odoo_skill/` | Create/read leads |

---

## 8. Testing
Run comprehensive test of all skills:
```bash
python test_all_skills.py
```

This will test WhatsApp, Gmail, Odoo, LinkedIn and send you an email summary.

---
*Panaversity AI Employee - WSL Oracle Deploy Edition (2026)*
