# Future Projects

Backlog of projects to explore or implement.

---

## Moltbot (AI Personal Assistant)

**Added:** 2026-01-28  
**Status:** Backlog  
**Priority:** Medium

**What:** Self-hosted AI assistant that bridges LLMs (Claude, OpenAI, Gemini via OpenRouter) to messaging platforms (WhatsApp, Telegram, Discord, Slack).

**Why:** Always-on AI sidekick with persistent memory, proactive notifications, and autonomous task execution.

**Resources:**

- GitHub: [moltbot/moltbot](https://github.com/moltbot/moltbot) (~88k ⭐)
- Docs: [docs.clawd.bot](https://docs.clawd.bot)
- Install: `curl -fsSL https://molt.bot/install.sh | bash`

**Notes:**

- Native Gemini support pending; works via OpenRouter today
- Try on Chromebook first, then consider Docker on NUC for prod
- Security: Run `moltbot security audit --deep` before exposing

---

## Anova Oven Voice Control

**Added:** 2026-01-28  
**Status:** Backlog  
**Priority:** Medium

**What:** Control Anova Precision Oven via Google Assistant using n8n + Google Apps Script.

**Architecture:**

```
"Hey Google, preheat oven" → Google Home Routine → Apps Script → n8n Webhook → anova.py → Oven
```

**Resources:**

- Skill: [dodeja/anova-skill](https://github.com/dodeja/anova-skill)
- Requires: Anova token from app (More → Developer → Personal Access Tokens)

**Steps:**

1. Clone `anova-skill` on NUC, set up venv + token
2. Create n8n workflow with webhook + Execute Command node
3. Deploy Google Apps Script web app to call n8n webhook
4. Configure Google Home routines to invoke Apps Script

**Notes:**

- Cloudflare tunnel already configured for n8n
- Start with "preheat to X°F", expand to sous vide, stop, etc.
