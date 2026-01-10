# Ubuntu Server Setup Guide

This guide documents the setup and configuration of my "Always-On" Ubuntu Server.

## Connection Details
- **Server IP**: `172.30.0.169`
- **User**: `tariqk`
- **Access**: Passwordless SSH (configured)

## Primary Stack
- **OS**: Ubuntu Server 24.04 LTS
- **Dashboard/Management**: [CasaOS](https://casaos.io/)
- **Automation**: [n8n](https://n8n.io/)
- **Runtime**: Python 3, Node.js

## Installation Checklist

### 1. Base OS
- [x] Install Ubuntu Server 24.04 LTS
- [x] Update system: `sudo apt update && sudo apt upgrade -y`

### 2. Core Services
#### CasaOS
- [x] Install CasaOS: `curl -fsSL https://get.casaos.io | sudo bash`
- **Access**: `http://172.30.0.169`

#### n8n
- [x] Installed via CasaOS (Docker)
- **Access**: `http://172.30.0.169:5678` (default port)

### 3. Developer Tools
- [x] Python 3
- [x] Node.js & npm
- [x] Git

### 4. Custom Automations
#### Plaud Gmail-to-Drive
- [x] Migrated from local environment.
- **Path**: `/home/tariqk/github/tariqk00/plaud`
- **Schedule**: Daily at 07:00 AM (via systemd user timer).
- **Control**: `systemctl --user status plaud-automation.timer`
- **Review Logs**: `journalctl --user -u plaud-automation.service -f`

## Maintenance Commands
- **Check n8n status**: `docker logs n8n` (if using Docker)
- **Check CasaOS status**: `sudo systemctl status casaos-gateway`

### 5. NUC Reliability (CRITICAL)
Essential fixes for NUC8i5 stability on Linux (prevents random freezes).

#### 1. Disable Sleep
- [x] Mask sleep targets: `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`

#### 2. Kernel Stability (C-States)
- [x] Limit C-states in GRUB:
    - Edit `/etc/default/grub`
    - Set: `GRUB_CMDLINE_LINUX_DEFAULT="intel_idle.max_cstate=1"`
    - Run: `sudo update-grub`

#### 3. Hardware Watchdog (Auto-Reboot)
- [x] Enable `softdog` module:
    - Unblacklist: Comment out `blacklist softdog` in `/lib/modprobe.d/blacklist_linux_*.conf` (if present).
    - Persist: `echo 'softdog' | sudo tee /etc/modules-load.d/softdog.conf`
- [x] Configure Systemd Watchdog:
    - Edit `/etc/systemd/system.conf`:
        - `RuntimeWatchdogSec=20s`
        - `RebootWatchdogSec=30s`
    - Reload: `sudo systemctl daemon-reload`

### 6. Storage Expansion
- [x] All unallocated space merged into root filesystem.
- **Total Capacity**: 462GB (Full SSD).

## History
For a detailed forensic timeline of this server's installation and lifecycle, see [server_history_log.md](server_history_log.md).

