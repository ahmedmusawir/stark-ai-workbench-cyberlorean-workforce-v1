# Homepage-only concepts within larger approved scopes

## Why this matters

A design review can approve the list of seven pages while authorizing only a fresh homepage concept. Building sibling templates early violates the direction gate even if all those pages belong to eventual scope. Earlier directions may be rejected despite historical approval claims. Re-ground from current authority, not a previous completion narrative.

## Tested pattern

1. Read the current brief, source map and handoff. Separate eventual site scope from the present deliverable.
2. Inventory logo/screenshots. Build a labeled contact sheet, then inspect the logo and key desktop/mobile areas larger. Preserve logo bytes and native aspect ratio. A filename alone does not identify a screenshot's contents.
3. Snapshot protected artifacts and authorities before writes; use a new concept folder. Keep original backups when altering approved artifacts. A file with matching length is not evidence of identical bytes; mtime alone does not establish who changed it.
4. Author one responsive HTML page, semantic CSS tokens, local assets and original artwork where allowed. Do not let the rejected concept's HTML/tokens become the new design merely by recoloring them.
5. Record section-level content lineage: retain / rewrite / combine / omit / new-design-authored. Creative headlines and arrangement are not automatically new business facts. Conversely, source marketing language can still be prohibited by the approved brief.
6. Render full-page desktop/mobile PNGs after fonts load. Inspect the full composition plus readable crops of the header, provisional details and any modal states. Extremely tall screenshots can downscale into unreadable strips; a whole-page image is not sufficient legibility evidence.
7. Run layout, contrast, heading, source-markup, image, focus and copy checks. Keep measurements distinct from untested screen-reader/browser/performance coverage.
8. Save a compact completion handoff, then stop at direction approval rather than assembling a full site design package.

## Unbuilt routes: honest interaction instead of fabricated pages

A successful local homepage may contain intended `/contact/` and service destinations without permission to build them. One tested solution is to retain the actual href, mark it with `data-route`, and intercept only an exact set of future routes to open a native `<dialog>`:

- Clearly say “Homepage-only prototype,” identify the planned path, and state that the page is not built.
- Provide the working secondary action permitted by the brief, such as a `tel:` link. This does not verify carrier connectivity and must not place a call during preflight.
- Provide a close button; test Escape, focus return and viewport fit.
- Treat it as a review utility, not an implemented Contact page or production UX.
- Explain that the future href does not resolve locally without JavaScript.

Generic file-link preflight should report these paths as missing. Do not weaken its global dead-link rules. A concept-specific verifier may separately record `planned_unbuilt_routes`, validate the exact allowlist, exercise every notice, and continue checking real file and fragment destinations. Its result is **PASS HOMEPAGE CONCEPT**, not all-pages acceptance. Negative-test unexpected paths as well as ordinary markup/copy violations when extending the verifier.

Alternative: use an explicitly documented existing preview destination if the brief permits one. Do not add dummy sibling pages just to turn a link test green.

## Content gaps versus authored presentation

A missing dedicated Support capture can coexist with a captured Home support card/service summary. The latter can support short summaries of edits/maintenance but not service tiers, SLAs, prices, backup frequency or response guarantees. A footer can supply provisional phone/address without supplying Contact hours or appointment rules.

When told to omit email, leave it out entirely. Do not add “Not published,” “Contact us for email,” a disabled control, or a missing-email explanation in visitor-facing content.

For provisional facts, verify the actual rendered block has the word “Provisional” and a visible border. Color alone is insufficient. Inspect the opened notice as well as the default page if both contain contact facts.

## Evidence wording

Good: “No automated text-contrast failures at the tested widths; physical devices and screen readers not tested.”
Bad: “Fully accessible.”

Good: “Logo is byte-identical to supplied asset; width/auto-height preserve aspect ratio.”
Bad: “Same size, so original restored exactly.”

Good: “No phone call placed; href matches the provisional supplied number.”
Bad: “Phone connectivity verified.”

Good: “Generic checker found six missing future-route files; the concept verifier tested six explicit route notices.”
Bad: “All seven pages reachable.”

## Other lessons

- Check actual computed reduced-motion behavior and keyboard skip-link entry, not just whether corresponding selectors exist.
- Negative fixtures should be disposable copies. Deliberately inject malformed landmarks and prohibited copy, verify nonzero exit with the relevant finding, remove fixtures, and leave the original clean.
- A CSS class scanner can mistake `.woff2` in font filenames for a class. Record the specific false positive; do not suppress all unused-class warnings.
- Report CSS viewport dimensions separately from PNG pixel dimensions at 2× scale.
- Never invent defects to make a completion sound more rigorous. If the first render is clean, say which checks were actually run and what they cover.
