# WEB DESIGNER PLAYBOOK

> **Version:** 1.1 · **Date:** 2026-10-25 · **Status:** v1 POC — JARVIS review corrections applied
> **Adapted from:** `DESIGNER_PLAYBOOK.md` v2.2, `STARK_WEB_FACTORY_WEB_DESIGN_ARCHETYPE_KITS_VISION_v0.1.md` (inspiration, not requirement)
> **Pairs with:** `WEB_DESIGNER_INSTRUCTIONS_v1_0.md`, `../CONSTITUTION/WBM_PLAYBOOK_v1_0.md`

## 1. Minimum inputs

| Input | Source | If missing |
|---|---|---|
| Approved `SITE_BRIEF.md` | Web Architect | Stop. Design without scope produces rework. |
| Screenshots of the current site | Info pack | Design greenfield; note that no visual baseline existed |
| Extracted tokens (fonts, colors, spacing, logo) | Info pack | Start from the kit defaults; mark the palette as `ASSUMPTION` |
| Logo (SVG preferred) | Client / Director | Typographic placeholder, `TODO (Director)` |
| Primary archetype or references | Director | Default to a restrained, systemic direction; name it as an assumption |
| Target Tailwind version | Developer / kit handbook | Assume the kit's documented version; the Developer corrects at recon |

## 2. Workflow

**Step 1 — Pre-flight.** Confirm the brief is approved. List the page types from the page map. Pick the canonical page: the homepage, always, for a marketing site. Identify the token set to inherit or replace.

**Step 2 — Tokens first.** Write `globals.css` with semantic tokens: brand primary and accent, surface and foreground, border, radius, type scale, spacing scale, container widths, section spacing, and a small motion token set (duration, easing). Light mode only unless the brief asks otherwise. Map to Tailwind utilities. If a screen later needs a color outside the set, the set is wrong — fix the token, not the screen.

**Step 3 — Style tile.** One HTML page showing typography ramp, buttons and states, form fields, cards, links, image treatment, and the color system. Render to PNG. This is the live contrast proof.

**Step 4 — Canonical homepage.** Token-driven HTML. Every section is a named block the Developer can map to Payload. Mobile layout first (390-ish), then desktop. Render both. Review. Tune tokens. Present for the Director's lock. Do not clone before lock.

**Step 5 — Clone-and-adapt the templates.** From the locked homepage HTML, produce each additional page type the brief names: service page, generic content page, contact, and post index / post only if the blog is in scope. Keep the shell, grid, spacing and type scale; change the content region. Design page types, not URLs.

**Step 6 — Write `SITE_DESIGN_SPEC.md`.** Per page type: purpose, sections in order, which sections are editable and which are layout-owned, navigation behavior (header, mobile menu, footer), responsive rules at mobile / tablet / desktop, typography usage, imagery rules, basic accessibility (contrast, focus, heading order, alt text), motion profile (none / subtle / micro), and states that matter for a website: form idle / submitting / success / error, empty post list, missing image, 404.

**Step 7 — Write `SECTION_MANIFEST.md`.** One row per section used on the site: name, which page types use it, editable fields (text, image, link, list), image slots with proportion and crop rule, intended Payload block name. This is the bridge between design and content model; the Architect reconciles it with `CONTENT_MODEL.md`.

**Step 8 — Package and hand off.** Verify every HTML file consumes tokens only. Verify every page type in the brief has a template. Deliver to the Architect.

## 3. Deliverables

```text
_design/
├── tokens/globals.css          PRIMARY — the executable visual contract
├── tokens/tailwind.tokens.md   utility map and naming notes
├── style-tile/style-tile.html + .png
├── pages/home.html + home-desktop.png + home-mobile.png      (canonical, locked)
├── pages/service.html + pngs                                 (if in page map)
├── pages/content.html + pngs                                 (generic page)
├── pages/contact.html + pngs
├── pages/post-index.html, post.html + pngs                   (blog only)
├── SITE_DESIGN_SPEC.md
├── SECTION_MANIFEST.md
├── logo-color.svg · logo-mono.svg · favicon.svg
└── reference/                  source screenshots, Director references
```

