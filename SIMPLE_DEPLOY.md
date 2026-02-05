# ☁️ Simple Cloud Deployment (No Docker)

This is the easiest way to run your agent 24/7 on an Oracle Cloud (Ubuntu) server.

## 1. Copy Files to Cloud
Zip your project on your laptop (exclude `.venv` and `node_modules`):
```powershell
tar -czvf project.tar.gz . --exclude=.venv --exclude=node_modules --exclude=.git
```
Upload it to your Cloud VM (Open PowerShell/CMD):
```powershell
scp project.tar.gz ubuntu@YOUR_VM_IP:~
```

## 2. Install & Setup (One Command)
Login to your Cloud VM:
```powershell
ssh ubuntu@YOUR_VM_IP
```

Run these commands on the Cloud VM:
```bash
# Unzip
mkdir app && tar -xzvf project.tar.gz -C app && cd app

# Run the Simple Installer (Installs Python, Browsers, etc.)
chmod +x install_simple.sh
./install_simple.sh
```

## 3. Login to WhatsApp
Still on the Cloud VM, run the helper to get the QR code:
```bash
source .venv/bin/activate
python scripts/cloud_login.py
```
*Note: Since you can't see the screen, this script saves a `qr_code.png`. Download this file to your laptop (using `scp`) and scan it with your phone.*

To download the QR code (Run this on YOUR LAPTOP):
```powershell
scp ubuntu@YOUR_VM_IP:~/app/qr_code.png ./
```

## 4. Run Forever
Once logged in, start the watchers to run in the background (even if you disconnect):

```bash
nohup python watchers.py > watchers.log 2>&1 &
```

**That's it! Your agent is now alive 24/7.**
To check on it: `tail -f watchers.log`
To stop it: `pkill -f watchers.py`
