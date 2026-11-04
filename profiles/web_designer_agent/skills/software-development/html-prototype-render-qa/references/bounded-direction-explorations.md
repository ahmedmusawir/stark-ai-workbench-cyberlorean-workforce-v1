# Bounded direction exploration: design and verification patterns

Use when an approved larger site needs multiple small visual directions before the operator authorizes expansion. This is a reusable pattern, not a project completion log.

## 1. Establish two independent inputs

**Identity/business authority:** original logo, original-site screenshots, approved brief and captured text. Measure solid-color regions within relevant screenshot crops; filter transparent pixels when sampling a logo. Preserve the original logo file unchanged. Label derived AA-safe button/text variants as derived, not measured.

**Inspiration:** layouts, rhythm, expressive typography, layering, negative space, imagery posture. Open every requested image. Record the qualities that are useful, and what must not be borrowed: another brand's colors, logo, claims, watermarks, placeholder text, stock imagery without rights or distinctive layout.

Neither a pixel sample nor an inspiration match establishes operator approval.

## 2. Commit to a distinction matrix before building

A useful example matrix—not a compulsory aesthetic:

| Axis | Direction A | Direction B | Direction C |
|---|---|---|---|
| Composition | Offset organic split | Centered editorial object | Immersive image-led stage |
| Typography | Heavy geometric sans | Serif + italic contrast | Light grotesk |
| Imagery | Original fluid/device drawing | Original folded-plane sculpture | Original dimensional workspace |
| Lower section | Horizontal solution ribbons | Editorial service index | Practical process/capability rail |

Hold identity and business meaning constant; vary the actual spatial and narrative system. Do not let one reference become the master layout for all directions. A shared small Contact footer does not erase otherwise meaningful differences.

For each direction, author only the requested scope. A header, hero and meaningful lower section can demonstrate a direction without a seven-page build or full design-spec package.

## 3. Keep review commentary off the marketing surface

When requested, put authorship labels, evidence paths, concept limitations, recommendation and comparison rationale in a separate reviewer index/notes file. Do not insert “design study,” “original artwork,” “not built yet,” or provenance explanations into marketing copy or accessible image descriptions. Alt text describes the visual information. Required provisional-contact wording remains visible with a border, not color alone.

For a bounded study, `Let's talk → #contact` can reach real contact information and a working `tel:` action when the work order permits that accommodation. Explain outside the customer page that the eventual site will use its approved Contact route. Do not invent sibling pages to satisfy a generic link checker. If exact future route hrefs are explicitly required, use and verify the future-route notice pattern described in `homepage-concept-gates.md` instead.

## 4. Responsive images: the passing-overflow / broken-composition trap

Observed failure: an illustration used HTML `width="1200" height="820"`. CSS changed its width at mobile but left the height at 820 CSS pixels. The SVG's preserved internal aspect ratio produced a large empty stage even though the page had zero horizontal overflow and passed text-contrast checks.

Repair at the source stylesheet:

```css
.stage-art img {
  width: 100%;
  height: auto;
}
```

Retain correct HTML width/height attributes to reserve an intrinsic aspect ratio. Measure after fonts and images have loaded:

```js
const image = document.querySelector('.stage-art img');
const box = image.getBoundingClientRect();
const expected = image.naturalWidth / image.naturalHeight;
const ratioOK = Math.abs(box.width / box.height - expected) < 0.01;
```

For intentionally cropped images, verify the intended crop/container instead of requiring the image's displayed box to preserve its natural ratio. Re-render and visually inspect mobile; a mathematical ratio alone does not prove good composition.

A decorative image may intentionally exceed its stage bounds if the stage clips it. Distinguish raw element bounds from document overflow and confirm that no text/control is clipped. If an overlapping image can pass behind a text strip, give that strip an opaque surface and verify its actual contrast rather than relying on the ancestor background.

## 5. Measure both target dimensions