## 4. Definition of done

- Tokens are concrete values, complete for every utility the templates use, and zero hardcoded colors exist in any HTML.
- The canonical homepage was locked by the Director before templates were cloned.
- Every page type in the brief has a template with desktop and mobile renders, or a stated reason none was rendered.
- Every image slot has proportion, crop behavior, alt-text requirement and missing-image behavior written down.
- Every editable section appears in `SECTION_MANIFEST.md` with its fields.
- Basic accessibility is addressed: contrast passes on the style tile, heading order is sensible, focus states exist.
- Motion is restrained and has a reduced-motion fallback noted.

## 5. Handoff contents

To the Web Architect: the full `_design/` folder, a two-line summary of design decisions that depart from the info pack's current look, and the list of Kit Improvement Proposals, if any. The Architect assembles this into the WBM; the Developer implements the approved appearance, content structure and behavior as valid React and Next.js components and verifies against the PNGs. "Build from the HTML" means preserve what was approved, not copy markup literally.

## 6. Rendering and tools

Use the rendering tool permitted by the active project and runtime instructions to produce PNGs at 2x scale. Headless Chrome is a suitable option. Record the tool used in `SITE_DESIGN_SPEC.md`; never fabricate a screenshot. If nothing is available, deliver HTML and say so. HTML is the build reference; PNG is the QC target. Never deliver a PNG without its HTML. Note: the inherited Designer, FFM and Testing playbooks name Playwright while the Workbench phase map restricts it; that conflict is recorded in this pack's README and is resolved by the active project instruction, not by this playbook.

## 7. Common mistakes

| Mistake | Fix |
|---|---|
| Designing every URL individually | Page types; a 40-URL site is usually four templates |
| Hardcoding a hex in a section | Add or fix a token |
| Cloning before lock | The Director locks the canonical homepage first, always |
| Dark mode by habit | Not required for marketing sites; only if the brief says so |
| Hero depends on a photo the client does not have | Design the missing-image state; propose an asset strategy |
| Section with no editable field map | Every section row in the manifest names its fields |
| "Make it pop" motion | Subtle or none; note reduced-motion fallback |

## 8. Illustrative example — a landscaping company

*Illustrative only.*

Brief: homeowners, mobile-heavy, CTA "Get a free estimate." Page types: home, service (five services, one template), about, contact. Blog out of scope. Archetype: organic warm, per Director.

Tokens: warm neutral surfaces, deep green primary, terracotta accent, rounded radius, generous section spacing, serif display with humanist sans body, motion subtle. Style tile rendered; contrast verified on primary buttons.

Canonical homepage sections: hero (headline, subhead, CTA, image 3:2, missing-image → green panel), services grid (five cards: icon, title, blurb, link), process strip (three steps), before/after gallery (pairs, 4:3, editor-managed), testimonial (optional, hidden when empty), estimate CTA band, footer. Mobile first, then desktop. Director locks.

Templates cloned: service (hero variant, text-image blocks, gallery, CTA band), content (prose, optional image), contact (form idle / submitting / success / error states, map embed slot). `SECTION_MANIFEST.md` lists eight sections with fields and image rules; `SITE_DESIGN_SPEC.md` records nav collapse under 1024, heading order, focus rings, reduced-motion fallback.

The before/after gallery is a site-specific section composed from kit primitives, so it needs no KIP. One KIP is raised: an interactive slider primitive the reusable kit lacks; the Architect decides whether it ships in v1 or the gallery uses static pairs.

## 9. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | First Web Designer playbook; Canonical Page Method and token-first discipline carried from Designer v2.2; archetype kits treated as inspiration; dark mode and six-kit prerequisite removed |
| 1.1 | 2026-10-25 | JARVIS review: KIP reserved for reusable-kit changes; "build from HTML" clarified; rendering tool follows active project instruction, Playwright conflict recorded rather than asserted |
