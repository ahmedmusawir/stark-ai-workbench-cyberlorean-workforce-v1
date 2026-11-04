# WEB DEVELOPER PLAYBOOK

> **Version:** 1.1 · **Date:** 2026-10-25 · **Status:** v1 POC — JARVIS review corrections applied
> **Adapted from:** `ENGINEER_PLAYBOOK.md` v1.3, `STARTER_KIT_HANDBOOK.md` v1.2 (design reference), `FRONTEND_BUILD_PHASE_PLAYBOOK.md` v1.3.0
> **Pairs with:** `WEB_DEVELOPER_INSTRUCTIONS_v1_0.md`, `../CONSTITUTION/WBM_PLAYBOOK_v1_0.md`

## 1. Minimum inputs

| Input | Source | If missing |
|---|---|---|
| Complete WBM with `QAM/` | Web Architect via Director | Stop; do not build from chat |
| Hub established by the foundation task (Payload running, site-scoping mechanism verified) | Foundation task record | If absent, this is not a website WBM yet; report and stop |
| Approved site checkout, branch named after the module | Director | Report; do not create branches |
| Env variable names for build-time and runtime inputs | Director / `.env.example` | Name the gap; build everything not dependent on it |
| Design HTML and tokens | `_design/` | Stop; a site built without the package drifts |
| Info pack content | `_infopack/` | Seed with labeled placeholder content; flag as `GAP` |

## 2. The intended Web Factory starter and the hub/site boundary

This is architectural intent, not an inventory of what is on disk. Shot one establishes the truth.

**Two applications.** The **hub application** is Payload: editor authentication, site-scoped collections, database adapter to Supabase Postgres, storage adapter to Supabase Storage. The **website application** is one public Next.js project per client, built from the adapted starter, connected to the hub. Establishing the hub and adapting the starter happen **once**, in a scoped **foundation task** with its own plan, approval and QAM. Website WBMs do not repeat SaaS removal or CMS installation; they add a site.

**Existing, per the App Factory Starter Kit Handbook (claims to verify):** Next.js App Router, TypeScript strict, Tailwind with semantic tokens, Shadcn primitives, `Page` / `Row` / `Box` / `Container` content-flow layout, `PublicNav` and `PublicMobileNav`, `ThemeToggle`, Jest + React Testing Library, `page.tsx` thin wrapper plus co-located `<Feature>PageContent.tsx`, Zustand for client state, Supabase client utilities, and a full SaaS auth/role layer (login, signup, `AppRole`, `profiles` / `user_roles`, admin and superadmin portals).

**Proposed Web Factory adaptations (foundation task, once):**
- Remove the SaaS portal flows from the **dedicated kit checkout**: admin, superadmin, member routes and sidebars, `useAuthStore`, role guards. Dropping the `profiles` / `user_roles` tables or the `handle_new_user()` trigger in any **shared** Supabase database requires an ownership and dependency check and explicit Director authorization; it is not implied by code removal.
- Retain layout, theming, tokens, public navigation, Shadcn inventory, test setup and the page composition pattern.
- Establish the Payload hub application with editor access limited to authenticated, authorized Cyberize staff. Anonymous users cannot perform editing or administrative operations. A reachable login page is not exposed access; no VPN or gateway is mandated for the POC.
- Connect Payload to Supabase Postgres through its database adapter and to Supabase Storage through an S3-compatible storage adapter. Specify the required behavior; verify the exact adapter packages and versions against the installed Payload.
- Model content as site-scoped collections, including **site-scoped settings and navigation as one document per site** (a plain Payload global is one document for the whole hub). Use the selected multi-tenant mechanism's verified equivalent.

**Requiring inspection or testing later:** the installed Payload version and its multi-site mechanism; adapter package names; whether server-side upload limits apply on the chosen host; the publish mechanism's real latency; whether the website builds with or without live hub access; `agent_docs/**` exclusion from the build and image.

## 3. Workflow — the two engineering shots

### Shot 1 — recon and plan

