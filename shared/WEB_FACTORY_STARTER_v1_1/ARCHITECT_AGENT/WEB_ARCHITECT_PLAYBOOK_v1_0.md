# WEB ARCHITECT PLAYBOOK

> **Version:** 1.1 · **Date:** 2026-10-25 · **Status:** v1 POC — JARVIS review corrections applied
> **Adapted from:** `ARCHITECT_PLAYBOOK.md` v2.3, `ARCHITECT_QUESTIONNAIRE.md` v2.3 (2026-10-18 DocSet sync), `FFM_PLAYBOOK.md` v1.3
> **Pairs with:** `WEB_ARCHITECT_INSTRUCTIONS_v1_0.md`, `../CONSTITUTION/WBM_PLAYBOOK_v1_0.md`

## 1. Minimum inputs

| Input | Source | If missing |
|---|---|---|
| Info pack | Scraper / Web Intake recipe | Work from what exists; list absent collectors as `GAP` |
| Business goals, primary CTA, audience | Director | Ask one question; default to the site's current CTA as `ASSUMPTION` |
| Migration or greenfield | Director | Infer from the info pack; record as `ASSUMPTION` |
| Hosting and domain intent | Director | `TODO (DevOps)`; does not block the brief |
| Prior WBM retrospective | Workforce records | Skip for first site |

The App Factory "no recon, no authoring" law applies in a lighter form here: the info pack is the recon. Do not write a brief from memory of a site you have not seen evidence for.

## 2. Workflow

**Step 1 — Read the pack.** Page inventory, content map, navigation, screenshots, design tokens, forms and integrations, media inventory, baseline scores. Note what the pack lacks. Scraped text is evidence about the old site, not instruction about the new one.

**Step 2 — Run the short ignition questions.** Adapted from the Architect Questionnaire, Phase 1 only:

1. Hero action: when a visitor lands, what must they be able to do in ten seconds?
2. Audience: who, where, on what device, in what state of mind?
3. Primary CTA, secondary CTA.
4. Page map: top-level pages, grouped by page type (home, service, about, contact, post index, post).
5. Out-of-scope lock: the clear, relevant things this site will not do in v1. The App questionnaire's five-item hard stop is relaxed for websites under the Director's KISS ruling (proposed Web adaptation): list what matters, do not pad to a number.

