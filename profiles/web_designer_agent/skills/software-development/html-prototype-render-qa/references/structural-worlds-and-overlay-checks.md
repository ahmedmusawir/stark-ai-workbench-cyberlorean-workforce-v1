# Structural exploration and overlay checks

## Trigger
A technically passing concept set is rejected as too closely related. The correction concerns design types, not polish or colour accuracy. This workflow was exercised in a four-reference agency exploration; the particular aesthetic choices are examples, not future defaults.

## Composition-first restart
1. Preserve the rejected output under its original path. Respect forbidden-read rules; write confinement can preserve an old package without opening it to hash or copy it.
2. Reopen the assigned references and describe composition, scale, shapes, image placement, whitespace and transitions. Write the matrix before implementation.
3. Allocate distinct structural languages. In the worked exploration: navigation rail + graphic poster + service tickets; editorial masthead + serif/sculpture stage + prose spread; curved canopy + service route; photographic opening + native disclosures. Shared facts and tokens did not require shared markup.
4. Keep service descriptions comparable. When using disclosures, initially open all entries if equal visible coverage is the review goal; still test close/reopen through real keyboard activation.
5. Capture every concept at desktop/mobile after fonts/images decode. Inspect all initial previews. Reserve targeted follow-ups for actual changes and a combined final desktop grayscale sheet.
6. Judge whether the set remains distinguishable without colour. A small overview proves silhouette only: use full previews/readable crops for typography and detail. Report the judgment as subjective, never Director approval.
7. Supply a mix-and-match table: header, hero/transition, substantive lower section, contact treatment, reuse caution. Suggest a few combinations without implementing another concept. Require one coherent type/spacing system for later consolidation.

## Mobile curved-field repair
A desktop SVG canopy entered the mobile text region. Opaque navy backgrounds behind individual text elements made automated contrast pass but produced visible rectangular patches across the curve. The successful repair was a dedicated mobile SVG whose solid text field extended below the actual wrapped paragraph, selected with `<picture><source media=...>`. Verify `img.currentSrc` at narrow and wide breakpoints, then inspect a readable mobile hero crop. A technical pass did not establish this visual fix.

## Contrast beyond ancestor-background heuristics
Absolutely positioned artwork is often a sibling, not a text ancestor. Supplement DOM contrast with explicit bounds and actual visual clearance.

For white text over a photograph under a uniform dark overlay, the brightest possible underlying photo pixel is white. Composite each channel as `overlay_alpha * overlay_channel + (1-overlay_alpha) * 255`, then compute WCAG relative luminance/contrast from that composite. In the worked case, 84% navy (14,27,51) yielded a conservative white-text contrast of about 10.51:1. Recalculate for the actual colours and alpha; the number is not a reusable guarantee. For other foregrounds/overlay colours, determine the actual worst-case background rather than assuming white is always worst.

For large red type over a light sculpture, bound the darkest material in the observed overlap and inspect the rendered intersection. The worked pair (185,35,6) on (200,209,220) measured about 4.12:1. That bound is not an exhaustive pixel audit and does not cover unrelated dark details elsewhere in the artwork.

## Nested focus surfaces
A rule such as `.inverse a:focus-visible { outline-color: white }` also affects links in a white tray nested within the dark section. The fix was a scoped tray override with a contrasting blue outline and inward offset. Check all controls, widths and relevant states, not only the main CTA. Enter keyboard modality before inspecting `:focus-visible`; `.focus()` alone can reflect pointer modality. Ancestor-background measurements remain insufficient where the outline crosses image or split surfaces; inspect those cases.

## Verification harness hygiene
- Strip CSS `url(...)` strings before regex class extraction; otherwise a filename extension such as `.svg` becomes a false unused class. This improves a lightweight scan, not a substitute for a CSS parser.
- An error array in JSON is not enough: exit non-zero when it contains failures. Preserve diagnostic reports before exiting.
- Negative-test copy parity by changing a service paragraph in the temporary browser DOM and asserting mismatch, without altering delivered source.
- Keep scope checks compatible with legitimately different DOM structures; don't enforce one layout just to simplify a test.
- After final document writes, rerun link checks and verify no in-progress stubs remain. Package inside the allowed root if output confinement rules out the user's usual Downloads preference. Verify ZIP members and bytes, and disclose omitted review history.