1. Read the WBM in its declared order. Read the handbook as aspirational.
2. Inspect read-only: branch, full HEAD, dirty files, Node version, the package manager actually in use (lockfile), the real scripts in `package.json`, dependencies, hub reachability and its collections, Tailwind version, existing routes and components, test baseline using the checkout's own test script in non-watch mode, env variable names present. Do not name a command you have not seen in the checkout.
3. Kit audit: what the kit provides, what this site consumes, what must be built. Flag any content-model addition this site needs as a hub change.
4. Decide and justify the publish mechanism. Default lean: on-demand revalidation triggered by a Payload `afterChange` hook, with full rebuild as the fallback. Record the expected latency window; QA tests against it.
5. Decide whether the site builds against the live hub or from a published export; document build-time inputs separately from runtime inputs.
6. Return one plan: affected paths, content records and any hub additions, template mapping from `SECTION_MANIFEST.md`, content load approach, exact self-check commands with working directories, aggregated blockers, the factual handoff you will produce.

Stop there. The Architect reviews; the Director releases.

### Shot 2 — implementation and handoff

Execute in this order, continuously, with no approval stops between steps unless a declared hard stop fires:

1. **Hub additions, if any.** Only the collection or block additions the plan flagged, identified as a hub change with their own deploy implication recorded. No SaaS removal, no CMS installation — those belong to the foundation task.
2. **Site records.** Create this site's documents on the hub per `CONTENT_MODEL.md`: the site record, its one navigation document and one settings document, pages whose blocks match `SECTION_MANIFEST.md`. Site ownership on every record, enforced by Payload access control, not only by queries.
3. **Media.** This site's uploads go to Supabase Storage under the site's prefix with generated sizes per the design spec's image rules. Rows hold metadata and URLs only. The prefix organizes; the storage access policy authorizes.
4. **Templates.** One route per page type. Implement the approved appearance, content structure and behavior from the design HTML as valid React and Next.js components; verify against the PNGs. Each block in the design maps to one section component reading one Payload block.
5. **Content load.** Seed pages, navigation, settings and top-level media from the info pack. Mark every seeded text block with its brief disposition: keep / rewrite / new. Placeholder where content is pending, labeled.
6. **Publish loop.** Implement the chosen mechanism. Test it: edit → publish → observe the site, record the time.
7. **Forms and integrations.** Real endpoints only; no fake success. Tracking tags and embeds as the brief lists them.
8. **Self-check.** Typecheck, then the checkout's test script in non-watch mode, then a clean build using the documented, approved build-time configuration. Record required variable names and service prerequisites (hub URL, read token). Supply secrets only through the approved environment or secret mechanism; never commit, echo, bundle into browser code or bake into an image layer. If the site builds without live hub access, test that mode too. Navigation walk through every intended public page. Mobile and desktop at the design spec's breakpoints. Each editable region renders, including empty state; drafts do not appear publicly. Image replacement renders at the declared proportion. Anonymous requests cannot perform editor operations. Every real form submits and errors honestly.
9. **Handoff.** Fill `QAM/QAM_MANIFEST.md` and `QAM/HANDOFFS/ENGINEERING_HANDOFF.md`: HEAD, changed paths, exact commands with working directories, ports or URLs, required services and success checks; build-time vs runtime variable names; per-AC claims with evidence; known limitations; publish mechanism and its window; owned processes and temp paths. Suggested commit message and exact paths for the Director. Candidate is "pending Director commit" until it exists.

## 4. Deliverables

- Site code on the module branch, uncommitted, with a changed-path inventory
- This site's hub records; any approved hub collection or block additions, identified as a hub change
- Seeded content and media references
- Documented and tested publish mechanism
- Self-check record with commands and results
- `QAM_MANIFEST.md` and `ENGINEERING_HANDOFF.md`
- Short `playbook/RETROSPECTIVES/RUN_NNN.md` draft, honest

## 5. Definition of done (engineering complete, not certified)

