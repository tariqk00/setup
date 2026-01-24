# Master Environment Setup: Chromebook & NUC

This is the definitive "Manual" for rebuilding and operating the ecosystem.

> **For AI Rules & Stack Preferences**: See `setup/docs/SYSTEM_PROMPT.md`.

It covers the **Chromebook (Dev)** and **NUC (Prod)** environments, including authentication, git deployment, and automation rules.

---

## 🏗️ 1. Architecture Overview

- **Storage**: GitHub Private Repo (`tariqk00/toolbox`, `tariqk00/setup`).
- **Dev Environment**: Chromebook (`penguin` container).
  - Used for: Coding, Testing, Dry Runs.
  - **RESTRICTION**: No automation timers enabled.
- **Prod Environment**: Intel NUC (`nuc8i5-2020`).
  - Used for: Hosted execution.
  - **FEATURE**: Runs hourly `ai-sorter.timer` automation.

---

## 💻 2. Chromebook Setup (Development)

### A. Prerequisites & Packages

```bash
sudo apt update
sudo apt install -y git python3 python3-venv gh
```

### B. GitHub Authentication (Critical)

We use a specific identified key for Antigravity access.

1.  Ensure `~/.ssh/id_ed25519_antigravity` exists.
2.  Configure SSH (`~/.ssh/config`):
    ```text
    Host github.com
      HostName github.com
      User git
      IdentityFile ~/.ssh/id_ed25519_antigravity
      IdentitiesOnly yes
    ```
3.  Authenticate GitHub CLI:
    ```bash
    gh auth login
    # Select: GitHub.com -> SSH -> /home/takhan/.ssh/id_ed25519_antigravity.pub
    ```

### C. Repository & Environment

```bash
cd ~/github/tariqk00
gh repo clone tariqk00/toolbox
gh repo clone tariqk00/setup

# Setup Toolbox Venv
cd toolbox/google-drive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run System Shortcut Fixes (Critical for ChromeOS)
cd ~/github/tariqk00/toolbox
./scripts/fix_shortcuts.sh
./scripts/fix_sommelier.sh
```

### D. IDE Configuration (Antigravity)

> [!IMPORTANT]
> See `docs/gemini.md` for critical path differences in this environment.

- **Config Path**: `~/.antigravity/`
- **Data Path**: `~/.config/Antigravity/`

### A. System Prep

Connect via SSH (User: `tariqk`, IP: `172.30.0.169`):

```bash
# If configured in ~/.ssh/config as 'nuc'
ssh nuc

# Manual connection
ssh tariqk@172.30.0.169

# Standard Install
sudo apt update && sudo apt install -y git python3 python3-venv
```

### B. NUC Reliability (Hardware Fixes)

_Prevents random freezes on NUC8i5._

1.  **Disable Sleep**: `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`
2.  **Limit C-States**: `GRUB_CMDLINE_LINUX_DEFAULT="intel_idle.max_cstate=1"` in `/etc/default/grub`.
3.  **Watchdog**: Enable `softdog` in `/etc/modules-load.d/` and `RuntimeWatchdogSec=20s` in `/etc/systemd/system.conf`.

### C. GitHub Authorization (Deploy Key)

Since the NUC is a headless server, we use a **Deploy Key**.

1.  Generate Key (if missing):
    ```bash
    ssh-keygen -t ed25519 -C "nuc8i5-2020" -f ~/.ssh/id_ed25519 -N ""
    ```
2.  Add to GitHub:
    - Copy key: `cat ~/.ssh/id_ed25519.pub`
    - Go to: `https://github.com/tariqk00/toolbox/settings/keys`
    - Add new Deploy Key (Read/Write recommended for logging).

### D. Deploy Code

```bash
mkdir -p ~/github/tariqk00
cd ~/github/tariqk00
git clone git@github.com:tariqk00/toolbox.git
cd toolbox/google-drive

# Setup Python Venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### E. Automation (The "Live" Switch)

1.  **Enable Linger**: `sudo loginctl enable-linger tariqk`
2.  **Install Service Files**:
    ```bash
    mkdir -p ~/.config/systemd/user
    cp ai-sorter.service ~/.config/systemd/user/
    cp ai-sorter.timer ~/.config/systemd/user/
    systemctl --user daemon-reload
    ```
3.  **Activate**:
    ```bash
    systemctl --user enable --now ai-sorter.timer
    ```

### F. Remote Access (Cloudflare Tunnel)

1.  **Install**:
    ```bash
    curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared.deb
    ```
2.  **Credentials**:
    - Ensure `/etc/cloudflared/<UUID>.json` exists (from `setup/hosts/nuc-server/cloudflared/config.yml`).
3.  **Activate**:
    ```bash
    sudo cp ~/github/tariqk00/setup/hosts/nuc-server/systemd/cloudflared.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now cloudflared
    ```

---

## 🔒 4. Secrets Management

Both environments require a `.env` or `credentials.json` (depending on the tool).
_Note: These are NOT in Git._

- **Google Credentials**: `credentials.json` and `token.json` must be manually SCP'd to `toolbox/google-drive/`.
- **Gemini Key**: Export `GEMINI_API_KEY` in environment or `.env` file.
