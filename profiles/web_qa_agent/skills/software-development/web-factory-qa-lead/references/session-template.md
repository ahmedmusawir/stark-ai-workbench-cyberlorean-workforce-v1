# Q1/Q2 session recipe — Web Factory WBM QA Lead

## Pre-flight

- Confirm role assignment is Q1-only or full Q1+Q2.
- Locate WBM root (`.../WBM/`); project `_site/`, `_design/`, `_infopack/` may be at project root per `PROJECT_GUIDE.md` mapping.
- Verify candidate repo path, branch, and SHA.
- Confirm no product edits; only disposable QA helpers and temporary content edits that are restored.

## Q1 checklist

1. Read `WBM/WBM_ENTRY.md` → `WBM_STATE.md` → `WBM_RULINGS.md` (latest ruling wins).
2. Read `PROJECT_GUIDE.md` for POC deferrals and folder mapping.
3. Read `_site/*.md` contract files.
4. Read `WBM/verification/DESIGN_FREEZE.md`, `DESIGN_REFERENCE_MAP.md`, `GATES.md`.
5. Read approved design package: `SITE_DESIGN_SPEC.md`, `SECTION_MANIFEST.md`, `PAGE_ROUTE_CONTENT_MAP.md`, `CONTENT_NOTES.md`, `ASSET_INVENTORY.md`.
6. Read `QAM_ENTRY.md`, `QAM_PREFLIGHT.md`, `QAM_RISK_REQUIREMENTS.md`, `QAM_MANIFEST.md`, `HANDOFFS/ENGINEERING_HANDOFF.md`, `GOVERNING/README.md`.
7. Verify candidate identity:
   - `git branch --show-current`
   - `git rev-parse HEAD`
   - `git status --short`
   - `git diff --binary | sha256sum`
   - `git log --format='%H %s' -1`
8. Verify design freeze: `python3 WBM/verification/check_design_freeze.py`.
9. Probe tool capability: `npx playwright test --list`, `npx lighthouse --version`.
10. Write `QAM_RECON_REPORT.md`, `QAM_TEST_PLAN.md`, `QAM_APPROVAL.md`, `QAM_STATE.md`.
11. Compute file hashes and combined package hash; return concise summary.

## Q2 checklist (after Director release)

1. Re-verify candidate identity (same SHA, clean worktree).
2. Clean rebuild: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run build`.
3. Routes / 404 / link inventory.
4. Navigation / keyboard / breakpoint / FAQ states.
5. Responsive overflow + touch targets at all widths.
6. Content edit/restore + provisional toggle.
7. Asset hashes + font loads + forced image fallback.
8. Visual capture: 14 canonical PNGs + independent subset tiles + inspect engineering tiles.
9. Accessibility: axe, H1, headings, skip link, contrast, reduced motion.
10. Lighthouse Home + 1–2 further pages.
11. Metadata / starter-branding scan.
12. Cleanup: restore any temporary edits; run design freeze checker; record evidence inventory.
13. Classify findings; issue verdict; write `QAM_EXECUTION_REPORT.md`, `FINDINGS.md`, `QAM_CLEANUP_REPORT.md`, `QAM_CERTIFICATION.md`.

## Verdict vocabulary

Use exact words only: `PASS`, `PASS WITH FOLLOW-UP FINDINGS`, `PASS WITH KNOWN RISK`, `FAIL`, `BLOCKED`.

## Evidence paths

- Engineering evidence: `WBM/EVIDENCE/engineering/` (read-only for QA).
- QA evidence: `WBM/QAM/evidence/qa-q2/<timestamp>/`.

## Common blockers

- `STOP-IDENTITY`: wrong branch, dirty worktree, missing SHA.
- `STOP-ENV`: tool or server not reachable.
- `STOP-EVIDENCE`: cannot export evidence safely.
- `BLOCKED` criterion: required input or tool missing.
- `FAIL`: required AC fails; stays FAIL until repaired + retested or authorized contract exception.
