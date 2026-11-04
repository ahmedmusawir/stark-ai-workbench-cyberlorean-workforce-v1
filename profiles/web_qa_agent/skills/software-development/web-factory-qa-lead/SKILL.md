---
name: web-factory-qa-lead
description: "Run Web Factory WBM QA Lead two-shot website certification."
license: MIT
version: 1.0
author: web_qa_agent
metadata:
  hermes:
    tags:
      - web-factory
      - qa
      - wbm
      - qam
      - acceptance-criteria
      - playwright
      - lighthouse
      - accessibility
      - visual-fidelity
      - nextjs
    related_skills:
      - dogfood
      - systematic-debugging
---

# web-factory-qa-lead

## When to use

Use when you are assigned as the independent Web QA Lead for a Stark Web Factory Website Build Module (WBM) and need to:

- Plan Q1 recon and test planning for a Next.js website candidate (local-content POC or Payload-hub site).
- Execute and adjudicate Q2 independent verification of the 12 standard WBM acceptance criteria.
- Produce `QAM_RECON_REPORT.md`, `QAM_TEST_PLAN.md`, `QAM_APPROVAL.md`, `QAM_STATE.md`, `QAM_EXECUTION_REPORT.md`, `FINDINGS.md`, `QAM_CLEANUP_REPORT.md`, or `QAM_CERTIFICATION.md`.

This skill governs the independent QA lifecycle inside a WBM `QAM/` folder. It does **not** cover engineering implementation, deployment, or Git mutation. It is class-level: applicable to any website WBM, not one specific candidate.

## When NOT to use

- Engineering implementation, code repair, or content authoring — use the Web Developer skill/playbook instead.
- Deployment, DNS, or production release — use Web DevOps.
- Design creation or visual concept work — use Web Designer.

## Triggers

- User assigns: "KIMI — CYBERIZE INDEPENDENT QA, SHOT Q1 ONLY" or equivalent.
- You must read `WBM/WBM_ENTRY.md` and `WBM/QAM/QAM_ENTRY.md` first.
- A committed candidate SHA is supplied on a `qa/<module>` branch.
- Engineering handoff exists but is explicitly not a QA result.

## Hard boundaries

- **Independent of engineering.** Never adopt engineering PASS claims as QA results. Engineering evidence is `CLAIM`; QA produces `EVIDENCE`.
- **No product edits.** QA can create disposable helpers and temporary content edits that are restored; never commit or modify product code.
- **No Q2 without release.** Q1 = recon + plan + QA Lead approval + Director release. Do not begin the Q2 test campaign or issue a verdict/certificate until Q2 is released.
- **No publication or deployment certification.** Gate D is separate and Director-controlled.
- **No credential values** in any evidence, log, or reply.

## Required read order (do not skip)

1. `WBM/WBM_ENTRY.md` — dispatch, current ruling, read order.
2. `WBM/WBM_STATE.md` and `WBM/WBM_RULINGS.md` — latest attributed ruling overrides historical holds.
3. `PROJECT_GUIDE.md` — project-specific POC rulings and folder mapping.
4. `_site/SITE_BRIEF.md`, `_site/CONTENT_MODEL.md`, `_site/CONTENT_CONFIRMATIONS.md`, `_site/ACCEPTANCE_SPEC.md` (project-root `_site/`, not `WBM/_site/`, per PROJECT_GUIDE mapping).
5. `WBM/verification/DESIGN_FREEZE.md`, `WBM/DESIGN_REFERENCE_MAP.md`, `WBM/verification/GATES.md`.
6. `_design/<approved-package>/SITE_DESIGN_SPEC.md`, `SECTION_MANIFEST.md`, `PAGE_ROUTE_CONTENT_MAP.md`, `CONTENT_NOTES.md`, `ASSET_INVENTORY.md`.
7. `WBM/QAM/QAM_ENTRY.md`, `QAM_PREFLIGHT.md`, `QAM_RISK_REQUIREMENTS.md`, `QAM_MANIFEST.md`, `HANDOFFS/ENGINEERING_HANDOFF.md`, `GOVERNING/README.md`.

