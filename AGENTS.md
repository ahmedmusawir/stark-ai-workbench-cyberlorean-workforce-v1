# Cyberlorean Workforce — agent entry (AGENTS.md ≡ CLAUDE.md)

This repo is the **safe, sanitized baseline** of the five-role Stark Web Factory workforce running on Hermes Agent.
It contains no credentials, sessions, memories or logs. It is the source of truth for role definitions; the live
copies are deployed into `~/.hermes/profiles/<profile_id>/` (see `manifests/manifest.tsv`, column `restore_target`).

## Read order
1. `README.md` — what this is, layout, shortest path.
2. `config/ROLE_MAP.md` — role → profile ID → port → model/provider → ADK app.
3. `manifests/OUTSIDE_GIT.md` — what recovery still needs from outside this repo.
4. `config/CREDENTIALS.md` — secret NAMES and how the operator re-enters them.
5. `runbooks/` — capture, restore outline (unproven), historical startup runbooks.
6. `agent_docs/RESPONSES/` — evidence reports.

## Rules
- Never commit a filled `.env`, `auth.json`, `*.db`, session, memory or log file. Templates only (`env.template`, `config.template.yaml`).
- Before any commit, run `scripts/preservation/scan_for_secrets.py <repo>`; it must print `RESULT: CLEAN`.
- Git mutation (add/commit/push) belongs to the Director (Tony). Agents prepare changes and hand over the command block.
- Do not start, stop or restart live workers as part of preservation. Starting workers is a separate, explicit request.
- Do not edit the live profiles from this repo without a diff/backup step; re-capture first (`runbooks/PRESERVATION_CAPTURE.md`).
- Shared starter pack lives once in `shared/WEB_FACTORY_STARTER_v1_1/`; each profile receives `README.md`, `CONSTITUTION/` and its own role folder (`manifests/roles.json` → `starter_parts`).
