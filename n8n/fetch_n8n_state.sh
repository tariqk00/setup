#!/bin/bash
# fetch_n8n_state.sh
# Connects to NUC, exports n8n workflows, and copies them local for analysis.

# Default to 'nuc', but allow override via argument (e.g. ./fetch_n8n_state.sh 172.30.0.169)
HOST="${1:-nuc}"
REMOTE_FILE="/DATA/AppData/export.json"
REMOTE_USER="tariqk"
LOCAL_DIR="./debug_n8n"

echo "🔌 Connecting to $REMOTE_USER@$HOST to export workflows..."

# 1. Run export inside the docker container
ssh "$REMOTE_USER@$HOST" "sudo docker exec -u node n8n n8n export:workflow --all --output=/home/node/.n8n/export.json"

# 2. Move it out of the volume mapping (Assuming ~/.n8n is mapped to /home/node/.n8n)
# Check ENV_SETUP for volume mapping: "-v ~/.n8n:/home/node/.n8n"
# So it should be in ~/.n8n/export.json on the host.

# 3. Download
mkdir -p "$LOCAL_DIR"
echo "⬇️  Downloading to $LOCAL_DIR..."
scp "$REMOTE_USER@$HOST:$REMOTE_FILE" "$LOCAL_DIR/current_workflows.json"

echo "✅ Done. Check $LOCAL_DIR/current_workflows.json"
