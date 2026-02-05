#!/bin/bash
echo "==========================================="
echo "   Panaversity Assistant - Simple Installer"
echo "==========================================="

# 1. Update System
echo "[1/5] Updating System..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
fi

if [[ "$OS" == *"Oracle"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"CentOS"* ]]; then
    echo "Detected Oracle/RHEL Linux. Using dnf..."
    sudo dnf install -y python3 python3-pip alsa-lib at-spi2-atk gtk3 nss libXScrnSaver alsa-lib
    # Ensure pip is available
    if ! command -v pip3 &> /dev/null; then
        sudo dnf install -y python3-pip
    fi
else
    echo "Detected Debian/Ubuntu. Using apt..."
    sudo apt-get update && sudo apt-get install -y python3-pip python3-venv libasound2 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1 libasound2
fi

# 2. Setup Python Environment
echo "[2/5] Setting up Virtual Environment..."
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Requirements
echo "[3/5] Installing Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install Browsers
echo "[4/5] Installing Playwright Browsers..."
playwright install chromium
playwright install-deps

# 5. Create Directories
echo "[5/5] Creating Data Folders..."
mkdir -p data/vault/Inbox data/vault/Needs_Action data/vault/Logs whatsapp_session linkedin_session logs

echo "==========================================="
echo "✅ Setup Complete!"
echo "To run:"
echo "1. source .venv/bin/activate"
echo "2. python scripts/cloud_login.py"
echo "3. nohup python watchers.py > watchers.log 2>&1 &"
echo "==========================================="
