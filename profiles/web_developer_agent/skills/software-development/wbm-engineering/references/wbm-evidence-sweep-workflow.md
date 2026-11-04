# WBM evidence sweep — finishing an inherited incomplete engineering shot

Class-level recipe. Use when an assignment resumes a WBM engineering shot whose handoff reports
"implementation complete, verification incomplete" with an AC table carrying UNVERIFIED/partial
entries — and the operator's authorization is to FINISH the existing work and write the handoff,
not to rebuild. Worked example: `cyberize-shot2-resumption-20261101.md` (two turns, same module).

## 1. Reconcile the record before doing anything

Operators check your numbers. The prior handoff/summary may carry arithmetic slips (e.g. a summary
message totaling 106 when the unique inventory was 94 — auxiliary inspection calls added into a
unique-tile count).

- Disk-audit the evidence inventory in one script: actual files per folder vs the index JSON vs the
  counts the record asserts (e.g. `os.listdir` per `comparisons-chrome/<pair>/` vs
  `comparisons-chrome/index.json` vs handoff text).
- Separate "unique inventory" counts from "total actions" counts and state both explicitly in the
  review record. Record the correction prominently — do not silently adopt either number.
- Re-verify the inheritable identity facts (branch/HEAD/diff-hash/untracked hashes) so the new
  handoff can assert "unchanged by this session" if true.

## 2. Read the acceptance spec and classify every remaining gap

For each open item in the handoff's gap list, classify against the actual AC text:

- **Mandatory and doable** → schedule it (state captures, navigation walk, touch targets,
  reduced-motion, contrast, branding/claims scans, empty-state tests).
- **Not applicable** → disposition with the reason from the contract (e.g. "no optional-empty
  sections exist in the approved package", "references only exist at 1440/390 so intermediate
  widths verify overflow only").
- **Genuinely unavailable** → UNVERIFIED with the specific tool/environment reason (e.g. no
  screen-reader in the environment). Never silently downgrade; an unverified required AC is
  reported, not relabeled.

## 3. One consolidated browser script for all remaining state/functional checks

Do not spread browser work across many one-off invocations. Write ONE Node script (Playwright,
system Chrome via `executablePath`) that emits one JSON with all outputs, e.g.
`finish_checks.cjs` → `finish-checks.json`. Proven contents:

- **State captures** for every remaining page × width (exact reference interaction sequence — read
  2–3 frozen references FIRST to pin the state contract, then script it).
- **Real navigation walk**: from every page, click brand → wait URL → assert `/`; every Services
  panel link → wait URL → assert its route; header CTA → `/contact`. See the URL-wait pitfall in
  SKILL.md.
- **Open-state touch measurements** (390px, menus/FAQ open) alongside the previous session's
  closed-state numbers.
- **Reduced-motion probe** (Playwright `reducedMotion: 'reduce'`; assert computed
  `transitionDuration/animationName` neutralized on a real element).
- **Branding/claims scans** on rendered `document.documentElement.textContent` (starter names;
  excluded commercial/booking/guarantee terms).
- **Contrast measurement**: computed `color`/`backgroundColor` (ancestor walk for effective bg) /
  `fontSize` / `fontWeight` for a fixed selector list per route, classified with the WCAG
  large-text rule (≥24px/18.66px bold = 3.0:1; else 4.5:1). Record the qualifying size for any
  sub-4.5 pair.

If a check fails on instrumentation (not the product), fix the script and re-run only that section
if separable — else re-run the whole script; it is cheap by design.

## 4. Batch the vision review

- Composite grids (PIL): stack N reference/implementation pairs vertically with labels, 6 pairs per
  grid → 12 state captures reviewed in 4 vision calls. Full recipe in SKILL.md §Visual-fidelity.
- Reuse the existing tile index and prior inspection record; only inspect what is NEW or was
  previously uninspected.
- Budget guard: if the remaining calls cannot fit, checkpoint (skill reference file listing exact
  remaining steps + owned processes) BEFORE writing handoff documents — a checkpoint without
  handoff updates is recoverable; handoff text asserting completed checks is not.

## 5. Close out: identity, freeze, cleanup, documents

1. Re-run the design freeze checker after all writes.
2. Refresh the untracked-file hash inventory (new evidence files are outside the repo; repo files
   should hash-match the previous inventory — assert that explicitly).
3. Re-assert the tracked diff hash is unchanged (proof the sweep made no repo source changes).
4. Stop owned background processes (verify port free after; name any process NOT owned and left
   running).
5. Write the three documents (QAM_MANIFEST, ENGINEERING_HANDOFF, WBM_STATE) in one pass: corrected
   counts, per-AC dispositions, actual commands + outputs, remaining limitations, candidate
   uncommitted, no-QA-claim boundary.
6. End with a readiness decision + exact remaining blockers, not a preparation summary.

## Anti-patterns (each one drew operator correction)

- One-image-per-turn review of a large tile/state set — batch with composites.
- "Preparation-only summary" while authorized work remains — the sweep continues to completion or
  checkpoints with exact remaining steps.
- Counting assertions not backed by a disk audit — reconcile first, cite the audit.
- Storing aggregate booleans (green/dim) instead of per-item outcomes in check JSONs.
- Claiming inspection of artifacts the session never opened with a vision-capable tool.