# First WBM — Cyberize Group POC (worked example)

Session date 2026-10-28. The first end-to-end WBM the Web Architect assembled. Use as a concrete
shape reference, not a template to copy client content from.

## Project shape

- Project root: `/home/moose/web-factory/projects/cyberize-poc/`
- Module root: `WBM/` (module ID `cyberizegroup_p1_wbm`)
- Website repo: `https://github.com/ahmedmusawir/web-factory-poc-site-1.git`
- Engineering branch `cyberizegroup_p1_wbm`; QA branch `qa/cyberizegroup_p1_wbm`
- Starter (reference, never modify): `/home/moose/nextjs/web-factory-nextjs-starter-v1`
- Scope: 3 pages (Home, Services, Contact), local content + local images. Payload/Supabase/auth/CMS
  deferred. Primary CTA "Let's talk" → `/contact`, phone-only (no form/booking/email).

## File tree produced

```
WBM/
├── README.md · WBM_ENTRY.md · WBM_STATE.md · WBM_RULINGS.md · EXECUTION_PLAN.md
├── FIRST_WBM_LEARNING.md · EVIDENCE/README.md
├── playbook/ 00-OVERVIEW · 01-RECON · 02-CONTENT-MODEL · 03-TEMPLATES · 04-CONTENT-LOAD · 05-PUBLISH-LOOP · 06-SELF-CHECK
├── verification/ GATES.md · BUILD_CHECKLIST.md
└── QAM/ QAM_ENTRY · QAM_STATE · QAM_PREFLIGHT · QAM_RISK_REQUIREMENTS · QAM_MANIFEST
         QAM_RECON_REPORT · QAM_TEST_PLAN · QAM_APPROVAL · QAM_EXECUTION_REPORT
         AC_EVIDENCE_MATRIX · FINDINGS · QAM_CLEANUP_REPORT · QAM_CERTIFICATION
         HANDOFFS/ENGINEERING_HANDOFF.md · GOVERNING/README.md · AUTOMATION/README.md · evidence/README.md
_site/ SITE_BRIEF.md · CONTENT_MODEL.md · ACCEPTANCE_SPEC.md · INTAKE_SUMMARY.md   (project root)
```

Note: `CLAUDE.md` / `AGENTS.md` omitted (blocked filenames — see SKILL.md pitfalls; recorded as R-008).

## The FFM structural reference

`references/successful-ffm/FFM-ABM-001-SUBSCRIPTION-PORTAL_v1_0.zip` was the supplied completed-FFM
example. Reused its *structure* only: root `FFM_ENTRY`/`STATE`/`RULINGS`/`ACCEPTANCE_SPEC`/
`ACCEPTANCE_LEDGER`/`EXECUTION_PLAN`/`RETROSPECTIVE`, and the full `QAM/` file set with every result
field empty (`NOT EXECUTED` / `PENDING` / `NOT AUTHORED`). Adapted names to the WBM playbook
(`WBM_ENTRY.md`, `WBM_STATE.md`, `WBM_RULINGS.md`) and dropped FFM-specific subjects (mock service
layer, auth gate, Stripe/billing, personas, themes) that have no website POC equivalent. Inspected by
extracting to `/tmp/ffm-ref`; the original ZIP was left unchanged.

## Rulings written (R-001 … R-008)

- R-001 POC scope + deferrals (Payload/Supabase/auth/CMS/form/booking/email/blog … deferred).
- R-002 Primary CTA "Let's talk" → `/contact`; contact phone-only.
- R-003 Provisional phone/address (`(800) 983-0668` / `+18009830668`; `3110 Hatton St Sarasota, FL`);
  email omitted.
- R-004 Copy discipline (no guarantee/timeline/result/ranking/count/testimonial).
- R-005 Starter's prior QA is baseline, not certification of this website.
- R-006 No deployment authorized by module assembly (Gate D excluded).
- R-007 No invented governing provenance — `QAM/GOVERNING/` holds pointers, not playbook copies.
- R-008 `CLAUDE.md`/`AGENTS.md` omitted (environment guard); `WBM_ENTRY.md`/`QAM_ENTRY.md` carry the role.

## Acceptance spec (12 ACs)

AC-01 clean build · AC-02 navigation/404 · AC-03 responsive (390/≥1200, ≥44px, no overflow) ·
AC-04 content render + hide-on-empty · AC-05 structured content (no JSX literals) · AC-06 CTA + tel: ·
AC-07 no form/booking/email · AC-08 provisional flag on/off · AC-09 copy discipline ·
AC-10 design fidelity vs PNGs · AC-11 accessibility (AA, one H1, focus, reduced-motion) ·
AC-12 Lighthouse a11y ≥90 on Home+Contact (perf/SEO recorded only).

A "standing-AC applicability" table in ACCEPTANCE_SPEC.md marks CMS edit loop / image loop / media
storage / access / forms / migration as N/A with reasons — never silently dropped.

## Gotchas that actually fired this session

1. **Phone masking**: `read_file`/`search_files`/`grep`/`xxd` ASCII all rendered `+180****0668`, but
   `od -c` and `xxd` hex showed the true `+18009830668`. Filed a false "masked tel:" defect, then
   retracted it on byte-level proof. Verification recipe: `grep -c '8009830668'` → 4 per file proves
   the full digits are present; `grep -ac 'tel:+180\*\*\*\*0668'` → 0 proves no asterisks on disk.
2. **Copy-compliance drift**: the design spec §12 claimed the 30-day guarantee and 6–8-week timeline
   were "Omitted per brief" while the HTML still contained them. Grep rendered pages, not the summary.
3. **Markup validity invisible to DOM checks**: duplicate `<main id="main">` + stray `</footer></footer>`
   survived `check.py` (contrast/overflow/headings only) because the browser silently repairs them.
   The Designer's fix was at the generator (`build_pages.py`), not the output.

## Pending gate at assembly

Tony's visual approval of the design package was NOT recorded — the module shipped as DRAFT with that
single gate named in `WBM_STATE.md` + `WBM_RULINGS.md`. Shot 1 (read-only recon + plan) was released;
build/QA gated on the approval.
