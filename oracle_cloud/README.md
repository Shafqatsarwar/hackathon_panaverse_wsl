# Oracle Cloud Skill

This folder contains the Oracle Cloud deployment skill and SSH key.

## Structure
```
oracle_cloud/
├── oracle/
│   └── oracle_key.key      # SSH key (NEVER COMMIT)
├── ORACLE_DEPLOY_GUIDE.md  # Deployment commands & troubleshooting
└── README.md               # This file
```

## Quick Commands

### SSH to Server
```bash
ssh -i oracle_cloud/oracle/oracle_key.key ubuntu@141.147.83.137
```

### Upload File
```bash
scp -i oracle_cloud/oracle/oracle_key.key <localfile> ubuntu@141.147.83.137:~/
```

### Deploy
See `ORACLE_DEPLOY_GUIDE.md` for full instructions.

## Security
- `oracle/` folder is in `.gitignore`
- Never commit SSH keys
