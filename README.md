# Setup & Dotfiles

This repository contains automation scripts and configuration files to quickly rebuild my developer environment on any OS, with a primary focus on ChromeOS (Crostini).

## Quick Start (Bootstrap)

To set up a fresh environment, clone this repository and run the bootstrap script:

```bash
git clone https://github.com/tariqk00/setup.git ~/github/tariqk00/setup
cd ~/github/tariqk00/setup
python3 bootstrap.py
```

### What it handles:
- **Linux/ChromeOS**:
    - Installs `gnome-keyring` for secure credential storage.
    - Configures Antigravity/VS Code to use the secure keyring (fixing the "OS keyring" error).
- **Windows/macOS**:
    - Detects OS and provides recommendations for native package managers.

## Manual Steps (Post-Setup)

While the script handles system configuration, the following must be done manually:

1.  **Sign in to GitHub**: Click the accounts icon in the IDE and sign in to restore repository sync.
2.  **Clone Repositories**: Clone your active projects (e.g., `media`).
3.  **Install Language Tools**:
    - **HandBrake CLI**: `sudo apt install handbrake-cli`
    - **Python 2** (if needed for older scripts): `sudo apt install python2`

## Repository Structure
- `bootstrap.py`: Core automation script.
- `README.md`: Setup instructions and manual checks.
