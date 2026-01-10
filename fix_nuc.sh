#!/bin/bash

# Configuration
# Assumes standard layout: ~/github/tariqk00/{setup,plaud,toolbox}
BASE_DIR="$HOME/github/tariqk00"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting NUC Cronjob Fixer (User: $USER)...${NC}"

# Function to pull repo
update_repo() {
    local repo_name=$1
    echo -e "\n${GREEN}Updating $repo_name...${NC}"
    if [ -d "$BASE_DIR/$repo_name" ]; then
        cd "$BASE_DIR/$repo_name" && git pull
    else
        echo -e "${RED}Warning: $repo_name not found!${NC}"
    fi
}

# 1. Update Code (All Repos)
echo -e "\n${GREEN}[1/5] Pulling latest code...${NC}"
update_repo "setup"
update_repo "plaud"
update_repo "toolbox"

# 2. Refresh Tokens
echo -e "\n${GREEN}[2/5] Refreshing Authentication Tokens...${NC}"
echo "You will need to copy/paste URLs to your browser."
cd "$BASE_DIR/setup" || exit 1
python3 refresh_all_tokens.py

if [ $? -ne 0 ]; then
    echo -e "${RED}Token refresh script failed.${NC}"
    exit 1
fi

# 3. Install & Patch Service Files
echo -e "\n${GREEN}[3/5] Updating & Patching Service Definitions...${NC}"
mkdir -p "$USER_SYSTEMD_DIR"

install_service() {
    local src=$1
    local name=$2
    local dest_service="$USER_SYSTEMD_DIR/$name.service"
    local dest_timer="$USER_SYSTEMD_DIR/$name.timer"

    if [ -f "$src.service" ]; then
        echo "Installing $name..."
        # Copy file to allow editing (don't symlink)
        cp "$src.service" "$dest_service"
        cp "$src.timer" "$dest_timer"

        # PATCH: Replace hardcoded /home/takhan with current $HOME
        # Also replace %h if it exists, just to be safe and explicit
        sed -i "s|/home/takhan|$HOME|g" "$dest_service"
        sed -i "s|%h|$HOME|g" "$dest_service"
        
        echo "  -> Patched paths to: $HOME"
    else
        echo "  -> Warning: Source for $name not found at $src.service"
    fi
}

# Install Plaud
install_service "$BASE_DIR/plaud/plaud-automation" "plaud-automation"

# Install AI Sorter
install_service "$BASE_DIR/toolbox/google-drive/ai-sorter" "ai-sorter"


# 4. Systemd Configuration
echo -e "\n${GREEN}[4/5] Configuring Systemd Timers...${NC}"

# Reload to pick up changes
systemctl --user daemon-reload

# Enable AI Sorter
echo "Enabling ai-sorter.timer..."
systemctl --user enable ai-sorter.timer
systemctl --user start ai-sorter.timer

# Restart Plaud Automation
echo "Restarting plaud-automation.timer..."
systemctl --user restart plaud-automation.timer

# 5. Status Check
echo -e "\n${GREEN}[5/5] Verifying Status...${NC}"
systemctl --user list-timers --no-pager | grep -E "plaud|ai-sorter"

echo -e "\n${GREEN}Done!${NC}"
echo "Check logs with:"
echo "  journalctl --user -u plaud-automation -n 50"
echo "  journalctl --user -u ai-sorter -n 50"
