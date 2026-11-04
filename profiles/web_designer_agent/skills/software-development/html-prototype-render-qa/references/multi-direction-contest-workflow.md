# Multi-direction contest workflow — render/preflight recipes

Sessions: Cyberize design contest entries `3-kimi-v2` (2026-11-02) and `8-minimax` (2026-11-03) —
four bounded directions from four references, delivered in one package each. These are the
render/preflight lessons that the shared bounded-directions section does not already cover.

## 1. `render_cdp.py` is single-target with fixed output names

The renderer accepts **one** file-or-dir target and always writes `index-desktop.png` /
`index-mobile.png` under `--out`. Looping four directions into a shared `previews/` dir silently
overwrites the previous direction on every iteration — you end up with only the last page's PNGs.

**Recipe** — render each target to its own temp dir, then move into the final names:

```bash
R=<skill>/scripts/render_cdp.py
for d in 01 02 03 04; do
  python3 -B "$R" direction-$d/index.html --out /tmp/rd$d \
      --viewport desktop:1440x1000 --viewport mobile:390x844 >/dev/null 2>&1
  mv /tmp/rd$d/index-desktop.png previews/direction-$d-desktop.png
  mv /tmp/rd$d/index-mobile.png  previews/direction-$d-mobile.png
done
```

After a batch, `ls previews/` and count before claiming the set exists.

## 2. `design_preflight.py` scope and its two false-signal modes in multi-direction packs

The preflight also accepts **one** `pages` argument. For a pack of sibling direction folders, run it
once per direction (loop) and once on the package root for the comparison index.

- **CSS↔HTML cross-check false-fires on inline `<style>` pages.** When directions style themselves
  in `<style>` blocks and you pass only the shared token CSS via `--css`, every direction-internal
  class reports "markup class with no CSS rule" and shared utility classes report "never used."
  These are scope artifacts, not defects — either concatenate the relevant CSS, or read them as
  expected noise and keep the real gate green. Never report them as unused-code bugs to a reviewer.
- **Pseudo-element surfaces produce fake contrast failures.** White text on a dark gradient that is
  implemented as `::before { background: radial-gradient(...) }` is measured against the transparent
  ancestor → reported as "white on white, ratio 1". This is the documented heuristic limit. The
  correct response is the one already in the main pitfall list: verify on the rendered PNG and label
  the machine result a false positive with the actual surface described. But be careful the
  **opposite** failure hides in the same report: a genuinely invisible white nav on a white header
  appears as the *same* "white on white" signature. Both fired in one run here — dismiss only the
  instances you have visually confirmed on the pixels, never whole-file.

## 3. The 44px tap-target fix needs width AND a decoration-aware treatment

Raising `min-height:44px` alone does not clear the check:

- Short-word links ("SEO", "PPC" ≈ 34px wide) also need `min-width:44px` (with
  `display:inline-flex; align-items:center; justify-content:center`).
- Links reporting 41–43px heights are suffering line-height/rounding collapse — switch
  `inline-block` + vertical padding to `inline-flex` + `align-items:center` + explicit `min-height`.
- A nav CTA underlined with `border-bottom` gains the 44px flex box, and the border then sits at the
  bottom of the box, visibly detached from the text. Replace it with
  `text-decoration:underline; text-decoration-thickness:2px; text-underline-offset:6px;` so the
  underline stays glued to the glyphs inside the taller target.
- The shared skip link needs the same treatment in the token file (`min-height:44px; inline-flex`),
  so fix it once there rather than per page.

## 4. Brand-red contrast ladder — second verified data point

Same identity red as the earlier worked example (`#F12800`). Measured this session:

| Pair | Ratio | Verdict |
|---|---|---|
| `#F12800` on white | 4.16 | large text / bold only |
| white on `#F12800` | 4.16 | **fails AA normal** — do not use for button labels |
| white on `#D93206` | 4.76 | passes AA normal — the button-fill fix, hue almost unchanged |
| `#B32300` on white | 6.65 | safe small-text accent |
| `#A81E00` on white | 7.37 | AAA normal |
| `#FF9E8A` on navy `#1B2340` | 7.72 | on-dark accent |
| `#FF7A5C` on navy `#1B2340` | 6.02 | on-dark accent, large/semibold |

Pattern: for a red-filled pill with a white label, keep the identity `#F12800` for shapes/icons and
step the *fill* down one notch to `#D93206`; reviewers cannot tell the difference and the check goes
green. (Contrast checker's `large-text` rule still applies to the big display headline on the same
red.)

## 5. Full-package green-run order that avoids the sequencing artifact

1. Write all report/docs the index links first (even as stubs) — or run the index's preflight last,
   after REVIEW/HANDOFF exist. Two "dead link REVIEW.md/HANDOFF.md" failures are the known
   sequencing artifact, not defects; fix by ordering, not whitelisting.
