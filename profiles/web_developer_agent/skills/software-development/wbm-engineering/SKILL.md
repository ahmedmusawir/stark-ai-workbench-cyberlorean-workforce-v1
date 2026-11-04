---
name: wbm-engineering
description: Use when running a WBM engineering shot (recon or build).
category: software-development
version: 1.2
author: web_developer_agent
license: MIT
metadata:
  hermes:
    tags: [wbm, recon, shot-1, shot-2, nextjs, checkout-discipline, resumption, visual-review, evidence-sweep]
    related_skills: [codebase-inspection, plan, dogfood]
---

# WBM engineering — operational companion to the project playbook

The project's own documents (`WBM_ENTRY.md`, `playbook/`, `_site/ACCEPTANCE_SPEC.md`,
`_site/CONTENT_MODEL.md`, rulings) own the WHAT — read order, sections, ACs, gates. The profile
constitution is injected every session. This skill owns only the HOW: operational discipline learned
executing shots against a real checkout. When this skill and the project's WBM docs differ, the
project docs govern.

## When to use

- **Shot 1** — read-only recon + one implementation plan. Stop after returning the plan; no product
  code, no Git mutation, no QA contact.
- **Shot 2** — approved implementation, self-checks, factual handoff, executed continuously.
- **Resumption / evidence sweep** — verify `WBM_STATE.md` against the actual tree (HEAD, changed
  paths, plan version) before resuming; never reconstruct history from guesswork. An inherited
  "implementation present, verification incomplete" handoff is completed by the FINISH phase, not a
  rebuild — see the finish-sweep workflow below.

## Shot-1 recon sequence (proven)

1. Read the WBM in its declared order. Do not skip the rulings — they carry POC deferrals and pending
   gates (e.g. "visual approval blocks shot 2, not the plan").
2. Git facts: `git status`, `git branch -vv`, `git rev-parse HEAD`, `git log --oneline`, `git remote
   -v`, `git ls-files`. Record upstream state — an engineering branch can exist locally with no
   upstream (the Director pushes, not you).
3. Diff the checkout against its reference starter (exclude `node_modules`, `.git`, `.next`, report
   dirs) and compare lockfile hashes. Establishes "checkout IS the starter" vs drifted.
4. Verify the toolchain from disk: Node version vs `engines`, package.json deps and scripts — never
   name a command not present in `scripts` — lockfile, tsconfig, lint/e2e configs.
5. Check port occupancy (`ss -tlnp`) before naming run targets. Record which ports belong to other
   services and never touch them. Before reusing or stopping an inherited server: verify ownership
   (start time + parent session/pid against your own records); kill only what you started.
6. Baseline re-verification — prior QA is baseline, never certification: `npm ci` (fresh checkout has
   no `node_modules`) → typecheck → lint → build → e2e. Record CWD, exit code, output path each.
7. Verify design-package claims on disk with byte-level spot checks (banned-copy regex scans,
   `tel:` hrefs, form-control counts). Reproduce spec claims — including claims that a defect was "a
   tooling artefact" — before relying on them.
8. Write the three deliverables: evidence file (`WBM/EVIDENCE/E1_RECON.md`), plan (replace the
   `EXECUTION_PLAN.md` template wholesale, every named section filled), `WBM_STATE.md` update.
   Return the plan and stop.

## Resuming an inherited handoff (mid-shot continuation)

When an assignment resumes a partially completed shot whose handoff was written by another session,
do not trust or rebuild it — establish the facts, then extend:

1. Read the inherited handoff, visual-review record and state file as CLAIMS. Verify each load-bearing
   claim against disk/log evidence before relying on it: branch/HEAD vs `git`, diff-stat shape,
   evidence files exist and contain the asserted results (20/20 in an e2e log, zero violations in an
   axe JSON, empty lists in a probe JSON). Spot-check the strongest falsifiable claims first.
