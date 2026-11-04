# Verification playbook — defects found by rendering

A session record. Every entry is a defect that **passed source review** and was caught
only by rendering the artifact and looking at the pixels, or by the automated preflight.
Read this when a preflight failure is puzzling, or when you suspect a defect class that
is not yet covered by the preflight script.

---

## 1. Duplicated navigation below the breakpoint

**Symptom.** On a 390px render, the header showed a full desktop nav row *and* a mobile
nav row beneath it — two sets of the same three links.

**Cause.** The stylesheet had a desktop rule with no matching media query, so the
desktop link list was never hidden. The mobile row was added with its own
`@media (min-width: 1024px) { display: none; }` but nothing hid the desktop one below
that width.

**Fix.** Default the desktop element to hidden, then reveal it at the breakpoint:

```css
.site-nav__links { display: none; align-items: center; gap: var(--space-5); }
@media (min-width: 1024px) { .site-nav__links { display: flex; } }
```

**Lesson.** In a responsive system, the *larger* viewport's layout should be the
opt-in, not the default. Set the base rule to the mobile presentation and let media
queries add the desktop one. Otherwise every new desktop element leaks onto mobile.

---

## 2. A button clipped by its section band

**Symptom.** On the Services page, the "Let's talk" button in the dark page-header band
had its bottom edge flush against the band's lower boundary — zero clearance, visibly
cut off.

**Cause.** The CSS defined padding on `.page-head__inner`:

```css
.page-head__inner { padding-block: var(--space-9) var(--space-9); }
```

But the markup used `.container.page-head__grid` — **`.page-head__inner` was never in
the document**. The band therefore had no vertical padding at all, and the grid's
content ran to the very edge.

**Fix.** Put the padding on the class the markup actually uses:

```css
.page-head__grid { display: grid; gap: var(--space-8); align-items: end;
                   padding-block: var(--space-9) var(--space-9); }
```

**Lesson.** This is the single most valuable static check: **a CSS rule whose selector
never appears in the markup is a silent failure.** It produces a wrong result with no
error anywhere — no console message, no failed assertion. `design_preflight.py` reports
both directions of the mismatch: rules with no markup, and markup with no rule.

Read the rendered output, not the CSS, when a page has a band or panel whose content
looks tight against an edge.

---

## 3. Primary CTA failing WCAG AA while looking correct

**Symptom.** The primary button was white text on a saturated coral accent. Visually
it looked like a deliberate, high-quality button. Measured: **3.07:1** against a 4.5:1
requirement for body-size text.

**Fix.** Keep the brand colour, change the foreground. Deep ink on the same coral:

| Foreground | Ratio on `#FF5C35` | Verdict |
|---|---|---|
| white `#FFFFFF` | 3.07 | FAIL |
| ink `#0A242C` | **5.25** | PASS |
| ink-deep `#071A20` | 5.80 | PASS |

**Lesson.** Saturated warm accents are almost always too light for white text. Dark ink
on the accent is the standard answer — and it looks *more* deliberate, not less. Compute
the ratio; do not eyeball it, and do not abandon the accent colour to "fix" contrast.

Derivation helper:

```python
def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126*f(rgb[0]) + 0.7152*f(rgb[1]) + 0.0722*f(rgb[2])

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
```

Search for a passing value rather than accepting the failure:

```python
for c in ["#64777C", "#5A6D72", "#556A6F", "#506469"]:
    print(c, round(ratio(hex_rgb(c), hex_rgb("F7F4ED")), 2))
```

---

## 4. Muted text below AA in two places

| Token | Was | Ratio | Now | Ratio |
|---|---|---|---|---|
| `--text-muted` | `#64777C` | 4.28 | `#5A6D72` | **4.95** |
| `--warn-500` | `#B07203` | 3.64 | `#8A5602` | **5.60** |

Both looked "grey enough" and "amber enough" to the eye. Neither passed.

**Lesson.** Muted text and warning colours are the two most common AA failures, because
they are chosen by feel against a *known* surface rather than measured. Derive them from
the surface colour.

Note the check must resolve the **effective** background by walking ancestors —
`--text-muted` on a white card inside a bone page is a different ratio than on the page
itself. The preflight script composites ancestor layers and skips elements sitting on a
background image, where the answer is not determinable.

---

## 5. Tap targets under 44px

Seven distinct elements failed on mobile. Each was a real, reachable link:

- a skip link, 121×25 — present and focusable, but under the floor
- the wordmark, 170×32
- arrow links in solution cards and service rows, ~25px tall
- footer column links, 19px tall
- service-page in-page TOC chips, 35px tall
- the phone link inside the CTA band, 34px tall
- the phone link inside a contact card, 22px tall

**Fixes.** Vertical padding plus `min-height: 44px` on each. Where the element was an
inline link inside a larger block, the link itself got the height:

