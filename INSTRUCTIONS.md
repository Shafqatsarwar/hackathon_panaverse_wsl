# ⚙️ Comprehensive Setup & Deployment Instructions (WSL Edition)

This document details the complete deployment process for the **Panaversity AI Employee** from WSL Ubuntu to Oracle Cloud.

---

## 📋 Prerequisites
- **OS**: Ubuntu 22.04 (WSL2 on Windows)
- **Python**: 3.12+ (use `python3`)
- **Node.js**: v20 LTS
- **Oracle Cloud**: Free tier instance running Ubuntu
- **SSH Key**: `oracle/oracle_key.key` for server access

---

## 🚀 DEPLOYMENT STEPS (Step-by-Step)

### Step 1: Navigate to Project
```bash
cd /home/shafqatsarwar/Projects/hackathon_panaverse_wsl
```

### Step 2: Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Step 3: Create Deploy Package
```bash
python3 create_deploy_package.py
```
**Expected Output:**
```
📦 Compressing project into: panaverse_full_project.zip...
  Adding: Dockerfile
  Adding: docker-compose.yml
  ...
✅ SUCCESS: panaverse_full_project.zip is ready!
```

### Step 4: Upload to Oracle Cloud
```bash
scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/
```
**Expected Output:**
```
panaverse_full_project.zip    100%  XXX MB   X.X MB/s   00:XX
```

### Step 5: SSH into Oracle Cloud Server
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137
```

### Step 6: Extract and Deploy (On Server)
```bash
cd ~
rm -rf panaverse 2>/dev/null
unzip -o panaverse_full_project.zip -d panaverse
cd panaverse
```

### Step 7: Stop Old Containers (On Server)
```bash
sudo docker-compose down
```

### Step 8: Build and Start Services (On Server)
```bash
sudo docker-compose up --build -d
```
**Expected Output:**
```
Building whatsapp...
Building watcher...
Creating panaversity_whatsapp ... done
Creating panaversity_watcher  ... done
```

### Step 9: Scan WhatsApp QR Code (On Server)
```bash
sudo docker logs -f panaversity_whatsapp
```
Wait for QR code to appear, then scan with WhatsApp mobile app.

### Step 10: Verify Services Running (On Server)
```bash
sudo docker ps
```
**Expected Output:**
```
CONTAINER ID   IMAGE                   STATUS          NAMES
abc123...      panaverse_whatsapp      Up 2 minutes    panaversity_whatsapp
def456...      panaverse_watcher       Up 2 minutes    panaversity_watcher
```

### Step 11: Exit SSH
```bash
exit
```

---

## 🔧 TROUBLESHOOTING

### ❌ Error: `python` command not found
**Solution:** Use `python3` instead of `python`:
```bash
python3 create_deploy_package.py
```

### ❌ Error: Permission denied (SSH key)
**Solution:** Fix key permissions:
```bash
chmod 600 oracle/oracle_key.key
```

### ❌ Error: Connection refused (SSH)
**Solution:** Check if Oracle Cloud instance is running and has public IP.

### ❌ Error: Port 22 connection timeout
**Solution:** Check Oracle Cloud Security Lists:
1. Go to Oracle Cloud Console → Networking → Virtual Cloud Networks
2. Click your VCN → Security Lists → Default Security List
3. Add Ingress Rule: Source 0.0.0.0/0, Port 22, TCP

### ❌ Error: Docker compose not found
**Solution:** Install Docker Compose on server:
```bash
sudo apt update
sudo apt install docker-compose -y
```

### ❌ Error: WhatsApp not connecting
**Solution:**
1. Check container logs: `sudo docker logs panaversity_whatsapp`
2. Delete old session and restart:
```bash
sudo docker-compose down
sudo rm -rf whatsapp_baileys_session/*
sudo docker-compose up --build -d
sudo docker logs -f panaversity_whatsapp
```
3. Scan new QR code

### ❌ Error: Container keeps restarting
**Solution:** Check logs for specific error:
```bash
sudo docker logs panaversity_watcher --tail 100
sudo docker logs panaversity_whatsapp --tail 100
```

### ❌ Error: Package not found during build
**Solution:** Make sure requirements.txt is present:
```bash
cat requirements.txt
```

---

## 📱 QUICK COMMANDS REFERENCE

### Local (WSL)
| Action | Command |
|--------|---------|
| Activate venv | `source .venv/bin/activate` |
| Create package | `python3 create_deploy_package.py` |
| Upload to server | `scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/` |
| SSH to server | `ssh -i oracle/oracle_key.key ubuntu@141.147.83.137` |

### Server (Oracle Cloud)
| Action | Command |
|--------|---------|
| Deploy | `cd ~/panaverse && sudo docker-compose up --build -d` |
| View logs | `sudo docker-compose logs -f` |
| WhatsApp logs | `sudo docker logs -f panaversity_whatsapp` |
| Restart services | `sudo docker-compose restart` |
| Stop all | `sudo docker-compose down` |
| Check status | `sudo docker ps` |

---

## 🔄 QUICK REDEPLOY (One-Liner)

From WSL terminal:
```bash
cd /home/shafqatsarwar/Projects/hackathon_panaverse_wsl && source .venv/bin/activate && python3 create_deploy_package.py && scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/ && ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && cd ~ && unzip -o panaverse_full_project.zip -d panaverse && cd panaverse && sudo docker-compose up --build -d"
```

---

*Panaversity AI Employee - WSL Oracle Deploy Edition (2026)*
