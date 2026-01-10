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

# 3. Link Service Files (Ensure we use the repository versions)
echo -e "\n${GREEN}[3/5] Updating Service Definitions...${NC}"
mkdir -p "$USER_SYSTEMD_DIR"

# Link Plaud
if [ -f "$BASE_DIR/plaud/plaud-automation.service" ]; then
    ln -sf "$BASE_DIR/plaud/plaud-automation.service" "$USER_SYSTEMD_DIR/plaud-automation.service"
    ln -sf "$BASE_DIR/plaud/plaud-automation.timer" "$USER_SYSTEMD_DIR/plaud-automation.timer"
fi

# Link AI Sorter
if [ -f "$BASE_DIR/toolbox/google-drive/ai-sorter.service" ]; then
    ln -sf "$BASE_DIR/toolbox/google-drive/ai-sorter.service" "$USER_SYSTEMD_DIR/ai-sorter.service"
    ln -sf "$BASE_DIR/toolbox/google-drive/ai-sorter.timer" "$USER_SYSTEMD_DIR/ai-sorter.timer"
fi

echo "Service files linked from repository."

# 4. Systemd Configuration
echo -e "\n${GREEN}[4/5] Configuring Systemd Timers...${NC}"

# Reload to pick up changes/links
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