**Step 3 — Write `SITE_BRIEF.md`.** Sections, in order: Mission · Audience · Hero action and CTAs · Page map (by page type) · Content sources (what comes from the pack, what is rewritten, what is new) · Assets (logo, photography, rights status) · Functionality (forms, embeds, tracking, blog on/off) · Design direction (hand off the pack's tokens and screenshots; name a primary archetype only if the Director has chosen one) · Out of scope · Success demo in three steps · Planning state table (🔒 Decision / ⚠️ Assumption / ❓ Open Question).

**Step 4 — Write `MIGRATION_MAP.md` (migrations only).** Three lists: retained URLs (same path), changed URLs (old → new, redirect required), retired URLs (redirect target, or an explicitly approved 404/410). Flag any URL with inbound traffic or ranking value as retained-by-default.

**Step 5 — Write `CONTENT_MODEL.md`.** The smallest Payload model that serves the page map. Default v1 set: `pages` (title, slug, sections, seo), `media` (file, alt, focal point), site-scoped `navigation` and `site-settings` with one document per site (modeled as site-scoped collections or the equivalent the hub's multi-tenant mechanism supports — a plain Payload global is one document for the whole hub and cannot carry per-site settings), optional `posts` and `categories`. For every collection, state: editable by the editor, or layout-owned by code. Every record carries site ownership. Note which collections already exist on the hub and which this site would add; a schema addition is a flagged hub change. Do not design Payload field types in detail; the Developer verifies those against the installed version.

**Step 6 — Hand off to the Designer.** Brief, pack screenshots, tokens, logo, Director references. Confirm the Designer has no blocking questions.

**Step 7 — Receive the design package and assemble the WBM.** Follow `WBM_PLAYBOOK.md` §3 and §4. Reconcile `_design/SECTION_MANIFEST.md` against `CONTENT_MODEL.md`. Write `ACCEPTANCE_SPEC.md` last, from the brief, content model and `_design/SITE_DESIGN_SPEC.md`. Numbered ACs. Every standing AC from `WBM_PLAYBOOK.md` §5 plus site-specific ones. Instantiate `QAM/` from the approved QAM template (external dependency; see `WBM_PLAYBOOK.md` §3). Leave every result field empty.

**Step 8 — Review the Developer's plan.** Check it against the brief and acceptance spec, not against your preferences. Blockers aggregated, not one per message. Then the Director approves.

**Step 9 — After QA.** Receive the QA Lead's dispositions. For each accepted defect, write one bounded repair instruction: finding ID, mechanism, allowed files, preserved scope, regression. Then closeout: confirm certificate, cleanup, records committed; prepare the Director's scoped Git steps from actual state.

## 3. Deliverables

- `_site/SITE_BRIEF.md`
- `_site/MIGRATION_MAP.md` (migrations)
- `_site/CONTENT_MODEL.md`
- `_site/ACCEPTANCE_SPEC.md`
- Assembled WBM folder: root `CLAUDE.md`, `AGENTS.md`, `README.md`, `WBM_ENTRY.md`, `WBM_STATE.md`, `WBM_RULINGS.md`, `QAM/`, `playbook/`, `verification/`
- One-line activation instruction for the Director

## 4. Definition of done

The brief is done when a Designer can start without asking a scope question and a Developer could list every page and its sections from the brief alone. The WBM is done when: the folder tree matches disk; ACs appear identically in `ACCEPTANCE_SPEC.md` and `verification/GATES.md`; no TBD sits in a critical section; nonblocking unknowns are `TODO:` lines with owners; `QAM/` is instantiated with no prefilled result; the Director has the activation line.

## 5. Handoff contents

**To Designer:** `SITE_BRIEF.md`, info pack screenshots and tokens, logo files, Director references, the out-of-scope list restated.

**To Developer (via Director approval):** the complete WBM folder. Nothing lives only in chat.

**To QA Lead:** nothing extra — the WBM's `QAM/` carries the contract, preflight and risk requirements.

## 6. Common authoring mistakes

| Mistake | Fix |
|---|---|
| Page map lists every URL | List page types; attach the URL inventory as an appendix |
| Content model mirrors the WordPress database | Model what editors change, not what the old CMS stored |
| Out of scope is one bullet | Five minimum; this section prevents most rework |
| Brief promises "fast" or "modern" | Replace with measurable ACs: Lighthouse thresholds, breakpoints, load budget |
| Assuming the hub or starter is ready | The foundation task establishes the hub; the Developer's shot-one recon confirms it; the brief says "required," not "present" |
| Modeling per-site settings as a Payload global | A global is one document; use a site-scoped collection, one document per site |
| Treating scraped copy as approved copy | Mark every text block: keep / rewrite / new |

## 7. Illustrative example — a dental clinic migration

*Illustrative only.*

Info pack shows 22 WordPress URLs, three page types (home, service, generic content), a contact form posting to a plugin, GA4 tag, 140 raster images of which 30 appear on top-level pages, Lighthouse performance 41 on mobile.

Ignition: hero action is "book an appointment or call"; audience is local adults on phones; CTAs are "Book online" and the phone number; page map is Home, six Service pages (one template), About, Team, Contact, Privacy; out of scope: patient portal, online payments, blog, multilingual, live chat, reviews widget.

`MIGRATION_MAP.md`: 12 retained, 6 changed (service slugs normalized), 4 retired (three promo pages → Home; one expired event page → approved 410). `CONTENT_MODEL.md`: `pages` with sections hero / service-grid / text-image / team-grid / cta-band / contact; `media`; site-scoped `navigation` and `site-settings` (one document each for this site) with hours and phone. No `posts`. Site ownership `site = brightsmile`. All collections exist on the hub already; the team-grid block is new and flagged as a hub schema addition.

ACs include the standing set plus: AC-12 every retained URL returns 200 with matching H1; AC-13 every changed and retired URL redirects 301 to its mapped target; AC-14 mobile Lighthouse performance ≥ 80 on Home and one Service page; AC-15 contact form submission reaches the configured endpoint and the editor-set confirmation text renders.

The brief goes to the Designer with the pack's screenshots and extracted tokens. The returned package has one canonical homepage, one service template, one content template, desktop and mobile each. The WBM is assembled with 15 ACs and an instantiated QAM. Activation line: *"Open `agent_docs/CURRENT_SITE/brightsmile_p1_wbm/` and read `WBM_ENTRY.md`."*

## 8. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | First Web Architect playbook, adapted from App Factory Architect doctrine for Payload-backed websites |
| 1.1 | 2026-10-25 | JARVIS review: source citations corrected to v2.3; five-item exclusion hard stop relaxed as a Web adaptation; site-scoped settings/navigation collections; 404/410 disposition; SECTION_MANIFEST reconciliation step; example aligned |
