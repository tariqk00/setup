# Implementation Plan - NUC Freeze RCA

## Goal Description

Perform a deep forensic analysis of the NUC server to identify the root cause of the "silent freeze" on Jan 13, 2026.

## Investigation Strategy

### 1. Hardware & Thermals

- [ ] Check active thermal zones for overheating signs.
- [ ] Check SMART data for NVMe drive health.
- [ ] Review `dmesg` for hardware error signatures (PCIe bus errors, invalid opcodes).

### 2. Software & Concurrency

- [ ] Analyze "Last Breath" logs: Review logs immediately preceding 08:04 AM.
- [ ] Audit `casaos` and Docker resource usage (possible OOM kill without logging?).
- [ ] Inspect GPU/Graphics driver state (Intel i915 interactions with `lubuntu-desktop`).

### 3. Power Management

- [ ] Verify if `intel_idle.max_cstate=1` is actually active.
- [ ] Check for C-state residency or sleep attempts.

## Verification Plan

- [ ] Produce an RCA Report with findings.
- [ ] Propose specific remediation (e.g., Kernel parameter adjustments, Removal of GUI, BIOS updates).
