---
name: wbm-assembly
description: Use when assembling a Website Build Module (WBM) + its QAM.
---

# Website Build Module (WBM) assembly

Assemble the Architect's delivery unit for one website (or one bounded phase): a self-contained
module folder that lets the Developer build without reconstructing the contract from chat, and lets
independent QA run from its embedded QAM. Governed by `WBM_PLAYBOOK.md` (shared) and the
`WEB_ARCHITECT_PLAYBOOK.md` — those live in the role's constitution, not here; this skill is the
*execution pattern* for turning brief + design into the module on disk.

## When to use

You are the Web Architect, the SITE_BRIEF is approved, the design package is in hand (and reviewed),
and Tony has released module assembly. NOT for intake/brief drafting (that precedes this), and NOT for
the Designer/Developer/QA seats.

## The contract first

Before writing files, establish: project root, the module-root path, the website repo + branches, and
what is per-site vs module-local. In the Cyberize POC the project guide overrode the playbook's flat
layout (see `references/first-wbm-cyberize.md`):

- `_site/`, `_design/`, `_infopack/` live at the **project root**, one level above the module root.
- The module root (e.g. `WBM/`) holds entry/state/rulings/playbook/verification/`QAM/`.
- Reference the per-site trees by **absolute path** — never duplicate them into the module root.
- A placement not covered by the mapping goes into `WBM_RULINGS.md`, not a second copy.

## Module anatomy (what to write, in order)

1. **Entry** (`WBM_ENTRY.md`) — deterministic read order + phase dispatch + authority + subject
   precedence. This is the *activation* file; `README.md` is the operator (Director) guide.
2. **State** (`WBM_STATE.md`) — a small current-state index: module ID, repo/branch, pending gates,
   what's done vs not, next owner. "Status text grants no authority."
3. **Rulings** (`WBM_RULINGS.md`) — append-only approvals, errata, deviations. Each ruling: ID,
   authority, observation, exact decision, affected ACs/files, regression. Never rewrite prior verdicts.
4. **Contracts** (per-site, in `_site/`): `SITE_BRIEF.md` (scope), `CONTENT_MODEL.md` (data contract —
   a *local typed module* when CMS is deferred), `ACCEPTANCE_SPEC.md` (frozen numbered ACs).
5. **Playbook** (`playbook/00-OVERVIEW` … `06-SELF-CHECK`) — the build sequence the Developer follows.
6. **Verification** (`verification/GATES.md` + `BUILD_CHECKLIST.md`) — GATES.md mirrors the ACs
   verbatim (definition of done requires ACs to appear identically in both places).
7. **QAM** (`QAM/`) — see below.
8. **Learning record** (`FIRST_WBM_LEARNING.md` on the first one) — reused patterns, adaptations,
   resolved ambiguities, what execution must still prove.

## QAM instantiation (the part people get wrong)

The QAM owns independent QA. Files: `QAM_ENTRY.md`, `QAM_STATE.md`, `QAM_PREFLIGHT.md`,
`QAM_RISK_REQUIREMENTS.md`, `QAM_MANIFEST.md`, `HANDOFFS/ENGINEERING_HANDOFF.md`, plus the *result*
files: `QAM_RECON_REPORT`, `QAM_TEST_PLAN`, `QAM_APPROVAL`, `QAM_EXECUTION_REPORT`,
`AC_EVIDENCE_MATRIX`, `FINDINGS`, `QAM_CLEANUP_REPORT`, `QAM_CERTIFICATION`.

**Hard rules:**
- Every result/approval/certificate field ships **empty** — `NOT EXECUTED`, `PENDING`, `NOT AUTHORED`,
  `NOT CERTIFIED`. Never prefill a PASS. The pattern is "authored future-state record, not execution
  evidence" with a one-line note of what the owning seat will write there.
- `AC_EVIDENCE_MATRIX` gets one row per AC, all `NOT EXECUTED` / `PENDING`.
- `QAM/GOVERNING/` holds **pointers** to the governing playbooks, not copies — never claim a
  byte-identical copy of an unseen template (record that as a ruling).
