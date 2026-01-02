# Developer Setup & Infrastructure

This repository centralizes automation scripts and documentation for my development environment and server infrastructure.

## Structure

- `bootstrap.py`: Main entry point for running setup modules.
- `dev_env_setup.py`: Local developer environment configuration (e.g., Antigravity/ChromeOS fixes).
- `server_status.py`: Health check script for the Ubuntu Server (pings, SSH, and web services).
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
