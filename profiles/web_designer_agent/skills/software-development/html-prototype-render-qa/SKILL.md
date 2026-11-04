---
name: html-prototype-render-qa
description: Render and preflight HTML design artifacts without installs.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, html, prototype, rendering, screenshots, cdp, accessibility, wcag, contrast, preflight, verification]
    related_skills: [claude-design, design-md, popular-web-designs, inspecting-hermes-desktop-dom]
---

# Rendering and preflighting HTML design artifacts

## Overview

You have produced an HTML prototype, landing page, style tile, or design system board.
Now you need to (a) produce PNGs someone can look at, and (b) prove the thing actually
holds up — no overflow, no tiny tap targets, no failing contrast, no dead links, no
styles that were never applied.

Two facts drive everything in this skill:

> **A design artifact is not verified until it has been rendered and looked at.**
> Source review finds almost none of the real defects. Rendering finds them immediately.

> **Machine-checkable layout and accessibility defects should be checked by machine.**
> Eyeballing 44px tap targets or WCAG ratios across a dozen pages is slow, unreliable,
> and wrong in the details. Automate them.

This skill covers the *verification* half of a design task. For the *design* half
(composition, taste, surface archetype, slop audit) use `claude-design`.

## When to use

- You built an HTML artifact and need desktop + mobile PNGs.
- You need a design preflight before handing a prototype to anyone for review.
- The machine has no Playwright/Puppeteer/Selenium and you must not install a toolchain.
- You need WCAG AA contrast, tap-target, overflow, heading-order, alt-text, form-control
  and dead-link assurance across a set of pages.

