# WEB DEPLOYER / DEVOPS PLAYBOOK

> **Version:** 1.1 · **Date:** 2026-10-25 · **Status:** v1 POC — JARVIS review corrections applied
> **Adapted from:** `DEPLOYMENT_PLAYBOOK.md` v1.0 (authority and identity rules; its OPEN items remain open), the `next-deploy-generate` / `next-deploy-execute` skill pair (procedure), `QA_PLAYBOOK.md` v1.2 §13 Gate D
> **Pairs with:** `WEB_DEVOPS_INSTRUCTIONS_v1_0.md`, `../CONSTITUTION/WBM_PLAYBOOK_v1_0.md`

## 1. Minimum inputs

| Input | Source | If missing |
|---|---|---|
| Certified candidate SHA | `QAM/QAM_CERTIFICATION.md` | Stop; nothing to deploy |
| Director release for that SHA, environment and target | Director | Stop; certification is not release |
| GCP project ID, region, service names | Director | Prepare files with placeholders named; do not invent |
| Environment variable names | Developer handoff | List from `.env.example`; flag absences |
| Deployment skill or runbook | Runtime | Generate files by hand from the skill's documented shape; state that the skill did not run |
| Domain and DNS intent | Director | Deploy to the platform URL; DNS stays a listed manual step |

## 2. Two services, two lifecycles

| Service | What it is | Deploys when | Owner of the decision |
|---|---|---|---|
| **CMS hub** | One Payload service shared by all sites, talking to Supabase Postgres and Storage | Hub code or config changes; adding a site is a data change, not a deploy | Director, as a separate release |
| **Public site** | One Next.js service per client, reading published content from the hub at build or request time | Each site's WBM closes, or its code changes | Director, per WBM |

Adding a site that uses existing fields and blocks is normally a data change, not a hub deployment. New hub schema, block definitions, plugins or configuration may require a separately identified hub deployment; the website WBM's plan records that conditional change, and no new standing approval ceremony is created for it. A hub deploy is its own bounded change with its own smoke checks and rollback, and it affects every site, so it is identified separately from the site release even when both happen in the same week.

`TODO (Director):` hub hosting — Cloud Run with a minimum instance, or an existing server. Until ruled, this playbook assumes Cloud Run for both services and marks the hub's profile as unverified.

## 3. Workflow

**Step 1 — Verify the release binding.** Candidate SHA in the certificate matches the SHA the Director released and the HEAD of the branch you are deploying. Mismatch is `STOP-IDENTITY`.

**Step 2 — Generate the deployment package.** Use the available Cloud Run generation skill for Next.js. Expected outputs in the site repo: a `Dockerfile`, a `cloudbuild.yaml`, a `deploy.sh`, an `init-app.sh` for first-time service setup, and a pre-filled `DEPLOYMENT_CHECKLIST.md`. Confirm each file exists on disk after generation. If the skill is not available, write the same files from its documented shape and say so.

**Step 3 — Exclusions.** Prove `agent_docs/**`, `QAM/**`, test fixtures and local env files are excluded on three surfaces: the TypeScript and test scope, the ignore files (`.dockerignore`, `.gcloudignore`), and the built image or bundle. Record the inspection command, working directory, exit code and output as `EVIDENCE`.

**Step 4 — Environment.** List every variable the site needs by name, separating build-time inputs (hub URL, site read token if content is fetched at build) from runtime inputs (revalidation secret, analytics IDs, form endpoints). Values go into the platform's secret manager by the Director or under an explicit delegated step, and reach the build through the approved mechanism. Never in committed files, deliverables, logs, image layers or client bundles.

**Step 5 — Build and deploy.** Run the pipeline. Capture build ID, image digest, revision name, service URL. If this runtime cannot run the deploy, hand the Director the exact command sequence with working directories.

**Step 6 — Smoke checks.** On the deployed URL: HTTPS resolves; the revision serving traffic is the one just built; home and one page per page type render with content; an image from Storage loads; a Payload publish reaches the deployed site within the documented window; one real form reaches its endpoint; no console errors on the walk. Record each as `EVIDENCE` with time.

**Step 7 — Rollback instruction.** Before any production traffic change: the previous revision name and the command to shift traffic back, or — for a first deployment with no prior revision — the procedure to withdraw or disable the service and the DNS state to restore. State what a rollback does not undo (published content, form submissions, external effects). A deploy without a written rollback or withdrawal procedure is not complete.

