# Cyberize POC Q2 example — 2026-11-01

Concrete reference from the first Cyberize website POC Q2 execution and certification, following Q1 amendments from Tony/JARVIS.

## Assignment signal

"KIMI — Q1 REVIEW COMPLETE: AMEND THE PLAN, THEN EXECUTE Q2"
"Tony/JARVIS approves Q2 with the amendments below. Record them before testing."
"Execute the amended AC-01 through AC-12 plan independently."

## Candidate identity (re-verified before Q2)

- Repo: `/home/moose/nextjs/web-factory-poc-site-1`
- Branch: `qa/cyberizegroup_p1_wbm`
- SHA: `822716cd007744cada19b86e65cc9d7860ffc72c`
- Worktree: clean
- Design freeze: verified (`477 files, 0 errors`)

## Amendment handling

1. Original Q1 files preserved to `WBM/QAM/HANDOFFS/q1-history-20261101/`.
2. `QAM_TEST_PLAN.md`, `QAM_APPROVAL.md`, and `QAM_STATE.md` updated to v2.0-Q1A.
3. Placeholder hash removed from `QAM_APPROVAL.md`; replaced with actual SHA-256 hashes of the four QAM files.

## Key executed checks

- Clean build, typecheck, lint: pass.
- Existing E2E suite: 20/20 pass.
- Routes: all 7 pages 200; real 404 rendered.
- Links: 0 `.html` hrefs, 0 dead internal links.
- Responsive: no overflow at 320/390/768/899/900/901/1024/1440; touch targets ≥ 44×44.
- Menu breakpoint reset verified at 899 → 901.
- Content edit/restore smoke: marker rendered, source restored, rebuilt.
- Provisional toggle: `contactProvisional=false` hides notice but keeps phone; restored.
- Visual: 14 canonical full-page PNGs + 14 expanded-menu PNGs + FAQ states; side-by-sides reviewed.
- Accessibility: axe-core 0 violations; one H1/page; heading hierarchy clean; skip link works; image labels verified.
- Lighthouse: Home 99/100/100, PPC 86/100/100, Contact 87/100/100.
- Assets: 17/17 SHA-256 hashes match frozen approved design package.
- Image fallback: blocking `agency-connected.svg` renders accessible `.image-fallback` panel.
- Metadata and starter branding: no leaks detected.

## Findings

- **F-01 (Medium):** Phone `tel:` href is masked as `tel:+180****0668` in both frozen approved design source and implementation. Visible text `(800) 983-0668` is correct. Classified as contract gap / pre-existing defect because implementation matches approved source.
- **F-02 (Low):** Optional empty-section behavior not testable because current static JSON schema has no optional fields (`content()` throws on missing values). Consistent with POC deferral of Payload/Supabase.

## Skipped test

- Playwright project `mobile` skipped explicit 899→901 breakpoint reset.
- Reason: probe intentionally resizes viewport in desktop Chromium to isolate CSS media-query behavior; running under `isMobile: true` would conflate mobile UA/touch emulation with the media query.
- Impact: none; probe still passed in desktop project.
- Documented in `FINDINGS.md` and `VISUAL_ADJUDICATION.md`.

## Visual adjudication record

Added `WBM/QAM/evidence/qa-q2/VISUAL_ADJUDICATION.md` covering:
- All 7 pages × 1440/390 captured and compared.
- Expanded menu and FAQ state coverage table.
- Discrepancy dispositions (one observation: Contact starting-point link underline, not a defect).
- Skipped-test rationale.

## Verdict

`PASS WITH KNOWN RISK`

## Cleanup

- Temporary helper scripts (`tests/qa-q2.spec.ts`, `tests/contrast-reduced.cjs`) deleted.
- Source bytes restored after content/provisional mutations.
- Final clean build passed.
- `git status --short` empty; `git rev-parse HEAD` unchanged.
- Background local server on port 3001 terminated.

## Deliverables

- `QAM_EXECUTION_REPORT.md` v2.0-Q2
- `AC_EVIDENCE_MATRIX.md` v2.0-Q2
- `FINDINGS.md` v2.0-Q2
- `QAM_CLEANUP_REPORT.md` v2.0-Q2
- `QAM_CERTIFICATION.md` v2.0-Q2
- `QAM_STATE.md` v2.0-Q2
- `VISUAL_ADJUDICATION.md` (in evidence/qa-q2/)
- Final ZIP: `/home/moose/Downloads/CYBERIZE_Q2_CERTIFICATION_822716c.zip`
- ZIP SHA-256: `97d0a95e9990a918dca510a7b0a78eec33af8459f077c551af4d0dcbc42dd7e9`

## Lessons for future sessions

- When the approved design source itself masks data (phone, address), the implementation is not defective for reproducing it, but the business must confirm the real values before launch.
- Running Lighthouse requires the dev server to be up; Playwright's `webServer` may exit after tests finish.
- Keep helper scripts outside the repo or delete them before the final build; a clean worktree is part of the verdict.
- Do not use `bs4` from `execute_code` sandbox when the venv lacks it; use stdlib regex or run Python via `terminal` with the project venv.
- Record the rationale for any skipped test explicitly in findings; never silently skip a contractual check.
- Preserve completed evidence and failed observations across the final delivery; do not discard intermediate failures that informed the final disposition.
