# Vision inspection capability and rendered-screenshot review

Scope: how to *prove* a semantic image-inspection path exists before committing to a design
assignment, and how to read tall rendered screenshots through it.

## Why prove it first

A capability check that answers "yes, I can see images" with an actual observation is worth
more than a claim. Pixel sampling, OCR, filenames and prior notes establish that bytes exist —
they do not establish that an image was *read*. A grader or an operator asking "prove the
capability" wants the observation, the tool behind it, and the limits.

## Establish the route: native vs auxiliary

Hermes `vision_analyze` has two routes:

- **native fast path** — the image is attached to the active main model as a multimodal tool
  result and the model inspects the pixels itself.
- **auxiliary route** — a separate vision LLM (OpenRouter / Nous / Codex / native Anthropic /
  custom OpenAI-compatible endpoint) is called and returns a text description.

Evidence, in order of authority:

1. **The tool's own return message.** Native: *"Image loaded into your context — you can see it
   natively now."* Auxiliary: prose with no such line.
2. **The gateway log**, which states the decision explicitly:
   `/home/moose/.hermes/profiles/<profile>/logs/agent.log`
   `INFO tools.vision_tools: vision_analyze: native fast path`
   Also `INFO agent.auxiliary_client: Vision auto-detect: using main provider <provider> (<model>)`
   — when that line names the main provider, native inspection is what is actually happening.
3. **The source.** `tools/vision_tools.py` → `_should_use_native_vision_fast_path()` →
   `decide_image_input_mode(provider, model, cfg)` (in `agent/image_routing.py`) plus
   `_supports_media_in_tool_results(provider, model)`.

**Caveat that cost real time once:** running `decide_image_input_mode` in a *standalone*
interpreter outside the live session does **not** reproduce the live decision — it lacks the
session's runtime identity, so capability lookup can return unknown and fall through to text
mode. A standalone probe that says "text" while the live session took the native fast path is
not a contradiction to report; the live tool message and the gateway log are authoritative.
Do not present the standalone result as a finding.

Report the route and the model/provider actually doing the seeing. Never infer vision
capability from the session model name, and never from a historical session's notes.

## The resize ceiling, and the crop that fixes it

Native vision does not receive original pixels. Before the image reaches the model, Hermes
downscales to `max_dimension=1568` and a ~0.2 MB payload budget. The log records it:

```
INFO tools.vision_tools: Image file is 0.3 MB (estimated base64 0.3 MB, limit 0.2 MB, max_dimension=1568), auto-resizing...
INFO tools.vision_tools: Auto-resized image fits: 0.1 MB (quality=85, 1055x1065)
```

Consequence for full-page captures — measured, not estimated:

| Target | Native size | Size delivered to the model |
|---|---|---|
| mobile full-page | 780×9624 | 97×1203 |
| desktop full-page | 2880×9138 | 360×1142 |

Page rhythm, section order and colour survive. Small body type does not.

**Working pattern — band the page with the `region` crop parameter:**

```
vision_analyze(image_url=<png>, question=<focused>, region=[x1, y1, x2, y2])
```

Cropping `[0,0,780,1500]` of a mobile render restored native width for that band and made
headline wording and control stacking reliably readable. Practical rules:

- Do a **full-page pass** for composition and section order.
- Do **targeted `region` bands** for any consequential read — headline wording, button/control
  arrangement, small type, expanded interactive states.
- Crop coordinates are in the **original image's pixel space**. The tool reports a downscale
  factor (e.g. "multiply any x coordinates you report by 8.04"); use it to map back.
- A cropped read loses page-level context, so the banded read supplements the full-page pass
  rather than replacing it.

## Capability-check-only assignments

Some assignments are explicitly a **capability check**: prove the inspection path works,
report the tool and its limits, and stop. Treat that as a bounded read-only task with its
own acceptance criteria, not as the first step of the design work.

- **Verify file access before inspecting.** Enumerate the named inputs and prove each one
  opens: a readability loop over the exact paths (`test -r "$f"` plus size) is stronger
  evidence than a directory listing, because a listing says a name exists while the loop
  says the bytes are readable. Report paths, line/byte counts and the specific named files
  that opened.
- **Produce no output files.** A capability check must leave the inputs tree untouched
  (`find <inputs> -newermt '-1 hour'` should return nothing) and the workspace unchanged.
  Say so explicitly in the report — "no design work started, no files written" is part of
  the deliverable.
