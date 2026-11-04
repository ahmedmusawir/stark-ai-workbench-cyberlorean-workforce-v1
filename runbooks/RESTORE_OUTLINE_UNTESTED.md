# Restore outline — UNTESTED (the guided, proven workflow is the next phase)

1. Prerequisites: Linux user with `$HOME`, git, Python 3.11, Node ≥ 22, Ollama (`ollama signin`), optional gcloud.
2. Hermes: install upstream `NousResearch/hermes-agent` by its supported git method, check out
   `4c1f53be10d0fce1d25aee1975e5149b6c54f25a`, then `git apply hermes-patches/a2a-operator-console-and-lastchunk.patch`
   and run `tests/plugins/test_a2a_plugin.py` (114 passed at capture).
3. Profiles: `hermes profile create <id>` for each of the five (or let Hermes create the folder), then place files per
   `manifests/manifest.tsv` → `restore_target`: SOUL.md, profile.yaml, workspace/.hermes.md, custom skill, scripts,
   `shared/WEB_FACTORY_STARTER_v1_1/{README.md,CONSTITUTION,<ROLE>_AGENT}` → `workspace/context/WEB_FACTORY_STARTER_v1_1/`.
   `config.template.yaml` → `config.yaml` (remap `/home/moose` if HOME differs); `env.template` → `.env` (mode 600) and fill secrets.
   Confirm the upstream skills listed in `manifests/roles.json` exist; install QA's optional `dogfood/adversarial-ux-test`.
4. Credentials: `config/CREDENTIALS.md` (Codex OAuth per profile, shared A2A token on both sides).
5. Utilities: `scripts/hermes-utils/*` → `~/.hermes/scripts/` (keep modes); `scripts/bin/hermes` → `~/.local/bin/hermes`.
6. Bridge: ADK repo at `6b0f5d3` (+ `.env`), Bob frontend with the web-agent wiring (see `manifests/OUTSIDE_GIT.md`).
7. Start only on request: `~/.hermes/scripts/start_<id>.sh`, then `verify_web_gateways_after_restart.sh`.
