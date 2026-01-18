#!/bin/bash
# setup_ssh_config.sh
# Adds the NUC keys and config to ~/.ssh/config for passwordless access.

SSH_DIR="$HOME/.ssh"
CONFIG_FILE="$SSH_DIR/config"
NUC_IP="172.30.0.169"
NUC_USER="tariqk"
NUC_ALIAS="nuc"

echo "🔧 Configuring SSH for $NUC_ALIAS ($NUC_IP)..."

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

if ! grep -q "Host $NUC_ALIAS" "$CONFIG_FILE" 2>/dev/null; then
    cat <<EOF >> "$CONFIG_FILE"

Host $NUC_ALIAS
    HostName $NUC_IP
    User $NUC_USER
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
EOF
    echo "✅ Added 'nuc' alias to $CONFIG_FILE"
else
    echo "ℹ️  'nuc' alias already exists in $CONFIG_FILE"
fi

# Ensure permissions
chmod 600 "$CONFIG_FILE"

echo "🧪 Testing connection..."
ssh -o BatchMode=yes -o ConnectTimeout=5 $NUC_ALIAS "echo '✅ Connection Successful: \$(hostname)'" || echo "❌ Passwordless login failed. You may need to run: ssh-copy-id $NUC_ALIAS"
