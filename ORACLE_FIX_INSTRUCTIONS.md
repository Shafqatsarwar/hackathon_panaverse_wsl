# 🚨 Oracle Cloud Deployment Fix (Critical Update)

Everything you need to fix the deployment issue is detailed below.

## 🚩 The Issue
Your deployment on Oracle Cloud was failing because the "headless" Chrome browser (used for WhatsApp & LinkedIn) requires specific Linux system libraries (like `libapps`, `libnspr4`) that were missing in the standard Python container.

This caused the error: `libnspr4.so: cannot open shared object file` which you likely saw in the logs (and we reproduced locally).

## ✅ The Fix (Applied)
I have updated your `Dockerfile` to include one critical line: `RUN playwright install-deps`. 
This forces the container to download all necessary Linux libraries during the build process, making the bot 100% self-sufficient.

## 🚀 How to Re-Deploy (Concise Steps)

Run these 3 commands in your local terminal to update the server.

### 1. Create New Package
```bash
python create_deploy_package.py
```

### 2. Upload to Oracle
```bash
scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/
```

### 3. Build & Restart (On Oracle Server)
SSH into the server:
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137
```

Then run these commands inside the server:
```bash
# Unzip and Overwrite
unzip -o panaverse_full_project.zip -d panaverse_bot
cd panaverse_bot

# Rebuild (Crucial step!)
sudo docker-compose up -d --build
```

**That's it.** The build process will take a few minutes longer this time as it installs the missing dependencies. Once done, check the logs for the WhatsApp QR code:

```bash
sudo docker-compose logs -f watcher
```