## Candidate identity verification (Q1 first step)

```bash
cd <repo>
git branch --show-current
git rev-parse HEAD
git status --short
git diff --binary | sha256sum
git log --format='%H %s' -1
```

Required outputs:
- Branch matches `qa/<module>`.
- HEAD matches the supplied candidate SHA.
- Worktree is clean (empty diff).
- Commit message and identity recorded.

If the candidate is uncommitted, dirty, or on the wrong branch: **STOP-IDENTITY** and report.

## Design freeze verification

```bash
python3 WBM/verification/check_design_freeze.py
```

Expected: `{"verified": true, "errors": []}`. Record manifest SHA-256. Any mismatch is a **BLOCKED** finding until an authorized successor freeze is recorded.

## Q1 deliverables

Write four documents in `WBM/QAM/`:

| Document | Purpose |
|---|---|
| `QAM_RECON_REPORT.md` | Candidate identity, environment/tools, readiness assessment, risk priorities, Q1-only observations, blockers. |
| `QAM_TEST_PLAN.md` | AC-by-AC independent test plan with methods, expected results, evidence paths, visual coverage, tool limitations, test-data/restoration needs, call budget. |
| `QAM_APPROVAL.md` | QA Lead approval decision, candidate SHA, environment, plan hashes, conditions, next owner. |
| `QAM_STATE.md` | Current state: Q1 complete / awaiting Q2 release. |

Default response format for the user summary (use exact vocabulary from the verdict set):

1. **Candidate and package** (SHA, package name, hashes).
2. **Decision** (approve / amend / hold).
3. **Findings and dispositions** (if any from Q1 recon).
4. **Limitations and untested areas**.
5. **Next owner and next permitted action**.

Keep the summary concise and include exact file paths and hashes.

## Q2 planning principles

### AC-by-AC coverage

Map every numbered AC in `ACCEPTANCE_SPEC.md` / `GATES.md` to one of:

- **Independent test** with method + expected result + evidence path.
- **Applicability ruling** (e.g., CMS loop N/A for local-content POC; auth/multi-tenant N/A without second site).
- **BLOCKED** disposition if a required input/tool is missing.

Never relabel a failed or untested required AC as PASS.

### Visual coverage (budget-conscious)

- Capture **14 canonical full-page PNGs** (7 pages × 1440/390, DPR2, matching reference browser).
- Re-generate section-comparison tiles **independently for a stratified subset** of pages (e.g., the page with the biggest positioning risk and the page with the most complex tiles).
- **Inspect engineering's existing tiles** for the remaining pages as supplementary claim evidence, but explicitly note this limitation.
- Capture expanded Services menu and FAQ states at both canonical widths.
- Record intermediate-width overflow probes (320/768/899/900/901/1024).
- **After capture, write a `VISUAL_ADJUDICATION.md`** that records exact page/viewport coverage, expanded-state coverage, and discrepancy dispositions (including observations that are not defects). This satisfies the amended-plan requirement to "record exactly which page/viewport/sections were inspected and any gaps."

Do not repeat expensive image calls merely to match an engineering count.

### Accessibility and baselines

- axe-core via Playwright injection per route.
- One H1, heading order, skip-link focus, keyboard Escape/focus restoration.
- Computed contrast helper; note any large-text exceptions explicitly.
- Reduced-motion check (`transitionDuration`, `animationName`, `scroll-behavior`).
- Lighthouse 13.6.0 (or current) with `CHROME_PATH` set to Playwright Chromium, categories performance/accessibility/seo for Home + 1–2 further pages.
- Record tool version, URL, environment.

### Tool limitations to declare

