---
name: cloud-deploy-prep
description: Use when preparing an authorized cloud deployment.
version: 1.0.0
author: web_devops_agent
license: MIT
metadata:
  hermes:
    tags: [deployment, cloud-run, devops, release-management, packaging]
    related_skills: [github-repo-management, plan, hermes-agent-skill-authoring]
---

# Cloud Deployment Preparation

## When to Use

- A website or app must be prepared for a platform deployment (e.g. Cloud Run) that requires an explicit release decision before any cloud write.
- You are resuming or reviewing deployment preparation (staging dirs, overlays, run records) left by an earlier session.
- You must verify whether a candidate is actually accepted before packaging it: certifications, repair commits, retests, POC exceptions.
- A repo must be packaged for a container build (Dockerfile, ignores, upload tree, inventory) without touching the product tree.
- An approval harness has blocked a deployment-prep command and you need the compliant recovery pattern.

Preparing a site/application deployment that requires an explicit release — e.g. Cloud Run for a Next.js site under a role-gated workflow (QA certification → Director release → DevOps execution). This skill covers the DevOps preparation lane: everything up to the authorized cloud write, plus honest handling of blocks.

If the project has its own deploy skill inside the repo (e.g. `agent_docs/SKILLS/*/CLAUDE.md`), that skill is the **governing procedure** and is user/project-owned — follow it, never edit it from the agent library. This skill adds operational patterns learned in execution that such procedures state only abstractly.

## 1. Intake and source identity

- Pin the candidate: full SHA, branch, `git status --porcelain` (record untracked skill folders separately), and remote match via `git ls-remote origin refs/heads/<branch>`. Never deploy "latest".
- Verify secret-free mode with evidence, not file absence: grep source trees for `process.env`, find `.env*`, check for remote fonts/images/backends. A repo with no env files but env reads in source is NOT secret-free.
- Check tooling in YOUR runtime (`command -v gcloud docker`, node/npm versions). Missing binaries are reported facts for the plan, never constraints; record local checks you cannot run as **NOT RUN** and require their cloud equivalents later.

## 2. Verify the acceptance chain — verdicts name candidates, not intentions

A certification binds to ONE candidate (SHA ± working-tree fingerprint). Deploy HEAD is frequently a commit LATER (repair commits). The chain is complete only when every link is evidenced:

**certified SHA → verdict → (if FAIL) repair ruling → repair commit → successor retest on the NEW SHA → release authorization**

- **FAIL + repair commit ≠ accepted.** A FAIL verdict followed by a Director-authorized repair commit does not make the candidate deployable. The targeted retest on the successor SHA — or an explicitly recorded Director POC exception naming that candidate — is a separate required link. Its absence is a GAP reported as a release input. DevOps does not investigate, run QA, or relabel anything.
- A newer commit on top of a certified SHA invalidates the certificate's applicability until a retest or impact review covers the diff. Diff the two SHAs yourself and confirm the changes are inside the repair's authorized scope (e.g. only the named literals, only the named files).
- Certification may live outside the repo (project WBM/QAM dirs, ZIPs with sidecar `.sha256` + verification JSON). Verify the sidecar hash before trusting the archive; the verification JSON inside may describe a PRE-repair state — read it as history, not current verdict.
- Record the disposition in an intake config (YAML) with `acceptance.kind` left **blank** until a valid kind is evidenced; the deploy script must fail closed on blank.

Worked example: `references/acceptance-chain-case-notes.md`.

## 3. Staging outside the checkout

- One new dated directory per run, OUTSIDE the repo. Preserve earlier attempts: no deletion, no `rsync --delete`, no optional cleanup bundled in.
- Assemble from the committed tree only: `git archive <pinned-SHA> | tar -x -C staging/upload`. Never copy the working directory — untracked files, secrets, `.env`, and build output ride along.
- Fail closed if the target upload dir is already non-empty (no-overwrite policy).
- Apply explicit exclusions AFTER extraction (`QAM/`, `agent_docs/`, tests, reports), keep font/artwork licenses, then emit a sha256-per-file inventory with sorted relative paths; the inventory hash is part of the package identity.
- Put an assembly script in staging (reviewable, re-runnable) rather than one-shot shell: it re-verifies pinned SHA and clean worktree before extracting.

## 4. Packaging overlays need explicit authorization

If the repo has NO `next.config.*` and standalone output is required by the container contract, the config addition is a product-tree change with two acceptable paths:

- **Path A (preferred):** Director commits a minimal `next.config.ts` (containing `output: "standalone"` and nothing else) to the repo; source identity is then the successor commit SHA alone.
- **Path B:** Director explicitly approves a hashed overlay kept in staging, copied into the upload tree by the assembly script; identity = candidate SHA + overlay SHA-256.

Either way, write an overlay manifest (content, hash, authorization status, excluded alternatives), and make the assembly script fail if a `next.config.*` already exists — an overlay over an existing config is not minimal. Starter file: `templates/overlay-next-config.ts`.

## 5. Pin container images to verified digests (works without docker)

Never build from a floating tag. With docker absent you can still verify a digest live from the registry API:

```sh
curl -fsS https://hub.docker.com/v2/repositories/library/node/tags/22-slim
# → JSON with "digest" (sha256) and "tag_last_pushed"
```

Record the verified digest and check time in the run record; pin tag AND digest in the Dockerfile:

```dockerfile
ARG NODE_IMAGE=docker.io/library/node:22-slim@sha256:<verified-digest>
```

