#!/usr/bin/env python3
import subprocess
import requests
import sys

# Server configuration
SERVER_IP = "172.30.0.169"
SERVER_USER = "tariqk"
SERVICES = {
    "CasaOS": f"http://{SERVER_IP}",
    "n8n": f"http://{SERVER_IP}:5678"
}

def check_ping(host):
    print(f"--- Pinging {host} ---")
    try:
        subprocess.run(["ping", "-c", "1", "-W", "2", host], check=True, capture_output=True)
        print("Ping: SUCCESS")
        return True
    except subprocess.CalledProcessError:
        print("Ping: FAILED")
        return False

def check_http_service(name, url):
    print(f"--- Checking {name} ({url}) ---")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code < 400:
            print(f"{name}: UP (Status: {response.status_code})")
            return True
        else:
            print(f"{name}: DOWN (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{name}: UNREACHABLE (Error: {e})")
        return False

def check_ssh(user, host):
    print(f"--- Checking SSH access ({user}@{host}) ---")
    try:
        # Just run a simple command via SSH
        subprocess.run(["ssh", "-o", "ConnectTimeout=5", f"{user}@{host}", "uptime"], check=True, capture_output=True)
        print("SSH: SUCCESS")
        return True
    except subprocess.CalledProcessError:
        print("SSH: FAILED")
        return False

def main():
    print(f"Verifying status for Ubuntu Server: {SERVER_IP}\n")
    
    server_up = check_ping(SERVER_IP)
    if not server_up:
        print("\nServer appears to be offline. Skipping further checks.")
        sys.exit(1)
    
    check_ssh(SERVER_USER, SERVER_IP)
    
    print("\nChecking Web Services:")
    for name, url in SERVICES.items():
        check_http_service(name, url)

if __name__ == "__main__":
    main()
