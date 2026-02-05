# Oracle Cloud Deployment Guide - Panaverse AI Assistant

## Server Details
- **IP:** 141.147.83.137
- **User:** ubuntu
- **SSH Key:** `oracle/oracle_key.key`

---

## Quick Deploy Commands

### 1. Create Deploy Package (Local)
```bash
.venv/bin/python create_deploy_package.py && mv panaverse_full_project.zip panaverse_fully_authenticated.zip
```

### 2. Upload to Server
```bash
scp -i oracle/oracle_key.key panaverse_fully_authenticated.zip ubuntu@141.147.83.137:~/
```

### 3. Deploy (Full Clean Deploy)
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && sudo rm -f whatsapp_session/whatsapp.lock && unzip -o ~/panaverse_fully_authenticated.zip -d ~/panaverse && sudo docker-compose up --build -d && sudo docker logs -f panaversity_watcher"
```

### 4. Quick Restart (No Rebuild)
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo rm -f whatsapp_session/whatsapp.lock && sudo docker-compose restart watcher && sudo docker logs -f panaversity_watcher"
```

---

## Monitoring Commands

### View Logs
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker logs --tail 100 panaversity_watcher"
```

### Follow Logs Live
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker logs -f panaversity_watcher"
```

### Check Container Status
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker ps && sudo docker stats --no-stream"
```

---

## Debug Commands

### Download Debug Screenshot
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo docker cp panaversity_watcher:/app/whatsapp_debug.png ~/debug.png" && scp -i oracle/oracle_key.key ubuntu@141.147.83.137:~/debug.png ./whatsapp_debug.png
```

### Check Session Files
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "ls -la ~/panaverse/whatsapp_session/ && sudo ls -la ~/panaverse/whatsapp_session/Default/ | head -20"
```

### Check IndexedDB (Session Data)
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo ls -la ~/panaverse/whatsapp_session/Default/IndexedDB/"
```

---

## Troubleshooting

### Issue: "Could not acquire lock"
**Solution:** Remove the lock file
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "sudo rm -f ~/panaverse/whatsapp_session/whatsapp.lock"
```

### Issue: QR Code Not Loading
**Cause:** WhatsApp page not fully rendering before checks
**Solution:** Increase `networkidle` timeout in `skill.py` Line 226

### Issue: Login Detected but Chat Rows Timeout
**Cause:** WhatsApp still syncing or DOM structure changed
**Check:** Download debug screenshot and verify what WhatsApp shows

### Issue: Session Not Persisting
**Check:** Volume mount in `docker-compose.yml`:
```yaml
volumes:
  - ./whatsapp_session:/app/whatsapp_session
```

### Issue: Container Frozen/No New Logs
**Solution:** Restart the watcher
```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose restart watcher"
```

---

## Clean Reset (Nuclear Option)

If everything is broken, do a complete reset:

```bash
ssh -i oracle/oracle_key.key ubuntu@141.147.83.137 "cd ~/panaverse && sudo docker-compose down && sudo rm -rf whatsapp_session/* && sudo docker system prune -f"
```

Then redeploy with step 3 above. **Note:** This will require a fresh WhatsApp QR scan.

---

## Known Issues (As of 2026-02-05)

1. **Chat rows not loading** - Login works but `div[role="row"]` never appears
   - **Status:** Investigating selector changes
   - **Workaround:** None currently

2. **Multiple QR codes printed** - Watcher loop sometimes runs twice
   - **Status:** May be related to watcher interval timing

---

## File Locations on Server

| Path | Description |
|------|-------------|
| `/home/ubuntu/panaverse/` | Main project directory |
| `/home/ubuntu/panaverse/whatsapp_session/` | WhatsApp browser session |
| `/home/ubuntu/panaverse/logs/` | Application logs |
| `/app/whatsapp_debug.png` | Debug screenshot (inside container) |