2. Final preflight sweep: per direction (loop) + package root.
3. Final `sha1sum assets/logo.png` against the source hash to prove byte-identical logo preservation
   in the delivered package.

## 6. Self-hosted fonts: copy once, prune once, license once

Fonts are the most common source of an accidental archive liability. The working sequence:

1. **Inventory what exists locally before designing.** `fc-list --format='%{family[0]}\n' | sort -u`
   gives the real families on the machine; `fc-list | grep -i '<family>'` gives the file paths.
   Copy only the specific weights the CSS will declare (`Regular`, `Bold`, `Medium`, `SemiBold`,
   `Italic`) from the family directory — not every file in it.
2. **Declare each weight explicitly** in `@font-face` with its own `font-weight`/`font-style`, and
   point `src` at the local relative path. Self-hosting means the pack renders identically offline
   and needs no install or network.
3. **Prune before packaging.** After all pages are written, diff the font directory against the
   `@font-face` declarations. Delete every `.ttf` that no rule references. This session copied
   families for two concepts that used the wrong weight set and had to remove the orphans — an
   unused binary still needs a licence notice, so it is a liability, not a free extra.
4. **Write the licence notice to match what actually ships.** `assets/fonts/FONT-LICENSES.md` should
   list each family, its licence (OFL 1.1 for all six here), and the system directory it came from.
   If you prune a file, the notice must not still claim to cover it.

Families used in the worked pack, all OFL and all present on the machine: Inter, Space Grotesk,
Noto Serif Display (incl. Italic), Roboto Condensed, JetBrains Mono, Michroma.

## 7. Inspection budget: whole page for rhythm, crops for anything that must be read

Eight full-page renders in one pack is a large token spend, and a full-page pass on a tall render
arrives downscaled to the point where small type is unreadable. The efficient split:

- **One whole-page pass per preview** to judge composition, order, rhythm and colour.
- **Region crops only where a read is consequential** — a header, a hero headline, a contact panel,
  a button row, a ticker. Budget these against the operator's explicit targeted-recheck limit and
  spend the budget on *changes*, not on the first survey.
- **Batch independent crops into one montage image** when several small regions need checking, so
  one vision call serves three questions. Label the panels so the reading is unambiguous.
- A full-page overview plus a targeted crop of each changed region is the efficient floor; a second
  full-page overview of an unchanged page buys nothing.

Keep the two budgets separate: inspecting the *input* images is evidence gathering and is not
charged against the operator's *output recheck* budget.

## 8. Build one grayscale comparison montage as the structural test

The brief's grayscale question ("if the colours disappeared, would a reviewer immediately recognise
N different approaches?") is best answered by *looking at the silhouettes side by side*, not by
reasoning about them one at a time. Build a single montage image and read it once.

```python
from PIL import Image, ImageDraw
P = 'previews/'
dirs = ['direction-01', 'direction-02', 'direction-03', 'direction-04']
tiles = []
for d in dirs:
    im = Image.open(P + f'{d}-desktop.png').convert('L')      # desaturate
    h = 900
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    tile = Image.new('RGB', (im.width, im.height + 34), 'white')
    tile.paste(im.convert('RGB'), (0, 34))
    ImageDraw.Draw(tile).text((10, 10), d.upper(), fill='black')
    tiles.append(tile)

W = sum(t.width for t in tiles) + 12 * (len(tiles) - 1)
sheet = Image.new('RGB', (W, max(t.height for t in tiles)), '#dddddd')
x = 0
for t in tiles:
    sheet.paste(t, (x, 0)); x += t.width + 12
sheet.save('/tmp/grayscale4.png')
```

Two things make the result trustworthy:

- **Desaturate with `.convert('L')`**, not by applying a CSS greyscale filter in the page — the
  question is about the *composition*, so the montage must show the actual rendered geometry.
- **Normalise the height, not the width.** Full-page renders differ in length (6018px vs 8258px
  here). Equal-height tiles keep the *proportions* of each composition comparable; equal-width
  tiles would make the longer page look like the denser design.

Then ask the question directly of the montage and read the answer as **subjective visual
judgment**, not as a passing test. If two silhouettes still read as one template, fix the
composition before delivery — and count that fix inside the recheck budget, since it forces a
re-render of both directions.

## 9. Brand accent roles: gold is a light-field accent, red is a fill

The preflight flagged a gold label (`#FFC53D`) placed on the brand-red fill as a contrast failure.
The rule that resolves it: **gold reads on the dark ink and on the cream/paper field; red reads as
a fill under dark or white text.** Gold-on-red is the mismatch, not red-on-cream.

Fix by moving the gold element onto the ink surface, or by confining gold strictly to the light
field. Do not "solve" it by shifting the red until gold passes on it — that breaks the brand
relationship for the rest of the page.
