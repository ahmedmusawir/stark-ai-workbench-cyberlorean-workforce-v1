# Approved design freeze and engineering release

Reusable lessons from design-to-WBM reconciliation. These are procedures, not current project approval or model identity.

## 1. Recover authority and actual target

Read current rulings, scope, design handoff and exact final directory. Record whether approval covers a direction, complete design, local implementation, QA execution or publication; these are distinct decisions. If local implementation is explicitly authorized without another permission round, do not retain an obsolete plan-approval stop.

Inspect target checkout read-only: Git remote, branch, HEAD, status, package scripts, test configuration and actual source. A historical recon is context, not current state. Preserve unexpected changes. Do not clone, switch branches or commit under Architect assembly authority.

## 2. Reconcile real artifacts

Check each approved route against actual root HTML, section IDs, manifest, local content namespaces and asset references. Inspect CSS and interactive code as well as specification prose. Review screenshots and actual artwork; an overview is useful for composition, not proof of small-text accessibility.

Create one route/reference table with absolute prototype paths, screenshot pairs, tokens/styles, fonts/artwork, source dispositions and state references. Map flat prototype filenames to public routes explicitly. Cover mobile navigation, nested Escape/focus behavior, active state, FAQ disclosures, image fallback and 404 guidance. Do not import historical before/revisions files as current runtime assets.

Treat source-map shorthand critically: a list of capabilities plus campaign formats is not automatically one homogeneous component list. Normalize approved local content into typed semantic data while preserving copy, emphasis, section order and links; do not make the whole page an opaque editable HTML blob.

## 3. Freeze without changing approved design

1. Archive superseded WBM/site contracts and plans before editing.
2. Enumerate all regular files under the approved package in sorted relative-path order. Reject or explicitly handle symlinks rather than accidentally hashing outside the package.
3. Write an external JSON manifest containing package root, approval reference, version/timestamp, relative path, byte size and SHA-256 per file.
4. Hash that manifest and record its digest in the ruling and release instructions.
5. Provide a verifier comparing both exact file set and bytes: missing, changed and added files fail.
6. Do not silently regenerate a manifest after drift. Require an attributed successor decision/version.
7. Explain which inventoried files are historical or tools versus runtime dependencies. Existing Designer ZIP/checksum files are included evidence, not automatically the authoritative freeze.

Hash freezing is tamper detection, not an OS write lock. Do not claim stronger immutability than provided.

## 4. Define measurable visual acceptance

Record CSS width, device pixel ratio, actual PNG dimensions, browser and capture states. Verify canonical screenshot hashes/dimensions against the Designer manifest where supplied. Require matching implementation renders after font/image readiness and per-page section-level comparisons. Include expanded menus and FAQ states.

Judge typography/line breaks, section geometry, color blocks, artwork scale/proportion and shared shell. Record discrepancy dispositions; anti-alias differences may be explained, but automated pixel thresholds or passing functional checks do not establish visual success. Designer preflight, engineering self-check and independent QA remain distinct.

Developer image-view verification must use an actual tool opening a known screenshot plus concrete visual observations. File presence, advertised model name and another agent's vision capability are not verification. Report limitations honestly.

## 5. Handle confirmations and inherited state

Keep a confirmation register: exact issue, source, owner, local handling and publication closure condition. Phone/address, commercial terms and platform terminology must not become verified facts merely because design was approved. Explicit permission may allow local implementation with frozen safe copy and visible provisional notices. Excluded claims remain excluded. Research findings are proposals for content rulings, not permission to alter approved copy silently.

Inspect QAM results before refreshing templates. Never replace actual results with blank records; archive/scope successor records appropriately. Preserve starter-QA history and test outputs. Existing tests may overwrite tracked historical screenshots: inspect destinations and change new engineering tests/evidence lanes before running.

## 6. Assembly verification and relay

- Acceptance spec and GATES contain identical ACs (byte-identical copies are easy to verify).
- QAM matrix has one unexecuted row per current AC; no implied certification.
- Required root navigation and embedded QAM files actually exist.
- Freeze checker passes; canonical image references and local dependencies exist.
- Repository identity/status is recorded and Architect has not changed product code.
- Stale design/engineering holds are explicitly superseded by current authority, not deleted from history.
- Any handoff ZIP declares whether absolute-path design/source dependencies are external; do not call a thin WBM archive a self-contained full project.

Final response: concise readiness summary, exact checkout/branch, then complete fenced-code relay prompt with absolute paths. No extra implementation permission round when already authorized; publication remains separately controlled.
