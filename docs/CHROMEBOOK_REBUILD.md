---
description: Complete Chromebook setup after fresh install/powerwash using secrets from Drive backup
---

# Chromebook Rebuild Workflow

Use this workflow after a powerwash or fresh Chromebook install.

## Prerequisites

1. Linux container (Crostini) must be enabled
2. Internet connection
3. Access to Google Drive (for secrets backup)

## 0. Pre-Rebuild Backup (from NUC)

Before wiping the Chromebook, ensure these secrets are backed up to Google Drive (e.g., in a `secrets/` folder):

1.  **SSH Keys**: `~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`
2.  **Google OAuth Tokens**:
    - `~/github/tariqk00/toolbox/config/credentials.json`
    - `~/github/tariqk00/toolbox/config/token_full_drive.json`
3.  **Plaud Credentials** (if active): `~/github/tariqk00/plaud/credentials.json`

Run this on NUC to backup to Drive (if mounted) or download manually:
```bash
# Example backup command on NUC
mkdir -p ~/backup_secrets
cp ~/.ssh/id_ed25519* ~/backup_secrets/
cp ~/github/tariqk00/toolbox/config/*.json ~/backup_secrets/
# Now copy ~/backup_secrets to your Google Drive
```

## 1. Install Base Packages

```bash
sudo apt update && sudo apt install -y git python3 python3-venv gh wget curl
```

## 2. Install Google Chrome (for Antigravity browser automation)

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

**Binary path:** `/usr/bin/google-chrome`

## 3. Restore Secrets

Copy the secrets you backed up from Google Drive (or USB) to their correct locations:

1.  **SSH Keys**:
    ```bash
    mkdir -p ~/.ssh
    # Copy id_ed25519 and id_ed25519.pub to ~/.ssh/
    chmod 600 ~/.ssh/id_ed25519
    chmod 644 ~/.ssh/id_ed25519.pub
    ```

2.  **Google OAuth Tokens**:
    ```bash
    # Ensure toolbox repo is cloned first (Step 5) or create dirs manually
    mkdir -p ~/github/tariqk00/toolbox/config
    # Copy credentials.json and token_full_drive.json to ~/github/tariqk00/toolbox/config/
    ```

3.  **Authentication**:
    Test GitHub access: `ssh -T git@github.com`

**Option B: Generate new Antigravity key**
```bash
ssh-keygen -t ed25519 -C "antigravity-chromebook" -f ~/.ssh/id_ed25519_antigravity
```
Then add public key to GitHub: https://github.com/settings/keys

## 4. Configure SSH

Create `~/.ssh/config`:
```text
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_antigravity
  IdentitiesOnly yes

Host nuc
    HostName 172.30.0.169
    User tariqk
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

## 5. GitHub Authentication

```bash
gh auth login
# Select: GitHub.com -> SSH -> ~/.ssh/id_ed25519_antigravity.pub
```

## 6. Clone Repositories

```bash
mkdir -p ~/repos/personal
cd ~/repos/personal

gh repo clone tariqk00/setup
gh repo clone tariqk00/toolbox
gh repo clone tariqk00/plaud
```

## 7. Setup Python Venv (for toolbox)

```bash
cd ~/repos/personal/toolbox/google-drive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 8. Run Environment Fixes

```bash
cd ~/repos/personal/toolbox
./scripts/fix_shortcuts.sh  # If exists
./scripts/fix_sommelier.sh  # If exists
```

## 9. Verify Setup

Test SSH to NUC:
```bash
ssh nuc 'hostname && uptime'
```

Test GitHub:
```bash
ssh -T git@github.com
```

## 10. Restore Antigravity Settings

Antigravity stores config in `~/.gemini/` and `~/.antigravity/`

Key files to check/restore:
- `~/.gemini/GEMINI.md` - Global rules
- `~/.gemini/antigravity/mcp_config.json` - MCP server config

## Reference Docs

- **Master Guide**: `~/repos/personal/setup/docs/ENV_SETUP.md`
- **System Prompt**: `~/repos/personal/setup/docs/SYSTEM_PROMPT.md`