2. Re-run the design freeze checker before any edit and again before handoff. A frozen-manifest
   SHA that no longer matches means someone touched the design — stop that path.
3. Hash-compare every copied asset against the frozen design copy (a flat per-file hash loop is
   cheap and settles "assets preserved" instantly).
4. Separate what the evidence already proves (reuse it, cite the same artifact) from what needs
   fresh work (do it, add new evidence). Never re-run a green check just to re-explain it, and never
   claim to have inspected artifacts you have not opened with a vision-capable tool.
5. Update only the handoff documents this seat owns. Preserve the prior session's record — append
   the resumption's findings, don't overwrite history.
6. Finish with a readiness decision, not a preparation summary. If forced to stop mid-work, name the
   exact remaining steps and any process you own that another session must kill or reuse — and save
   a checkpoint (a session-detail reference file under this skill) so the continuation never
   reconstructs what was done from a summary message.

## Evidence sweep — FINISHing an inherited incomplete shot

An inherited handoff whose AC table has gaps ("AC-N: UNVERIFIED", "not visually reviewed",
"remaining checks open") is completed by a closing sweep; the assignment normally says explicitly
that a rebuild is not wanted. Proven order (second resumption of the same module, 2026-11-01):

1. **Reconcile the record first.** Re-count the actual evidence inventory on disk (tiles, logs,
   JSONs) and compare against every count the prior record/summary asserted. An arithmetic slip in
   conversation history (auxiliary items added into a unique-inventory total) is exactly this
   pattern; the disk audit settles it in one script. Record the corrected counts explicitly in the
   review document — the operator will check them.
2. **Classify every remaining gap against the acceptance spec.** Mandatory → do it; not-applicable
   → disposition with reason (e.g. "no optional-empty sections exist in the approved package");
   genuinely unavailable → UNVERIFIED with the specific reason (e.g. no screen-reader tool in the
   environment). Never silently downgrade a requirement to fit what was done.
3. **Close the state/contract gaps with one consolidated browser script** (Playwright + system
   Chrome via `executablePath`): remaining state captures + real navigation walk (URL waits, see
   pitfalls) + open-state touch measurements + reduced-motion probe + branding/claims scans — one
   Node file, one JSON output, one run. Batching at the browser boundary is what makes the whole
   sweep fit the session budget.
4. **Batch the vision review.** Composite grids (see Visual-fidelity review) keep the review calls
   few. Stop a visual verification early if the budget pinches and checkpoint instead.
5. **Re-verify identity and freeze after all writes** (diff hash, untracked inventory, freeze
   checker), **stop owned processes**, then write the handoff documents last, in one pass.

## Visual-fidelity review of a rendered build (AC-09 class)

For "implementation matches the frozen design screenshots" checks on a real build:

- **Prove the vision tool live before trusting its output.** Feed it a deliberate mismatch (e.g. a
  non-image path) and confirm it errors correctly. A capability claim without a live result is not
  evidence; a file-exists check is not observation. (Note: the rejection alone doesn't prove image
  vision — the proof is the actual rendered images per tile; make sure every inspection call really
  returned the visual content.)
- **Inspect per-section comparison tiles, not full-page pairs.** The established pipeline: a script
  (`compare.py`-style) slices each reference/implementation full-page PNG into ~720 CSS px
  side-by-side tiles with an `index.json` (tiles per pair, sizes, height deltas), then every tile is
  actually opened and described with a vision tool. Record inspected area per tile; a generated tile
  that was merely produced is NOT an inspected tile.
- **Batch tile/state review with composite grids when the count is large.** The operator correction
  from 2026-11-01: "avoid another long sequence of one-image-per-turn calls — reuse valid evidence,
  batch where the tools support it." Proven recipes: (a) section tiles already sit side-by-side in
  each tile, so per-tile calls are genuinely necessary only when a tile is ambiguous; (b) remaining
  state captures (menu-open states, etc.) go into PIL composite grids — N reference/implementation
  pairs stacked with labels into 2–4 tall images reviewed in 2–4 vision calls; (c) reserve execution
  budget for the handoff documents, or checkpoint first. Encode which calls were batched and why in
  the review record.