- Screen-reader reading order beyond semantic structure is untested without an AT tool.
- Cross-browser matrix is untested beyond the canonical Chrome/Chromium; proportionate for POC.
- Lighthouse is a local static-build baseline, not a production performance claim.

### Evidence lane

All Q2 evidence goes under `WBM/QAM/evidence/qa-q2/` with timestamps. Engineering evidence at `WBM/EVIDENCE/engineering/` is referenced but never overwritten.

## Test data and restoration

For local-content edit/restore and provisional-toggle tests:

1. Read original bytes of the target file(s).
2. Make a temporary change with a visible QA marker.
3. Rebuild and verify render.
4. Restore original bytes and assert `file.read_bytes() == original_bytes`.
5. Run `git status` to confirm no persistent change.

If the file is JSON, use `json.dumps(..., ensure_ascii=False, indent=2)` and preserve trailing newline if present.

## Call budget

Plan Q2 to fit a single extended session. Typical website WBM Q2 requires:

- Build/setup: ~4 calls.
- Routes/404/links: ~3 calls.
- Navigation/responsive/touch: ~4 calls.
- Content edit/restore + provisional toggle: ~4 calls.
- Asset/font/fallback: ~3 calls.
- Visual capture + review: ~10–14 calls + vision analyses.
- Accessibility/Lighthouse: ~4 calls.
- Metadata/branding/cleanup: ~3 calls.
- Reporting: ~2 calls.

Total: ~37–45 direct tool calls + vision analyses.

## Handling amendments after Q1 approval

When Tony/JARVIS approves Q2 **with plan amendments** (as happened for Cyberize POC):

1. Do **not** treat the new instruction as a fresh recon cycle. It is the second QA shot under the approved (then amended) plan.
2. Record amendments in `QAM_TEST_PLAN.md` and `QAM_APPROVAL.md` before executing; preserve the original Q1 documents as history in `WBM/QAM/HANDOFFS/q1-history-<YYYYMMDD>/`.
3. Remove any unsupported placeholder hashes from `QAM_APPROVAL.md` / `QAM_STATE.md`; replace them with reproducible hashes of the actual amended package and document the exact inputs and method.
4. Re-verify candidate identity immediately before Q2 execution: branch, HEAD SHA, clean worktree, and design freeze must still match.
5. Execute the amended plan literally. Typical amendment categories:
   - Independent full visual coverage of all pages at canonical widths (not only sampling engineering tiles).
   - Expanded menu / FAQ state captures at both widths.
   - Intermediate-width boundary probes (320/768/1024 plus 899/900/901).
   - Exact assertion of approved source values (phone, metadata) against the frozen reference, not against engineering audit JSON.
   - Asset hashes compared to the actual frozen design package, not to engineering claims.
6. If a finding emerges from the amended checks (e.g., phone `tel:` value is masked in the approved source itself), classify it as a contract gap / pre-existing defect when the implementation matches the approved source, not as a product acceptance failure.
7. If an intermediate check fails due to a QA-helper bug, fix the helper, preserve the failure observation, and rerun. Do not discard failed observations that informed the final disposition.
8. After execution, delete temporary QA helper scripts from the candidate repo, restore any mutated source bytes, run a clean rebuild, and confirm `git status` is empty before issuing the verdict.

## Q2 verdict vocabulary (exact words only)

- `PASS`
- `PASS WITH FOLLOW-UP FINDINGS`
- `PASS WITH KNOWN RISK`
- `FAIL`
- `BLOCKED`

A failed required AC stays `FAIL` until repaired and retested or until an explicit authorized contract exception is recorded. A follow-up finding is outside the module's acceptance scope by definition.

## Certification reconciliation without restarting QA

When taking over completed Q2, preserve valid tests and snapshot current records with hashes before corrections. Keep raw failures; label superseded interpretations rather than rewriting raw results. Retest only the disputed requirement/evidence condition and affected regression.

