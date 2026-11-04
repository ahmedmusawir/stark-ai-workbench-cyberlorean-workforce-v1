# STARK WEB FACTORY — CYBERLOREAN STARTER SET v1.1

> **Date:** 2026-10-25 · Asia/Dhaka · **Status:** v1 POC material — JARVIS review (2026-10-24) corrections applied
> **Director:** Tony Stark · **Author:** Fable · **Reviewer:** JARVIS
> **Director's ruling:** KISS. POC first. Move fast. These documents evolve by building with them.

## Purpose

Twelve usable v1 documents so five Web Factory Cyberloreans can start building websites now: base instructions and a playbook for each role, plus the shared Website Build Module playbook. Every build follows the WBM with its own QAM inside, four shots per module.

The intended stack for every website: **Next.js** public frontend, **Payload CMS** for editable content and media, **Supabase Postgres** for CMS data, **Supabase Storage** for media binaries, **Cloud Run** as the intended deploy target. One shared Payload **hub application** serves many independent Next.js **website applications** with site-scoped content and media. Payload is standard; a CMS-free default is not offered.

The hub and the adapted starter kit are established once, under an explicitly scoped **foundation task** with its own plan, approval and QAM. Website WBMs consume them; they never install Payload, remove SaaS code or create databases.

## File map

```text
WEB_FACTORY_STARTER_v1_0/
├── README.md                                   this file
├── CONSTITUTION/
│   └── WBM_PLAYBOOK_v1_0.md                    shared Website Build Module playbook
├── ARCHITECT_AGENT/
│   ├── WEB_ARCHITECT_INSTRUCTIONS_v1_0.md
│   └── WEB_ARCHITECT_PLAYBOOK_v1_0.md
├── DESIGNER_AGENT/
│   ├── WEB_DESIGNER_INSTRUCTIONS_v1_0.md
│   └── WEB_DESIGNER_PLAYBOOK_v1_0.md
├── ENGINEER_AGENT/                             Web Developer lives here
│   ├── WEB_DEVELOPER_INSTRUCTIONS_v1_0.md
│   └── WEB_DEVELOPER_PLAYBOOK_v1_0.md
├── QA_AGENT/                                   Web QA Lead lives here
│   ├── WEB_QA_LEAD_INSTRUCTIONS_v1_0.md
│   └── WEB_QA_LEAD_PLAYBOOK_v1_0.md
└── DEVOPS_AGENT/
    ├── WEB_DEVOPS_INSTRUCTIONS_v1_0.md
    └── WEB_DEVOPS_PLAYBOOK_v1_0.md
```

Folder names match the source ZIP so each role's instructions sit beside the App Factory documents they were adapted from. These folders hold instructions and playbooks only; project deliverables follow the WBM layout at the module path each project declares. The original source documents are not modified by this pack.

## Read order

**Everyone, once:** `CONSTITUTION/WBM_PLAYBOOK_v1_0.md`.

**Each role, at startup:** its own `*_INSTRUCTIONS_v1_0.md`, then its own `*_PLAYBOOK_v1_0.md`, then the WBM sections its instructions name, then the project artifacts for the site in hand. No role rereads the whole Factory corpus every turn.

**Workflow for the POC, human-directed:**
Web Architect → Web Designer → Web Architect assembles WBM → Web Developer (two shots) → independent QA (two shots) → Director release → Web DevOps.

The first website candidate is CyberizeGroup.com, using the existing Architect info pack when supplied.

## Source and version notes

| New document | Adapted from | Notes |
|---|---|---|
| WBM_PLAYBOOK | FFM_PLAYBOOK v1.3, QAM_PLAYBOOK v1.0, ABM v1.0, APP_FACTORY_BLUEPRINT v2.2 | Mock-data service layer and backend swap point removed; Payload is present from day one |
| Web Architect | ARCHITECT_PLAYBOOK v2.3, ARCHITECT_QUESTIONNAIRE v2.3 (2026-10-18 DocSet sync) | Info pack replaces repo recon; SITE_BRIEF replaces APP_BRIEF; CONTENT_MODEL replaces DATA_CONTRACT; v2.3 workflow (Architect owns contract + assembly + QAM, Director approves and releases) is the one followed |
| Web Designer | DESIGNER_PLAYBOOK v2.2, Archetype Kits Vision v0.1 (inspiration only) | Canonical Page Method and token-first kept; dark mode and six-kit prerequisite dropped; rendering tool follows the active project instruction |
| Web Developer | ENGINEER_PLAYBOOK v1.3, STARTER_KIT_HANDBOOK v1.2 (design reference), FRONTEND_BUILD_PHASE v1.3.0 | Intended kit described as existing / proposed / to-verify; SaaS auth and portals removed; Payload + Supabase adapters introduced |
| Web QA Lead | QAM_PLAYBOOK v1.0 (process owner), QA_PLAYBOOK v1.2, TESTING_PLAYBOOK v2.2 | Two-shot QA retained; website standing risk set added; four layers and browser matrix made proportionate |
| Web DevOps | DEPLOYMENT_PLAYBOOK v1.0, next-deploy skill pair, QA_PLAYBOOK §13 | Hub-vs-site lifecycle split; OPEN items O-1 to O-6 carried unchanged |

