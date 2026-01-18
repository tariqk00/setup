# Remediation Log - Jan 14, 2026

## Actions Taken

1.  **Kernel Configuration**:

    - Modified `/etc/default/grub` to include `pcie_aspm=off`.
    - Purpose: Disable PCIe Active State Power Management to prevent NVMe controller locks.
    - Status: Applied and `update-grub` executed.

2.  **Software Cleanup**:
    - Removed: `lubuntu-desktop`, `sddm`, `gnome-shell`.
    - Executed `autoremove` to clean up dependencies (including `pipewire` user sessions).
    - Purpose: Remove unstable GUI/Audio stack causing `syslog` floods and power conflcits.

## Verification Required

- [x] Reboot NUC (`sudo reboot`).
- [x] Verify clean boot logs (no `RTKit` errors).
- [x] Monitor uptime > 24 hours (Confirmed: 1 Day 2 Hours, Jan 15).

## Post-Fix Status (Jan 15 16:45)

- **Stability**: PASS. Uptime > 26 hours. No freezes.
- **Kernel Cmd**: `pcie_aspm=off intel_idle.max_cstate=1` (Confirmed)
- **Memory**: 1.5Gi Used / 31Gi Total (Stable)
- **Logs**: Clean. No `pipewire` or `RTKit` spam. `wpa_supplicant` noise only.
- **Remote Access**: Verified `cloudflared` active (Confirmed).
