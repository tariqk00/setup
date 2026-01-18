# Gemini Context: Antigravity on ChromeOS

> [!IMPORTANT]
> **READ THIS FIRST**: This environment is **NOT** a standard Linux/VS Code setup.

## 1. System Identity

- **Hardware**: Chromebook (Asus cx5403, "rex" board).
- **OS**: ChromeOS (Beta Channel).
- **Container**: `penguin` (Crostini / Debian Bookworm).
- **IDE**: Google Antigravity (Project IDX / VS Code Fork).

## 2. Antigravity Specifics

The IDE is a specialized build, which affects file paths and process names.

| Standard VS Code Path | **Antigravity Path**               |
| :-------------------- | :--------------------------------- |
| `~/.vscode/argv.json` | **`~/.antigravity/argv.json`**     |
| `~/.config/Code`      | **`~/.config/Antigravity`**        |
| Binary: `code`        | Binary: `antigravity` (wraps code) |

## 3. Known Issues & Fixes

### A. Webview "InvalidStateError"

- **Cause**: Linux container GPU passthrough desyncs after sleep.
- **Fix**: Disable Hardware Acceleration.
- **Config**: Ensure `"disable-hardware-acceleration": true` is in `~/.antigravity/argv.json`.
- **Script**: `~/github/tariqk00/toolbox/scripts/fix_webview.sh`.

### B. Keyboard Shortcut Conflicts

- **Cause**: ChromeOS system shortcuts (Screenshot, etc.) are blocked by scan-code dispatch.
- **Fix**: Force key-code dispatch.
- **Config**: Ensure `"keyboard.dispatch": "keyCode"` is in `~/.config/Antigravity/User/settings.json`.
- **Script**: `~/github/tariqk00/toolbox/scripts/fix_shortcuts.sh`.

## 4. Automation Rules

- **NEVER** enable systemd timers or cron jobs on this container (Chromebook).
- Automation is strictly for the NUC (`nuc8i5-2020`).