**Don't use** for: reading a live app's DOM over an existing DevTools port (that's
`inspecting-hermes-desktop-dom`), or authoring a token spec file (that's `design-md`).

## The zero-install rendering path

System Chrome exposes the DevTools Protocol over a WebSocket. You can drive it with
**nothing but the Python standard library** — no npm install, no browser download, no
toolchain on the machine. `scripts/render_cdp.py` in this skill is a complete, working
implementation (~200 lines, stdlib only).

```bash
python3 scripts/render_cdp.py <html-file-or-dir> --out <dir> \
    --viewport desktop:1440x1000 --viewport mobile:390x844
```

It produces **full-page** PNGs at 2× device scale factor. That matters: a viewport-only
screenshot hides everything below the fold, which is usually where the layout falls apart.

Under the hood:

1. Launch `google-chrome --headless=new --remote-debugging-port=PORT --user-data-dir=<tmp>`.
2. Poll `http://127.0.0.1:PORT/json/version` until it answers (do not sleep a fixed amount).
3. Read `http://127.0.0.1:PORT/json/list`, pick the target with `"type": "page"`.
4. Connect a minimal RFC6455 WebSocket client (handshake, masked client frames, handle
   126/127 length forms, answer pings).
5. `Emulation.setDeviceMetricsOverride` for width/height/deviceScaleFactor/mobile.
6. `Page.navigate`, then **await `document.fonts.ready`** before measuring — self-hosted
   web fonts change layout, and measuring before they land gives you the wrong page height.
7. Measure `document.documentElement.scrollHeight`, re-apply device metrics at that height.
8. `Page.captureScreenshot` with `captureBeyondViewport: true`; base64-decode the payload.

`Runtime.evaluate` with `awaitPromise: true` lets you do the font wait and the height
read in one call — that is the single most important detail in the whole sequence.

## Image-ready comparison captures and bounded inspection

- Before awaiting image decoding on a full-page comparison, promote offscreen `img[loading="lazy"]` to `loading="eager"` in the capture context. Otherwise `document.readyState === 'complete'` and loaded fonts can coexist with unresolved image-decode promises. Diagnose readiness by logging the current page, font status, and each image's `complete`, `naturalWidth` and source; do not repeatedly rerun an undiagnosed timeout. Await decoding, then assert every image is complete with positive natural width—catching decode errors alone is not success.
- Capture the document with an explicit `Page.captureScreenshot` clip and `captureBeyondViewport: true` while retaining the target viewport dimensions. Changing viewport height to the document height can change viewport-relative layouts. Report CSS viewport size separately from 2× PNG dimensions.
- Respect the operator's inspection budget: enumerate initial desktop/mobile inspections for every direction, then allocate the permitted targeted rechecks to changed regions and the comparison index. Whole-page mobile thumbnails establish rhythm, not small-text legibility; use readable crops for consequential refinements. Never imply unperformed inspections.
- Embedded SVG labels can become unreadable when the illustration scales down even though DOM contrast checks pass. Use an art-directed mobile source without those labels plus readable adjacent HTML labels; preserve meaning in accessible text and verify the actual selected source and proportional layout.
- Under strict output confinement, put renderer profiles, fixtures and history inside the permitted output root, disable bytecode writes when importing read-only skill helpers, and terminate only processes started by the task. Keep completed review/handoff files outside unconditional generator writes so a rerun cannot replace them with in-progress stubs.

See `references/image-ready-comparison-captures.md` for the validated readiness fix, capture recipe and inspection-budget pattern.

## The preflight

`scripts/design_preflight.py` drives the same CDP client and runs four classes of check:

| Class | What it catches |
|---|---|
| **Layout** | Horizontal overflow at each viewport, and *which elements* cause it (named, with their overflow edge) |
| **Accessibility** | Tap targets under 44px, WCAG AA contrast for every distinct text/background pair actually rendered, heading order and H1 count, `<img>` without `alt`, SVG without an accessible name |
| **Semantics** | Form controls present (often a hard requirement), internal link targets that do not resolve to a real file |
| **Raw markup** | Structural errors the browser silently repairs: unbalanced or duplicated landmark tags (`<main>`, `<footer>`, `<header>`, `<nav>`, `<section>`, `<article>`, `<aside>`), doubled closing tags, duplicate `id` attributes. Read from the **file source**, not the DOM. |
| **Copy compliance** | Page text matching a banned-claim pattern — guarantees, delivery timelines, outcome claims, testimonials, or language implying a form/booking control. Configured per brief via `--banned-claim LABEL=REGEX`. |
| **Static CSS↔HTML** | CSS classes defined but never used in any page, and page classes with no matching rule |

The contrast check samples elements with direct text, walks ancestor backgrounds, applies
the large-text rule (3:1 at ≥24px, or ≥18.66px bold), and reports failures. It is a
heuristic, not a pixel-level contrast audit: translucent foregrounds can be skipped, and
an absolutely positioned image or pseudo-element behind text may not be an ancestor. A
passing result does not establish contrast in those cases. Inspect rendered overlays and
separate text from variable imagery with an opaque surface or verified clearance; check
focus-indicator contrast against each surrounding surface independently.

The static CSS↔HTML cross-check is the one people skip and should not: a rule written for a
class the markup never uses is dead code, and a class in the markup with no rule is an
unstyled element. Both are cheap to find statically and impossible to spot by eye.

### Raw-source markup check — why it is not optional

The browser **silently repairs** structural errors. A duplicate `<main id="main">` and a stray
`</footer></footer>` both vanish into a well-formed DOM, so the page *renders* correctly and
every DOM-level probe reports it as fine. A page with these defects passed a full preflight
passing contrast, overflow, heading, and tap-target checks — and was still wrong as reference
markup handed to a Developer.

Any check that reads the DOM cannot catch this. Read the file:

```python
src = pathlib.Path(page).read_text()
assert src.count("<main") == 1
assert "</footer></footer>" not in src
ids = re.findall(r'\bid="([^"]+)"', src)
dupes = {i for i in ids if ids.count(i) > 1}
```

The preflight script does this automatically for every page.

### Copy compliance — encode the brief's prohibitions

Some briefs forbid guarantees, delivery timelines, outcome claims, testimonials, or any
language implying a form or booking control. These are **content requirements that look
like copy review**, and they are exactly the kind of thing that slips through a purely
visual preflight. Encode them as machine checks so the artifact cannot silently drift:

```bash
python3 scripts/design_preflight.py ./pages --css tokens/globals.css \
  --banned-claim 'guarantee=\bguarantee' \
  --banned-claim 'day-count=\b\d+\s*days?' \
  --banned-claim 'week-count=\b\d+\s*weeks?' \
  --banned-claim 'absolute=at all times|optimal levels' \
  --banned-claim 'booking=book (my|a) |schedule|free (seo )?analysis'
```

The regexes are applied to the rendered `innerText`, so they match what a visitor reads,
not what the markup contains. Keep the patterns tight: a loose pattern like `free` will fire
on legitimate commercial copy ("royalty free images") and train you to ignore the check.

## Scope-aware concept review

When the brief approves a multi-page site but requests **one homepage concept first**, the site scope is not permission to build every page. Author only that concept, preserve earlier packages in separate folders, and stop at the explicit visual-direction gate. Rejection of an earlier direction removes it as a visual constraint; source evidence and approved business meaning still govern.

- Inspect supplied reference images, not just filenames or historical descriptions. A labeled contact sheet helps inventory many images; enlarge important regions before claiming legibility or content inspection. Identify what each screenshot actually shows rather than assuming `image.png` is the hero.
- Distinguish source-supported business facts from **design-authored** headlines, transitions, summaries, illustrations and arrangement. Label authored material and trace each section to evidence. Missing dedicated-page evidence does not erase a captured homepage summary, but it does not justify inventing hours, SLAs, response times, tiers or outcomes.
- If a field is explicitly **omitted**, do not add an empty card, explanatory placeholder or “Not published” state. Omission is not an empty-state design request.
- Future destinations are not existing pages. Preserve intended route targets where required and disclose unbuilt destinations. An explicitly labelled prototype-only route notice can keep a concept review usable without building sibling pages; test its keyboard behavior and working secondary action. Do not ship that utility as the eventual page.
- Keep a narrow, exact allowlist of planned/unbuilt routes separate from ordinary link checks. Verify each listed link has the intended notice behavior, while still checking all real files and anchors. Record the generic checker's missing-file failures honestly; a concept-aware pass must never become an “all pages/navigation passed” claim.
- Verify notices open, fit the viewport, meet contrast requirements, close with Escape, and restore trigger focus. Test actual Tab entry to the skip link and computed reduced-motion styles rather than merely searching CSS source.
- Snapshot protected files **before** writing. File size, mtime, stripped-link comparisons, or reconstructing from memory do not prove byte-identical restoration. Use an original backup plus a cryptographic hash or exact byte comparison. If only partial evidence exists, state that limit instead of claiming exact preservation.

See `references/homepage-concept-gates.md` for a worked scope-aware verification pattern and evidence boundaries.

## Bounded multi-direction explorations

When a work order asks for multiple directions, keep the eventual site scope separate from the exploration scope. Deliver the requested header/hero and meaningful lower section per direction—not several complete websites.

- Separate **identity authority** from **visual inspiration**. Establish the palette from original brand assets; inspiration contributes possibilities for composition, typography, depth and rhythm, not its own colors, logos, watermarked artwork, claims or placeholder copy. Inspect every requested reference; document useful qualities and how they were transformed.
- Make alternatives differ across **composition, typography, imagery and lower-section treatment**. Three font/color swaps of one layout are not three directions. Give each a coherent rationale and put the recommendation on a comparison index.
- Respect the requested separation of review material from customer copy: keep source/provenance labels, prototype limitations and design-authorship notes in the comparison page or notes file, not marketing footers, hero copy, notices or image alt text. Alt text should describe the image. A required provisional-contact flag is an explicit exception, not permission to add other process commentary.
- For bounded studies without an exact route-href requirement, a real in-page Contact area with a working phone link is simpler than a future-route dialog. Explain the fragment accommodation on the reviewer page; do not pretend it is the eventual Contact page. If exact future hrefs are required, use the scope-aware route-notice pattern above instead.
- Preserve the original logo bytes and aspect ratio. A white backing plate can make an unchanged logo legible on a dark composition without recoloring or inverting it. Distinguish sampled identity colors from deliberately derived accessible text/action variants.
- Render and inspect desktop/mobile for **every direction**, then test the comparison page and its actual file links after reports and notes exist. Stop for a direction decision; a recommendation is not approval.

See `references/multi-direction-contest-workflow.md` for the comparison matrix, responsive-image repair, two-dimensional target probe and copy-check false-positive regression recipe, plus a worked brand-red→accessible-action-color (#F12800→#A81E00) and the flat-staging-dir dead-link artifact recipe (§8 of the earlier pack's notes). It also carries the self-hosted-font workflow — inventory with `fc-list`, copy only the declared weights, **prune unreferenced `.ttf` files before packaging** (an unused binary still needs a licence notice, so it is a liability), and write `FONT-LICENSES.md` to match exactly what ships — the inspection-budget split (one whole-page pass per preview for rhythm, batched region crops only where a read is consequential, whole-page overviews of unchanged pages buy nothing), and the **grayscale montage recipe** (§8) with the gold/red accent-role rule (§9).

For a contest-style pack of several directions in sibling folders under one output root, see `references/multi-direction-contest-workflow.md`: the renderer is single-target with fixed `index-*.png` output names (loop to temp dirs and move), the preflight is single-directory (run per direction and once at the root), inline-`<style>` pages make the CSS↔HTML cross-check noisily false-fire, pseudo-element gradient surfaces fake "white on white" contrast failures that must be pixel-verified individually rather than dismissed wholesale, the 44px tap-target fix needs `min-width` plus decoration-aware underline treatment, and a second measured brand-red contrast ladder (white on `#D93206` = 4.76 passes where `#F12800` = 4.16 fails).

See `references/archive-integrity-and-invisible-text.md` for the archive/verification recipes and the defect classes that a green preflight did not catch: an archive can never contain its own digest (compute size and SHA-256 once, after the last write, and report them outside the package), the extracted archive must be verified independently of `unzip -t` (protected-asset hash, every local `href`/`src` resolved, required members present by name), and — most importantly — a bare-element descendant selector such as `.nav a { color: … }` silently out-specifies a single-class child rule and can render white-on-dark text **invisible** while the preflight still reports no contrast failure. Only the rendered pixels expose it.

## Structurally different design worlds

When this user rejects alternatives as too closely related, restart the compositions rather than styling one shared layout. They want identifiable components to mix later, not a prebuilt hybrid. Before implementation, write a concept matrix covering each direction's primary reference, design type, hero reading path, typography/art direction, lower-section organization and reusable contribution. Follow any explicit reference-to-direction mapping; a current instruction permitting one dominant reference supersedes an earlier balanced-reference constraint.

- Vary header arrangement, hero geometry, text/art relationship, typography density, section transition, lower-section organization and contact treatment. Share identity tokens, assets and content if useful, but not a common structural template with theme switches.
- Reopen the assigned inspiration images. Interpret composition and scale originally; do not import their branding, text or artwork. Preserve the business identity and comparable service coverage.
- Inspect each desktop/mobile preview, then compare all final desktop compositions together in grayscale. This silhouette test diagnoses structural similarity, not text legibility or objective visual quality. If two still read as one template, change composition before delivery. Allocate the combined comparison within the user's targeted-recheck budget. Build the grayscale comparison as **one montage image** (desaturate each render with `.convert('L')`, normalise tile **height** so differing page lengths stay comparable) and read it once — reasoning about four compositions separately cannot answer "are these four different approaches?".
- Deliver a component menu with a few suggested combinations, compatibility cautions and one primary-system rule. Do not build a fifth hybrid without authorization. Preserve the pre-build matrix and append implementation deltas rather than rewriting history.
- Curved backgrounds can pass DOM contrast checks while exposing ugly rectangular text backings on mobile. Art-direct a mobile curve with clearance for actual wrapped text, assert the selected `currentSrc`, and inspect a readable crop.
- Check focus indicators inside nested light-on-dark contexts: an inverse ancestor can give white links on a white inset tray an invisible white outline. Scope the light inset's focus colour explicitly and test every surrounding surface.

See `references/structural-worlds-and-overlay-checks.md` for the bounded comparison workflow and contrast-verification techniques.

## High-fidelity comparison and visual refinement

A bounded scope is not a low-polish brief. When the user requests high-fidelity marketing concepts, complete reference inspection, imagery planning, implementation and visual refinement within the assignment unless an intermediate gate is explicitly required. Do not impose a preset archetype over the supplied references.

- Preserve the original brand's **relative color balance**, not just its hex values. An accent-color logo does not authorize an accent-colored page. Explain visible reference influence using actual filenames and observable composition/type/image decisions, without copying reference assets or forcing every reference into every direction.
- Write a deliberate imagery plan **before implementation**. Local delivery does not prohibit appropriately licensed sourced/generated imagery. Record source, author, license basis, transformations and local filename; inspect the actual image and its final crops. Zoom into incidental screen text, code, logos and other legible details—not just the overall subject. Reject or replace imagery with inappropriate content or misleading marks, and document any material substitution; a stock license does not make its visible contents suitable. Never imply stock/generated imagery is real client work. Do not default to unrelated geometric SVGs beside oversized slogans.
- Keep the same content coverage across directions, including the requested number of meaningful lower sections. A shared copy dataset with stable field identifiers makes the comparison fair while allowing genuinely different composition, typography and image treatment.
- Provide large comparison previews, responsive mobile previews where useful, and links to complete HTML/full-page PNGs. Disclose preview cropping. Tiny thumbnails cannot establish legibility: inspect readable image regions as well as overall page rhythm.
- Preserve first-pass evidence when refining. Fix actual visual weaknesses even when technical tests pass; measure headline wrapping at the target width, then recheck narrow widths after adding fluid type. Remove arbitrary staggering or decoration rather than calling it polish.
- Report **technical preflight** and **subjective visual assessment** separately. Neither a passing test count nor a numerical self-audit proves visual quality or Director approval. State strengths, trade-offs and the remaining decision honestly.

See `references/high-fidelity-comparison-checks.md` for copy-parity, image-provenance and verification-harness details, and `references/cc0-stock-sourcing.md` for the validated Wikimedia Commons CC0 photo sourcing recipe (search/filter/fetch code, provenance record shape, and the license-vs-suitability inspection gate).

## Creative restarts and paired-page reviews

When a Director rejects a technically passing package as repetitive or dull, treat the correction as a **composition and imagery problem**, not permission to recolor the same template. Re-ground in the current ruling, retain business/identity constraints, and inspect only the prior artifacts explicitly selected as references. A bounded two-page restart calls for two complete, polished pages—not hero studies and not renewed full-site expansion.

- Give each page a different substantive visual narrative while sharing brand, navigation and footer. Purposeful imagery must continue through lower sections; avoid repeating one sculpture, serif treatment, card grid or ruled-list pattern everywhere. Explain each visual's service role before implementation.
- Preserve source distinctions: capability headings, campaign formats and process stages are not interchangeable counts. Historical terminology is evidence, not proof of current platform availability; record verification gates and meaningful omissions outside customer copy.
- Treat explanatory artwork as composed information. `object-fit:cover` can cut through words, browser chrome and diagrams even when overflow tests pass. Prefer full proportional framing when meaning depends on the whole scene; move overlapping seals away from messages and actions.
- Inspect computed heading sizes at breakpoints. A specific desktop selector can override a later generic mobile heading rule. Loosening tracking can introduce new orphans: group a short final phrase with `white-space:nowrap` only if it fits the narrowest tested width, then rebalance font size and re-render both viewports.
- Make the evidence pipeline explicit: source/assets → font/image-ready canonical PNGs → readable section crops → comparison/index previews → reports → archive. After a visual edit, regenerate downstream derivatives and remove or clearly archive superseded loose previews. A tiny whole-page comparison establishes rhythm, not legibility.

See `references/paired-page-creative-restarts.md` for image-ready capture, section inspection and finalization recipes.

## Independent explorations and run records

When the user explicitly requests an independent experiment, the permitted shared evidence—not previous outputs—is the starting point. Do not open previous packages, screenshots or completion handoffs, or import their fonts/assets/code. Use a new output directory and the separately requested handoff filename. This overrides the usual protected-file snapshot step for files the user forbids inspecting: confine writes and describe that preservation evidence honestly instead of reading old bytes to hash them. Existing conversation history is not erasable; distinguish “no prior artifacts opened in this run” from a scientifically blinded experiment.

For a requested run record, capture an actual clock observation near the start and another at artifact completion, including timezone; calculate elapsed time with a tool. Label the interval as wall-clock, not inference time. Distinguish observable runtime model/provider labels from independently verified provider response identifiers. Record effort, actual token usage and cost only when exposed; otherwise write “unavailable.” Do not infer them from the assignment, inspect secret-bearing configuration, or make extra model calls for accounting.

See `references/runtime-model-identity.md` for the log lines that establish which model/provider actually served a session, how to detect a mid-chat model switch, and how to report the model label separately from a provider response ID that was never exposed.

## Selected-concept expansion into a full-site design package

When current authority selects a foundation and explicitly authorizes full design, re-ground in that ruling: earlier concept-only limits no longer cap the design scope, but selection is not final-design approval, engineering release or publication permission. Render the exact selected artifact before extending it; preserve its source and distinguish that authorized reuse from independent explorations, where prior package code/assets must not be opened or imported. Obtain reusable test tooling from the skill library rather than a forbidden previous package. Preservation/independence claims must reflect actual tool access, not intended confinement.

- Enumerate every approved page as a separate completion item. Vary its substantive composition while retaining the selected visual system. Replace concept Contact fragments with the completed Contact page. Keep public routes separate from prototype filenames and document the mapping and local serving command.
- Build page content and shared contact/footer/CTA settings as local structured data. For each actual section, record the source-map row, exact captured file/section or line range, retain/rewrite/combine/design-authored disposition, proposed fields, and meaningful omissions. Preserve supported process/FAQ substance without copying prohibited claims; explain any non-verbatim safety rewrite instead of labeling it verbatim.
- Render every page plus nested style tiles explicitly, await fonts and image decoding, then regenerate the review index after its page PNG dependencies exist. Inventory expected page/render pairs programmatically; whole-page thumbnails do not establish legibility, so inspect lower content, dark contexts and expanded states at readable scales too.
- Re-run the two-dimensional target and contrast probes at **every width and state**, not just one mobile viewport. Content-width desktop footer links can be tall enough but narrower than the target floor; native menu and FAQ expansions need their own reflow/contrast and keyboard checks. A passing main-page sweep does not cover a nested style tile.
- Audit customer copy, including expanded answers, for leaked editorial notes such as “the captured offer” or “in this prototype.” Keep provenance in review documentation; retain only specifically required provisional-contact notices on marketing pages. Add a forbidden-positive fixture and legitimate-copy regression test rather than loosening the detector globally.
- Keep canonical identity colors separate from accessible action/text derivatives. Light artwork can disappear on white even when all text/layout tests pass. Inspect the actual composite. Avoid cyclic token maps such as `--text-body: var(--text-body)`; use a distinct canonical variable, e.g. `--text-body: var(--size-body)`.
- Stamp active deliverables and handoffs with Version and full Updated timestamp/timezone. Preserve pre-adjustment source/content/assets/renders and attribute direct decisions separately from Designer refinements. Audit archived assets too: unused copied font binaries still need their notices, or should be excluded from the delivered archive.
- Report repeated assertions as assertions, not independent acceptance criteria. Separate source preservation proved by hashes from other packages protected only by write confinement. Verify the final ZIP's integrity and required members, record untested areas, and stop at full-design review/contract reconciliation rather than releasing engineering.
- For this user's review deliveries, prefer a date-and-time-stamped ZIP in Downloads when the active output scope permits it. Include the local review entry, final assets/fonts/notices and before/after dependencies; explicitly state any revision history excluded from the compact archive. Verify archived member bytes and the delivered copy, and tell the reviewer which HTML file to open after extraction.

See `references/full-site-design-handoff.md` for the selected-foundation expansion checklist, artifact matrix and verification pitfalls.

## Positioning corrections within an approved direction

Creative approval and correct business positioning are separate. When the user says Home reads like one service rather than the whole agency, retain the approved visual craft and revise the **headline, supporting copy, dominant artwork and opening hierarchy together**. A tiny “digital marketing agency” eyebrow cannot compensate for a website-building headline and overwhelmingly website-only imagery. For this user's agency work, introduce Design/Development, Support/Maintenance and Traffic through SEO/PPC prominently, with meaningful dedicated-service paths; put the deeper website-building story on Web Design. Generalize the same test to the actual offering in other briefs rather than imposing these services on unrelated clients.

- Preserve the approved prototype/assets/PNGs unchanged; work in the newly authorized package. Supply exact before/after paths and comparable desktop/mobile viewports, with source trace and a large labeled comparison linked from the review index.
- Test the opening without relying on its eyebrow or footer. Inspect the rendered service names and visual balance, and actually exercise the opening's service links—not only the shared navigation.
- Report positioning findings separately from subjective visual findings and technical probes. A positioning correction does not automatically reopen creative exploration, grant full-site approval or authorize engineering.
- For state evidence, assert the native disclosure is open before capture. An immediate viewport screenshot after smooth `scrollIntoView()` can show the hero while being mislabeled “expanded FAQ.” Prefer an exact section-bound CDP clip using document coordinates, or verify that scrolling has settled. Preserve and replace misleading evidence rather than treating it as proof of a UI failure.
- Inspect focused expanded answers, not just their contrast and overflow. An outward summary focus ring can overlap the first answer line; provide measured clearance and re-test affected widths. When a scoped dark component inherits the wrong paragraph rule, verify computed **font size/line height as well as color**—a contrast-only repair can leave its display typography suppressed by selector specificity.

See `references/positioning-corrections-and-state-evidence.md` for the joint positioning repair, reliable section capture and focused-answer checks.

## Native keyboard controls in CDP

Before replacing working native UI after an automated keyboard failure, verify the test's input semantics. Focus the intended control and inspect `document.activeElement` and its initial state. For an Enter activation, send the complete character-bearing event: `keyDown` with `key='Enter'`, `code='Enter'`, virtual key 13, `text='\r'` and `unmodifiedText='\r'`, followed by `keyUp`. A tested native `<summary>` remained closed with a character-less dispatch and opened with the complete event. Assert the actual `details.open` transition; do not substitute `.click()` or setting `.open=true` for keyboard evidence. Check expanded content for layout and contrast too.

See `references/independent-runs-and-keyboard-probes.md` for the validated event recipe and run-record evidence boundaries.

## Workflow

1. **Build** the artifact(s). Tokens in one CSS file; templates reference tokens only.
2. **Render** desktop + mobile PNGs (`render_cdp.py`).
3. **Preflight** (`design_preflight.py`). Expect failures on the first run.
4. **Look at the PNGs with a vision tool.** A screenshot you have not looked at is not
   evidence. Read the actual pixels for: duplicated navigation, elements clipped by a
   section boundary, text running off the edge, broken grids, wrong colours, empty
   sections, awkward whitespace.
5. **Fix and re-render.** Bump through steps 2–4 until preflight is clean *and* the
   images look right. These are two independent gates; passing one does not imply the other.
6. **Report** the verification result — which checks passed, which defects were found by
   rendering, and what was not verified at all.

## The defects that rendering catches and source review does not

These are not hypothetical. Each of them was found in a single real session by rendering
and looking, while reading the source had looked fine:

- **Duplicated navigation.** A desktop nav and a mobile nav both visible below the
  breakpoint, because the "hide on mobile" rule was never added.
- **A button clipped by its section band.** The CSS put vertical padding on
  `.page-head__inner`; the markup used `.page-head__grid`. The class that received the
  padding was never in the document. **The static class cross-check finds this; a human
  reading the CSS will not.**
- **A primary CTA failing WCAG AA** at 3.07:1 that looked perfectly fine — white on a
  saturated coral. Reads as deliberate, measures as a failure.
- **Muted text below 4.5:1** in two places. Both looked "grey enough" to the eye.
- **Anchor navigation landing under a sticky header**, hiding the target heading.
- **A "skip to content" link that was 25px tall** — present, focusable, but under the
  44px target floor.

The pattern: **every one of these is invisible in the source and obvious in the pixels.**

## Contrast: derive, don't eyeball

Never guess a passing colour. Compute it.

```python
def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2])

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
```

Then, for a failing pair, **search for a value that passes** rather than accepting the
fail or dropping to a different colour. Often the fix is inverting the foreground rather
than changing the brand colour: white-on-coral at 3.07:1 becomes deep-ink-on-coral at
5.25:1, and the button looks *more* deliberate, not less.

A saturated accent that is too light for white text is extremely common. Dark ink on a
warm bright accent is the usual answer, and it reads as a designed choice.

## Grounding a design in reference assets, not impressions

If the brief supplies a logo, screenshots of a current/competitor site, or any other
reference imagery, **extract concrete facts from the pixels before choosing tokens** —
do not describe the reference impressionistically and invent a palette that "feels like
it." Pixel sampling establishes concrete asset facts; it does **not** establish approval
or guarantee a successful composition. Use measured colors as evidence and distinguish them
from deliberately derived accessible action colors. Approval remains an explicit current
ruling, never a conclusion inferred from palette fidelity or a historical session narrative.

Two moves, both stdlib + Pillow, no extra install:

```python
from PIL import Image

im = Image.open("logo.png").convert("RGBA")
# Exact brand colour, ignoring anti-aliased edge pixels and transparency:
colors = {}
for x in range(im.width):
    for y in range(im.height):
        r, g, b, a = im.getpixel((x, y))
        if a > 200:                      # skip near-transparent edge pixels
            colors[(r, g, b)] = colors.get((r, g, b), 0) + 1
dominant = max(colors, key=colors.get)   # the actual mark colour, not a guess

# Exact proportions, so a supplied logo is never stretched:
print(im.size)                           # (w, h) — preserve this ratio everywhere
```

For a reference *screenshot* (not a flat logo), sample a small box in the region you
care about rather than the whole image — `im.crop(box).getcolors()` — because a full-image
histogram is dominated by whatever covers the most pixels (usually the background), not
the button or headline colour you're trying to confirm.

Use a vision tool to describe *what* each reference image shows (which page, what layout,
what hierarchy) and use pixel sampling to confirm *the exact colour values* — the two are
complementary, not redundant. A vision description alone will approximate a colour
("navy", "bright red-orange"); pixel sampling gives you the hex to put in a token file.

**Gotcha — a transparent logo is misread by a quick flattened histogram.** Running
`im.convert("RGB")` (or `resize` then counting colours) flattens every transparent pixel to
the RGB of its palette slot, so a red mark on a *transparent* background can histogram as
"green" when the PNG's background index happens to be a green value with alpha 0. Sample
**opaque pixels only** (`a > 200` after `.convert("RGBA")`, as in the recipe above) and read
the mark colour from the opaque cluster, not the flattened histogram. Confirm with a corner /
alpha check (`im.getchannel("A")` — a fully transparent background confirms the mark sits on
nothing).

### Prove the inspection route before you claim it

When asked to demonstrate image-inspection capability — or simply before you depend on it —
establish which route actually ran, and say so precisely. `vision_analyze` either attaches the
image to the **active main model** (native fast path; the tool says *"Image loaded into your
context — you can see it natively now"*) or calls a **separate auxiliary vision LLM** and
returns prose. The gateway log states it outright:
`/home/moose/.hermes/profiles/<profile>/logs/agent.log` →
`INFO tools.vision_tools: vision_analyze: native fast path`, alongside
`Vision auto-detect: using main provider <provider> (<model>)`.

Never infer vision capability from the session model name, from filenames, or from a prior
session's notes. Note that running the routing helper in a **standalone** interpreter does
not reproduce the live decision (it lacks the session's runtime identity) — the live tool
message plus the gateway log are authoritative.

Two log lines in this harness are easy to misread, and misreading them produces a false
capability report:

- `agent.auxiliary_client: Auxiliary approval: using custom (<model>) at http://…` is
  printed on the **native** path as well — it records the provider identity used for the
  multimodal request, not an auxiliary vision call. It is **not** evidence that a separate
  vision LLM did the seeing. Count the route instead, in the profile's `logs/agent.log`:
  `grep -c 'vision_analyze: native fast path'` versus `grep -c 'vision_tools.*aux'`.
  (Measured on a live session: 513 native, 0 auxiliary.)
- `RuntimeError: No LLM provider configured for task=vision provider=auto` in
  `logs/errors.log` belongs to an **earlier** session or model unless its timestamp falls
  inside the current session. Read the timestamp before reporting it as a live blocker.

How the native route can be enabled with **no** config override at all: `decide_image_input_mode`
asks `_lookup_supports_vision`, which consults the models.dev capability cache. A cache
entry for the active model slug with `attachment: true` and `modalities.input` containing
`image` resolves `supports_vision=True`, which satisfies the OR-condition inside
`_should_use_native_vision_fast_path()` even though `_supports_media_in_tool_results("custom", …)`
returns False. Read the cached entry to explain *why* native inspection happened: the route
itself is observed, but the mechanism is worth reporting when a capability check is asked
for, and it explains how a local Ollama provider can be vision-capable without any
`supports_vision` key in `config.yaml`.

**Tall screenshots lose fidelity before the model sees them.** Hermes downscales to
`max_dimension=1568` and a ~0.2 MB budget: a 780×9624 mobile render arrives at 97×1203, a
2880×9138 desktop render at 360×1142. Rhythm, section order and colour survive; body type
does not. For any consequential read — headline wording, control stacking, small type,
expanded states — use the `region` crop parameter to inspect the page in native-width
vertical bands, alongside a full-page pass for composition.

See `references/vision-inspection-capability.md` for the native-vs-auxiliary evidence chain,
the measured resize table, the banded-crop pattern, the rendered-screenshot read results and
the reporting shape for a capability check.

### When the assignment is only a capability check

A capability check is a bounded read-only task with its own acceptance criteria — verify
the named inputs open, inspect one image semantically, name the tool/model and limits, and
**stop**. It is not permission to begin the downstream design work, and no output files
should be produced during one. Prove file access with a readability loop over the exact
paths rather than a directory listing, confirm the inputs tree and workspace are unmodified
before reporting, and re-inspect the image with pointed questions (exact button label,
which word carries the accent, is there a stock watermark) to prove the read is real
rather than impressionistic. Report the requested detail count concretely — composition
and placement, typography and headline treatment, one distinctive visual element.

**When no vision provider is configured** (`vision_analyze` → "No LLM provider configured for
task=vision", common on text-only models), do not fabricate what a reference "shows" or what a
render "looks like". Keep the task moving with **programmatic-only inspection**: opaque-colour
sampling + a coarse luminance grid + aspect/orientation for *input* images, and dominant-colour /
average-luminance / blank-render checks for your *own* rendered PNGs (a near-uniform or
wrong-colour render is caught without a screenshot). Then report the exact blocker and mark
every fact **measured vs. inferred** — pixel/colour/luminance data is measured; "the reference
reads warm/airy/dark" is an inference from that data, not a visual observation. Never claim a
render was "looked at" when only machine checks ran.

### Test shared components in every background context they appear in, not just once

A component meant to appear on both light and dark surfaces — an `.eyebrow` label, a
plain `<p>`, a muted caption — usually gets one color tuned for the light theme. When the
same class is reused inside a dark band elsewhere in the same page set (a page-head
banner, a CTA panel, a footer), it silently inherits that light-theme color and can fail
contrast outright: 3.5:1 against navy, nowhere near AA, while the identical token reads
fine against white. This is invisible by eye and only surfaces when the preflight measures
the *actual* computed color against the *actual* composited background for that specific
instance, not one representative sample of the class.

Fix with a scoped override on the darker context, not a global repaint of the component:

```css
.page-head .eyebrow { color: var(--brand-400); }      /* readable on navy */
.page-head p:not(.lead):not(.eyebrow) { color: var(--ink-inverse-muted); }
```

Then extend the preflight's contrast sample list to include the component **inside its
dark-context selector** (e.g. `.page-head .eyebrow`, not just `.eyebrow`) so the check
exercises the same instance that actually ships on that band. A check that only ever
measures the bare `.eyebrow` class against the page body background will never catch this
— it has to be checked once per background context the class is dropped into.

## Pitfalls

- **Inspect every supplied reference with the semantic pass, not just pixel sampling.**
  Pixel sampling gives exact colour values and dimensions; it cannot tell you whether a
  checkerboard block is solid greyscale texture or a transparency indicator, and it will
  never surface a **stock watermark** ("dreamstime"), embedded logos or placeholder copy.
  Ask about marks and watermarks explicitly on every reference. A watermarked stock mockup
  is **reference-only** — it may inform composition, but its artwork, logo slot, copy and
  marks cannot be reused in a client deliverable, and its presence in an inputs tree does
  not license it. State that plainly and check sibling images for the same condition.

- **A bare-element descendant selector silently erases a token-driven colour — and the
  preflight will NOT catch it.** `.nav a { color: var(--ink); }` has specificity (0,1,1) and beats
  `.nav-cta { color: var(--ink-inverse); }` at (0,1,0) for every link inside `.nav`, however the
  second rule is written or ordered. The result is dark-on-dark text that is **invisible on the
  rendered page**. In one session this hid a header phone number *and* the text of a required
  provisional-notice box, while the preflight reported only a tap-target width failure and **zero**
  contrast failures — the sampled pair resolved to the same colour family. Only the pixels exposed
  it. Fix by making the child win (`.nav a.nav-cta { … }`) or by colouring the base `a` class
  alone — never by re-ordering the cascade, since specificity beats order. Audit every rule that
  sets colour on a **bare element name** (`a`, `p`, `li`, `b`, `span`) under a scoped parent.
- **An archive can never contain its own hash.** Writing a ZIP's SHA-256 or byte size into a file
  *inside* that ZIP is circular — the write changes the digest. Compute the size and SHA-256 once,
  as the final step after the last document edit, and report them **outside** the package
  (delivery message or a sidecar file next to the archive). Inside, record the path plus member
  and file counts. Never zip → edit → zip → edit; each cycle invalidates the recorded value.
- **Verify the extracted archive, not just `unzip -t`.** `unzip -t` proves compression integrity
  only. Extract to a temp dir and assert: the protected asset hashes identically to its source,
  every local `href`/`src` in every HTML file resolves, and every required member is present **by
  name**. Note that the zip member count includes directory entries, so it exceeds the real file
  count — say which number you report. Keep `ZipFile.namelist()` inside the `with` block; calling
  it afterwards raises `AttributeError: 'str' object has no attribute 'namelist'`.
- **A comparison index is an artifact too — render and inspect it.** Full-page renders in a pack
  have different aspect ratios, so thumbnails need an explicit crop
  (`.shot img{width:100%;height:420px;object-fit:cover;object-position:top}`) to keep every card's
  hero in frame and the grid even, and the cropping must be **disclosed on the index page** so a
  reader does not mistake a cropped thumbnail for the whole page.
- **Never give a new utility/navigation file the same filename as an existing approved
  deliverable.** A "see all pages" index written to `index.html` silently overwrote an
  already-approved homepage in one session — the write succeeded, nothing errored, and the
  loss was only caught afterward by a content check (grepping for a phrase that
  should still have been there). Give meta/navigation pages a name that cannot collide
  (`PACKAGE_INDEX.html`, `_overview.html`), and after any batch of writes into a folder
  that may already hold approved content, verify every touched path still contains what
  it should — a successful write is not proof it didn't clobber something.

- **Long inline shell payloads can be blocked before they run.** A single command mixing
  pipes, `$()` and several greps may hit a command-parser / hardline block — the block
  fires on payload *shape*, not on the operation being harmless. A filesystem-wide `find`
  can also exceed the foreground timeout and return nothing useful. Work in smaller calls:
  `search_files` with `output_mode="count"` for occurrence counts, or one `grep -c` per
  pattern in its own terminal call, and target only the directories you need. A blocked
  command is a harness artefact, not a finding about the artifact under review.
- **Do not mistake an "Auxiliary approval" log line for an auxiliary vision call.** It
  appears on the native path too. Count `vision_analyze: native fast path` versus
  `vision_tools.*aux` in the profile's `logs/agent.log` and report the measured counts;
  likewise, check the timestamp on any `No LLM provider configured for task=vision` error
  before calling it a live blocker — it is usually from an earlier session or model.

- **Never claim visual verification without looking at the render.** "The file renders"
  is not "the design is right." Use a vision tool on the PNG.
- **`--default-background-color=0` is invalid** and makes Chrome's `--screenshot` mode
  exit with an error and write **no file at all**. Use a hex value or omit the flag. If
  `google-chrome --headless --screenshot=out.png` produces nothing, suspect a bad flag
  before suspecting a missing browser.
- **Chrome's `--screenshot` flag captures the viewport only.** For full-page PNGs you
  need the CDP path.
- **Measure the page height after `document.fonts.ready`.** Self-hosted fonts change
  layout; measuring early yields a truncated screenshot.
- **Responsive image width needs responsive height.** An `<img>` with intrinsic width/height
  attributes can retain a desktop CSS height after its width shrinks, leaving a huge empty
  mobile stage while overflow and contrast still pass. Use `height: auto` for proportional
  scaling, verify the intended aspect ratio or crop, then inspect the render.
- **A 44px target check must measure width AND height.** A tall but narrow navigation link
  does not meet a 44×44px design floor. The supplied probe checks both dimensions; do not
  describe that project-specific floor as WCAG AA's universal requirement.
- **Copy-check false positives need regression fixtures.** Use word boundaries: a loose
  `book a` pattern can match “Facebook advertising.” Preserve legitimate copy, tighten the
  pattern, and test both a forbidden positive and an allowed negative example.
- **Tool output can be redacted, and the file on disk is fine.** During one session the
  display layer masked a phone number in every read and search result, which looked
  exactly like the file containing `****`. Before "fixing" a string you believe was
  corrupted, verify the bytes on disk with a boolean containment check or a hash
  comparison against the value you expect. Editing a correct file to satisfy a
  redacted readback is a self-inflicted bug.
- **A rule for a class that is not in the markup is a silent failure.** Padding declared
  on the wrong class produces a clipped element with no error anywhere. Cross-check
  statically.
- **Dropping a shared base rule during a per-concept CSS restructure breaks every concept
  at once — and every automated check still passes.** In one session the shared
  `.hero-art{position:relative}` + `img{object-fit:cover}` pair was lost while splitting
  styles into per-direction blocks: the decorative `::before` backing shapes then painted
  OVER all three hero photographs (one hero showed a plain red rectangle instead of its
  image). No overflow, no contrast failure, no unused-class warning — the class was still
  referenced; only its layering behavior vanished. Pattern: any `::before`/`::after`
  backing layer needs its container to establish stacking (`position:relative`, image
  `position:relative` or `z-index` above the pseudo-element). After restructuring shared
  CSS, re-render and LOOK at every page before trusting a green preflight.
- **Custom DOM-structure checks must tolerate wrapper divs.** A `main>section` child
  selector undercounts when one concept wraps its hero `<section>` in a full-bleed panel
  `<div>`; use `main section` (descendant) with an exact expected count instead, so the
  bound still holds without forbidding legitimate wrappers.
- **Contrast failures are not always fixed by darkening the foreground** — but they almost
  always can be fixed by *changing* it, rather than by abandoning the accent.
- **Do not install a large toolchain just to render.** System Chrome plus stdlib is
  enough, and the pack-level constraint may forbid the install anyway.
- **Verify the page is not wider than the viewport, not just that a scrollbar exists.**
  `scrollWidth - innerWidth > 0` is the overflow signal; report the offending elements.
- **A passing preflight is not a passing artifact.** The preflight only covers the
  checks it implements. Markup structure, copy compliance and visual composition are
  separate gates, and a reviewer can find defects the machine cannot see. When someone
  reports a defect your preflight did not catch, that is a gap in the *script*, not a
  wrong report — add a check for it.
- **Fix the generator, not the generated file.** If a page comes from a build script
  or template, patching the output is a half-fix: the next run reintroduces the
  defect. Find the root cause in the generator. The usual culprit is a slice helper
  with an **inclusive** end marker, which silently swallows the next element's
  opening tag:
  ```python
  j = text.index(end, i) + len(end)   # inclusive — swallows what follows
  j = text.index(end, i)                # exclusive — correct
  ```
  Symptom: a duplicate `<main>` or a doubled `</footer>` in pages built from a shared
  shell, while the canonical source page is clean.
- **Regenerating from a fixed generator can revert earlier direct patches.** If you
  ever hand-edited a generated file, that edit is now owned by the generator and the
  next regeneration will wipe it. Re-apply it at the source of truth and re-run the
  preflight — it surfaces the regression as a concrete failure rather than silently.
- **`design_preflight.py --viewport` takes `name:WIDTH`, not `WIDTHxHEIGHT`.** Passing
  `--viewport 390x844` crashes with `ValueError: invalid literal for int() ... ''` because
  the parser splits on `:` and takes only a width. Use `--viewport mobile:390`
  (`w320:320 w390:390 w768:768 w1440:1440` for a four-width sweep). The renderer
  (`render_cdp.py`) is the one that takes `name:WxH` — the two scripts differ.\n- **Create linked report files before the link check runs.** A comparison index that links
  `verification.json` or `RUN_RECORD.md` fails its own dead-link check on the first run if
  those files don't exist yet. Write an initial in-progress RUN_RECORD.md and a placeholder
  report at package setup (the run record should exist from the start anyway to hold the
  observed start timestamp), then overwrite with finals. A first-run link failure on a
  not-yet-written report is a sequencing artifact, not a design defect — but fix the
  sequence rather than whitelisting the link.\n- **Rendered-text parity checks must normalize CSS text transforms.** `innerText` reflects
  `text-transform: uppercase`, so an exact compare of rendered copy against the source
  dataset fails on every uppercased label even though the markup is correct. Either compare
  `textContent`, or normalize case/`\\u00a0` (non-breaking spaces inserted to fix orphaned
  headline words) on both sides before comparing. Keep a negative control proving a real
  copy change still fails.\n- **An orphaned word on its own headline line is a rendering-caught defect.** Fix with a
  `\\u00a0` between the last two words or a rebalanced `<br>`, then re-render BOTH viewports
  — and remember the nbsp now lives in the copy dataset, so parity checks need the
  normalization above.\n- **Negative-test every new check.** A check that passes everything is worthless.
  Build a deliberately broken copy — inject a duplicate `<main>`, a stray closing
  tag, a banned phrase — and confirm the script exits non-zero and names the right
  defect. A check you have never seen fail is a check you cannot trust to pass.

## What to report

Say plainly:

- which automated checks passed, with the numbers (contrast ratios, overflow pixels);
- which defects were found **by rendering**, since that is the evidence that matters;
- which defects were found by **a reviewer that your checks did not cover** — and that you
  then added a check for. Silence about a reviewer's catch implies the machine was right
  about everything, which it was not;
- what was **not** verified (real devices, other browsers, screen readers, performance
  scores, the production build) — never imply coverage you do not have.

When a reviewer's reported defect turns out to be a tool artefact, say so **and** check
whether the underlying risk is real under a different framing. "The evidence was wrong" is
not the same as "the finding was wrong" — see the playbook, §12.

## Support files

| File | Purpose |
|---|---|
| `scripts/render_cdp.py` | Full-page PNG renderer. System Chrome + DevTools Protocol over a raw stdlib WebSocket. Zero install. |
| `scripts/design_preflight.py` | Automated preflight: overflow, tap targets, WCAG contrast, heading order, alt text, form controls, dead links, raw-source markup validity, copy compliance, CSS↔HTML class cross-check. Exits non-zero on failure. |
| `references/verification-playbook.md` | The session record: each defect, how it was caught, and the exact fix. Read when a preflight failure is puzzling or a new class of defect appears. |
| `references/vision-inspection-capability.md` | Native-vs-auxiliary vision evidence chain, the auto-resize ceiling and the `region` banded-crop pattern for tall screenshots, semantic-vs-pixel inspection boundaries, the capability-check-only assignment shape, and the reporting shape for a capability check. |
| `references/runtime-model-identity.md` | How to establish which model/provider actually served a session from runtime logs, detect mid-chat model switches, and report the model label vs. an independently verified provider response ID honestly. |
| `references/archive-integrity-and-invisible-text.md` | The archive self-hash trap and the extract-and-verify recipe; the invisible-text defect class a green preflight misses (bare-element descendant selector out-specifying a token-driven colour); comparison-index thumbnail cropping and disclosure; gold-on-red accent mismatch; pruning unused font binaries before packaging; the 390px nav-row-to-grid repair. |
