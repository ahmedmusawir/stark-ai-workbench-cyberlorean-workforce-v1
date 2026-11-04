# Field notes — cyberizegroup_p1_wbm shot 1 (2026-10-28)

Session-specific record for the first WBM. Read before shot 2 of THIS module. Facts here are
point-in-time; re-verify against `WBM_STATE.md` and the tree on resumption. No secrets.

## Module identity

- Module: `cyberizegroup_p1_wbm` · WBM root: `/home/moose/web-factory/projects/cyberize-poc/WBM/`
- Checkout: `/home/moose/nextjs/web-factory-poc-site-1` · branch `cyberizegroup_p1_wbm` (local, no
  upstream — Tony pushes) · baseline HEAD `445f162` "Initial commit" == main == origin/main
- Starter (protected): `/home/moose/nextjs/web-factory-nextjs-starter-v1`
- Shot-1 deliverables: `WBM/EVIDENCE/E1_RECON.md` v1.0, `WBM/EXECUTION_PLAN.md` v1.0 (all nine
  sections), `WBM_STATE.md` v0.2. Status: awaiting Architect review + Director approval + Tony's
  visual approval (recorded nowhere yet — blocks shot 2).

## Verified toolchain (disk, 2026-10-28)

Node v26.7.0 / npm 11.19.0 (engines >=22 ✓) · next 16.4.3 · react 19.2.4 · **tailwindcss 3.4.19**
(RESOLVES design-spec open item 5 — the 3.4 assumption held) · typescript 5.9.3 · eslint 9.39.4 +
eslint-config-next 16.4.3 · @playwright/test 1.59.1 (chromium 1217/1234 cached; system Chrome
`/usr/bin/google-chrome`). Lockfile sha256 identical to starter's. Port 3001 = run target (dev+prod);
port 3000 owned by unrelated next-server pid 1732858 — never touch. Scripts: `dev`/`start` on
`-p 3001`; `lint` = `eslint . --max-warnings=0`; `typecheck` = `next typegen && tsc --noEmit`;
`test:e2e` = `playwright test` (prod webServer `127.0.0.1:3001`, reuseExistingServer false).

## Baseline numbers (R-005 re-verification, CWD = checkout)

`npm ci` exit 0 · typecheck PASS · lint **FAIL 13 errors** (all `no-require-imports` in
`QAM/evidence/qa-q2/20261028T081836Z/*.cjs` prior-QA helpers; product paths clean; prior QA's clean
lint predates those committed files) · build PASS (static `/` + `/_not-found`) · e2e **2/2** pass.

## Byte-verified design-package facts

- `tel:` hrefs: 12 total (4/page), **zero asterisk bytes** — full dialable E.164 `+180****0668`
  shape (11 digits incl. leading 1). The masked rendering is the Hermes tool-output artefact. The
  number is scraped → stays **provisional** (R-003); transcribe the href from file bytes in shot 2,
  never from rendered output.
- Banned-claim regex scan on design HTML: zero matches. Form/email controls (`<form|<input|
  <textarea|<select|mailto:`): zero matches. Contact page carries the authored "no form … nothing is
  booked online" disclaimer (expected positive text for AC-07).
- "Payment not scheduled until initial deposit" FAQ line = F1-RETAINED commercial term, NOT a banned
  delivery timeline. Do not "fix" it.
- 9 self-host fonts present in `_design/assets/fonts/` (Archivo 500/600/700/800, Inter 400/500/600,
  JetBrains Mono 400/500). Page titles authored. All six QC PNGs present.

## Pending decisions (blockers/questions from the plan, §9)

- B-1: Tony's visual approval — gates shot 2.
- B-2: Lighthouse not installed; default = honest UNVERIFIED claim for AC-12 unless ruled otherwise.
- Q-1: eslint `globalIgnores` += `QAM/evidence/**` (proposed as labeled ASSUMPTION); lockfile commit
  intent for Tony.
- Q-2: `unrs-resolver` postinstall install-scripts warning — advisory/no-action default.
- Q-3/Q-4: reconciled during recon (Contact pageHead meta rows; hero.secondaryCta hide-on-empty).

## Contract deltas shot 2 must close (checkout vs design contract)

Three pages + 404 vs one starter Home · 15 components (SITE_DESIGN_SPEC §3) vs one JS hamburger
header — which VIOLATES the design's CSS-only nav rule (token-map rule 3) and must be rewritten ·
content module per CONTENT_MODEL §2–§7 (site fields incl. separate `phoneDisplay`/`phoneHref`,
`provisional` boolean; nav; 4 service records one shape; home sections; contact cards; ctaBand) ·
Tailwind token map + semantic palette vs stock stone/orange · self-hosted fonts vs system Arial ·
aria-current + anchor scroll-margin vs none · provisional-flag mechanism absent · e2e suite bound to
starter demo copy ("Stark Studio") must be rewritten to the real contract.

## Shot-2 hygiene carry-overs

- The e2e spec writes screenshots to TRACKED `QAM/evidence/*.png` — backup/restore discipline applies
  to any full-suite run before the candidate exists; after shot-2 writes begin, that write must be
  owned and documented in the handoff.
- Content module location: existing `content/site.ts` (satisfies CONTENT_MODEL's "e.g.
  lib/content/site.ts"; single typed module; no dependency change).
- No new npm dependency is permitted for this POC (token-map rule 2); fonts via `next/font/local`
  pointing at copied `woff2` files, never `next/font/google`.

Superseded note: shot 2 ran on a different content-layer shape than recorded here (`content/
cyberize.{ts,json}` with a `content(group, field)` lookup and an `Artwork` client component for the
image-fallback rule — NOT `content/site.ts` or `next/font/local`). Read this file for shot-1 facts
only; `references/cyberize-shot2-resumption-20261101.md` records the implemented reality.