**Step 8 — Record and hand off.** Write `DEPLOYMENT_RECORD.md`. Update `WBM_STATE.md`. Hand the revision identity to the QA Lead for Gate D if required. Hand DNS records to the Director: exact host, type, value, TTL. Domain mapping and SSL verification follow the execute skill's steps once DNS is live.

## 4. Deliverables

- Deployment package in the site repo: `Dockerfile`, `cloudbuild.yaml`, `deploy.sh`, `init-app.sh`, `DEPLOYMENT_CHECKLIST.md`
- `DEPLOYMENT_RECORD.md`: release identity chain, environment variable names, exclusion evidence, smoke results, rollback instruction, DNS handoff, open items
- Updated `WBM_STATE.md` deployment line

## 5. Definition of done

- Release identity is complete: repository → commit → build/image → revision → environment → URL.
- Exclusion evidence exists for all three surfaces.
- Smoke checks recorded with results, including the publish-loop check on the deployed site.
- Rollback instruction written and the previous revision retained, or a withdrawal procedure recorded for a first deployment.
- DNS handed off as explicit records, or recorded as not in scope.
- Nothing claims Gate D. Nothing claims production readiness.

## 6. Handoff contents

To the QA Lead: the identity chain and smoke results, so Gate D starts from an identified deployment. To the Director: `DEPLOYMENT_RECORD.md`, the manual steps list, the acceptance decision requested. To the next WBM: the hub's current revision and the site-add procedure, so the next site does not rediscover it.

## 7. Open items inherited from the Deployment Playbook

These remain OPEN unless the Director has explicitly resolved them. Do not treat a successful first deploy as a ruling.

- O-1 DevOps authority in cloud contexts; whether an engineer may deploy to staging during a build
- O-2 DevOps Architect seat occupant
- O-3 Staging → production promotion doctrine
- O-4 Monitoring and incident detection after deploy
- O-5 Non-Next.js deployment packages (the Payload hub may fall here if hosted separately)
- O-6 Gate D mapping on platforms beyond the first target

Working default for the POC: one staging deploy per site, Director inspects, Director promotes. Record it as a default, not doctrine.

## 8. Common mistakes

| Mistake | Fix |
|---|---|
| Redeploying the hub to add a site | A site using existing blocks is a data change; a schema or plugin change is a separately identified hub deploy |
| First deploy with no rollback because "nothing to roll back to" | Record the withdrawal or disable procedure |
| "Deployed" with no revision name | The chain is the deliverable |
| Secrets in `cloudbuild.yaml` or the image | Secret manager; names only in files |
| Smoke check is "the URL loads" | Revision match, content, image, publish loop, form |
| Rollback written after the incident | Written before traffic promotion |
| Promising DNS propagation | List records; propagation is observed, not promised |

## 9. Illustrative example — first site on a new hub

*Illustrative only.*

Certified candidate `f7a9…` for `harbor_cafe_p1_wbm`. Director releases to staging on Cloud Run, project and region supplied, hub already running at its own revision.

Generation skill runs: five files land in the site repo; checklist pre-filled with service name and region. Exclusion evidence: `tsconfig` excludes `agent_docs`, `.dockerignore` and `.gcloudignore` list `agent_docs/` and `QAM/`, image inspection shows neither path. Variables listed by name: `HUB_API_URL`, `HUB_SITE_TOKEN`, `REVALIDATE_SECRET`, `GA4_ID`, `FORM_ENDPOINT`. Director loads values into the secret manager.

Deploy runs: build `b-2231`, image digest recorded, revision `harbor-cafe-00003`, staging URL live. Smoke: HTTPS ok; revision header matches; home, menu, about, contact render; hero image from Storage loads; a menu-item edit in Payload appears on staging in 6 seconds; contact form posts to the configured endpoint; console clean. Rollback: previous revision `00002` retained, traffic command recorded, note that published content is not reverted by rollback.

Record written. Identity to the QA Lead for Gate D. DNS records for `harborcafe.example` listed for the Director. Production promotion waits on Gate D and the Director.

## 10. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | First Web DevOps playbook; authority and identity rules from Deployment Playbook v1.0; procedure sourced from the Cloud Run skill pair; hub-vs-site lifecycle split; OPEN items carried unchanged |
| 1.1 | 2026-10-25 | JARVIS review: hub redeploy made conditional on schema/plugin/config change; build-time vs runtime variables; first-deployment withdrawal procedure; secrets wording scoped |
