---
description: Fix WhatsApp login issues on Oracle Cloud
---

# WhatsApp Baileys Troubleshooting Workflow

// turbo-all

## ⚠️ IMPORTANT: New Architecture
We now use **Baileys** (direct WebSocket) instead of **Playwright** (browser automation).
This is much more reliable and harder for WhatsApp to detect.

## Pre-requisites
- SSH access to Oracle Cloud server
- Local project at `/home/shafqatsarwar/Projects/hackathon_panaverse`

---

## Step 1: Check Current Services Status
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker-compose ps && sudo docker logs --tail 30 panaversity_whatsapp"
```

## Step 2: Check WhatsApp Connection Status (via API)
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "curl -s http://localhost:3001/api/status | jq"
```

## Step 3: Get QR Code (if not connected)
```bash
# Get QR data
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "curl -s http://localhost:3001/api/qr | jq"

# OR download QR image
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cat ~/panaverse/whatsapp_baileys_session/qr.png" > whatsapp_qr.png && xdg-open whatsapp_qr.png
```

## Step 4: Watch Logs During QR Scan
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker logs -f panaversity_whatsapp"
```
**→ Scan QR with WhatsApp mobile app when it appears**

## Step 5: Test Sending Message
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "curl -X POST http://localhost:3001/api/send -H 'Content-Type: application/json' -d '{\"to\": \"+923244279017\", \"message\": \"Test from Oracle Cloud!\"}' | jq"
```

---

## Full Redeploy (if code changed)

### Local: Create Package
```bash
.venv/bin/python create_deploy_package.py && mv panaverse_full_project.zip panaverse_fully_authenticated.zip
```

### Upload
```bash
scp -i oracle/oracle_key.key panaverse_fully_authenticated.zip ubuntu@141.147.83.137:~/
```

### Deploy
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && unzip -o ~/panaverse_fully_authenticated.zip -d ~/panaverse && sudo docker-compose up --build -d && sudo docker logs -f panaversity_whatsapp"
```

---

## Architecture (New)
```
┌─────────────────┐     HTTP API     ┌─────────────────┐
│  Python Watcher │ ◄──────────────► │ Baileys Service │
│  (panaversity_  │   Port 3001      │  (Node.js)      │
│   watcher)      │                  │  (panaversity_  │
└─────────────────┘                  │   whatsapp)     │
                                     └────────┬────────┘
                                              │ WebSocket
                                              ▼
                                     ┌─────────────────┐
                                     │    WhatsApp     │
                                     │    Servers      │
                                     └─────────────────┘
```

## Files to Check
- `skills/whatsapp_baileys/` - New Baileys skill (Node.js)
- `skills/whatsapp_baileys/skill.py` - Python bridge
- `whatsapp_baileys_session/` - Session data (mount as volume)

## Advantages over Old Playwright Skill
| Feature | Playwright (Old) | Baileys (New) |
|---------|-----------------|---------------|
| Detection | Easy to detect | Hard to detect |
| Session | Unreliable | Reliable |
| Speed | Slow | Fast |
| Resources | Heavy (Chromium) | Light (Node.js) |
| Docker Image | ~1GB | ~200MB |
