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
  - **Aliases**: `nuc`, `nuc server`, `ubuntu server`, `prod`.
  - Used for: Hosted execution.
  - **FEATURE**: Runs hourly `ai-sorter.timer` automation.

---

## ⚡ Quick Rebuild Checklist (Chromebook)

> [!TIP]
> Use this checklist for rapid recovery. Full details in sections below.

1. **Enable Linux (Crostini)** — ChromeOS Settings → Developers → Linux
2. **Install packages** — `sudo apt update && sudo apt install -y git python3 python3-venv gh docker.io`
3. **Restore secrets from Drive** — Download `CHROMEBOOK_SECRETS_BACKUP.txt` from `PKM/Infrastructure`
4. **Restore SSH key** — Copy to `~/.ssh/id_ed25519_antigravity`, run `chmod 600`
5. **Restore SSH config** — Copy to `~/.ssh/config`
6. **Clone repos** — `cd ~/github/tariqk00 && gh repo clone tariqk00/toolbox && gh repo clone tariqk00/setup`
7. **Setup venv** — `cd toolbox/google-drive && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
8. **Install Antigravity** — See Section 2.G
9. **Restore MCP config** — Copy to `~/.gemini/antigravity/mcp_config.json`
10. **Restore Google creds** — Copy `credentials.json` to `toolbox/google-drive/`
11. **Run fix scripts** — `./scripts/fix_shortcuts.sh && ./scripts/fix_sommelier.sh`
12. **Install Chrome** — See Section 2.E

---

## 💻 2. Chromebook Setup (Development)

### A. Prerequisites & Packages

```bash
sudo apt update
sudo apt install -y git python3 python3-venv gh docker.io
```

> [!NOTE]
> `docker.io` is required for MCP servers (GitHub, n8n) which run in containers.

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
- **MCP Config**: `~/.gemini/antigravity/mcp_config.json`

**Restore MCP Config** (after Antigravity install):

```bash
mkdir -p ~/.gemini/antigravity
# Copy mcp_config.json from backup file to ~/.gemini/antigravity/mcp_config.json
```

### E. Chrome Browser (Required for Browser Agent)

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

**Binary path for Agent**: `/usr/bin/google-chrome`

### F. Secrets Recovery

Secrets backup: [CHROMEBOOK_SECRETS_BACKUP.txt](https://drive.google.com/file/d/1Xs8J2NZQYnmWaDdNfxPlOX-tTTiOBbgb/view)

| Secret       | Restore Location                            |
| ------------ | ------------------------------------------- |
| SSH Key      | `~/.ssh/id_ed25519_antigravity` (chmod 600) |
| SSH Config   | `~/.ssh/config`                             |
| MCP Config   | `~/.gemini/antigravity/mcp_config.json`     |
| Google Creds | `toolbox/google-drive/credentials.json`     |

### G. Antigravity IDE Installation

1. **Download** from [antigravity.google](https://antigravity.google)
   - Select the **Linux (.deb)** package

2. **Install**:

   ```bash
   cd ~/Downloads
   sudo apt install -y ./antigravity_*.deb
   ```

3. **Launch**: Search "Antigravity" in the ChromeOS launcher or run `antigravity` in terminal

4. **First Run**:
   - Sign in with Google account
   - Open folder: `~/github/tariqk00`

> [!IMPORTANT]
> After install, restore MCP config to `~/.gemini/antigravity/mcp_config.json` and run `fix_shortcuts.sh`.

---

## 🖥️ 3. NUC Setup (Production)

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

### B. Dashboard (CasaOS)

_Primary Interface & Docker Manager._

1.  **Install**:
    ```bash
    curl -fsSL https://get.casaos.io | sudo bash
    ```
2.  **Access**: `http://<nuc-ip>` (Port 80/81).
3.  **Usage**: Installed first to manage subsequent Docker containers.

### C. NUC Reliability (Hardware Fixes)

_Prevents random freezes on NUC8i5._

1.  **Disable Sleep**: `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`
2.  **Limit C-States**: `GRUB_CMDLINE_LINUX_DEFAULT="intel_idle.max_cstate=1"` in `/etc/default/grub`.
3.  **Watchdog**: Enable `softdog` in `/etc/modules-load.d/` and `RuntimeWatchdogSec=20s` in `/etc/systemd/system.conf`.

### D. GitHub Authorization (Deploy Key)

Since the NUC is a headless server, we use a **Deploy Key**.

1.  Generate Key (if missing):
    ```bash
    ssh-keygen -t ed25519 -C "nuc8i5-2020" -f ~/.ssh/id_ed25519 -N ""
    ```
2.  Add to GitHub:
    - Copy key: `cat ~/.ssh/id_ed25519.pub`
    - Go to: `https://github.com/tariqk00/toolbox/settings/keys`
    - Add new Deploy Key (Read/Write recommended for logging).

### E. Deploy Code

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

### F. Automation (The "Live" Switch)

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

### G. Automation (n8n)