- **Reproduce the reference capture conditions before capture.** The designer's screenshots are
  browser-specific (Chromium vs system Google Chrome wrap differently). Check the frozen design's
  documented capture condition (e.g. system Chrome 153, 1440/390 CSS px, DPR2, fonts/images settled)
  and capture the implementation with the SAME condition; only matched-browser tiles are valid
  comparison evidence. Full-page heights must be equal (height-delta 0) before section comparison is
  meaningful.
- **Element screenshots can show state a live viewport does not.** Playwright's element-capture
  scroll/clip can paint a hidden element (a skip link above the viewport, y<0) into the tile — in
  the recorded session, `faq-matched-390.png` showed a "Skip to content" overlay the live viewport
  never showed. On any suspicious overlay: measure the element rect live in the same interaction
  state, capture the plain viewport screenshot, and if the rect sits outside the viewport (fully
  negative or clipped), record the tile's overlay as a capture artifact with the measurement — don't
  chase phantom implementation bugs and don't dismiss it without the probe.
- **Expanded-state captures must reproduce the reference's exact interaction state** — which
  disclosures/menu were opened, which element carries keyboard focus — or the tile comparison
  records false differences. Note the focus target from the reference first, then script the same
  Tab/click sequence before capture. Reading 2–3 frozen references first to pin the state contract
  (panel geometry constant across pages, focus target, active-page marks) makes the scripted capture
  correct on the first try.
- **Contrast checks: measure computed pairs, read them against WCAG's size rule.** A sub-4.5:1
  finding may still be AA-compliant when the computed font size is large text (3.0:1 applies) —
  measure computed `color`/`backgroundColor`/`fontSize` pairs (walk the ancestor chain for the
  effective background) on every route into one JSON, classify with the large-text rule, and cite
  the size that qualifies; don't relabel 4.12:1 as "AA" without the size evidence.
- Pixel-diff statistics (mean channel diff, height delta) are supporting evidence, never a
  substitute for the visual pass; no arbitrary threshold waives inspection.
- **Record observations, not image loads.** A vision tool reporting that an image was loaded does not
  itself establish what was visually inspected or whether a comparison matched. Record the actual
  observed content and concrete discrepancies per tile or legible composite. Check the delivered
  image's downscaling/crops before claiming its text or fine details were reviewed. Reconcile the
  unique file inventory against the index AND the inspection records; do not invent auxiliary-call
  counts or reasons for an arithmetic discrepancy.
- **Metadata acceptance requires reference comparison.** Extract the approved title and description
  from each actual frozen reference and compare them to the rendered production DOM, recording
  the final HTTP status and description count for every route. A successful build, distinct values,
  or source-only assertions do not establish approved metadata or rendered equality. If a required
  check cannot run, leave it unverified and avoid an engineering-complete claim.

## Pitfalls (each one bit in a real shot)

- **Test runs can dirty a "read-only" recon.** The checkout's e2e spec writes screenshots to
  TRACKED paths (`QAM/evidence/*.png`). Before running any command in a read-only shot: grep the
  tests for writes to tracked paths, back those files up, run, restore, then prove `git status` is
  clean. Without this step, "read-only" is a false claim in the handoff.
- **Lint errors may be inherited, not yours.** A checkout can lint dirty because committed prior-QA
  helper scripts (`.cjs` under an evidence dir) trip rules, while every product path is clean.
  Verify per-path before reacting. Disposition: propose ignoring the evidence dir in lint config
  (labeled `ASSUMPTION:`, flagged for approval) or record a known limitation — never delete
  prior-QA evidence to go green, never weaken the rule silently.
