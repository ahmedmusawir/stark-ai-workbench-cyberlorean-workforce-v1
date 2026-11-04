# High-fidelity comparison checks

Use for bounded, multi-direction marketing studies where the user needs a fair visual comparison, not multiple differently pitched websites.

## Source-grounded imagery

Plan the subject, purpose, crop and relation to copy before implementing. Distinguish brand authority (original identity and color proportions), composition inspiration (supplied reference filenames), and factual copy authority (source documents). Inspect all explicitly requested images; document any genuinely inaccessible ones.

For sourced photography, retain a provenance record containing source page/file URL, author, license name and URL or source metadata, downloaded file identity, derivative filename, and transformations. Wikimedia Commons imageinfo/extmetadata is one usable source of explicit licensing records; do not assume every Commons image is freely interchangeable or CC0. Verify the actual record for each asset. Repository metadata is evidence of a stated license, not an independent chain-of-title audit. Cropping or obscuring a mark does not itself confer rights.

Inspect both the original and the delivered crop. A contextual photo of a laptop, desk or hands can support website-making without being presented as the agency's staff or portfolio. Keep provenance in reviewer notes, not customer-facing headlines or alt text. Alt text describes the visible subject. If a source retrieval path is unsuccessful, try another legitimate source with inspectable license information; do not generalize a transient retrieval failure into a permanent tool limitation.

## Equal content, different design

Generate directions from one source-grounded copy dataset and stable identifiers such as data-copy. Check exact field sets as well as values: dictionary construction alone can conceal duplicate identifiers, so check identifier uniqueness separately. Assert the requested section count and meaningful content presence. This keeps typography, composition, image framing and section treatment—not unequal business coverage—as the comparison variables.

Rendered innerText reflects CSS text-transform. If designated kickers are uppercase, derive uppercase expected values for those explicitly designated fields rather than changing valid marketing copy or blindly lowercasing every comparison. Normalize whitespace deliberately around line breaks. A source-text check may instead use textContent with explicit handling of br elements; it is not equivalent to testing visible text. Add a changed-field fixture that passes through the actual parity checker and must fail, not merely a standalone dictionary inequality demonstration.

## Visual refinement evidence

1. Render all requested desktop/mobile views.
2. Inspect whole-page composition and readable crops. Extremely tall mobile screenshots can shrink to unreadable thumbnails in a vision tool.
3. Compare with the actual references: identify where image boundaries, layering, scale and type relationships are visibly transformed.
4. Record specific weaknesses before adjusting them. Passing contrast/overflow checks cannot detect an orphaned headline word or arbitrary decorative stagger.
5. For heading wrapping, measure bounding height and computed line-height after fonts load; test candidate sizes at the target width. Check adjacent widths before choosing a fluid clamp.
6. Preserve first-pass screenshots/CSS, refine, rerender, and inspect again. Do not claim that removing every stylistic convention is necessary or that a self-awarded zero score proves originality.
7. Give a subjective recommendation with risks. Approval remains with the user/Director.

## Harness pitfalls and report lifecycle

- Renderer and preflight CLI formats differ: render_cdp.py uses `--viewport desktop:1440x1000`; design_preflight.py uses `--viewport desktop:1440`. Inspect the actual help/parser before borrowing flags between helpers.
- An inexpensive CSS class regex can mistake `.ttf` inside a font URL for a selector. Inspect the reported source occurrence before editing working styles. Label the warning accurately; do not disable real class checks to silence it.
- Avoid deeply nested selector quoting in Python-generated JS. Selecting `a[href]` and filtering getAttribute('href').startsWith('#') is a simple alternative. A quoting error in the test harness is not a page defect.
- Write a genuine first-pass result before checking links to that result. Then rerun package-link verification after all reports exist. Do not create a fake passing report to satisfy a self-reference, or silently skip the report link forever.
- Preserve relevant initial failures, identify harness versus artifact defects, correct the cause, and rerun the real command. Record subprocess exit status directly rather than losing it through shell output filters.
- Report quantitative preflight evidence separately from visual judgment. Scope the claim: these checks do not establish cross-browser behavior, screen-reader quality, complete WCAG certification, production readiness or visual approval.
