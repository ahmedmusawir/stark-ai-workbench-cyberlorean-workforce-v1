# Acceptance-chain case notes — FAIL verdict, repair commit, missing retest

Worked example from a real session (2026-11-03, Cyberize POC site, Cloud Run prep). Names are as found in records; the pattern is the lesson.

## Situation

Intake found the deploy branch HEAD at `efe7e96` ("Web Factory Static POC Site Complete"), one commit ahead of `822716c` ("Implement Cyberize seven-page local website"). No skill instructions said anything about acceptance — the gap surfaced only by reading the project's QA records.

## The chain as reconstructed from records

1. **Reconciled Q2 certification** (`WBM/QAM/QAM_CERTIFICATION.md`, v2.1-Q2R): verdict **FAIL** for candidate `822716c` — AC-11 failed: all seven route meta descriptions mismatched the frozen approved HTML. Eleven other ACs PASS.
2. **Repair ruling R-016** (`WBM/WBM_RULINGS.md`): Tony authorized restoring the seven descriptions to the frozen HTML values. Bounded repair: seven route-local description literals only, titles unchanged. The ruling explicitly says the FAIL stands until independent retest.
3. **Architect repair work order** (`handoffs/ARCHITECT_TO_DEVELOPER_AC11_METADATA_REPAIR.md`) with exact before/after strings per route and a required retest protocol after the Director commits.
4. **Developer repair handoff**: edits made, build/typecheck/lint exit 0, but rendered verification BLOCKED by a tool-policy denial. Honest handoff states the repair is NOT complete.
5. **Director commit**: `efe7e96` contains exactly the seven description literals — verified by `git diff 822716c efe7e96` (7 files, 7 insertions, 7 deletions, all in the `metadata` export line).
6. **Missing link**: no targeted AC-11 retest on `efe7e96` anywhere in the project tree (`find -newermt` after the commit date; `grep` for the new SHA in project records → nothing). No explicit Director POC acceptance exception either.

## What the DevOps disposition was

- Recorded `acceptance.kind` as **blank** with the full evidence trail in the intake YAML; `qa_record` documents the FAIL + repair + missing-retest state.
- Reported the GAP in the final reply as a release input: either the QA Lead records the targeted retest on `efe7e96`, or Tony explicitly records a POC exception naming that SHA.
- Did NOT run any QA, relabel the candidate, or treat the repair commit as acceptance. The deploy script was generated to fail closed on blank `acceptance.kind`.

## Detection techniques that worked

- `git log --format='%h %ad %s' --date=iso` — the commit message "Web Factory Static POC Site Complete" hints at a completion but says nothing about acceptance.
- `git diff <certified-SHA> <HEAD>` — proving the delta is exactly the authorized repair scope (seven literals) rules out unrelated drift, but does NOT substitute for the retest: it proves what changed, not that the changed state passes.
- Sidecar hash verification: `artifacts/<name>.zip.sha256` vs `sha256sum` of the ZIP before trusting its contents. The ZIP's internal `verification.json` showed `"verdict": "FAIL"` with `failedACs: [AC-11]` — a PRE-repair snapshot. Archives describe the moment of archiving, not the current state.
- Freshness sweep: `find <project> -newermt '<commit date>'` to find any record written after the repair commit that could contain a retest. Empty result = the retest does not exist.

## Anti-patterns avoided

- "The Director committed it, so it's accepted" — a commit records that a repair was applied, not that it was verified. The repair ruling itself demanded a successor retest.
- "The diff is tiny and clearly correct, so I can vouch for AC-11" — verifying scope is DevOps work; verifying the AC is QA work. The seat boundary is the point.
- "The old certificate said PASS WITH KNOWN RISK" — that certificate was explicitly superseded by the reconciled FAIL. Always read the LATEST verdict document, and check for a "supersedes" relationship.

## Transferable rule

The deployable identity chain is: **certified/excepted SHA == the SHA you package**, or an evidenced repair path between them ending in a retest or explicit exception. Any broken link is reported, never repaired, by the deploying agent.