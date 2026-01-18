# NUC Ubuntu Server: Forensic History Report

**Target**: `nuc8i5-2020` (`172.30.0.169`)
**Analysis Date**: 2026-01-10
**Data Sources**: `/var/log/installer`, `/var/log/apt`, `/var/log/dpkg`, `/etc` config files.

## 2026-01-16: AI Sorter Upgrade & Reliability Hardening

**1. Reliability Fix (Systemd Lingering)**

- **Issue**: Automated jobs (`plaud-automation`, `ai-sorter`) were dying on SSH logout because `systemd --user` session was terminating.
- **Fix**: Enabled lingering for user `tariqk` (`sudo loginctl enable-linger tariqk`).
- **Result**: User-level systemd timers now run 24/7 independent of active sessions.

**2. AI Drive Sorter v0.4.0**

- **Feature**: Centralized Logging.
  - Moved local history CSV to Google Drive Folder: `_Master_Archive_Metadata`.
  - Auto-syncs `renaming_history.csv` after every run.
- **Enhancement**: Enriched Data Schema.
  - Added columns: `Target_Folder` (Destination) and `Run_Type` (Auto vs Manual).
- **Cleanup**: Archived legacy logs to `_legacy_backup_jan10.csv`.

## 1. Genesis: Installation (Jan 1, 2026)

The system was provisioned via **Autoinstall** (automated Ubuntu Server installer).

- **OS Base**: Ubuntu Server 24.04.3 LTS ("Noble Numbat").
- **Hostname**: `nuc8i5-2020`
- **Primary User**: `tariqk` (configured with passwordless sudo).
- **Network**: Wired Ethernet (`eno1`) using DHCP. WiFi was detected but not configured.
- **Storage Layout**:
  - **Disk**: 500GB Samsung SSD 970 EVO (`/dev/nvme0n1`)
  - **Partitioning**: LVM (Logical Volume Manager).
    - **Total Capacity**: ~500GB
    - **Allocated**: 100GB to Root (`/`).
    - **Unallocated**: ~400GB remains available in the Volume Group (`ubuntu-vg`) for future snapshots or expansion. This was a default installer choice.

## 2. The "CasaOS" Era (Jan 1 - Jan 4)

Immediately following the OS install, a third-party management layer was deployed.

- **Stack**: CasaOS (Community-based personal cloud OS).
- **Evidence**:
  - `apt` logs show bulk installation of `docker-ce`, `udevil` (drive mounting), `samba` (file sharing), and `mergerfs`.
  - These packages are signatures of the CasaOS installation script.

## 3. The "Desktop" Pivot (Jan 5, 2026)

A significant deviation from a standard headless server occurred on Jan 5.

- **Event**: Manual installation of a Graphical User Interface.
- **Command**: `apt-get install -y lubuntu-desktop --no-install-recommends`
- **Time**: ~18:00 Local Time.
- **Impact**:
  - Installed `sddm` (display manager), `lxqt` (desktop environment), and X11/Xorg subsystems.
  - **Consequence**: This likely introduced desktop-class power management rules (suspend/sleep on idle) which conflicted with the NUC hardware, leading to the instability observed later.

## 4. Reliability Hardening (Jan 10, 2026)

Response to system freezes/crashes.

- **Kernel**: Modified `/etc/default/grub` to set `intel_idle.max_cstate=1` (prevents deep CPU sleep states known to freeze NUCs).
- **Watchdog**: Enabled `softdog` hardware watchdog and systemd `RuntimeWatchdog` to auto-reboot if the kernel hangs.
- **Power**: Masked all systemd sleep targets.

### January 10, 2026: storage Expansion

- **Action**: Expanded root filesystem to utilize full SSD capacity.
- **Before**: 100GB allocated, ~400GB unallocated.
- **After**: 462GB allocated (Full Disk).
- **Command**: `lvextend -l +100%FREE` + `resize2fs`.

## Configuration Audit

### Storage (`/etc/fstab`)

- **Root**: Ext4 on LVM.
- **Boot**: Ext4 on partition 2.
- **EFI**: VFAT on partition 1.
- **Swap**: File-based swap (`/swap.img`).
- **Note**: No external drives or NAS mounts are currently defined in `fstab`, despite the presence of `samba`/`mergerfs` (CasaOS often manages mounts dynamically outside `fstab`).

### Network (`/etc/netplan`)

- **Config**: `50-cloud-init.yaml`
- **State**: Default DHCP. No static IP configured at the OS level (likely handled by router reservation).

### Software Timeline

| Date       | Action          | Context                                            |
| :--------- | :-------------- | :------------------------------------------------- |
| **Jan 01** | **OS Install**  | Ubuntu Server 24.04 (Headless)                     |
| **Jan 01** | **CasaOS**      | Docker, Samba, MergerFS added                      |
| **Jan 01** | **Dev Tools**   | Python3, Node.js installed                         |
| **Jan 05** | **GUI Install** | **Lubuntu Desktop** added (System became "Hybrid") |
| **Jan 05** | **Crash**       | First recorded crash/freeze following GUI install  |
| **Jan 08** | **Crash**       | Second major freeze requiring hard reboot          |
| **Jan 10** | **Fixes**       | Watchdog & Power settings applied                  |

## Recommendations

1.  **LVM Expansion**: You have ~400GB of unallocated space on your NVMe. You can expand your root filesystem or create a distinct `/home` or `/data` volume if needed.
2.  **Desktop Removal?**: If the server is intended to be headless, removing `lubuntu-desktop` and `sddm` would save resources and reduce complexity, though the recent reliability fixes should mitigate the stability risks.

### January 13, 2026: The "Silent Freeze" & Power Outage

- **Event**: System stopped logging at `08:04 AM` (Jan 13).
- **Context**: Remained unresponsive for ~14 hours.
- **Power Loss**: Occurred at `22:37 PM` (Jan 13), confirmed by client-side logs.
- **Recovery**: Manual power-on at `08:11 AM` (Jan 14).
- **Analysis**:
  - The Jan 10 reliability fixes (watchdog/power) **failed** to prevent this freeze or auto-reboot the system.
  - BIOS "After Power Failure" is likely set to "Stay Off".
  - `softdog` is active but did not trigger a reboot, suggesting a partial hang or GPU/Power state lockup rather than a full kernel panic.
