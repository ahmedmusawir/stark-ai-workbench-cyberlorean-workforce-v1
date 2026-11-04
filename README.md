# stark-ai-workbench-cyberlorean-workforce-v1
This is where Hermes becomes Cyberloreans

## What is here
The preserved, secret-free baseline of the five Web Factory roles (Hermes Agent profiles) as captured on
2026-11-04 17:32 (Asia/Dhaka) from the working VM, plus the tooling that captured and checked it.

| Path | Contents |
|---|---|
| `profiles/<profile_id>/` | `SOUL.md`, `profile.yaml`, `workspace/.hermes.md`, custom skill, profile scripts, `config.template.yaml`, `env.template` |
| `shared/WEB_FACTORY_STARTER_v1_1/` | Constitution (WBM playbook) + per-role instructions and playbooks (one copy, deployed to each profile's `workspace/context/`) |
| `scripts/hermes-utils/` | Maintained `~/.hermes/scripts` (start/stop/verify/model-change/contest checks), modes preserved |
| `scripts/bin/hermes` | The `~/.local/bin/hermes` launcher wrapper |
| `scripts/preservation/` | `capture_safe_export.py` (re-capture) and `scan_for_secrets.py` (leak gate) |
| `hermes-patches/` | Local Hermes A2A plugin modification as a patch against upstream base `4c1f53be` |
| `bridge/bob/` | Snapshot of the Workbench (Bob) web-agent manifest entries — reference only |
| `config/` | Role map and credential names |
| `manifests/` | `versions.json`, `roles.json`, `env-variable-names.json`, `manifest.tsv` (size/mode/sha256/source/target), `OUTSIDE_GIT.md` |
| `runbooks/` | Capture procedure, restore outline (UNTESTED), historical startup runbooks v1.0/v1.1 |
| `SHA256SUMS` | Checksums of every captured file (`sha256sum -c SHA256SUMS` from the repo root) |

## Shortest path
- Verify this baseline: `sha256sum -c SHA256SUMS && python3 -I scripts/preservation/scan_for_secrets.py .`
- Re-capture after live changes: see `runbooks/PRESERVATION_CAPTURE.md`.
- Recover on a new machine: `runbooks/RESTORE_OUTLINE_UNTESTED.md` (guided recovery workflow is the next phase).