- Every AC in `ACCEPTANCE_SPEC.md` has an engineering claim with evidence or an honest "not implemented / unverified" entry.
- Verification triad green: typecheck, the checkout's tests, clean build with the documented build-time configuration.
- The CMS edit loop and image loop were exercised by you and recorded.
- Binaries are in Storage; CMS rows carry references.
- Site ownership is enforced by a named mechanism: Payload access control and storage access policy. Anonymous editor operations are denied; drafts are excluded from public pages.
- No credential value appears in committed files, deliverables, logs, images or client bundles. Approved ignored local configuration is permitted.
- The factual handoff exists. You have not written a QA result, plan approval or certificate.

## 6. Handoff contents

To the Director: changed-path list, suggested commit message, any hub change flagged for its own deploy, note that the candidate SHA does not exist until committed. To QA (through `QAM/`): the manifest and engineering handoff, exact reproduction commands with working directories and ports, build-time and runtime variable names, required services, the publish window, limitations.

## 7. Rules carried from the Engineer Playbook

- Consume kit primitives directly; do not wrap what the kit provides.
- Regression first: solving one AC must not break a passing one.
- Never comment out a test to go green. Never add hidden retries.
- Surface assumptions before acting; stop on genuine confusion rather than guessing.
- Record the session in the repo's existing session convention; write QA records only inside `QAM/`.
- `agent_docs/**` stays out of the build and the image; verify, do not assume.

## 8. Common mistakes

| Mistake | Fix |
|---|---|
| Installing Payload or removing SaaS code inside a website WBM | Foundation task does that once; a website WBM adds a site |
| Per-site settings as a Payload global | Site-scoped collection, one document per site |
| Site filter only in the page query | Enforce in Payload access control and storage access policy; a prefix is not a rule |
| Storing image bytes in Postgres | Storage adapter; rows hold references |
| "Publish works" with no mechanism named | Name it, test it, record the window |
| Naming `npm test` before reading `package.json` | Inspect the package manager and scripts first |
| Promising a secret-free cold build | Use the documented build-time configuration; record what it needs |
| Trusting the handbook's component list | Grep the checkout |
| Fake form success | Real endpoint or an honest `BLOCKED` in the handoff |

## 9. Illustrative example — a one-page consultant site

*Illustrative only.*

Shot one finds: the hub is running with `sites`, `pages`, `media`, site-scoped `navigation` and `site-settings` collections and the multi-tenant mechanism verified by the foundation task; the website checkout uses pnpm (lockfile present), scripts `dev`, `build`, `test` (Jest, non-watch via `pnpm test -- --ci`), `typecheck`; Tailwind 3.4; Shadcn present; no SaaS portal code remains. Plan: create the `consultant` site record and its navigation and settings documents; pages mapped to existing blocks hero, list, text-image, testimonial, contact; no hub schema change needed; build reads published content from the hub at build time, so `HUB_API_URL` and `HUB_SITE_TOKEN` are build-time inputs; publish by on-demand revalidation from the hub's `afterChange` hook, fallback full rebuild; blocker: form endpoint not yet supplied (variable `FORM_ENDPOINT` named). Director releases.

Shot two: site record and documents created; access control confirmed to scope the consultant editor identity. Media uploads land under `consultant/` with hero and portrait sizes generated; rows hold URLs. Home template implemented as five section components matching `home.html`, verified against the PNGs. Seed loads six text blocks (four keep, two rewrite) and three images. Publish loop tested: headline edit visible in 4 seconds. Typecheck, `pnpm test -- --ci`, and `pnpm build` with the documented build-time variables green; working directories recorded. Navigation walk clean. Mobile and desktop verified. Anonymous request to an editor operation denied; a draft page does not appear publicly. Form endpoint arrived mid-run; form submits to it. Handoff filled with exact commands, ports and variable names. Candidate pending Director commit.

## 10. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-24 | First Web Developer playbook; Engineer doctrine adapted for Payload + Supabase websites; SaaS removal and intended-kit section added; two-shot engineering per WBM |
| 1.1 | 2026-10-25 | JARVIS review: hub application vs website application and one-time foundation task; site-scoped settings collections; shared-database drop guard; runnable build environment replaces secret-free cold build; access boundary and storage-prefix wording; checkout-first commands; secrets language scoped; example rewritten |
