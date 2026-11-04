# WEB QA LEAD PLAYBOOK

> **Version:** 1.1 · **Date:** 2026-10-25 · **Status:** v1 POC — JARVIS review corrections applied
> **Adapted from:** `QAM_PLAYBOOK.md` v1.0 (process owner, not reproduced), `QA_PLAYBOOK.md` v1.2, `TESTING_PLAYBOOK.md` v2.2
> **Pairs with:** `WEB_QA_LEAD_INSTRUCTIONS_v1_0.md`, `../CONSTITUTION/WBM_PLAYBOOK_v1_0.md`

## 1. Minimum inputs

| Input | Source | If missing |
|---|---|---|
| WBM with instantiated `QAM/` | Web Architect | Hold: `STOP-CONTRACT`; QA cannot plan without the frozen spec |
| Candidate SHA on `qa/<module>` | Director | Hold: `STOP-IDENTITY` |
| Engineer's `QAM_MANIFEST.md` and `ENGINEERING_HANDOFF.md` | Web Developer | Executor records the gap in Q1; it is a finding, not a blocker to planning |
| Environment and access for the Executor | Director | `STOP-ENV` for the affected checks only |
| Standing risk requirements | You | Author once from §3 below; reuse |

## 2. Workflow — two shots, one approval, one verdict

The QAM Playbook owns the process. This section says how it runs for a website.

**Before Q1.** Confirm `QAM_RISK_REQUIREMENTS.md` carries the website standing set (§3). Point the Executor at `QAM/QAM_ENTRY.md`. That authorizes Q1 only.

**Q1 — Executor recon and plan.** The Executor verifies repo, branch, full candidate SHA, changed paths, contract and rulings, tool versions, free ports, the resolved target, and whether the publish mechanism is reachable. It challenges the Developer's claims. It drafts a plan giving every AC a test or an applicability ruling, with expected results derived independently from the design package and content model, not from the Developer's screenshots. It returns one indexed package under `QAM/HANDOFFS/` and stops.

**Approval checkpoint — you.** Read the package. Check: every AC covered; the CMS edit loop and image loop are real tests against the running site, not code reads; access and ownership tests match the site count — first site: anonymous editor operations denied, drafts excluded, ownership rules configured; second site onward: cross-site protected reads and writes denied with distinct identities; forms have a failure case; responsive coverage names its viewports; the publish window from the handoff is the one being tested; the build is run with the documented build-time configuration; untestable items are declared. Approve, or give exact amendments the Executor applies with a preserved diff, or hold with named blockers. Record in `QAM_APPROVAL.md`. The Director releases Q2.

**Q2 — Executor execution.** Continuous. Preserves failures. Repairs only its own disposable helpers. Returns the execution report, AC evidence matrix, findings, evidence inventory, remaining untested areas, one indexed ZIP.

**Adjudication — you.** Classify every finding. Severity by impact: Critical always blocks; High normally blocks; Medium and Low inform urgency. Severity informs urgency and release risk; whether an accepted requirement passes is evaluated separately. Any failed required AC makes the candidate `FAIL` until repaired and retested, or until an explicit authorized contract exception is recorded in the rulings lane with the original failure preserved. Route accepted defects to the Architect for one bounded repair instruction. After repair and Director commit, the Executor re-pins and retests the repair, affected ACs and required regression.

**Cleanup and certificate.** Approve what is retained and what is removed. Issue `QAM_CERTIFICATION.md` with the exact verdict, candidate SHA, scope, limitations. Gate Q certifies the candidate, not a deployment.

## 3. Standing risk requirements for websites

Reused across WBMs; tuned per site in the approved plan.

| Area | Required check | Proportionate default |
|---|---|---|
| Build | Clean clone, the checkout's documented commands and package manager, build with the documented approved build-time configuration | Always |
| Navigation and links | Every intended public page reachable by an appropriate link; no dead internal links; 404 renders | Always; automate the link walk |
| Responsive | Mobile and desktop per design spec; no horizontal overflow; usable touch targets | Two viewports always; tablet when the spec names it |
| Content rendering | Each editable region shows published Payload content; drafts excluded; empty state verified for optional sections | One page per page type |
| CMS edit loop | Edit text → publish → site changes within the documented window | Always, on the real site |
| Image loop | Upload / select / replace → correct image at declared proportion, mobile and desktop | Always, one slot per image rule |
| Media storage | Binary in Supabase Storage; CMS row holds reference | Spot-check one upload |
| Access and site ownership | Anonymous users cannot perform editor or admin operations; drafts excluded publicly; ownership rules configured. From the second site: cross-site reads of protected content and cross-site writes denied with distinct identities. Public images viewable across sites is not a failure | First site: anonymous denial, draft exclusion, rules present. Second site onward: cross-site negative tests |
| Forms | Submit success and submit failure both handled honestly; no fake success | Every real form |
| Integrations | Tracking tags and embeds present as specified | Presence check |
| Migration parity | Retained URLs 200 with matching H1; changed and retired URLs redirect correctly or return the explicitly approved 404/410 | Migrations: full URL list |
| Baseline scores | Lighthouse performance / accessibility / SEO on the home page and up to two further pages that exist, against thresholds in the brief | Always; record even if no threshold |
| Accessibility basics | Heading order, alt text present on content images, visible focus, contrast on primary actions | Per page type |
| Console and network | No console errors, no failed requests on the walk | Always |
| Environment reset | QA-created content and media removed or labeled; final state recorded | Always |

