# Paired-page creative restarts: inspection and evidence

Use when a small number of complete marketing pages must prove a new direction after an earlier package was rejected. This extends the umbrella workflow; it is not a fixed visual style.

## 1. Re-ground without importing the rejected template

Read the current authority and actual business capture. Render the specifically selected reference HTML at desktop/mobile and inspect its CSS and assets. Separate reusable qualities (layering, image scale, flow, expressive typography) from literal sections and repeated motifs. Do not browse other rejected packages when the work order excludes them.

Write a concise image-role plan before implementation. Explain what each lower-page visual communicates. Original explanatory interfaces and diagrams are useful when rights to source imagery are unknown; do not turn them into fictional client work or measured dashboards. Keep provenance and source caveats in review notes, not customer copy. Preserve explicitly required provisional-contact notices with wording and a border.

Content taxonomy matters: six capability headings plus three advertising formats are not nine equally defined capabilities. Use the captured source to resolve shorthand source-map errors. Record current-availability questions separately before implementation/publication.

## 2. Wait for actual dependencies

`document.fonts.ready` alone does not establish image readiness. Before measuring/capturing, evaluate with `awaitPromise:true`:

```js
(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  return {
    fonts: document.fonts.status,
    images: [...document.images].map(i => ({
      src: i.getAttribute('src'),
      loaded: i.complete && i.naturalWidth > 0
    })),
    height: document.documentElement.scrollHeight
  };
})()
```

Catching decode failures prevents a hung batch; it does NOT make an image pass. Assert every `loaded` value. Check each intended font family with `document.fonts.check(...)` as an additional readiness signal and inspect the rendered type. Capture full-page PNGs at the requested CSS widths/device scale.

## 3. Inspect sections, not just tall thumbnails

A full mobile page reduced into a contact sheet can become too small to read. Use the full comparison only for rhythm, density and the relationship between pages. Capture each real section and footer separately, or crop the canonical PNG at readable scale.

For CDP section capture, measure `getBoundingClientRect()` and convert Y to document coordinates with `r.y + scrollY`. Capture using `Page.captureScreenshot` with `captureBeyondViewport:true` and a clip `{x:0,y,width:innerWidth,height:r.height,scale:1}`. Adapt the section selector to actual wrappers; do not silently omit nested sections.

Inspect text-bearing illustration edges, mobile proportions, all dark contexts, incidental labels and overlap. In a validated refinement, proportional framing restored blueprint/planning labels that cover-crops had cut; moving an approval seal restored an obscured action. Such edits require visual inspection even when no layout or contrast probe fails.

## 4. Typography refinements can create regressions

Inspect computed font size at each width, not just media-query source order. A specific `.hero-top h1` rule can beat a later `h1` mobile declaration and quietly shrink the hero.

After easing tight letter spacing, recheck wrapping. An orphaned final word may require a smaller desktop headline and a non-breaking final phrase, not a return to illegible tracking. Apply non-breaking grouping only to a phrase that fits the narrowest layout. Verify desktop and mobile again; passing overflow does not imply balanced lines.

## 5. Test actual controls and gate claims

At every requested/intermediate width, run both-dimensional target, overflow and computed-text contrast probes. For the review index, repeat with native disclosure sections closed AND expanded. Activate disclosures with the complete character-bearing Enter sequence documented in SKILL.md; assert `details.open`.

For skip links, test actual first Tab, visible focus, Enter activation and the resulting focused landmark. A `tabindex="-1"` on the main target supports programmatic focus without adding an ordinary Tab stop. Test Home/service navigation through actual links. Validate telephone hrefs without placing calls.

Negative controls should make checks fail for missing files/fragments, duplicate IDs and malformed landmarks. Report raw CSS-class warnings with context: filename extensions can be mistaken for classes, and identity hooks may receive shared/descendant styling. Do not add empty rules merely to silence a regex warning, or dismiss an actually unstyled component without inspection.

## 6. Freeze downstream evidence last

Preserve the current source/assets/renders before a visual revision. After changes, regenerate canonical PNGs first, then section images/comparisons/index previews. Keep superseded derivatives in clearly named revision evidence, not loose among final screenshots.

Create linked reports before the final index link sweep. Make the final report reflect the final sweep, rather than leaving an earlier failed log on disk while claiming success. Finish run record and handoff, then write checksums and the review archive. Check archive integrity and required members. Explicitly state whether revision/research history is included or remains only on the shared disk.

Keep technical results separate from subjective assessment. Record strengths, trade-offs, actual refinements and untested browsers/devices/accessibility layers. A passing self-check is neither independent QA nor the Director's visual approval. Stop at the requested small-page gate.
