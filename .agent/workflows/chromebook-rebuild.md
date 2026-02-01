---
description: Complete Chromebook setup after fresh install/powerwash using secrets from Drive backup
---

# Chromebook Rebuild Workflow

// turbo-all

## Prerequisites Check

Verify Linux environment is ready:

```bash
which git docker
```

## 1. Create Directory Structure

```bash
mkdir -p ~/github/tariqk00 ~/.ssh ~/.gemini/antigravity
```

## 2. Authenticate GitHub CLI

```bash
gh auth login
# Select: GitHub.com -> SSH -> Create new key
```

## 3. Clone Repositories

```bash
cd ~/github/tariqk00
gh repo clone tariqk00/setup
gh repo clone tariqk00/toolbox
```

## 4. Restore Secrets from Drive Backup

Download [CHROMEBOOK_SECRETS_BACKUP.txt](https://drive.google.com/file/d/1Xs8J2NZQYnmWaDdNfxPlOX-tTTiOBbgb/view) to ~/Downloads

Extract and restore each section:

- SSH Key → `~/.ssh/id_ed25519_antigravity` (chmod 600)
- SSH Config → `~/.ssh/config`
- MCP Config → `~/.gemini/antigravity/mcp_config.json`
- Google Creds → `~/github/tariqk00/toolbox/google-drive/credentials.json`

## 5. Setup Python Environment

```bash
cd ~/github/tariqk00/toolbox/google-drive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 6. Run Fix Scripts

```bash
cd ~/github/tariqk00/toolbox
./scripts/fix_shortcuts.sh
./scripts/fix_sommelier.sh
```

## 7. Install Chrome Browser

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

## 8. Verify Setup

```bash
ssh -T git@github.com
```
