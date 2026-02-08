#!/bin/bash

# Configuration
REPO_DIR="$HOME/github/tariqk00/setup"
BACKUP_DIR="$REPO_DIR/n8n/backups"
EXPORT_FILE="workflows.json"
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# 1. Export workflows from Docker container
echo "Exporting n8n workflows..."
# Note: /home/node/.n8n is mounted to /DATA/AppData on host.
# We can use the CLI inside the container.
docker exec -u node n8n n8n export:workflow --all --output=/home/node/.n8n/workflows_export.json

# 2. Copy from host mount to repo
# /DATA/AppData is where the container writes.
cp /DATA/AppData/workflows_export.json "$BACKUP_DIR/$EXPORT_FILE"

# 3. Git Commit (Local Only)
cd "$REPO_DIR"

if [[ -n $(git status --porcelain "$BACKUP_DIR/$EXPORT_FILE") ]]; then
    echo "Changes detected. Committing..."
    git add "$BACKUP_DIR/$EXPORT_FILE"
    git commit -m "backup(n8n): daily workflow export $DATE"
    echo "Backup committed successfully."
else
    echo "No changes detected. Skipping commit."
fi

# 4. Optional: Copy to external backup location (e.g. for Drive sync)
# mkdir -p ~/google-drive/backups/n8n
# cp "$BACKUP_DIR/$EXPORT_FILE" ~/google-drive/backups/n8n/