- **Ask the image a second, more specific question to prove the read is real.** After an
  open-ended description, re-inspect with pointed questions — exact button label, which
  word carries the accent colour, is the texture solid or a transparency checkerboard, is
  there a stock watermark and where. A second pass that returns precise, correct strings
  distinguishes genuine semantic reading from impressionistic description.
- **Name the stock/watermark condition in the report.** If the reference carries a stock
  mark, say the artifact is reference-only and cannot be reused in a deliverable.
- **Report the three details the assignment asked for, concretely** — composition and
  placement, typography and headline treatment, one distinctive visual element — rather
  than a general description of the image.
- **Stop at the gate.** Do not begin the design assignment, and do not write a plan for it.

## Two log lines that are easy to misread

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

## Reading a rendered screenshot through this path

Verified on a real desktop/mobile pair produced from the same build:

| Target | Native size | Delivered size | What was readable |
|---|---|---|---|
| `home-desktop.png` (full) | 2880×9138 | 360×1142 | first section below the header; headline colour treatment |
| `home-mobile.png` (full) | 780×9624 | 97×1203 | layout and rhythm only; body type too small |
| `home-mobile.png` (region 0,0,780,1500) | — | native width | headline text; buttons stacked vs side-by-side |

A second live session confirmed the same ceiling on taller captures and showed the
`region` crop recovering native width even when the full-page pass had collapsed to
360×1473:

| Target | Native size | Delivered size | What was readable |
|---|---|---|---|
| `ppc-desktop.png` (full) | 2880×11786 | 360×1473 | section order and colour bands only |
| `ppc-desktop.png` (region 0,0,1440,220) | — | native width | logo lockup text, nav labels, top-right CTA label |
| `home-mobile.png` (full) | 780×10970 | 97×1371 | structure and rhythm only |
| `home-mobile.png` (region 0,0,780,1400) | — | native width | exact headline wording, eyebrow, CTA label, first graphic |

Two practical consequences worth carrying forward:

- A full-page read at 97px wide still reliably recovers **structure**: the section list,
  the accent colour, whether the CTA is a pill or a rectangle, and the shape of the hero.
  Use it for composition questions and pair it with a cropped read for wording.
- The crop's `region` box is in original-image pixels, and the tool scales it down
  internally. Cropping `[0,0,1440,220]` of a 2880-wide render reads the **left half** at
  full desktop resolution — that is how the nav labels came out crisp rather than as
  smudged text.

Inspect the desktop and mobile renders **from the same build together**. The pair is what
supports a responsive judgement; either alone can mislead. The same path handles a PNG
produced by a headless-Chrome CDP capture with no extra tooling, install or configuration.

## What only semantic inspection resolves

Two things this session's reference image showed that pixel analysis could not have settled:

- A **checkerboard block** read as solid greyscale squares, not a transparency indicator.
  Colour histograms confirm the greys but not the *intent*; only looking settles it, and the
  answer changes whether the texture may be reused.
- A **stock watermark** ("dreamstime") was legible across the middle-right of the poster.
  Filenames, dimensions and pixel statistics never surface it.

Practical rule: run the semantic pass on **every** supplied reference before deciding
anything about its usability, and ask explicitly about watermarks, stock marks, placeholder
copy and embedded logos.

## Provenance consequence

A watermarked stock mockup is **reference-only**. It may inform composition and technique, but
its artwork, logo slot, copy and marks cannot be reused in a client deliverable, and its
presence in an inputs tree does not license it. State this plainly when reporting, and check
the remaining supplied images for the same condition before any imagery direction is built on
them.

## Reporting shape

Keep the requested shape exactly, and keep technical facts separate from subjective visual
judgement:

- READY or BLOCKED
- **file-access result** — path, read-only status, the specific named files that opened, and
  hash evidence where identity matters (a supplied logo verified byte-identical to the
  authoritative copy by sha1 is strong, cheap evidence)
- **the observed details** — concretely, from the image itself
- **inspection tool, route (native vs auxiliary), model/provider doing the seeing, and
  limitations**
- **whether the same path handles rendered desktop/mobile captures**

Stop at the requested gate. A capability check is not permission to begin the downstream
assignment, and no output files should be produced during one.

## Command-payload limits in this harness

Long inline shell payloads that mix pipes, `$()` and several greps can hit a command-parser /
hardline block *before* they run — the block fires on payload shape, not on the operation
itself. Working alternative: split the work. Use `search_files` with `output_mode="count"` for
occurrence counts, or one `grep -c` per pattern in its own terminal call. A filesystem-wide
`find` can also exceed the foreground timeout and return nothing useful — target the
directories you actually need.
