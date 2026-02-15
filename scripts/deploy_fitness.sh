#!/bin/bash
# NUC Deployment Script for Fitness Automation services

set -e

SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"

echo "=== Deploying Fitness Services to NUC ==="

# Link service files
echo "Linking service files..."
ln -sf "$HOME/github/tariqk00/setup/services/garmin-sync.service" "$SERVICE_DIR/"
ln -sf "$HOME/github/tariqk00/setup/services/garmin-sync.timer" "$SERVICE_DIR/"
ln -sf "$HOME/github/tariqk00/setup/services/trainheroic-extract.service" "$SERVICE_DIR/"
ln -sf "$HOME/github/tariqk00/setup/services/trainheroic-extract.timer" "$SERVICE_DIR/"

# Reload daemon
echo "Reloading systemd daemon..."
systemctl --user daemon-reload

# Enable and start timers
echo "Enabling timers..."
systemctl --user enable --now garmin-sync.timer
systemctl --user enable --now trainheroic-extract.timer

# Verify
echo "=== Deployment Complete ==="
echo "Status of timers:"
systemctl --user list-timers --all | grep -E 'garmin|trainheroic'
