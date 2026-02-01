# Chromebook Powerwash Recovery

> **Goal**: Get Antigravity running ASAP so the agent can finish setup.

## Phase 1: Manual (5 min)

1. **Sign in** with Google account
2. **Enable Linux** → Settings → Developers → Linux → Turn On (allocate 20GB+)
3. **Open Terminal** (search "Terminal" in launcher)

```bash
# Install prerequisites
sudo apt update && sudo apt install -y git docker.io wget

# Download Antigravity
wget -O ~/Downloads/antigravity.deb "https://antigravity.google/download/linux"

# Install Antigravity
sudo apt install -y ~/Downloads/antigravity.deb
```

4. **Launch Antigravity** from ChromeOS launcher

## Phase 2: Agent Completes Setup

Once in Antigravity, tell the agent:

> "Run the Chromebook rebuild from ENV_SETUP.md in tariqk00/setup"

The agent will:

- Clone repos (`tariqk00/setup`, `tariqk00/toolbox`)
- Restore secrets from [Drive backup](https://drive.google.com/file/d/1Xs8J2NZQYnmWaDdNfxPlOX-tTTiOBbgb/view)
- Configure SSH, MCP, venv
- Run fix scripts

## Secrets Backup Location

[CHROMEBOOK_SECRETS_BACKUP.txt](https://drive.google.com/file/d/1Xs8J2NZQYnmWaDdNfxPlOX-tTTiOBbgb/view)

Contains: SSH key, SSH config, MCP config, Google credentials
