# Capture a new safe export (read-only against live files)

```bash
cd /tmp   # any neutral dir
~/.hermes/hermes-agent/venv/bin/python -I \
  ~/nextjs/stark-ai-workbench-cyberlorean-workforce-v1/scripts/preservation/capture_safe_export.py
# -> ~/web-factory/preservation/workforce-safe-export-<YYYYMMDD-HHMM>/   (refuses an existing folder)

E=~/web-factory/preservation/workforce-safe-export-<stamp>
~/.hermes/hermes-agent/venv/bin/python -I \
  ~/nextjs/stark-ai-workbench-cyberlorean-workforce-v1/scripts/preservation/scan_for_secrets.py "$E"   # must print RESULT: CLEAN
(cd "$E" && sha256sum -c SHA256SUMS --quiet && echo CHECKSUMS_OK)
```

What it captures: see `README.md`. What it never reads into the export: `.env` values (only names, plus the
non-secret settings listed in `ENV_KEEP`), `auth.json`, databases, sessions, memories, logs, caches.
The capture aborts if a `config.yaml` value looks secret, if a curated tree contains a symlink, or if the
shared starter pack differs between profiles.

To refresh this repo from a new export: diff it against the repo (`diff -r "$E" <repo>` ignoring `.git`, docs),
copy changed files over deliberately, re-run the scanner on the repo, then hand the Director the commit block.
The scanner loads secret values from the live stores into memory and reports only file + variable name.
