# Developer Setup & Infrastructure

This repository centralizes automation scripts and documentation for my development environment and server infrastructure.

> **Repository Policy**: This repo is the single source of truth for configuration across all user endpoints, including:
> - **Chromebook**: Local development environment (VS Code, Antigravity, tools).
> - **NUC8i5 Server**: Always-on services (CasaOS, n8n, automation).
> - **Future Endpoints**: Any other configurable machines.

## Structure

- `bootstrap.py`: Main entry point for running setup modules.
- `dev_env_setup.py`: Local developer environment configuration (e.g., Antigravity/ChromeOS fixes).
- `server_status.py`: Health check script for the Ubuntu Server (pings, SSH, and web services).
- `server_reliability_patch.py`: **[NEW]** Automation script to apply critical NUC8i5 reliability fixes (Watchdog, C-states).
- `ubuntu_server_setup.md`: Guide and checklist for setting up the "Always-On" Ubuntu Server.

## Usage

### Local Developer Environment
To set up or fix a local developer environment:
```bash
python3 bootstrap.py dev-env
```
*(Handles `gnome-keyring` installation and VS Code/Antigravity encryption settings)*

### Ubuntu Server
For server setup steps (CasaOS, n8n, etc.), refer to:
[ubuntu_server_setup.md](file:///home/takhan/github/tariqk00/setup/ubuntu_server_setup.md)

To check the status of your server and its services:
```bash
python3 server_status.py
```

---

## Repository Sync
This folder (`~/github/tariqk00`) is the root for all repositories. Ensure all projects are cloned here for consistency.

### Chrome Installation (Chromebook Fix)
If the agent cannot detect Chrome, manually install the stable binary:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

**Binary path for Agent Configuration:** `/usr/bin/google-chrome`
