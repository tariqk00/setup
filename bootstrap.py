#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import json
from pathlib import Path

def run_cmd(cmd, check=True):
    print(f"Running: {cmd}")
    try:
        return subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def setup_linux():
    print("Detected Linux/ChromeOS environment.")
    
    # 1. Install gnome-keyring
    res = run_cmd("dpkg -l gnome-keyring", check=False)
    if res.returncode != 0:
        print("Installing gnome-keyring...")
        run_cmd("sudo apt-get update && sudo apt-get install -y gnome-keyring")
    else:
        print("gnome-keyring is already installed.")

    # 2. Configure argv.json
    # Locate Antigravity/VS Code config
    possible_paths = [
        Path.home() / ".antigravity" / "argv.json",
        Path.home() / ".vscode" / "argv.json",
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"Found config at {path}. Checking encryption settings...")
            with open(path, "r") as f:
                content = f.read()
            
            # Simple check for existing entry
            if '"password-store": "gnome-libsecret"' not in content:
                print(f"Updating {path} to use gnome-libsecret...")
                # We carefully append before the final brace to avoid breaking comments
                content = content.strip()
                if content.endswith("}"):
                    # Remove trailing brace, add comma, add setting, add brace
                    new_content = content[:-1].rstrip()
                    if not new_content.endswith(","):
                        new_content += ","
                    new_content += '\n    "password-store": "gnome-libsecret"\n}'
                    with open(path, "w") as f:
                        f.write(new_content)
                    print("Updated successfully. RESTART the IDE to take effect.")
                else:
                    print("Could not automatically parse argv.json. Please add \"password-store\": \"gnome-libsecret\" manually.")
            else:
                print("Encryption settings are already correctly configured.")
            break
    else:
        print("Could not find argv.json in common locations. Skipping IDE config.")

def setup_darwin():
    print("Detected macOS environment.")
    print("MacOS usually handles keychains natively. No specific fixes are currently needed.")
    print("TIP: Consider installing Homebrew: https://brew.sh/")

def setup_windows():
    print("Detected Windows environment.")
    print("Windows uses the integrated Windows Credential Manager. No specific fixes are currently needed.")
    print("TIP: Consider using Winget for package management.")

def main():
    current_os = platform.system()
    
    if current_os == "Linux":
        setup_linux()
    elif current_os == "Darwin":
        setup_darwin()
    elif current_os == "Windows":
        setup_windows()
    else:
        print(f"Unsupported OS: {current_os}")

    print("\nSetup script complete.")
    print("Manual Steps Required:")
    print("1. Sign into your GitHub account in the IDE.")
    print("2. Clone your repositories.")

if __name__ == "__main__":
    main()
