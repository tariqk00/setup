# Automation Run Notifications

> **Status**: Planned  
> **Created**: 2026-01-25

## Goal

Send run status notifications (success/failure, execution time, errors) to Google Chat for all automations running on the NUC.

---

## Proposed Changes

### Google Chat Webhook

Already created: `https://chat.googleapis.com/v1/spaces/AAQAwBUX5QU/messages?key=...&token=...`

Target: "Automations" space (`tariq@techs4good.org`)

---

### n8n Workflows

For each active workflow, add notification nodes:

#### [MODIFY] Readwise Daily Digest v3

- Add `Error Trigger` node to catch failures
- Add success webhook POST at end of flow
- Message format:
  ```
  ✅ Readwise Daily Digest - Success
  📊 3 articles processed
  ⏱️ 12.3s execution time
  ```

#### [MODIFY] Plaud Emails to Drive

- Same pattern: Error Trigger + success POST

#### [MODIFY] Gemini Journal to Drive

- Same pattern

---

### systemd Timers

Add notification scripts to service files:

#### [MODIFY] `~/.config/systemd/user/ai-sorter.service`

```ini
[Service]
# ... existing config ...
ExecStartPost=/home/tariqk/github/tariqk00/toolbox/scripts/notify-chat.sh "ai-sorter" "success"
ExecStopPost=/bin/sh -c 'if [ "$$SERVICE_RESULT" != "success" ]; then /home/tariqk/github/tariqk00/toolbox/scripts/notify-chat.sh "ai-sorter" "failure"; fi'
```

#### [MODIFY] `~/.config/systemd/user/plaud-automation.service`

- Same pattern

#### [NEW] `toolbox/scripts/notify-chat.sh`

```bash
#!/bin/bash
SERVICE_NAME="$1"
STATUS="$2"
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQAwBUX5QU/messages?key=...&token=..."

if [ "$STATUS" = "success" ]; then
  EMOJI="✅"
else
  EMOJI="❌"
fi

curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$EMOJI $SERVICE_NAME - $STATUS\nTime: $(date)\"}"
```

---

## Verification Plan

1. **n8n workflows**: Trigger each workflow manually, verify Chat notification
2. **systemd timers**: Run `systemctl --user start <service>`, verify Chat notification
3. **Failure test**: Intentionally break a service, verify failure notification

---

## Message Format

| Status  | Format                                             |
| ------- | -------------------------------------------------- |
| Success | `✅ [Name] - Success\n⏱️ [duration]\n📊 [summary]` |
| Failure | `❌ [Name] - FAILED\n🔴 [error message]`           |