```css
.link-arrow { padding-block: 0.55rem 0.45rem; min-height: 44px; }
.footer-col a { display: inline-flex; align-items: center; min-height: 44px; }
.contact-card__value a { display: inline-flex; align-items: center; min-height: 44px; }
```

**Lesson.** `min-height` alone does not work on a non-flex inline element — it needs
`display: inline-flex; align-items: center` to actually take effect. Measure the
*rendered* box, not the intent.

---

## 6. Chrome's `--screenshot` wrote no file

**Symptom.** `google-chrome --headless --screenshot=out.png` exited with an error and
produced no image, while the identical command without one flag worked perfectly.

**Cause.** `--default-background-color=0` is not a valid value — it must be a hex
`RRGGBB[AA]`. Chrome rejected the flag and aborted the capture.

**Lesson.** When a headless Chrome command produces no file, **suspect a bad flag
before suspecting a missing browser**. Run the command with the flag removed to
isolate. Also note the `--screenshot` flag captures the **viewport only**; full-page
captures need the DevTools Protocol path.

---

## 7. Tool output redaction vs. real file corruption

**Symptom.** Every read of the HTML showed a phone number as `+180****0668` — the
number was `+18009830668` when written. Attempts to write the correct value
"failed": the file still showed the masked form.

**Cause.** The **display layer** of the tool output was redacting the digit run. The
file on disk was correct the whole time. Confirmed by a boolean containment check and
a SHA-256 comparison of the file bytes against the expected bytes.

**Lesson.** Before "repairing" a string you believe was corrupted on disk, verify the
bytes:

```python
data = pathlib.Path(p).read_bytes()
assert b'8009830668' in data          # the real value is present
assert b'800****0668' not in data      # the masked form is absent
```

A hash comparison against the value you expect is even stronger. Editing a correct
file to satisfy a redacted readback is a self-inflicted bug, and a second
write can genuinely corrupt the file if you are not careful.

---

## 8. Verifying the fix with pixel geometry, not by eye

When a spacing or clipping question is ambiguous, measure it in the PNG rather than
squinting at it:

```python
from PIL import Image
im = Image.open("page-desktop.png").convert("RGB")
def px(x, y): return im.getpixel((x, y))

# find where a dark band ends
col = 200
for y in range(0, 1400):
    if px(col, y) == (247, 244, 237) and y > 200:
        band_bottom = y
        break

# find the extent of an accent-coloured element in a column range
rows = {}
for y in range(0, band_bottom + 40):
    xs = [x for x in range(1300, 2400, 2) if is_accent(px(x, y))]
    if xs:
        rows[y] = xs
```

The PNG is at 2× device scale, so divide device pixels by 2 for CSS pixels. This
turned "the button looks clipped" into "the button ended at CSS y 444 and the band
ended at CSS y 445" — and after the fix, "104px of clearance".

**Lesson.** When a layout question has a numeric answer, compute it. Pixel analysis
of the render is the ground truth about what shipped.

---

## 9. Waiting for fonts before measuring

Measuring `scrollHeight` before self-hosted web fonts load yields the wrong page
height and a truncated full-page screenshot. The fix is one `awaitPromise` call:

```js
(async () => {
  if (document.fonts && document.fonts.ready) { await document.fonts.ready; }
  return document.documentElement.scrollHeight;
})()
```

`Runtime.evaluate` needs `awaitPromise: true` for this to work. If fonts are fetched
from a remote origin, also confirm they actually loaded (a `document.fonts.check()`
probe) — a blocked font request silently falls back to a system face and changes
every metric.

---

## 10. Structural defects the browser silently repairs

**Symptom.** A reviewer found a duplicate `<main id="main">`, a stray `</footer></footer>`, and a
leftover `<!-- HERO -->` comment in two of three pages. The full preflight — contrast, overflow,
heading order, tap targets, alt text — reported **ALL CHECKS PASSED**, because every one of those
checks reads the DOM.

**Cause.** The browser repairs the markup on parse. A second `<main>` and an extra `</footer>`
are folded into a well-formed DOM, so the rendered page looks correct and *every DOM-level probe
agrees it is correct*. The defect only exists in the source file, which is what gets handed to a
Developer as reference markup.

**Root cause (deeper).** The pages were generated from a shared shell by a build script. The
slice helper used an **inclusive** end marker:

```python
j = text.index(end, i) + len(end)   # inclusive
```

so the header slice ran to *and including* the `<!-- HERO -->` marker — swallowing the canonical
page's `<main id="main">` — and the footer slice ran to *and including* `</footer>`, swallowing
the close tag. The canonical source page was clean; every generated page carried both artefacts.

**Fix (at the generator, not the output).**

```python
j = text.index(end, i)                # exclusive
header = between(HOME, '<!-- HEADER -->', '</header>') + '</header>'
footer = between(HOME, '<!-- FOOTER -->', '</footer>') + '</footer>'
```

