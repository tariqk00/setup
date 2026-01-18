# Root Cause Analysis (RCA) - Jan 13 Freeze

**Date:** Jan 14, 2026
**Target:** NUC8i5 (`nuc8i5-2020`)
**Incident:** Silent System Freeze (~14 hours) followed by non-rebooting Power Loss.

## 1. Executive Summary

The system experienced a **hardware-level IO deadlock** originating from the NVMe SSD controller. This was likely triggered by conflicting Power Management (ASPM) states between the Ubuntu Desktop kernel services and the NUC's hardware. The `softdog` watchdog failed to trigger a reboot because the root filesystem was inaccessible (IO Lock), preventing userspace watchdog updates or kernel panic logs from being written.

## 2. Findings

### A. The "Silent" Freeze (Primary Cause)

- **Symptom:** Logs cut off abruptly at `08:04 AM`. No "kernel panic" or stack trace was written to disk.
- **Evidence:**
  - `smartctl` reveals **1,659 Error Log Entries** on the NVMe drive (`/dev/nvme0n1`).
  - High error counts on NUC NVMe drives are a hallmark of **PCIe Active State Power Management (ASPM)** issues, where the drive fails to wake from a low-power state, locking the bus.
  - **Thermals are normal** (CPU 57°C, NVMe 34°C), ruling out overheating.

### B. The Desktop "Noise" (Contributing Factor)

- **Symptom:** `syslog` is flooded with `pipewire` and `RTKit` DBus errors.
- **Impact:** The `lubuntu-desktop` installation left active audio services (Pipewire) running in the background. These services constantly poll hardware/interrupts, potentially preventing deep idle states or causing race conditions with power management.

### C. Watchdog Failure

- **Why it failed:** The `softdog` depends on writing to `/dev/watchdog`. If the NVMe controller is locked (IO Deadlock), the system cannot interact with the watchdog file descriptor, and the kernel itself may be effectively frozen waiting on IO.

### D. Power Recovery Failure

- **Observation:** System did not Power On after outage.
- **Cause:** BIOS "After Power Failure" setting is default/off.

## 3. Remediation Plan (Recommended)

We must eliminate the software conflicts and disable the aggressive power saving on the PCIe bus.

1.  **Likely Fix (PCIe PM):** Add `pcie_aspm=off` to GRUB. This forces the PCIe bus to stay fully active, preventing the NVMe controller from sleeping and locking up.
2.  **Cleanup:** Remove `lubuntu-desktop` to stop the Pipewire/DBus thrashing.
3.  **BIOS:** Manually change "After Power Failure" to "Last State".

## 4. Next Steps

- [ ] Apply `pcie_aspm=off` to `/etc/default/grub`.
- [ ] Purge Desktop packages.
