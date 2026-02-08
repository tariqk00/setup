#!/usr/bin/env python3
import subprocess
import sys
import shutil
import json
from pathlib import Path

"""
Diagnostic script to verify health of NUC (remote) and Chromebook (local) environments.
Checks SSH, Docker containers, Systemd timers, and n8n workflows.
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
        self.mcp_config = self.home / ".gemini/antigravity/mcp_config.json"
        self.n8n_key = self.get_n8n_key()

    def get_n8n_key(self):
        try:
            if not self.mcp_config.exists():
                return None
            with open(self.mcp_config, 'r') as f:
                config = json.load(f)
                server_config = config.get("mcpServers", {}).get("n8n-mcp-server", {})
                args = server_config.get("args", [])
                for arg in args:
                    if arg.startswith("N8N_API_KEY="):
                        return arg.split("=", 1)[1]
        except Exception:
            return None
        return None

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
        self.check_file_exists(self.home / ".ssh/id_ed25519_antigravity", "Antigravity SSH Key")
        self.check_file_exists(self.mcp_config, "MCP Config")

        for repo in [self.setup_repo, self.toolbox_repo]:
            if repo.exists():
                print_status(f"Repo exists: {repo.name}", "PASS")
                ok, out = self.run_command(f"cd {repo} && git status --porcelain", shell=True)
                if ok and not out:
                    print_status(f"Repo clean: {repo.name}", "PASS")
                else:
                    print_status(f"Repo dirty: {repo.name}", "WARN", "Uncommitted changes")
            else:
                print_status(f"Repo missing: {repo.name}", "FAIL", repo)

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
        ok, out = self.run_ssh_command(host, "docker ps --format '{{.Names}}' | grep -w n8n")
        if ok and out == "n8n":
            print_status("Container running: n8n", "PASS")
        else:
            print_status("Container missing: n8n", "FAIL", "Not running")

        # 4. Systemd Health
        units = [
            ("ai-sorter.timer", "ai-sorter.service"),
            ("n8n-backup.timer", "n8n-backup.service"),
            ("plaud-automation.timer", "plaud-automation.service"),
            ("cloudflared.service", None)
        ]
        
        for timer, service in units:
            # Check Timer/Service active state
            is_user = "cloudflared" not in timer
            cmd_prefix = "systemctl --user" if is_user else "systemctl"
            
            ok, state = self.run_ssh_command(host, f"{cmd_prefix} is-active {timer}")
            if not ok or state != "active":
                print_status(f"Unit inactive: {timer}", "FAIL", state)
                continue
            
            if service:
                # Check Service Success status
                ok, out = self.run_ssh_command(host, f"{cmd_prefix} show {service} -p Result,ExecMainStatus")
                details = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
                
                result = details.get("Result", "unknown")
                status = details.get("ExecMainStatus", "-1")
                
                if result == "success" and status == "0":
                    print_status(f"Job healthy: {timer}", "PASS")
                else:
                    print_status(f"Job failing: {timer}", "WARN", f"Result={result}, Status={status}")
            else:
                print_status(f"Unit healthy: {timer}", "PASS")

        # 5. n8n Workflows
        self.check_n8n()

    def check_n8n(self):
        if not self.n8n_key:
            print_status("n8n Health", "WARN", "API Key missing in mcp_config.json")
            return

        print(f"\n{YELLOW}=== n8n Workflow Health ==={RESET}")
        
        critical_workflows = [
            "Readwise Daily Digest v3",
            "Gemini Journal to Drive",
            "Plaud Gmail to Drive"
        ]

        # Get all workflows to find active status and IDs
        api_url = "http://172.30.0.169:5678/api/v1"
        ok, out = self.run_command(f"curl -s -H 'X-N8N-API-KEY: {self.n8n_key}' {api_url}/workflows", shell=True)
        if not ok:
            print_status("n8n API Connection", "FAIL", "Could not reach API")
            return

        try:
            workflows = json.loads(out).get("data", [])
            for name in critical_workflows:
                matched = next((w for w in workflows if w["name"] == name), None)
                if not matched:
                    # Try fuzzy match for Plaud
                    if "Plaud" in name:
                        matched = next((w for w in workflows if "Plaud" in w["name"] and w.get("active")), None)
                    
                    if not matched:
                        print_status(f"Workflow missing: {name}", "FAIL")
                        continue

                # Check active status
                if not matched.get("active"):
                    print_status(f"Workflow inactive: {matched['name']}", "FAIL")
                    continue

                # Check last execution status
                wf_id = matched["id"]
                ok, ex_out = self.run_command(f"curl -s -H 'X-N8N-API-KEY: {self.n8n_key}' '{api_url}/executions?workflowId={wf_id}&limit=1'", shell=True)
                if ok:
                    executions = json.loads(ex_out).get("data", [])
                    if executions:
                        last = executions[0]
                        if last.get("status") == "success":
                            print_status(f"Workflow healthy: {matched['name']}", "PASS")
                        else:
                            print_status(f"Workflow failing: {matched['name']}", "FAIL", f"Status: {last.get('status')} at {last.get('stoppedAt')}")
                    else:
                        print_status(f"Workflow healthy: {matched['name']}", "PASS", "No recent runs")
        except Exception as e:
            print_status("n8n Check Error", "FAIL", str(e))

if __name__ == "__main__":
    checker = SystemChecker()
    checker.check_local()
    checker.check_remote()