- The QA Executor is "assigned by the Lead" (per project guide) — do not invent a named extra worker.
- QAM preflight/risk are written for the *website* (local content, no CMS/auth/forms → no
  credential/identity checks), not copied from an app-Factory FFM that had auth/billing.

## Acceptance spec — adapt, don't copy

Start from `WBM_PLAYBOOK.md` §5 standing ACs (build, navigation, responsive, content rendering, CMS
edit loop, image loop, media storage, access, forms, migration, baseline). For a local-content POC,
explicitly rule the N/A ones in a "standing-AC applicability" table rather than silently dropping
them; turn negations into positive requirements (e.g. "no form" becomes an AC). Give each AC
Requirement / Verification / Evidence. 10–14 ACs is right for a small site.

## Content source map (ground scope in the scraped source, not memory)

When Tony reopens scope (or on intake), re-read the scraper package directly — never reconstruct from
conversation summaries. Write `_site/CONTENT_SOURCE_MAP.md`:

- **Inventory**: captured pages, navigation, SEO metadata (titles/descriptions/canonicals), and media
  — split **downloaded assets** (actual files, incl. a `brand_reference/` folder) from **URL-only**
  references. The source site's real structure is usually larger than a first pass suggests (e.g. the
  Cyberize three-page assumption vs the actual five service pages + legal + blog).
- **Map table**: `source URL → exact evidence file → proposed destination → retain/rewrite/combine/
  omit/defer → reason`. Every substantial source page gets a row; nothing is silently discarded.
- **Name gaps honestly**: pages referenced but never captured (a prominent offer, a linked page, legal
  pages) are named, not invented.
- **Recommend a grounded page map** that preserves real service detail; defer out-of-scope sections
  (blog, partners, legal) explicitly rather than compressing them into generic cards.
- **Require traceability**: the design package's `SECTION_MANIFEST.md` must map every section back to
  the source map. A section with no source trace is treated as an invention.

See `references/content-source-map-pattern.md`.

## Independent design-review discipline (before assembly)

Review the *actual* files, not the Designer's completion claims. Reconcile `SECTION_MANIFEST.md`
against `CONTENT_MODEL.md`. Two specific traps seen in practice:

- **Copy-compliance drift**: the spec's §provenance may claim "omitted" while the HTML still carries
  the banned item (guarantee/timeline). Grep the rendered pages, not just the summary table.
- **Markup validity**: a duplicate `<main>` or stray `</footer>` is invisible to DOM-based checks
  (the browser repairs it). Verify raw source, not the live DOM.

## Pitfalls

- **Ground environment deviations in actual tool results.** Do not infer instruction-file restrictions from filenames or past sessions. If a write is actually refused, record that specific refusal and use an authorized navigation alternative; never claim files were blocked when the tool reported successful writes.
- **Phone numbers appear masked** in tool output (`+18009830668` → `+180****0668`) while the bytes are
  correct. When a number's exact value matters, verify with `od -c` / `xxd` (read hex, not the ASCII
  column) or `grep -c` on the plain digit substring. Don't file a false "masked value" defect — retract
  it and redirect to the real risk (scraped/unconfirmed).
- **Never invent an approval.** If Tony hasn't explicitly approved the design, ship the module as
  DRAFT with that one gate named in `WBM_STATE.md` + `WBM_RULINGS.md`. Shot 1 (recon/plan) may proceed;
  build/QA wait.
- **Don't copy a reference FFM's client content or historical PASS results** — reuse only its
  structure. Extract to `/tmp` to inspect, leaving the reference unchanged.
- **Boundaries**: module assembly does not clone the repo, touch the design, start QA, or contact
  other agents. The website repo is recorded (URL + branches), not cloned.
- **Other seats write to the same files.** The Developer runs shot 1 (updates `WBM_STATE.md`,
  `EXECUTION_PLAN.md`) while you work. Re-read a file before patching — a stale `old_string` fails
  with a "modified since last read" warning. Make minimal targeted patches and preserve the other
  seat's facts. When the design direction changes after shot 1, flag that the plan must be re-pointed.
