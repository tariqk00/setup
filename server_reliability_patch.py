#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command, description):
    print(f"--- {description} ---")
    try:
        subprocess.run(command, check=True, shell=True)
        print("SUCCESS")
    except subprocess.CalledProcessError:
        print(f"FAILED: {command}")
        # Continue execution, don't exit immediately unless critical

def main():
    if os.geteuid() != 0:
        print("This script must be run as root (sudo).")
        sys.exit(1)

    print("Applying NUC8i5 Reliability Fixes...")

    # 1. Disable Sleep
    run_command(
        "systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target",
        "Masking Sleep/Suspend Targets"
    )

    # 2. Kernel C-States (GRUB)
    grub_file = '/etc/default/grub'
    cstate_param = "intel_idle.max_cstate=1"
    
    with open(grub_file, 'r') as f:
        grub_content = f.read()
    
    if cstate_param not in grub_content:
        print(f"--- Updating {grub_file} for C-States ---")
        try:
            # Simple replacement for default line
            cmd = f"sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"/GRUB_CMDLINE_LINUX_DEFAULT=\"{cstate_param} /' {grub_file}"
            subprocess.run(cmd, check=True, shell=True)
            run_command("update-grub", "Updating GRUB bootloader")
        except Exception as e:
            print(f"Error updating GRUB: {e}")
    else:
        print("--- GRUB already contains C-State fix (Skipping) ---")

    # 3. Hardware Watchdog (Softdog) configuration
    modules_load_path = '/etc/modules-load.d/softdog.conf'
    if not os.path.exists(modules_load_path):
        print(f"--- Creating {modules_load_path} ---")
        with open(modules_load_path, 'w') as f:
            f.write("softdog\n")
    
    # Unblacklist softdog if needed (blind attempt at common paths)
    blacklist_path = "/lib/modprobe.d"
    print("--- Checking for softdog blacklist ---")
    try:
        # Recursive sed to comment out blacklist entries
        subprocess.run(f"find {blacklist_path} -name '*.conf' -exec sed -i 's/^blacklist softdog/#blacklist softdog/' {{}} +", shell=True)
        print("Unblacklisted softdog in " + blacklist_path)
    except Exception as e:
        print(f"Warning unblacklisting: {e}")

    # 4. Systemd Watchdog Config
    systemd_conf = '/etc/systemd/system.conf'
    print(f"--- Updating {systemd_conf} ---")
    run_command(f"sed -i 's/^#RuntimeWatchdogSec.*/RuntimeWatchdogSec=20s/' {systemd_conf}", "Setting RuntimeWatchdogSec")
    run_command(f"sed -i 's/^#RebootWatchdogSec.*/RebootWatchdogSec=30s/' {systemd_conf}", "Setting RebootWatchdogSec")
    
    run_command("systemctl daemon-reload", "Reloading Systemd")

    print("\nChanges applied. Please REBOOT the server to verify.")

if __name__ == "__main__":
    main()