A link can be 48px high but only 30px wide. A height-only check cannot support a 44×44px assertion.

```js
const small = [...document.querySelectorAll('a[href],button,summary')]
  .filter(element => {
    const box = element.getBoundingClientRect();
    return box.width > 0 && box.height > 0 &&
      (box.width < 44 || box.height < 44);
  });
```

Add minimum width as well as height to short navigation labels; do not shrink the logo or adjacent text to force a cramped header to fit. This skill's 44px floor is a design requirement, not a claim that WCAG AA universally prescribes 44px targets or has no exceptions.

## 6. Negative-test copy rules without deleting valid content

A loose pattern `book (my|a|your)` falsely matched **Facebook advertising**. The fix is a word boundary, not removal of legitimate advertising copy:

```python
pattern = r'\bbook (my|a|your)'
assert re.search(pattern, 'Book a call', re.I)
assert not re.search(pattern, 'Facebook advertising', re.I)
```

Keep both the forbidden positive fixture and legitimate negative fixture. Do the same for claim words, timeframes and domain-specific terms. Avoid broad patterns such as `free` that match allowed phrases like royalty-free imagery. Report a false positive as a checker correction, not a content defect.

## 7. Close the package with real evidence

1. Hash protected files before writing; keep new concepts in a fresh folder.
2. Build reviewer notes and results files before the final index link check. An index can render perfectly while linking to reports that do not exist yet.
3. Render every direction at desktop/mobile; inspect each, not just the recommended one.
4. Run raw markup, copy, both target dimensions, text contrast, local assets, one-H1/heading order and anchor/file checks. Check narrow/tablet widths as well as the required two sizes when practical.
5. Test actual Tab entry to the skip link, visible focus, Contact action and computed reduced-motion styles. Validate the literal phone href without placing a call.
6. Negative-test probes with disposable fixtures. Distinguish detector-level tests from a complete independent QA run.
7. Re-render affected PNGs after repairs; inspect image/text intersections and contact notices at readable scale.
8. Compare original protected hashes. Preserve earlier packages and archive any replaced completion handoff separately.
9. Report actual viewport dimensions separately from PNG pixel dimensions at device scale. State what remains untested: real devices, other browsers, screen readers, production build, telephony and business-detail accuracy.
10. Recommend one coherent direction and stop for explicit operator approval. Do not infer approval from successful verification or expand to implementation.

## 8. Two field recipes from a real four-direction run

Concrete, reusable patterns — not session trivia.

**AA action color derived from a strong brand red (worked value).** A canonical logo/brand red `#F12800` measured **4.16:1** with white button text (fail). Applying "search for a passing value instead of abandoning the accent" produced the derived sibling **`#A81E00` at ≈5.9:1** with white. Keep roles separate so the page still reads as the brand while the action surfaces pass AA:

```css
:root{
  --brand:#F12800;       /* canonical — artwork, accent rules, non-text decorations */
  --brand-deep:#A81E00;  /* derived accessible action red — white text on buttons ≥4.5:1 */
}
.btn-solid{ background:var(--brand-deep); color:#fff; }
```

Generalizes: for any saturated warm accent that sits near 4:1 with white, derive a darker sibling for the text-bearing surfaces and keep the canonical color for the mark and decorations.

**Flat staging dir → bogus dead-link failures (harness artifact).** To run the per-directory preflight across several standalone concept pages, you may copy them into one flat staging folder. Any page that links to the comparison index (`<a href="../index.html">` for "back to all directions", or `index.html`) will **false-fail** the link check, because those targets live in the REAL output root, not the flat staging dir. This is a staging artifact, not a page defect — distinct from the not-yet-written-report false-failure named in the SKILL.md pitfalls. Two clean fixes: (a) copy the comparison index into the staging root so `../index.html` resolves, then re-run; or (b) check each page inside its own real folder where its relative links genuinely resolve. Distinguish this harness miss from a genuine broken link and record the preflight exit status directly.
