# Workforce preservation — Phase A/B evidence (2026-11-04)

Seat: Claudy (local). Captured 2026-11-04 17:32:51 +06 (11:32:51 UTC) on Zorin OS 18.1, Linux 7.0.0-31 x86_64, user `moose`, HOME `/home/moose`.
All inspection read-only. No upgrades, deletions, resets, restarts or live-file edits. No git mutations by the agent.

## Discovery
- **Workforce repo (first found):** `~/python/stark-ai-workbench-cyberlorean-workforce-v1`, remote `github.com/ahmedmusawir/stark-ai-workbench-cyberlorean-workforce-v1`,
  local `main` = local `origin/main` = `452925e` (Initial commit, README only), clean before this work. **Correction 18:15:** the local remote-tracking ref was stale; `git ls-remote` shows GitHub `main` at `2f1ef9d` (2026-10-01 "docs(p2a): bank recon report and session checkpoint", 2 files under `agent_docs/RESPONSES/` and `agent_docs/SESSIONS/`, no path overlap). The push needs `git pull --ff-only` first. Repo is public (anonymous API 200).
- **Hermes:** `~/.local/bin/hermes` wrapper → `~/.hermes/hermes-agent` (git install), Hermes Agent v0.20.5 (2026.8.19), HEAD `4c1f53be`
  (present upstream; API 200), venv Python 3.11.16. Local tracked changes: 4 files in the A2A plugin and its tests (operator-console frame,
  `lastChunk` persistence) — captured as `hermes-patches/a2a-operator-console-and-lastchunk.patch`. No untracked files.
- **Profiles:** five Web profiles, ports read from each `.env` (`A2A_PORT`) and confirmed against listeners: 9911 Architect, 9912 Designer,
  9913 Developer, 9915 DevOps listening; **9914 QA not listening at capture** (gateway down). Details: `config/ROLE_MAP.md`, `manifests/roles.json`.
- **Services:** none for Hermes/ADK/Bob (no systemd user/system units, no crontab, profile cron jobs empty). Workers run in foreground
  terminals via `~/.hermes/scripts/start_*.sh`. `ollama.service` (system) is active.
- **Bridge:** ADK `api_server` 127.0.0.1:8000 from `~/python/stark-ai-workbench-adk-backend-v1` (main `6b0f5d3`, pushed; web apps tracked);
  Bob = `~/nextjs/stark-ai-workbench-nextjs-frontend-v1` (`next-server v16.3.3` on :3000; main `466083f` pushed, 26 files uncommitted incl. all web-agent wiring).
  The `adk` peer token in all five profiles equals ADK `HERMES_A2A_TOKEN` (compared in memory, not printed).
- **Skills:** per profile, every skill dir compared file-by-file (sha256) with the pinned Hermes `skills/` and `optional-skills/`.
  82 identical upstream skills each (QA 83 with optional `dogfood/adversarial-ux-test`), plus exactly one custom skill per role (exported).
- **Instructions:** `SOUL.md` + `workspace/.hermes.md` + `workspace/context/WEB_FACTORY_STARTER_v1_1/`. The starter README and constitution are
  byte-identical across all five; stored once in `shared/`. External reference: `~/web-factory/projects/cyberize-poc/PROJECT_GUIDE.md` (project data, not exported).
- **Symlinks:** only under `<profile>/lsp/` (regenerable language-server bins); none in curated content (capture aborts on any).

## Export
- Path: `~/web-factory/preservation/workforce-safe-export-20261104-1732/` — 99 files, 1.3 MB; manifest `manifests/manifest.tsv`
  (relpath, size, mode, sha256, source, restore_target, kind) and `SHA256SUMS`. Copied into this repo with `--ignore-existing`
  (no collisions); `sha256sum -c SHA256SUMS` passes at the repo root.