- **Stage design approval according to the current assignment, not a fixed concept count.** A homepage can establish direction, but it does not demonstrate a coherent multi-page system. After repetitive full-site designs are rejected, commission a complete homepage plus one source-rich service page, including lower sections/footer, and stop for Tony's review before expansion. Choose the service from actual captured evidence. If Tony requests multiple concepts instead, preserve equivalent content coverage for fair comparison. Selection of a concept authorizes only the explicitly requested stage, never implementation or publication.
- **Creative success is separate from technical preflight.** Require actual rendered inspection, side-by-side desktop/mobile comparison, and refinement before delivery. Passing tests cannot establish visual approval. A high-fidelity limited slice needs fully considered imagery, composition and section rhythm, not minimal-polish demo defaults. Brand consistency does not mean the same decorative object, heading and text rows on every page.
- **Relay formatting and brevity.** When Tony asks for a prompt again, return the complete prompt in a fenced code block, with no unnecessary explanation. For a new work order, keep surrounding prose short: findings, selected scope and saved path; place absolute input/output paths and the complete assignment inside the code block.
- **Require the Designer to visually inspect brand assets** (logo + screenshots) with image/browser
  tools, and to report honestly if they can't view them — don't let a design proceed blind on the brand.

## Final approval → implementation release

- **Separate creative approval from positioning approval.** A visually approved homepage can still misrepresent an agency as a single-service business. Correct headline, supporting copy, dominant artwork and opening hierarchy together; a tiny agency eyebrow is not enough. Preserve the approved visual system, move deep service storytelling to its dedicated page, and require a comparable desktop/mobile before/after review. This is not automatically a creative restart.
- **Honor explicit development authorization.** When Tony authorizes in-scope local implementation without another permission round, record that authority and replace stale holds. Require a recon/plan refresh against the current contract, then continuous conformant execution—not another invented approval gate. Keep Git mutation, independent QA release and publication separately governed.
- **Freeze the actual package, not its delivery claim.** Inventory relative paths, byte sizes and SHA-256 hashes outside the design directory; hash the manifest itself. Provide a checker for missing, changed and added files. Identify root approved references versus historical before/revisions folders. Hashing detects drift; it is not filesystem immutability.
- **Carry uncertainty without silently confirming it.** Separate provisional contact facts and commercial/platform terminology into an owned confirmation register. With explicit authority, these may remain nonblocking for local implementation while unresolved for publication. Do not remove notices, add promises, or rewrite frozen wording without a ruling.
- **Match screenshot conditions.** Record CSS viewport, device scale, browser, fonts and interaction state. A 2880px PNG may represent a 1440px viewport at DPR2. Require per-page and expanded-state visual comparisons, not only thumbnails or automated counts. Verify the Developer can actually view images through its runtime tools; another role's successful vision call proves nothing about that runtime.
- **Archive before reconciliation, preserve executed evidence.** Preserve old contracts/plans before replacement; inspect QAM result status before initializing new placeholders. Keep real historical results in their original evidence lane. Inspect existing tests before running: screenshot tests can overwrite tracked historical evidence.

See `references/design-freeze-and-release.md` for the assembly and verification checklist.

## Definition of done

Folder tree matches disk; ACs identical in `ACCEPTANCE_SPEC.md` and `verification/GATES.md`; no TBD
in a critical section; unknowns are `TODO:` with owner; QAM has no prefilled result; the Director has
a one-line activation instruction; the pending approval is named.

## Tony's working preferences (embed these)

- **Version + timestamp stamp every deliverable/handoff**: `Version: vX.Y · Updated: YYYY-MM-DD
  HH:MM:SS +06:00` near the top, so the picker knows which is latest. Keep the stable filename as the
  "latest" pointer; bump the version on regeneration. Timezone is +06:00 (Asia/Dhaka).
- **Relay prompts go in a fenced code block** — any copy-paste prompt for the Designer/Developer/QA is
  rendered as a ``` code block so Tony can one-click copy. Never inline prose.

## References

- `references/creative-restart-handoffs.md` — source-grounded creative restarts, staged visual review, imagery provenance, session separation and final design-to-WBM reconciliation.
- `references/first-wbm-cyberize.md` — concrete Cyberize POC: exact file tree, the FFM reference
  structure adapted, rulings R-001…R-008.
- `references/content-source-map-pattern.md` — the scope-grounding inventory + map-table technique and
  the four-document reconciliation checklist.