**Lesson.** Patching the generated output would have left the generator to reintroduce the defect
on the next run. When a defect appears in *generated* files but not in their source, look at the
generator's slice/extraction boundaries before editing anything.

**Lesson.** Any check that reads the DOM cannot catch this class. Read the file:

```python
src = pathlib.Path(page).read_text()
assert src.count("<main") == 1
assert "</footer></footer>" not in src
ids = re.findall(r'\bid="([^"]+)"', src)
assert len(ids) == len(set(ids))
```

**Lesson.** A passing preflight is not a passing artifact. When a reviewer reports a defect
your preflight missed, the report is a gap in the *script*. Add the check.

---

## 11. Content-prohibited copy that survived a visual review

**Symptom.** The Web Design FAQ retained two items the brief explicitly excluded: a **30-day
bug-free guarantee** and a **6-to-8-week delivery timeline** (with "as little as 2 weeks"). The
visual preflight could not see them — the page was well-formed, accessible, and correctly styled.
The design spec's own provenance table even claimed "guarantees … timelines … Omitted per brief",
while the deliverable still shipped them.

**Why it slipped.** Copy compliance is a *content* requirement that looks like copy review. It
is invisible to every layout and accessibility check, and it is invisible to a reviewer focused
on layout. It only surfaces if you check the prose against the brief's explicit prohibitions.

**Fix.** Delete the two items. Do not simply delete the guarantee question and lose a genuine
customer question — replace it with a neutral process statement carrying no day count, no week
count and no outcome promise:

> **What happens after my site goes live?**
> Your site is yours to run, and we can stay involved after launch. Our website support and
> maintenance programs cover ongoing changes — content updates, menu and page edits, plugin and
> security upkeep — so you are not left managing the site alone. Contact us to talk about what
> ongoing support should look like for your business.

Keep the commercial-term items (payment methods, currency, hosting, custom quote) — those are
terms, not guarantees. Replaced the guarantee FAQ with a support statement; FAQ count 9 → 8.

**Also caught in the same pass** (adjacent absolutes under the same copy discipline):

| Was | Now |
|---|---|
| "process **ensures** your campaigns are producing **at optimal levels, at all times**" | "process **is designed to keep** your campaigns **performing as well as they can**" |
| "you'll have **full confidence** in what's happening" | "you'll **know what is happening**" |
| Chip: "**Bug-free**" | Chip: "**Carefully tested**" |

**Lesson.** Encode the brief's prohibitions as machine checks so the artifact cannot drift:

```bash
--banned-claim 'guarantee=\bguarantee' \
--banned-claim 'day-count=\b\d+\s*days?' \
--banned-claim 'week-count=\b\d+\s*weeks?' \
--banned-claim 'absolute=at all times|optimal levels|full confidence'
```

Keep patterns tight. A loose `free` will fire on legitimate commercial copy ("royalty free
images") and train you to ignore the check.

**Lesson.** When the brief forbids a *class* of claim, sweep the whole artifact for that class
rather than fixing only the item someone flagged. The two items reported were not the only
violations of the same rule.

---

## 12. A reported defect that was a tool artefact, not a real defect

**Symptom.** A reviewer recorded the `tel:` href as a masked placeholder — `+180****0668` — and
asked that it be flagged so a Developer would substitute a real number.

**Cause.** The **display layer** was redacting digit runs that resemble a phone number. The file
on disk contained the full, dialable value the whole time. The same masking had affected this
session's own earlier reports.

**Verification.** Byte-level containment, not a readback:

```python
data = pathlib.Path(page).read_bytes()
assert b"8009830668" in data      # the real value is present
assert b"800****0668" not in data  # the masked form is absent
assert b"*" not in href            # no asterisk in any tel: href
```

**Lesson.** Before acting on a reported corruption, check the bytes. A masked readback is not
evidence of a masked file.

**Lesson (the important one).** Do not simply dismiss the report as a tooling artefact — the
reviewer's *concern* may still be valid even when the *evidence* is wrong. Here the real risk was
the inverse of what was reported: a complete-looking `tel:` value could be mistaken by a
Developer for a finished, dialable number when the underlying data was still unconfirmed. So the
correct response was to **redirect** the flag — keep it, and state the real hazard explicitly —
rather than close it as a false alarm.

Distinguish: *the evidence is wrong* (verify and say so) from *the finding is wrong* (check
whether the underlying risk is real under a different framing).

---

## 13. What the preflight cannot check

State these limits honestly in the final report:

- **Cross-browser rendering.** Chrome only. Safari and Firefox differ.
- **Real devices.** Emulated mobile viewport is not a phone.
- **Screen-reader behaviour.** ARIA structure can be validated; actual announcements
  need a real screen reader.
- **Performance scores.** Lighthouse, Core Web Vitals.
- **The production build.** The prototype is a design artifact; the build is the
  Developer's job.
- **Focus order and focus visibility in practice.** The `:focus-visible` rule can be
  confirmed present; keyboard traversal should be tested by hand.