- Config: `config.yaml` → `config.template.yaml` after a gate that refuses secret-looking values (none found; credentials are not in config).
  `.env` → `env.template`: 17 settings keep values; `OLLAMA_API_KEY`, `A2A_PEER_TOKENS`, `ANTHROPIC_API_KEY` blank.

## Secret review
- `scripts/preservation/scan_for_secrets.py` loads 23 secret values from the live stores (5 profile `.env` + `auth.json`, Hermes home `.env`/`auth.json`,
  ADK `.env` + service-account JSON, Bob `.env.local`) and checks exact matches, plus token/key patterns and an e-mail inventory.
- Positive control: run against a live profile folder it flags `auth.json` and an `.env` backup (exit 1).
- Export: `RESULT: CLEAN`, no e-mail addresses, no cloud project IDs, run.app URLs or non-loopback IPs. Repo tree: see final scan below.
- Public-exposure note: content names the company (Cyberize) and local paths under `/home/moose`; role prompts and playbooks become public with the repo.

## Not done / open
- Commit and push: prepared, not executed (Director-owned git mutation). Command block in the chat checkpoint.
- Private encrypted machine backup (sessions, memories, credentials): does not exist; needs destination and key decision.
- Restore proof on an isolated target: Phase C/D.

## Final repo review (pending, unstaged)
- 112 files pending (`git status --porcelain --untracked-files=all`): 1 modified (`README.md`), 111 new. No `.env`, `auth.json`, `*.db`, memory, session or log paths.
- `scan_for_secrets.py <repo>` → `RESULT: CLEAN` (22 live secret values checked; `GOOGLE_APPLICATION_CREDENTIALS` reclassified as a path setting
  after it flagged the documented file *name*; the service-account file *contents* remain checked). Positive control still exits 1.
- `sha256sum -c SHA256SUMS` passes at the repo root. Largest file < 500 KB; total 1.4 MB.

## Post-push check (2026-11-04 18:15)
- The pasted hash `3549717` is in the **frontend** repo (`stark-ai-workbench-nextjs-frontend-v1`), parent `466083f`, now GitHub `main`. It committed that repo's 26 pending files (the Bob web-agent wiring) under the workforce commit message. Leak scan of all 26 committed files: CLEAN (only `test@example.com` in a test).
- The workforce repo is unchanged: no new commit, 14 pending entries, GitHub `main` still `2f1ef9d`. The workforce baseline is **not yet pushed**.
- Recommendation: leave the frontend commit as is (rewording would need a force-push); note the mislabel here.

## Reconciliation into the confirmed destination (2026-11-04 18:2x)
- Tony confirmed `~/nextjs/stark-ai-workbench-cyberlorean-workforce-v1` as the destination. It and `~/python/stark-ai-workbench-cyberlorean-workforce-v1` are **separate clones** (different inodes, no symlink, each its own git root) of the same remote `github.com/ahmedmusawir/stark-ai-workbench-cyberlorean-workforce-v1`.
- `~/nextjs` clone: `main` @ `2f1ef9d` = GitHub `main` (`git ls-remote`), clean; files `README.md` and two `agent_docs/` reports. `~/python` clone: stale at `452925e`, holds the prepared work (left in place, unchanged).
- Copied the 111 new files with `rsync -a --ignore-existing` (modes and mtimes kept; no collisions) and replaced `README.md`, which was byte-identical to the original two-line README that the new one keeps verbatim at the top. Existing `agent_docs/` files untouched.
- Path references in `runbooks/PRESERVATION_CAPTURE.md` updated to the `~/nextjs` location.
- Services: none exist on the live machine (Hermes, ADK and Bob run in foreground terminals); the start/stop/verify scripts are the service layer. No unit template was invented; an optional autostart template belongs to the guided startup phase.
- Preparation runbooks: historical fleet startup runbooks v1.0/v1.1 in `runbooks/historical/`; the multi-profile A2A/ADK runbook stays in the ADK repo (`docs/HERMES_MULTI_PROFILE_A2A_ADK_RUNBOOK_v1.0 (1).md`, tracked and pushed).
