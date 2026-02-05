# Phase 10: Future Deployment (Oracle Cloud & Docker) 🔮

**Status**: Planned / Next Steps.
**Goal**: Move from Localhost (`start.bat`) to a 24/7 Cloud Server.

## 1. Why Oracle Cloud?
We chose **Oracle Cloud Always Free Tier** over Vercel/Heroku because:
1.  **Persistent VM**: We need a real Linux server (Ubuntu) to run Headless Chrome (Playwright) for WhatsApp.
2.  **Storage**: We need to save the `whatsapp_session` folder so you don't have to scan the QR code every 10 minutes.
3.  **Specs**: The ARM Ampere instances (4 OCPU, 24GB RAM) are powerful enough for AI + Chrome.

## 2. Docker Strategy
To make deployment easy, we will containerize the app.

### The Planned `Dockerfile`
```dockerfile
FROM python:3.11-slim

# Install system deps for Playwright & Node.js
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python & Node deps
RUN pip install -r requirements.txt
RUN cd frontend && npm install && npm run build
RUN playwright install chromium --with-deps

CMD ["python", "-m", "src.main", "start"]
```

### The Planned `docker-compose.yml`
```yaml
version: '3.8'
services:
  assistant:
    build: .
    restart: always
    ports:
      - "8000:8000"
      - "3000:3000"
    volumes:
      - ./whatsapp_session:/app/whatsapp_session # PERSIST SESSION!
      - ./.env:/app/.env
```

## 3. Remaining Steps (Oracle Setup)
1.  **Create Account**: Sign up for Oracle Cloud Free Tier.
2.  **Launch Instance**: Create a VM.Standard.A1.Flex (Ubuntu 22.04).
3.  **Open Ports**: Add Ingress Rules for ports 8000 and 3000 in the VCN Security List.
4.  **Connect**: SSH into the server.
    ```bash
    ssh ubuntu@<your-server-ip>
    ```
5.  **Deploy**:
    ```bash
    git clone <your-repo-url>
    cd hackathon_panaverse
    docker-compose up -d
    ```

## 4. Final Handoff
This phase executes once the Hackathon demo (Localhost) is complete and approved.
