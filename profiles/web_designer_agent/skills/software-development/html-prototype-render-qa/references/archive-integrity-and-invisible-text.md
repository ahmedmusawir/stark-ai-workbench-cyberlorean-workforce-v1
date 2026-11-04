# Archive integrity, invisible-text defects, and comparison-index thumbnails

Session: Cyberize four-direction concept pack, entry `8-minimax` (2026-11-03). These are the
packaging, CSS-specificity and index-presentation lessons that the shared sections do not cover.

## 1. An archive can never contain its own hash

Embedding the ZIP's SHA-256 (or byte size) in a file **inside** that ZIP is circular: writing the
digest changes the archive, which changes the digest. Every repackage invalidates the recorded
value. This session burned three full repackage cycles chasing it — each one produced a different
hash than the one just written into `HANDOFF.md`.

Rules:

- Record the archive size and SHA-256 **only in the delivery message** (chat/email), computed once
  after the last write to the package.
- Inside the package, reference the archive by **path + member/file counts + member names**, never
  by digest. `HANDOFF.md` can say "47 zip entries, 39 files; digest reported in the delivery message".
- Compute the digest exactly once, as the final command, and never re-zip afterwards.
- If a reviewer genuinely needs the digest inside the package, the only correct placement is a file
  that is **excluded from the archive** (e.g. a sidecar `.sha256` next to the ZIP).

Final sequence that works: write every document → render → preflight → zip once → `sha256sum` once
→ report. Never zip → edit → zip → edit.

## 2. Verify the *extracted* archive, not just the source folder

`unzip -t` proves compression integrity but proves nothing about whether the package works once
extracted. Run an independent extraction check against a temp dir:

```python
import zipfile, hashlib, pathlib, tempfile, re

z = 'CYBERIZE_....zip'
tmp = tempfile.mkdtemp(prefix='zipcheck-')
with zipfile.ZipFile(z) as f:
    assert f.testzip() is None          # no corrupt member
    names = set(f.namelist())
    f.extractall(tmp)

root = pathlib.Path(tmp) / '8-minimax'
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# 1. protected asset survived byte-identical
assert sha(root/'assets/logo.png') == sha(SOURCE_LOGO)

# 2. every local reference in every page resolves
missing = []
for html in root.rglob('*.html'):
    t = html.read_text()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', t):
        v = m.group(1)
        if v.startswith(('http', 'tel:', '#', 'mailto:', 'data:')):
            continue
        if not (html.parent / v.split('#')[0]).resolve().exists():
            missing.append((html.name, v))
assert not missing, missing

# 3. required members present BY NAME, not by count
need = ['8-minimax/index.html', '8-minimax/DANDOFF.md', ...]
assert not [n for n in need if n not in names]
```

Two reporting traps: the **member count includes directory entries** (this pack: 47 zip entries vs
39 real files) — say which number you mean; and `zipfile.ZipFile` is a context manager, so calling
`.namelist()` after the `with` block raises `AttributeError: 'str' object has no attribute
'namelist'`. Keep the `names` set inside the block.

## 3. A descendant selector can silently erase a token-driven colour

**This is the highest-value defect class in the pack.** A bare-element descendant selector sets
colour with specificity (0,1,1) and beats every single-class child rule (0,1,0) in that subtree —
even when the child rule is written later and looks "more specific" by intent.

```css
.nav a   { color: var(--ink); }   /* 0,1,1 — wins over .nav-cta below */
.nav-cta { color: var(--ink-inverse); }  /* 0,1,0 — never applies */
```

Result: white text on a dark pill renders **dark-on-dark and is invisible**. The same pattern with
`.prov p { color: … }` erased the `.prov b { color: var(--ink) }` provisional-notice text, making a
required compliance notice unreadable.

Detection and repair:

- **Only the rendered pixels reveal it.** The preflight reported a *tap-target width* failure for
  the same element but **no contrast failure** — the computed colour and the background resolved
  to the same family, so the sampler saw nothing wrong. Read the actual pixels; an element that
  should carry text reads as an empty block.
- Fix by making the child rule win, not by re-ordering:
  `.nav a.nav-cta { color: var(--ink-inverse); }` (0,2,1), or drop the bare-element descendant
  colour and set the colour on the base `a` class only.
- Audit every rule that colours a **bare element name** (`a`, `p`, `li`, `b`, `span`) under a
  scoped parent — each one silently out-specifies single-class descendants for that subtree.
- Same trap for the reverse case: a single-class rule that a later, more specific rule overrides.
  The rule of thumb is *specificity beats order*; the cascade order only breaks ties.

Corollary for review reports: a green preflight did not imply the text was legible. Contrast
sampling only covers what it can resolve in the DOM; anything driven by `currentColor`, a
pseudo-element or a competing cascade needs eyes.

## 4. Comparison-index thumbnails need an explicit crop, and the crop must be disclosed

Full-page renders in a pack have wildly different aspect ratios (this pack: 2880×6018, 2880×8076,
2880×8258, 2880×5834). Rendering them at natural size inside a card gives one unreadable sliver
and a huge empty box for the others.

Recipe that worked:

```css
.shot img      { width:100%; height:420px; object-fit:cover; object-position:top; }
.shot--mob img { height:300px; }
```

`object-position:top` keeps the hero (the part worth judging) in frame for every card, and the
fixed height makes the grid even regardless of page length. Then **disclose the cropping on the
index page itself** — a reader who sees a cropped thumbnail will assume it is the whole page.

The index is itself an artifact: render it at desktop and mobile and inspect it, like any other
page. Two index-only defects this session: thumbnails at natural height (fixed above), and a
single-column fact-chip row on mobile that ran long — fixed with a two-column grid at ≤560px
(`grid-template-columns:1fr 1fr`) rather than by deleting content.

## 5. Gold and red are opposite-surface accents; pairing them as text-on-fill fails

A gold label (`#FFC53D`) placed on the brand-red fill was flagged by the preflight as a contrast
failure. Gold reads on the **dark ink** and on the **cream/paper field**; red reads as a fill
under **dark or white** text. Using gold *on* red is the mismatch. Fix by moving the gold label onto
the ink surface, or by keeping gold strictly inside the light field. (The confirmed brand-red
ladder — white on `#D93206` = 4.76 passing, white on `#F12800` = 4.16 failing — is in
`references/multi-direction-contest-workflow.md` §4.)

## 6. Drop unused font binaries before packaging

Copying a font family into `assets/fonts/` and then not using it leaves an unneeded binary in the
archive that must still carry a licence notice. Audit the font directory against the `@font-face`
declarations actually present, delete the unused `.ttf` files, and make the licence notice list
exactly the files that ship. This session shipped 16 TTFs across 6 families (Inter, Space Grotesk,
Noto Serif Display, Roboto Condensed, JetBrains Mono, Michroma), all OFL, self-hosted, with
`assets/fonts/FONT-LICENSES.md` naming each family, licence and source directory.

## 7. A mobile nav row cannot hold nav + a phone CTA side by side

At 390px, a row of four nav labels plus a dark phone pill exceeded the width. The preflight
reported the **tap-target width** failure correctly. The repair was structural, not cosmetic: the
mobile nav becomes a two-row grid — labels wrap onto the first row(s), the phone CTA spans the
full width on its own row. Do not shrink the type to fit; a 390px nav row that fits is one fewer
readable item, not a better design.
