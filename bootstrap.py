#!/usr/bin/env python3
import sys
import subprocess

def run_script(script_name):
    print(f"--- Running {script_name} ---")
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error: {script_name} failed.")
        sys.exit(1)

def show_help():
    print("Usage: python3 bootstrap.py [module]")
    print("\nAvailable modules:")
    print("  dev-env        - Initial setup for local developer environment (Antigravity/ChromeOS fixes)")
    print("  ubuntu-server  - Reference guide for Ubuntu Server setup (CasaOS, n8n, etc.)")
    print("  all            - Run all applicable setup scripts (default: dev-env)")
    print("\nIf no module is specified, it defaults to 'dev-env'.")

def main():
    if len(sys.argv) > 1:
        module = sys.argv[1].lower()
    else:
        module = "dev-env"

    if module in ["help", "--help", "-h"]:
        show_help()
        return

    if module == "dev-env":
        run_script("dev_env_setup.py")
    elif module == "ubuntu-server":
        print("Please refer to 'ubuntu_server_setup.md' for manual server setup steps.")
    elif module == "all":
        run_script("dev_env_setup.py")
        print("\nNote: For Ubuntu Server setup, please refer to 'ubuntu_server_setup.md'.")
    else:
        print(f"Unknown module: {module}")
        show_help()
        sys.exit(1)

    print("\nSetup process complete.")

if __name__ == "__main__":
    main()
