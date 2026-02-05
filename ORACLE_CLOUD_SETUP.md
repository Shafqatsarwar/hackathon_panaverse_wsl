# ☁️ Oracle Cloud Deployment Guide (24/7 AI Watcher)

This guide provides a fool-proof, step-by-step process to deploy your Panaversity AI Student Assistant to an Oracle Cloud VM for 24/7 autonomous operation.

---

## ✅ Prerequisites

1.  **Oracle VM IP:** `141.147.83.137` (as configured in `.env`)
2.  **SSH Key:** Located at `oracle/oracle_key.key`
3.  **Local Environment:** WSL (Ubuntu) or Linux.

---

## 🚀 Step 1: Prepare the Deployment Package

On your **Local Machine (WSL)**, generate a clean zip file that excludes unnecessary heavy folders (like `.venv` or `node_modules`).

```bash
# In your project root folder
python3 create_deploy_package.py
```
*This creates a file named `panaverse_full_project.zip`.*

---

## 📦 Step 2: Upload to Oracle Cloud

Transfer the package from your local machine to the Oracle VM.

```bash
# 1. Fix permissions for the SSH key (Required by Linux)
chmod 400 oracle/oracle_key.key

# 2. Upload the zip file using SCP
scp -i oracle/oracle_key.key panaverse_full_project.zip ubuntu@141.147.83.137:~/
```

---

## 🛠️ Step 3: Server Setup (One-Time)

Connect to your Oracle VM and install the necessary software (Docker & Unzip).

```bash
# 1. SSH into the server
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137

# 2. Update and Install Tools (Inside the VM)
sudo apt update
sudo apt install -y unzip docker.io docker-compose

# 3. Enable Docker to run on startup
sudo systemctl enable docker
```

---

## � Step 4: Deploy & Start

Extract the project files and start the AI Watchers using Docker Compose.

```bash
# 1. Unzip the project
unzip -o panaverse_full_project.zip -d panaverse_bot
cd panaverse_bot

# 2. Build and Start (Detached mode)
sudo docker-compose up -d --build
```

---

## 📱 Step 5: WhatsApp Authentication (IMPORTANT)

Since the cloud is headless, you must link your WhatsApp account via the terminal logs.

```bash
# 1. View the live logs to find the QR Code
sudo docker-compose logs -f watcher
```

1.  Wait for the logs to generate a **QR Code**.
2.  Open **WhatsApp** on your phone.
3.  Go to **Linked Devices** > **Link a Device**.
4.  Scan the QR code displayed in your terminal.
5.  Once you see `✅ SUCCESS: Logged in!`, press `Ctrl+C` to exit the logs.

**The bot is now running 24/7!**

---

## 🔍 Monitoring & Management

| Action | Command |
| :--- | :--- |
| **Check if running** | `sudo docker ps` |
| **View real-time logs** | `sudo docker-compose logs -f watcher` |
| **Restart the bot** | `sudo docker-compose restart watcher` |
| **Stop the bot** | `sudo docker-compose down` |
| **Update code** | Upload new zip, unzip, and run `sudo docker-compose up -d --build` |

---

## ⚠️ Troubleshooting

*   **Permissions Error:** If `scp` or `ssh` fails, ensure you ran `chmod 400 oracle/oracle_key.key`.
*   **Memory Issues:** Oracle Free Tier has limited RAM. If the build fails, try stopping other services first.
*   **Session Expiry:** If the bot stops reading messages, run the logs command again to see if a new QR code scan is required.
