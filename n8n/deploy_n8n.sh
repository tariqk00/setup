#!/bin/bash
# deploy_n8n.sh
# Push current local workflow to the NUC and import it.

HOST="${1:-nuc}"
REMOTE_USER="tariqk"
LOCAL_FILE="setup/n8n/plaud_workflow_v5.json"
REMOTE_TEMP="/home/tariqk/plaud_workflow_v5.json"

echo "🚀 Deploying $LOCAL_FILE to $REMOTE_USER@$HOST..."

# 1. Copy file to host
scp "$LOCAL_FILE" "$REMOTE_USER@$HOST:$REMOTE_TEMP"

# 2. Import (Overwriting existing if same ID, or creating new)
# Note: We moved the file to the volume mapped folder /DATA/AppData -> /home/node/.n8n
echo "📦 Importing into n8n..."
# Move file to volume directory first
ssh "$REMOTE_USER@$HOST" "sudo mv $REMOTE_TEMP /DATA/AppData/plaud_workflow_v5.json && sudo chown 1000:1000 /DATA/AppData/plaud_workflow_v5.json"
# Run import using internal path
ssh "$REMOTE_USER@$HOST" "sudo docker exec -u node n8n n8n import:workflow --input=/home/node/.n8n/plaud_workflow_v5.json"

echo "✅ Deployment finished."
echo "   Please refresh your n8n UI (https://n8n.takhan.com or local) to see changes."
