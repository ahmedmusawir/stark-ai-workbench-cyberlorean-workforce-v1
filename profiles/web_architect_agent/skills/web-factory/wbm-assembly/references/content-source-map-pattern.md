# Content source map pattern (scope grounding + reconciliation)

Session 2026-10-30: Tony reopened the Cyberize three-page scope to a seven-page scope, grounded in
the actual scraper package. This documents the grounding technique and the four-document
reconciliation that follows.

## Trigger

Tony says something like "reopen scope / use the captured evidence directly, not summaries of earlier
conversations." The earlier brief had compressed a full service business into generic cards; the
source had far more substance (five service pages + support + contact + legal + blog).

## Source package layout (Cyberize example)

`_infopack/CyberizeGroup-com-Scraped-Data-For-Architect/`
- `START_HERE.md`, `PACKAGE_MANIFEST.json`
- `outputs/recon/.../INVENTORY.md` + `MENU.md` — full URL inventory + nav (42 pages / 166 posts advertised)
- `outputs/prepared/...-reviewed/pages/*.md` — 6 captured pages (Home, SEO, PPC, Web Design, Web Dev, Growth Call)
- `.../METADATA_REVIEW.json` — title/description/canonical/JSON-LD per page
- `.../BOILERPLATE.md` — header/footer nav + contact + social
- `.../GAPS_AND_REQUESTS.md` — honest gaps
- brand references (Tony-supplied): `_infopack/brand_reference/` — `logo.png` (260×84) + 10 current-site
  screenshots (3840×2160 desktop, 1295×2149 / 1363×2149 mobile)

## Inventory checklist

1. Captured pages + substance (heading/paragraph counts).
2. Navigation (header dropdown + footer columns).
3. SEO metadata per captured page (title, meta description, canonical, og:image, JSON-LD org).
4. Media: downloaded files vs URL-only references. No vision tool? Use `file *.png` for dimensions.
5. Referenced-but-uncaptured pages (the gaps) — name them, don't invent them.

## Map table columns

`source URL | evidence file | proposed destination | disposition | reason`

Disposition vocabulary: **retain / rewrite / combine / omit / defer / new**. "Defer" (vs "omit") =
an explicit out-of-scope decision recorded for a later phase, not a silent drop. A page whose content
was never captured gets "new — assemble from evidence only, do not invent" or "defer".

## Reconciliation (when scope is approved)

Four documents must agree as ONE consistent contract:

- `_site/SITE_BRIEF.md` — the approved scope (page map, CTA, deferrals, assets).
- `_site/SCOPE_PROPOSAL.md` — mark APPROVED; record the page map + deferrals.
- `_site/CONTENT_SOURCE_MAP.md` — dispositions reconciled to the approval (deferred rows marked R-###).
- `handoffs/ARCHITECT_TO_DESIGNER_v2.md` — the corrected Designer contract.

Record the approval as a ruling (`WBM_RULINGS.md`), and update `WBM_STATE.md` status + next owner.
When a prior visual approval is withdrawn, record that too (approval is append-only; never rewrite).

## Traceability requirement

The Designer's `SECTION_MANIFEST.md` must map every section back to `CONTENT_SOURCE_MAP.md` (source
file + disposition). Design-authored material (original headlines, transitions, illustrations, section
arrangements) is allowed where it preserves source-supported meaning, but is labeled "design-authored"
— not silently treated as a business claim.

## Email / contact handling

When the source has no email, **omit it entirely** — do not show a "Not published" card. Contact is
phone + address only (provisional, flagged). No form/booking that claims to send or book.
