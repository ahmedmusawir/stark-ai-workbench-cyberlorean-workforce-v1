# Positioning corrections and truthful interactive-state evidence

Use when an approved visual direction needs a business-positioning correction during a multi-page expansion, or when state screenshots disagree with otherwise passing interaction tests.

## 1. Repair the message without discarding approved craft

A homepage can look excellent yet misrepresent a multi-service business. Diagnose what a visitor sees first, not what the source technically mentions:

| Layer | Failure | Repair |
|---|---|---|
| Headline | Expressive wording describes only one service | Reframe around the agency's complete source-supported offer |
| Lead | Mentions only a new or redesigned website | Explain the relationship among the actual service groups |
| Artwork | One huge website mockup outweighs everything else | Rebalance the composition so other offerings have meaningful visual presence |
| Opening hierarchy | Full offering exists only in a tiny eyebrow/footer | Prominent readable service groups and clear paths in the opening itself |
| Lower content | Home duplicates the dedicated design page | Concise agency orientation on Home; deeper service narrative on its own page |

For this user's digital-agency work, the corrected grouping is Website Design/Development, Website Support/Maintenance, and Website Traffic through SEO/PPC. This is a content-positioning preference, not a universal list for unrelated businesses. Preserve approved typography, palette, logo and illustration quality. An explicit correction within the direction is not permission to restart exploration.

Before changing anything, preserve the selected HTML/CSS/assets/PNGs and hash the actual inputs you can verify. Work in a new authorized destination. Do not claim all prior histories were hash-checked when only selected inputs were. Document:
- exact old/new prototype and screenshot paths;
- matching desktop/mobile CSS widths and image scale;
- headline, lead, artwork and hierarchy changes;
- precise source meaning and editorial rewrites;
- whether each original was copied unchanged or independently rerendered.

Link a large before/after comparison from the review index. Label cropped previews and keep full-page PNG links. Actually click the hero/service links at both viewport classes; shared-menu tests alone do not establish those paths. Separate positioning, visual and technical findings, and stop at the authorized review gate.

## 2. Capture the state that actually exists

Observed failure: native FAQ answers were genuinely open, but an immediate screenshot after smooth scrolling still showed the hero. The interaction test was valid; its screenshot was not evidence of the claimed visible region.

Preferred sequence:
1. Wait for fonts and image decoding; separately assert assets loaded rather than swallowing decode errors as success.
2. Focus and activate each native summary using complete keyboard events.
3. Assert `details.open` or the expected open count.
4. Capture the desired section directly in document coordinates, avoiding dependence on a scrolling animation.
5. Open the PNG and confirm the answers and focus state are actually visible.

With the skill's CDP client, after keyboard activation:

```python
assert cdp.evaluate(
    "document.querySelectorAll('.faq-list details[open]').length"
) == expected_count

clip = cdp.evaluate("""
(() => {
  const r = document.querySelector('.faq-section').getBoundingClientRect();
  return {
    x: 0,
    y: r.y + scrollY,
    width: innerWidth,
    height: r.height,
    scale: 1
  };
})()
""")
shot = cdp.call(
    'Page.captureScreenshot',
    format='png',
    captureBeyondViewport=True,
    clip=clip,
)
```

This full-width section recipe was exercised successfully at desktop/mobile. Device scale remains whatever was configured with `Emulation.setDeviceMetricsOverride`; record it rather than calling the clip's scale a device-pixel ratio. For a narrower component, derive its horizontal bounds too. If a viewport screenshot is required instead, confirm the intended region is in view and scrolling has settled before capture; do not rely on an arbitrary sleep.

Archive the misleading image with an artifact label, replace the active evidence and fix the capture helper. Do not claim a browser/UI defect merely because evidence was captured incorrectly. Likewise, a corrected screenshot does not invalidate a separate genuine accessibility finding.

## 3. Inspect focus clearance and the whole computed type rule

An expanded summary can pass contrast, target-size and overflow probes while its outward focus outline crosses the first answer line. Inspect the focused open state at readable scale. Account for outline width and outline offset; add enough spacing before the answer's text without hiding the focus indication. A tested repair used 10px answer top padding for that design's ring—not a universal spacing requirement. Preserve the before state, repeat the affected expanded-state probes at all target widths, capture and inspect again.

A second observed defect involved specificity:

```css
.prose > div > p:not(.eyebrow) { color: var(--muted); font-size: 14px; }
.prose .note > p { color: var(--inverse); font-size: 48px; }
```

The generic paragraph selector can win because `:not(.eyebrow)` contributes specificity. Merely making the note white may pass contrast while leaving its intended large typography at body size. Repair the owning selector/component and inspect computed color, size and line height at mobile and desktop; then view the render. Do not use a global repaint to fix one dark context.

## 4. Keep evidence and bundles current

After refinements, update the canonical renders and downstream previews that actually changed. Remove or clearly archive superseded loose inspection files so the active package does not contain ambiguous alternatives. A change confined to expanded FAQ padding need not alter closed canonical pages, but its affected states must be retested and recaptured; state the scope rather than implying an unrelated full retest.

Keep actual route paths exact in documentation: do not abbreviate `screenshots/page-mobile.png` to a root-relative filename that does not exist. Audit every active HTML page, style tile, comparison and review index, including local resources and fragments. A localhost smoke server can test real resources, then shut down; it is not deployment or public-route rewriting.

For this user's delivery preference, provide a date/time-stamped ZIP in Downloads when permitted by the active output scope. Include all runtime fonts/assets, license notices, before-state comparison dependencies, source/content files, required final PNGs and handoff. Clearly disclose if revision histories stay only on the shared disk. Read back ZIP members against source bytes and verify the Downloads copy, not just the archive-creation command. Do not overwrite an earlier bundle or package.
