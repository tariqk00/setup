# Setup & Infrastructure Tasks

## Operations & Reliability

- [x] [Ops] Deep Analysis & RCA of Jan 13 Freeze (See `docs/RCA_2026_01_13_Freeze.md`)
- [x] [Ops] Remediate NUC Stability (Kernel Fix + Remove GUI)
- [x] [Ops] Verify Server Uptime (Found: Frozen 14hr before power loss; Watchdog failed)
- [x] [Ops] Check `cloudflared` tunnel status and health
- [ ] [Ops] Verify `n8n` container health and resource usage

## Configuration & Backups

- [ ] [Config] Create automated backup for `n8n` workflows
- [x] [Config] Audit `cron` vs `systemd` timers (Fixed: Enabled Linger for `tariqk`)

## Documentation

- [ ] [Docs] Update `server_history_log.md` (Remove outdated storage expansion recommendation)
- [ ] [Docs] Document `cloudflared` setup in `README.md` details