> [!TIP]
> **Detailed Guide**: See `setup/n8n/README.md` for Docker, Workflow Import, and Gmail/Drive credential setup.

1.  **Overview**: n8n runs via Docker and is exposed via Cloudflare Tunnel.
2.  **Access**: `https://n8n.khantastic.org`
3.  **Workflows**:
    - **Plaud Email**: Intercepts recordings and saves to Drive.
    - **Gemini Journal**: Processes captured thoughts.

### H. Remote Access (Cloudflare Tunnel)

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

### G. Dashboard (CasaOS)

_Optional GUI for managing Docker & Files._

1.  **Install**:
    ```bash
    curl -fsSL https://get.casaos.io | sudo bash
    ```
2.  **Access**: `http://<nuc-ip>` (Port 80 by default).
3.  **Note**: Use this to visualize the `n8n` and `github-mcp` containers managed by our system.

---

## 🚀 4. Deployment Strategy (CI/CD)

We follow a strict "Commit-Deploy-Restart" lifecycle to prevent configuration drift between Dev (Chromebook) and Prod (NUC).

### Deployment Script

Use the `toolbox/scripts/deploy_to_nuc.sh` script on the Chromebook to automate the release process.

```bash
# From ~/github/tariqk00/toolbox
./scripts/deploy_to_nuc.sh
```

**What this script does:**

1.  **Safety Check**: Verifies there are no uncommitted changes locally.
2.  **Commit**: Pushes `master` to GitHub.
3.  **Deploy**: SSHs into the NUC (`172.30.0.169`) and runs `git pull`.
4.  **Restart**: Reloads the `ai-sorter.service` to pick up code changes.
5.  **Verify**: Prints the systemd service status.

### Root Cause Analysis (RCA) Protocol

If a deployment fails or behaves unexpectedly, use the **5 Whys** method:

1.  **Check Service Status**: `systemctl --user status ai-sorter`
2.  **Check Logs**: `journalctl --user -u ai-sorter -n 50`
3.  **Verify Paths**: Ensure `ExecStart` in `.service` files matches `pwd`.
4.  **Verify Secrets**: Check `toolbox/config/` for missing API keys.
5.  **Re-deploy**: Run `deploy_to_nuc.sh` to ensure sync.

---

## 🔒 5. Secrets Management

Both environments require a `.env` or `credentials.json` (depending on the tool).
_Note: These are NOT in Git._

- **Google Credentials**: `credentials.json` and `token.json` must be manually SCP'd to `toolbox/google-drive/`.
- **Gemini Key**: Export `GEMINI_API_KEY` in environment or `.env` file.

---

## 🤖 6. MCP Server Configuration (Antigravity)

> **Config Path**: `~/.gemini/antigravity/mcp_config.json`

### Active Servers

| Server              | Transport | Description                        |
| ------------------- | --------- | ---------------------------------- |
| `github-mcp-server` | Docker    | GitHub API (search, commits, PRs)  |
| `n8n-mcp-server`    | Docker    | n8n workflow management (19 tools) |
| `docker-nuc`        | SSH       | Remote Docker on NUC               |
| `google-drive`      | Python    | Google Drive search                |

### Server Details

#### github-mcp-server

- **Image**: `ghcr.io/github/github-mcp-server`
- **Auth**: `GITHUB_PERSONAL_ACCESS_TOKEN` (env var)
- **Disabled**: Issue/PR write tools (safety)

#### n8n-mcp-server

- **Image**: `ghcr.io/czlonkowski/n8n-mcp:latest`
- **Auth**: `N8N_API_KEY` (JWT token from n8n Settings → Public API)
- **Host**: `http://172.30.0.169:5678`
- **Key Tools**: `n8n_create_workflow`, `n8n_list_workflows`, `validate_workflow`

#### docker-nuc

- **Transport**: SSH to `tariqk@172.30.0.169`
- **Binary**: `/home/tariqk/mcp-venv/bin/mcp-server-docker`
- **Disabled**: Destructive tools (remove_image, remove_volume)

#### google-drive

- **Transport**: Local Python
- **Path**: `toolbox/mcp-servers/gdrive/server.py`
- **Auth**: Uses `credentials.json` from `toolbox/google-drive/`

---

## 📋 7. n8n Workflows

| Workflow              | Trigger       | Description                                          |
| --------------------- | ------------- | ---------------------------------------------------- |
| Plaud Gmail to Drive  | Gmail polling | Intercepts Plaud recordings, saves to Drive          |
| Readwise Daily Digest | Cron (7 AM)   | Fetches unread articles, Gemini summary, Google Chat |

### Workflow Files

- **Source of Truth**: `toolbox/n8n/`
- **Deploy via**: `n8n-mcp-server` (`n8n_create_workflow` tool)

### Deployment Preference Order

When deploying workflows or configs to the NUC:

1. **MCP Server** – Use `n8n_create_workflow` or `docker-nuc` tools directly.
2. **SSH + GitHub** – Push from Chromebook, `git pull` on NUC, then API call.
3. **Manual UI** – Last resort; use n8n's Import function.
