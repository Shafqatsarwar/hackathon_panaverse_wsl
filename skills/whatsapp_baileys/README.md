# WhatsApp Baileys Skill

## Overview
This is a **NEW** WhatsApp skill using the **Baileys** library instead of Playwright.

### Why Baileys?
| Feature | Playwright (Old) | Baileys (New) |
|---------|-----------------|---------------|
| Connection | Browser automation | Direct WebSocket |
| Detection | Easy to detect | Much harder |
| Session | Unreliable | Reliable |
| Speed | Slow (browser overhead) | Fast |
| Resources | Heavy (Chromium) | Light (Node.js only) |

## Architecture
```
┌─────────────────┐     HTTP API     ┌─────────────────┐
│  Python Agent   │ ◄──────────────► │ Baileys Service │
│  (main watcher) │   Port 3001      │  (Node.js)      │
└─────────────────┘                  └─────────────────┘
                                            │
                                            ▼
                                     ┌─────────────────┐
                                     │   WhatsApp      │
                                     │   (WebSocket)   │
                                     └─────────────────┘
```

## Quick Start

### Local Development
```bash
cd skills/whatsapp_baileys
npm install
npm start
```

### Docker
```bash
docker build -t whatsapp-baileys .
docker run -p 3001:3001 -v $(pwd)/sessions:/app/sessions whatsapp-baileys
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Connection status |
| GET | `/api/qr` | Get QR code for scanning |
| POST | `/api/send` | Send message `{to, message}` |
| GET | `/api/chats` | Get recent chats |
| GET | `/api/health` | Health check |

## Python Integration
```python
import requests

BAILEYS_URL = "http://localhost:3001/api"

# Check status
status = requests.get(f"{BAILEYS_URL}/status").json()

# Send message
result = requests.post(f"{BAILEYS_URL}/send", json={
    "to": "+923244279017",
    "message": "Hello from Python!"
}).json()
```

## Session Persistence
Sessions are stored in `./sessions/` directory. Mount this as a Docker volume to persist across restarts.

## Port
Default: `3001` (configurable via `WHATSAPP_PORT` env var)
