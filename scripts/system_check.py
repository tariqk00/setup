#!/usr/bin/env python3
import subprocess
import sys
import shutil
from pathlib import Path

"""
Diagnostic script to verify health of NUC (remote) and Chromebook (local) environments.
Checks SSH, Docker containers, Systemd timers, and git repo status.
"""

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(check_name, status, message=""):
    if status == "PASS":
        print(f"[{GREEN}PASS{RESET}] {check_name}")
    elif status == "FAIL":
        print(f"[{RED}FAIL{RESET}] {check_name} - {message}")
    elif status == "WARN":
        print(f"[{YELLOW}WARN{RESET}] {check_name} - {message}")

class SystemChecker:
    def __init__(self):
        self.home = Path.home()
        self.setup_repo = self.home / "repos/personal/setup"
        self.toolbox_repo = self.home / "repos/personal/toolbox"

    def run_command(self, cmd, shell=False):
        try:
            result = subprocess.run(cmd, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()

    def run_ssh_command(self, host, cmd):
        ssh_cmd = f"ssh {host} '{cmd}'"
        return self.run_command(ssh_cmd, shell=True)

    def check_file_exists(self, path, desc):
        if Path(path).exists():
            print_status(f"File exists: {desc}", "PASS")
        else:
            print_status(f"File missing: {desc}", "FAIL", path)

    def check_local(self):
        print(f"\n{YELLOW}=== Chromebook (Local) Checks ==={RESET}")
        
        # 1. Critical Secrets
        self.check_file_exists(self.home / ".ssh/id_ed25519_antigravity", "Antigravity SSH Key")
        self.check_file_exists(self.home / ".gemini/antigravity/mcp_config.json", "MCP Config")
        # self.check_file_exists(self.toolbox_repo / "config/credentials.json", "Google Credentials") # Might be in google-drive/

        # 2. Repos
        for repo in [self.setup_repo, self.toolbox_repo]:
            if repo.exists():
                print_status(f"Repo exists: {repo.name}", "PASS")
                # Check for uncommitted changes
                ok, out = self.run_command(f"cd {repo} && git status --porcelain", shell=True)
                if ok and not out:
                    print_status(f"Repo clean: {repo.name}", "PASS")
                else:
                    print_status(f"Repo dirty: {repo.name}", "WARN", "Uncommitted changes")
            else:
                print_status(f"Repo missing: {repo.name}", "FAIL", repo)

        # 3. Venv
        venv_path = self.toolbox_repo / "google-drive/venv"
        if venv_path.exists():
            print_status("Python Venv exists", "PASS")
        else:
            print_status("Python Venv missing", "WARN", venv_path)

    def check_remote(self):
        print(f"\n{YELLOW}=== NUC (Remote) Checks ==={RESET}")
        
        host = "nuc"
        
        # 1. SSH Connection
        print("Checking SSH connection...", end="\r")
        ok, out = self.run_ssh_command(host, "echo connected")
        if not ok:
            print(" " * 40, end="\r")
            print_status("SSH Connection", "FAIL", "Could not connect to nuc")
            return
        print(" " * 40, end="\r")
        print_status("SSH Connection", "PASS")

        # 2. Disk Usage
        ok, out = self.run_ssh_command(host, "df -h / | tail -1 | awk '{print $5}'")
        if ok:
            usage = int(out.replace('%', ''))
            status = "PASS" if usage < 85 else "WARN"
            print_status(f"Disk Usage ({usage}%)", status)
        
        # 3. Docker Containers
        containers = ["n8n"]
        for container in containers:
            ok, out = self.run_ssh_command(host, f"docker ps --format '{{{{.Names}}}}' | grep -w {container}")
            if ok and out == container:
                print_status(f"Container running: {container}", "PASS")
            else:
                print_status(f"Container missing: {container}", "FAIL", "Not running")

        # 4. Systemd Timers/Services
        units = [
            ("ai-sorter.timer", "active"),
            ("n8n-backup.timer", "active"),
            ("plaud-automation.timer", "active"),
            ("cloudflared.service", "active")
        ]
        
        for unit, expected_state in units:
            # Check is-active
            ok, out = self.run_ssh_command(host, f"systemctl --user is-active {unit} 2>/dev/null || systemctl is-active {unit}")
            # cloudflared is system-level, others user-level. The OR logic handles both if we're lazy, 
            # but better to be specific. ENV_SETUP says cloudflared is system check.
            
            # Actually, let's just try both for safety or be specific
            if "cloudflared" in unit:
                 ok, out = self.run_ssh_command(host, f"systemctl is-active {unit}")
            else:
                 ok, out = self.run_ssh_command(host, f"systemctl --user is-active {unit}")

            if ok and out == expected_state:
                print_status(f"Systemd Unit: {unit}", "PASS")
            else:
                print_status(f"Systemd Unit: {unit}", "FAIL", f"State: {out}")

if __name__ == "__main__":
    checker = SystemChecker()
    checker.check_local()
    checker.check_remote()