- Tool output may redact public phone-like values. Never infer literal asterisks from a displayed string. Test actual source/DOM equality, E.164 format, digit/asterisk counts and SHA-256 in process; store safe structured assertions. Retract a false finding explicitly.
- Browser availability or Lighthouse userAgent does not prove the screenshot process browser. Record actual launched version/executable, DPR, viewport, device emulation, loaded fonts/images. A mismatched/unrecorded canonical browser condition can be repaired with bounded matched-reference/candidate captures; preserve original tests. Check freshly rendered references against frozen PNGs.
- Static content/CMS deferral does not by itself waive optional-empty tests. Use approved-plan conditional applicability only when the manifest/model designate no current optional section; enumerate actual sections/code and do not remove required fields as a fake optional test.
- Extracted candidate metadata is not an approved-reference comparison. Compare exact title/description values against the actual frozen authority, preserving all mismatches. If distinct descriptions are required but frozen HTML supplies a shared one, route the contract conflict to Architect/Director; do not invent approval or silently pass substitute copy.
- Raw HTML/entity/whitespace heading matching can yield false missing headings. Preserve the failed parser output and compare normalized DOM headings/section order before disposition.
- Reconcile certificate, state, matrix, findings, execution, cleanup and approval together using actual AC numbering. Keep self-hashes out of their own files; use an independent hash manifest and external ZIP hash sidecar. Verify archive CRC, each archived file and original raw-evidence preservation.
- Stopping an npm process wrapper can leave its next-server child listening. Identify only the QA-owned child, terminate it, and verify the port free; do not claim cleanup from wrapper termination alone.

## Pitfalls

- **Approving a plan from the Executor's summary.** Read the package.
- **Edit loop tested by reading code.** For local-content POC, actually edit JSON, rebuild, render, restore.
- **Visual review replaced by pixel-diff threshold.** Use human adjudication; only raster anti-alias/glyph differences are dismissible.
- **Adopting engineering PASS claims.** Always independently verify or explicitly disposition as claim evidence.
- **Forgetting the 900px boundary.** Test 899/900/901 explicitly.
- **Overwriting historical evidence.** Never touch `WBM/EVIDENCE/engineering/` or starter screenshots.
- **Recording credential values.** Never.
- **Leaving temporary QA helpers in the candidate repo.** Any Playwright spec, helper script, or content mutation must be reverted and the worktree returned to clean before issuing the verdict. Run `git status --short` after the final clean build.
- **Running Lighthouse against a stopped server.** The Playwright `webServer` may exit after tests; for Lighthouse, start `npm run start -- --hostname 127.0.0.1` in the background and terminate it after the runs.
- **Using `bs4` or other venv-only packages from `execute_code`.** The sandbox interpreter may lack them. Use stdlib regex/string tools inside `execute_code`, or run Python via `terminal` using the project venv.
- **Silently skipping a contractual check.** If a test must be skipped, document the reason and acceptance impact in `FINDINGS.md` and `QAM_EXECUTION_REPORT.md`. Never let a skipped required check become an implicit PASS.

## References

- `references/session-template.md` — condensed Q1/Q2 session recipe and file checklist.
- `references/cyberize-poc-q1-20261101.md` — concrete example from the first Cyberize POC Q1 (candidate SHA, hashes, plan structure, budget).
- `references/cyberize-poc-q2-20261101.md` — concrete example from the first Cyberize POC Q2 (amendments, executed checks, skipped-test rationale, findings, verdict, ZIP hash).
- `templates/playwright-qa-spec.md` — reusable Playwright QA spec template for static Next.js WBM candidates.

## See also

- Web Factory constitution: `WBM_PLAYBOOK.md` §5, §8.
- QA doctrine: `QAM_PLAYBOOK.md`, `QA_PLAYBOOK.md`, `TESTING_PLAYBOOK.md`.
- Role instructions: `WEB_QA_LEAD_INSTRUCTIONS.md`, `WEB_QA_LEAD_PLAYBOOK.md`.