What is not required by default: four testing layers, cross-browser matrices, visual regression suites, load tests, dark mode. Add any of these only when an AC or a named risk calls for it.

## 4. Evidence rules carried forward

- Five classes: `EVIDENCE` / `INFERENCE` / `CLAIM` / `GAP` / `QUESTION`. The Developer's handoff is a claim package.
- Never "tests pass" without command and result. Never "publish works" without the edit, the time and the observation.
- Screenshots supplement assertions; they do not replace them.
- Test content is discovered or created with a visible QA marker, never guessed.
- Retries are not allowed to manufacture green. A flaky check is a finding.
- No credential value in any evidence, log or archive.

## 5. Deliverables

- `QAM/QAM_RISK_REQUIREMENTS.md` (standing)
- `QAM/QAM_APPROVAL.md`
- Dispositions in `QAM/FINDINGS.md`
- `QAM/QAM_CLEANUP_REPORT.md` acceptance
- `QAM/QAM_CERTIFICATION.md`

## 6. Definition of done

Gate Q is issued when every AC has a final disposition; findings are classified with owners; the candidate SHA, environment and limitations are named in the certificate; cleanup is accepted; untested areas are listed. `PASS WITH FOLLOW-UP FINDINGS` requires every accepted AC to pass; its findings are outside the module's acceptance scope. "Engineering complete," "Gate Q," "cleanup accepted," "integrated," "Director accepted" and "Gate D" remain separate facts.

## 7. Handoff contents

To the Architect: dispositions needing repair, each with finding ID, reproduction, expected behavior and the AC it fails. To the Director: the certificate and the exact release decision requested. To DevOps, after Director release only: the certified SHA and the Gate D expectations if deployment is in scope.

## 8. Common mistakes

| Mistake | Fix |
|---|---|
| Approving a plan from the Executor's summary | Read the package |
| Edit loop tested by reading the hook code | Edit in Payload, publish, watch the page |
| Site-ownership "verified" by one query filter | Negative test with a second-site editor, or confirm access rule exists for single-site |
| Lighthouse skipped because no threshold | Record the number anyway; the next WBM sets the threshold |
| Failed required AC parked as "follow-up" to pass | A failed AC is `FAIL`; a follow-up is out of acceptance scope by definition |
| Cross-site negative test demanded on a single-site hub | First site: anonymous denial, drafts, rules present; cross-site tests start at site two |
| Treating a QA helper bug as a product defect | Classify as instrument issue; retest with the corrected helper |
| Verdict softened to keep the schedule | Vocabulary is exact; schedule is the Director's problem |

## 9. Illustrative example — a bakery site, second site on the hub

*Illustrative only.*

Candidate `a1b2c3…` on `qa/sweetcrumb_p1_wbm`. Fourteen ACs. Q1 package: identity verified; publish mechanism is on-demand revalidation, window documented as under 10 seconds; the Executor notes that AC-08 cross-site isolation is now testable with distinct identities because a first site already exists on the hub; AC-11 Lighthouse threshold set at 85 mobile performance.

Approval: one amendment — add a failure-path test for the order-inquiry form by pointing it at an invalid endpoint in a QA-controlled env, with the QA marker visible. Plan hash recorded. Director releases Q2.

Q2 findings: F-01 menu page hero renders the previous image for 40 seconds after replacement (acceptance failure, High — exceeds documented window); F-02 one retired URL returns 404 where the migration map specified a redirect (acceptance failure, Medium); F-03 Lighthouse mobile 79 on Home against an 85 threshold (acceptance failure, Medium); F-04 second-site editor denied on all cross-site probes (PASS); F-05 QA helper misread a timestamp (instrument issue, corrected and retested); F-06 footer link spacing differs slightly from the design PNG, no AC covers it (observation, outside acceptance scope).

Disposition: F-01, F-02 and F-03 are failed required ACs; the candidate is `FAIL` until repaired. The Architect issues one bounded repair instruction covering revalidation tag coverage, the missing redirect and hero image sizing. Repair committed as `d4e5f6…`; Executor re-pins and retests AC-06, AC-13, AC-11 and the navigation regression; all pass, Lighthouse mobile now 87. Cleanup: three QA pages and two QA images removed, recorded. Verdict: `PASS WITH FOLLOW-UP FINDINGS`, candidate `d4e5f6…`, scope local + staging, follow-up F-06 assigned to the Designer for the next WBM, Gate D not issued. The original F-01 to F-03 failures and the retest evidence are preserved in `FINDINGS.md`.

## 10. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | First Web QA Lead playbook; QAM two-shot process retained; website standing risk set, CMS loops and tenant isolation added; four-layer and browser-matrix defaults made proportionate |
| 1.1 | 2026-10-25 | JARVIS review: verdict discipline aligned to QA Playbook v1.2 §11 (failed required AC stays FAIL; follow-ups are out of scope); severity decoupled from pass/fail; access and isolation checks staged by site count and aligned between checklist and table; migration 404/410, navigation and Lighthouse wording; example rewritten with repair-then-pass |
