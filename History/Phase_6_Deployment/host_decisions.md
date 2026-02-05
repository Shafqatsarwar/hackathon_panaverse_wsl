# Phase 6: Deployment Architecture ☁️

**Focus**: Solving the "Where do we host this?" question.

## 1. The Serverless Attempt
- **Initial Request**: "Free Vercel Hosting".
- **Analysis**: Vercel Functions are ephemeral (last 10-60s) and have size limits (50MB).
- **Conflict**: Our WhatsApp code requires a full Chrome binary (~300MB) and a persistent process to listen for messages.
- **Outcome**: Vercel Rejected.

## 2. The VPS Solution
- **Action**: Pivoted to Docker-based deployment.
- **Target**: Free Tier VPS (Oracle Cloud Always Free / Google Cloud e2-micro).
- **Benefit**:
    - "Always On" background processes.
    - Persistent disk for Session storage (no QR scanning on reboot).
    - Full Docker support.

## 3. Artifacts
- Created `Dockerfile` and `docker-compose.yml` (Conceptually prepared, though prioritizing local dev for Hackathon demo).