Director rulings applied where older source differs: Payload standard; shared hub on shared Supabase; WBM naming (not SBM, not FFM); two storage purposes (Workbench GCS vs Website Supabase); four-shot pattern with QAM inside every module.

**Recorded policy conflict — browser rendering tool.** The Workbench phase map v1.1 (ruling 12) restricts Playwright. The supplied Designer v2.2, FFM v1.3 and Testing v2.2 playbooks explicitly use it. This pack does not assert either as a factory-wide rule. Agents use the rendering tool permitted by the active project and runtime instructions, record the tool used, and never fabricate screenshots. The conflict is reconciled when the phase map is next updated.

## External dependencies

These are required by the pack but are not inside the ZIP. An agent must not invent a missing one or claim a skill ran.

| Dependency | Source and version | How supplied | Status |
|---|---|---|---|
| QAM governing playbook | `QAM_PLAYBOOK.md` v1.0 (2026-10-14), in the source ZIP under `QA_AGENT/` | Already in the source set | Present |
| QAM module template | `03_BUILD_METHODOLOGY/_templates/QAM/` as named by FFM Playbook v1.3 §3 and Architect Playbook v2.3 | Factory doc set on the build machine | Location on Zorin **unresolved**; needed only at first WBM instantiation |
| QA doctrine | `QA_PLAYBOOK.md` v1.2, `TESTING_PLAYBOOK.md` v2.2, in the source ZIP | Already in the source set | Present |
| Starter kit handbook | `STARTER_KIT_HANDBOOK.md` v1.2, in the source ZIP | Design reference only; the Web Factory kit is produced by the foundation task | Present as reference |
| Cloud Run deployment procedure | `next-deploy-generate` / `next-deploy-execute` skill pair (APP_FACTORY_SKILLS_PLAYBOOK §14) | Installed skill in the engineering runtime | Availability verified at first deploy |
| ABM playbook | `ABM_PLAYBOOK_v1_0.md` (2026-10-17), cited for the four-shot pattern | Director's doc set | Present outside the ZIP |

Role-document review and Workbench connection testing do not depend on the unresolved template location.

## Runtime note

These are portable Markdown instruction sets. Nothing here assumes Hermes or any runtime loads them automatically. Installation mapping into worker profiles (SOUL, constitution, context folder, workspace pointer) follows separately under the Workbench lab's worker packaging step.

## Deferred implementation decisions

| Decision | Owner | Where it lands |
|---|---|---|
| Foundation task scope and timing: establish hub, adapt starter, verify multi-site mechanism | Director + Web Architect | WBM §1 and §7, Developer §2 |
| Hub hosting: Cloud Run vs existing server | Director | WBM §7, DevOps §2 |
| Payload multi-site mechanism, site-scoped settings/navigation collections and adapter packages on the installed version | Foundation task | Developer §2, Architect §2 |
| Publish mechanism default (revalidation vs rebuild) | Web Developer per WBM, Architect review | Developer §3 |
| Rendering tool for Designer PNGs | Runtime capability | Designer §6 |
| Lighthouse thresholds per site | Architect in each SITE_BRIEF | QA §3 |
| Staging → production promotion rule | Director | DevOps §7 (O-3) |
| Spoke template: one with flags vs two | Director | Future WBM playbook revision |
| When the tenant-isolation negative test becomes mandatory | QA Lead at second site | QA §3 |
| Web Factory starter kit: actual removal and Payload introduction | Separate engineering work | Developer §2 is the intent description |

## Genuine source gaps

- No App Factory document defines a DevOps or QA *role*; both roles here are authored from QA, testing and deployment doctrine rather than ported.
- The Deployment Playbook contains authority and identity rules but no procedure; procedure is sourced from the deployment skill pair.
- No source document names Lighthouse, accessibility tooling, visual regression or link checking; the QA standing set introduces them.
- The Web Factory starter kit does not yet exist; the Developer playbook describes intent and marks what shot-one recon must verify.

## Version history

## Change summary — v1.1 (JARVIS review, 2026-10-24)

1. Hub application vs website application made explicit everywhere; one-time foundation task introduced; website WBMs no longer install Payload or remove SaaS code.
2. Per-site navigation and settings corrected from Payload globals to site-scoped collections, one document per site.
3. QA examples and verdict rules aligned to QA Playbook v1.2 §11: failed required AC stays FAIL, unavailable evidence stays BLOCKED, follow-ups are out of scope; severity decoupled from pass/fail.
4. Secret-free cold build replaced by a clean build with documented build-time configuration; commands inspected from the checkout before being named; secrets language scoped to committed files, deliverables, logs, images and bundles.
5. Access boundary stated as authenticated/authorized editor operations, not "admin never public"; storage prefix is organization, not authorization; isolation tests staged by site count and aligned between QA checklist and standing table.
6. External dependency table added; QAM template named with its Factory path and marked unresolved on Zorin.
7. Architect source citations corrected to v2.3; Playwright policy conflict recorded rather than asserted.
8. Five-item exclusion hard stop relaxed for websites; KIP reserved for reusable-kit changes; "build from HTML" clarified; authoring order corrected; PAGE_SPEC folded into SITE_DESIGN_SPEC; navigation, migration 404/410, Lighthouse sampling and first-deployment rollback wording fixed.

No file was added or removed. Twelve documents, six folders.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | Initial twelve-document starter set |
| 1.1 | 2026-10-25 | JARVIS review correction pass; see change summary above |
