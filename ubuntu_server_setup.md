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

## Maintenance Commands
- **Check n8n status**: `docker logs n8n` (if using Docker)
- **Check CasaOS status**: `sudo systemctl status casaos-gateway`