- **Tool output can mask sensitive strings.** Terminal and file-tool output rendered
  `tel:+180****0668` while the file bytes held the full dialable E.164 number — the design spec's
  claim of "a display artefact" was correct, but trusting either the masked output OR the doc
  without checking is how false findings get recorded. When an exact digit string matters, verify at
  byte level: open `'rb'`, count asterisks, compare digit sequences.
- **E2E instrumentation races: read UI state with waits, not a bare boolean.** A navigation walk
  that `click()`s then immediately compares `page.url()` records races; storing only an aggregate
  boolean in one JSON key (`servicesAllTrue`) hides per-link outcomes and makes a green result
  uninterpretable. Store per-link/per-step results and synchronize with
  `page.waitForURL(cb)` before reading state. URL callbacks receive the URL object — compare
  `u.pathname`; note `waitForURL('http://host/full/path/')` can time out when the app serves the
  same path WITHOUT a trailing slash — match on pathname, not the full URL string.
- **Vision inspection consumes iterations fast; budget it.** 94 tiles burned nearly a whole session
  at one call per turn — when the assignment allows batching and the tile count is meaningful, use
  the composite-grid recipe (above) and stop/checkpoint if the budget pinches.
- **Fresh checkout ≠ runnable checkout.** `npm ci` before any verification; check `engines` first.
- **Missing instrument ≠ invented score.** If an AC requires a tool that isn't installed (e.g.
  Lighthouse), record an honest UNVERIFIED claim plus a blocker with options and a default — never
  fabricate a number, never install without approval.
- **npm warnings are advisories first.** npm 11 install-scripts warnings (e.g. `unrs-resolver`
  postinstall) are non-fatal; record as advisory with a no-action default, await a ruling.
- **Copy-discipline false positives.** A banned-word regex can hit a *retained commercial term*
  ("payment not scheduled until initial deposit") inside an F1-retained FAQ — check the review
  rulings' retention list before flagging or "fixing" copy the Architect deliberately kept.

## Plan-authoring rules

- Replace the template wholesale; every named section filled; no TBD.
- Every fact traced to an observed command or file read. Handbook/spec claims verified on disk or
  labeled as claims.
- One consolidated blockers/questions list: each item with owner, default, and needed-by. Label
  `ASSUMPTION:` for defaults you proceed on. Do not run a questionnaire for facts discoverable by
  inspection.
- Precondition gates (e.g. unrecorded visual approval) block execution, not the plan — say so
  explicitly in both plan and state.
- End with an approval record: authored date / Architect review PENDING / Director approval PENDING;
  state the exact executable scope on approval and the hard stops (contract conflict, protected-repo
  modification request, deployment request, Git mutation request).

## Shot-2 discipline (when approved)

- Write only inside the checkout and the engineering evidence lanes. Never the starter repo, never
  prior-QA records, never Git, never deployment.
- Same tree discipline as shot 1: any self-check command that writes a tracked path gets the
  backup/restore treatment, or the write is owned and documented. Final `git status` before handoff
  shows only intended changed paths.
- Structured content from the first line of the first component — retrofitting "no string literals
  in JSX" after building is expensive.
- Handoff = facts only: per-AC claims with evidence or honest UNVERIFIED entries; the candidate is
  "pending Director commit" until the Director commits it.

## Support files

- `references/cyberizegroup-p1-field-notes.md` — shot-1 specifics for the first WBM (checkout
  identity, baseline numbers, pending decisions, byte-verified facts, contract deltas shot 2 must
  close). Read before shot 2 of that module.
- `references/cyberize-shot2-resumption-20261101.md` — resumption-session record; now covers BOTH
  turns of 2026-11-01: first turn's inspection outcomes + second turn's finish-sweep (menu captures,
  nav walk, contrast/touch/reduced-motion/branding checks) and final handoff state.
- `references/wbm-evidence-sweep-workflow.md` — the class-level finish-sweep recipe (gap
  classification, consolidated browser script, composite-grid batching, record reconciliation,
  handoff write-up); this module's two resumption records are its worked examples.