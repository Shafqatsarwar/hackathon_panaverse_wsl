# Oracle Cloud Skill

Manage Panaverse AI deployment on Oracle Cloud server.

## Features
- Check container status
- Get logs
- Restart watcher
- Full deploy (upload, extract, rebuild)
- Download debug screenshots

## Usage

```python
from skills.oracle_skill.skill import OracleCloudSkill

skill = OracleCloudSkill()

# Check if container is running
status = skill.check_container_status()
print(status)

# Get logs
logs = skill.get_logs(50)
print(logs["logs"])

# Restart watcher
result = skill.restart_watcher()

# Full deploy
result = skill.full_deploy("panaverse_fully_authenticated.zip")

# Download debug screenshot
result = skill.download_debug_screenshot("./debug.png")
```

## Requirements
- SSH key at `oracle_cloud/oracle/oracle_key.key`
- Network access to server 141.147.83.137