Check the image's Node satisfies BOTH `package.json` engines and the framework's own engines (they can differ; e.g. app demands ≥22 while the framework demands ≥20.9). Same image for deps, build and runner stages; non-root user; `HOSTNAME=0.0.0.0`; listen on the platform's port.

## 6. Fail-closed execution scripts

Generate reviewable scripts driven by the intake YAML (parse with a real YAML library in a helper function; never `eval`):

- Blank required config → non-zero exit with the missing key named. Never a guessed default.
- Re-verify pinned SHA, clean tracked worktree, and active cloud account == expected account before any submission.
- Deploy by immutable digest resolved from the build's structured results — validate `^sha256:[0-9a-f]{64}$` and the repository path — never `latest`.
- Split execution: submit build (async) → capture BUILD_ID → second stage resolves digest → deploys the digest with explicit project/region/service/SA/port/memory/limits/access → writes readback files (service YAML, URL, revision+traffic table, IAM policy).
- A deploy without readback files is incomplete. Read scripts fully before proposing anyone run them; `bash -n` and YAML-parse everything before execution.

## 7. When the approval harness blocks a command mid-prep

If a command is denied with a do-NOT-retry / timed-out-without-consent instruction, comply exactly: no retry, no rephrase, no same outcome via a different tool. Then:

1. Append a row to the staging `ISSUES.md` ledger (observation, cause, remedy, outcome) — append-only.
2. Convert the blocked operation into a reviewable script in staging (same steps, parameterized) so a consented run — by the user or a later approved session — executes exactly what was reviewed.
3. Continue every part of preparation that does not depend on the blocked outcome (file generation, records, plans, checklists).
4. End the turn with ALL missing inputs batched: decisions, cloud values, and explicit consent to run the prepared scripts.

Never claim a blocked step ran. Mark it PENDING in records and checklists; do not describe the prepared-but-unexecuted scripts as a validated workflow.

## 8. First deployment has no rollback — record a withdrawal procedure

For a service with no prior revision, write the withdrawal procedure BEFORE any traffic: ingress restriction vs service deletion have different blast radii; the Director chooses, DevOps never executes either by default. Record what a rollback would not undo (external effects, submissions, published content). Once a prior revision exists, capture its name and full traffic allocation and produce exact traffic-shift commands from those observed values.

## Pitfalls

| Pitfall | Fix |
|---|---|
| Harness block on a whole batch → silent hole in verification | Convert each blocked batch into a reviewable script with the same steps; run under consent later; ledger in ISSUES.md |
| Google API 429 (RESOURCE_EXHAUSTED, per-minute quota) during prerequisite reads | Wait out the ~60s window once (sleep ~80s), rerun the SAME script; do not hammer, do not request quota changes |
| New Cloud Run domain mapping: mapping API says Ready/CertificateProvisioned=True but TLS resets at Google's edge worldwide | Managed-cert edge rollout lags ~15–60 min after the DNS record exists; HTTP:80 redirects early. Diagnose via port-80 302 + sibling-mapping control + global vantage (check-host.net); report PENDING with bounded watch, never as a deploy defect and never with curl -k |
| `gcloud beta run domain-mappings describe <domain>` positional arg fails | Pass the domain with `--domain <name>`, not positionally (create accepts positional; describe does not) |
| First content-grep smoke FALSE-FAILs under `set -o pipefail` | `curl | grep -q` closes the pipe early → curl SIGPIPE → check fails despite matching content. Capture body to a variable and use `case "$body" in *pattern*)` shell matching |
| Sibling Cloud Run mappings on the same base domain | Existing working mappings are the perfect control for isolating new-mapping TLS problems from DNS/DO issues |
| `bash -n`/self-test run from the skill folder with repo-relative paths (silent "No such file" failures) | Run repo-file checks from the repo root; run kit self-tests from the kit folder; verify each check actually executed |
| `rm -rf .next` flagged by the approval harness before a verification build | Clean rebuild via `npm run build` only when needed for standalone verification; prefer in-place build, no destructive pre-clean |
| Verify the build but never exercise the built server | After standalone build, assemble the exact container layout (static + public into standalone/) and smoke-test pages/assets over HTTP before proposing release |
| Treating a repair commit as acceptance | Demand the successor retest or explicit POC exception naming the SHA; report the gap, don't resolve it |
| Packaging the working directory | `git archive <pinned-SHA>` only; exclusions after extraction; inventory hashes |
| Floating image tag in Dockerfile | Verify digest from registry API; pin tag@digest; record check time |
| Overlay silently added to config | Explicit Path A/B authorization + manifest; assembly fails if config exists |
| Blocked command retried or rerouted | Stop, ledger, script-for-review, continue independent work, batch questions |
| "Rollback: none needed" on first deploy | Record the withdrawal procedure and its non-undo effects |
| Readback skipped after deploy | Service YAML, URL, revisions+traffic, IAM readback to files, every time |
| Numbered list slips after an insertion | Re-check the numbers on every edit to a numbered procedure |

## Verification before proposing execution

1. `bash -n` every generated shell script; YAML-parse every config.
2. Dry-run the fail-closed checks: blank config exits non-zero, wrong account exits non-zero.
3. Upload-guard (effective upload listing) mock: clean, forbidden-filename, and error cases.
4. Inventory + overlay hashes recorded in the run record; checklist marks every NOT RUN item honestly.
5. Present the plan with target/exposure/identities/IAM changes and stop for explicit authorization.

## Support files

- `references/acceptance-chain-case-notes.md` — worked example: FAIL verdict → repair ruling → repair commit → missing successor retest, detected from record archaeology.
- `templates/overlay-next-config.ts` — minimal standalone-output overlay to copy when the repo has no `next.config.*`.