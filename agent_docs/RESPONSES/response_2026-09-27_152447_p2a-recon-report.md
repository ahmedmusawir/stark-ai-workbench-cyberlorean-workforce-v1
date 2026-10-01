# P2-A Recon Report — Cyberlorean Workforce

**Inspected:** 2026-09-27, 14:00–14:10 +06:00 (Asia/Dhaka)
**Saved:** 2026-09-27 15:24:47 +06:00 (Asia/Dhaka)
**Method:** read-only filesystem + git inspection. No services started, no agents run, no files written outside the session scratchpad, no git mutations, no secret values printed.
**Evidence standard:** every claim below is disk-verified unless explicitly marked *unverified* or *inferred*.

---

## A. Workforce repo — **empty shell, confirmed**

| Fact | Value |
|---|---|
| Path | `/home/moose/python/stark-ai-workbench-cyberlorean-workforce-v1` |
| Branch | `main` |
| HEAD | `452925e231cc2f854044d5bd4fdbef08d6cd09fe` ("Initial commit") |
| Status | **clean** (0 porcelain lines) |
| Remote | `https://github.com/ahmedmusawir/stark-ai-workbench-cyberlorean-workforce-v1.git` |
| Tracked content | **1 file**: `README.md` (88 bytes, 2 lines) |

`README.md` in full:

```
# stark-ai-workbench-cyberlorean-workforce-v1
This is where Hermes becomes Cyberloreans
```

There is **no** `CLAUDE.md`, `AGENTS.md`, `.hermes.md`, no directory structure, no roster, no templates, no worker definitions. Total size excluding `.git`: 8 KB.

**Verdict: the repo is a named placeholder with an intent statement. Zero workforce material exists on disk.**

> Note: the `agent_docs/RESPONSES/` folder and this report file were created *after* the recon snapshot above, under a separate explicit bookkeeping authorization. The repo state described in section A is the state at inspection time.

---

## B. Hermes

| Fact | Value |
|---|---|
| Install | `/home/moose/.hermes/hermes-agent` (git clone, `.install_method` = `git`) |
| Upstream | `https://github.com/NousResearch/hermes-agent.git` |
| Version | `0.20.5` (`pyproject.toml:5`) |
| HEAD / pinned commit | `4c1f53be10d0fce1d25aee1975e5149b6c54f25a` (2026-08-25, PR #94568 merge) |
| Working tree | **clean** — zero local modifications to the Hermes source |
| Update status | `.update_check`: `behind: 911` commits, ver `0.20.5` |
| Profiles | `architect_agent`, `designer_agent`, `devops_agent` — **three, no QA** |

**Local customization of Hermes itself: none.** The install tree is byte-clean against the pinned upstream commit. Every Stark-specific thing lives in `~/.hermes/profiles/*` and `~/.hermes/*` runtime files, not in the vendor tree.

### Profile loading convention (traced in source)

`agent/prompt_builder.py:2594-2611` — `build_context_files_prompt()` docstring states the resolution order:

1. `.hermes.md` / `HERMES.md` (walk up to git root)
2. `AGENTS.md` (merged chain)
3. `CLAUDE.md` (cwd only)
4. `.cursorrules`

**First found wins — only ONE project context type is loaded.** `SOUL.md` from `HERMES_HOME` is independent and always included.

The discovery helper is `_find_hermes_md()` (`agent/prompt_builder.py:101-115`), names tuple `_HERMES_MD_NAMES = (".hermes.md", "HERMES.md")`.

**The hinge:** what `.hermes.md` gets found depends entirely on `terminal.cwd` in the profile's `config.yaml`.

- Architect: `cwd: /home/moose/.hermes/profiles/architect_agent/workspace` → **finds the constitution**
- Designer: `cwd: .`
- DevOps: `cwd: .`
- Root: `cwd: .`

### A2A mechanism — upstream, not Stark-built

A2A is a stock Hermes **platform plugin**: `/home/moose/.hermes/hermes-agent/plugins/platforms/a2a/` (`adapter.py`, `protocol.py`, `security.py`, `tools.py`, `plugin.yaml`, `DESIGN.md`). It serves the card at `GET /.well-known/agent-card.json` (`adapter.py:219`; canonical v1.0, legacy `agent.json` also answers).

Recognized env vars (from plugin source): `A2A_PORT`, `A2A_AGENT_NAME`, `A2A_AGENT_DESCRIPTION`, `A2A_PEER_TOKENS`, `A2A_BEARER_TOKEN`, `A2A_HOST`, `A2A_PUBLIC_URL`, `A2A_ALLOWED_USERS`, `A2A_ALLOW_ALL_USERS`, `A2A_TRUSTED_PEERS`, `A2A_MAX_PINGPONG_TURNS`, `A2A_RATE_LIMIT`, `A2A_REPLY_TIMEOUT`, `A2A_ADVERTISED_TOOLSETS`, `A2A_PROVIDER_ORG`, `A2A_PROVIDER_URL`, `A2A_PUSH_SECRET`, `A2A_PEER`.

**Stark configures four of them.** Everything else is upstream default.

### Skills — zero Stark authorship

Architect profile skill categories are **identical** to `~/.hermes/skills` and to upstream `hermes-agent/skills`. `software-development/` contains exactly the 11 upstream skills. A `find` for `*stark*` / `*recon*` / `*factory*` across all three profiles' skills returned **nothing** (the `merge-reconciler` hit is upstream, matched on "recon").

Per-profile skill runtime state exists: `.bundled_manifest`, `.curator_state`, `.curator_backups/`, `.usage.json`, `.skills_prompt_snapshot.json`.

---

## C. Architect — primary reference

**Profile:** `/home/moose/.hermes/profiles/architect_agent`

### Static definitions (the actual IP)

| File | Size | Date | Content |
|---|---|---|---|
| `SOUL.md` | 6,355 B | 2026-08-31 | "ARCHITECT JARVIS — SOUL.md" v1.0. 10 sections: Identity, Mission, Relationship With Tony, Character, Architectural Instincts, Primary Deliverables, Role Boundaries, Grounding Philosophy, Mantra, Version History. |
| `workspace/.hermes.md` | 16,947 B | 2026-09-03 | "STARK INDUSTRIES — ARCHITECT WORKSPACE CONSTITUTION" **v1.1**, 28 sections. |
| `workspace/context/` | 27 files, ~1.0 MB | 2026-07-12 | Full Factory doctrine library. |

`.hermes.md:15-17` states the layering explicitly: *"`SOUL.md` defines who the Architect is. This file defines how the Architect must operate."*

### Context — historical claim verified, with a correction

**Historical evidence said "`.hermes.md` + 27 context documents." Both parts are confirmed true as of today.** Exactly 27 `.md` files in `workspace/context/`, zero symlinks, zero subdirectories.

**New finding not in the handoff:** I checksummed all 27 against the canonical source. They are **byte-for-byte identical** to `/home/moose/Documents/APP FACTORY DOCS/`, which also contains exactly 27 files. Inodes differ (`137352` vs `1873108` for `ARCHITECT_PLAYBOOK.md`) — these are **real copies, not symlinks and not hardlinks**. There is zero drift between canonical and runtime today, but nothing enforces that; they will silently diverge on the next canonical edit.

`.hermes.md:551-570` (§28 Runtime Factory Context Library) documents this deliberately: the context dir is *"a deterministic materialization of Tony's canonical Factory source `/home/moose/Documents/APP FACTORY DOCS/`"*, with an explicit rule to *"stop and report context drift"* if they differ.

### Mandatory startup reads (`.hermes.md:31-37`)

1. `context/ARCHITECT_PLAYBOOK.md`
2. `context/ARCHITECT_QUESTIONNAIRE.md`
3. `context/APP_FACTORY_BLUEPRINT.md`
4. `context/SOFTWARE_FACTORY_PLAYBOOK.md`

The other 23 are on-demand doctrine.

### Load trace — what actually reaches the model

| Layer | Mechanism | Loaded? |
|---|---|---|
| `SOUL.md` | `HERMES_HOME`, independent slot | **Yes** |
| `workspace/.hermes.md` | `_find_hermes_md()` from `terminal.cwd` | **Yes** — because `config.yaml:121` sets `cwd: /home/moose/.hermes/profiles/architect_agent/workspace` |
| `context/*.md` | **Not auto-loaded.** Loaded only by the agent obeying the `.hermes.md` §2 instruction to read them. | Instruction-dependent, **not mechanically guaranteed** |

This is the single most important architectural fact about the working Architect: **context is a behavioral contract, not a harness guarantee.** The `config.yaml.before-context-cwd` backup (2026-08-31) is the fossil of the fix that made this work.

### Model / provider / A2A (sanitized)

From `config.yaml` (secret values redacted, never printed):

```
model.provider:   ollama-launch
model.base_url:   http://127.0.0.1:11434/v1
model.default:    deepseek-v4-pro:cloud
model.api_key:    <present, redacted>
agent.max_turns:  150
agent.reasoning_effort: medium
toolsets:         [hermes-cli, web]
terminal.cwd:     .../architect_agent/workspace
_config_version:  38
```

Note the inconsistency inside the file itself: `providers.ollama-launch.default_model` is `deepseek-v4-flash:0731-cloud` while `model.default` is `deepseek-v4-pro:cloud`. `model.default` is the operative one.

**A2A identity and port come from `.env`, not `config.yaml`** — `config.yaml` has no A2A block at all. `architect_agent/.env:506-510`:

```
A2A_AGENT_NAME="Architect Agent"
A2A_PORT=9901
A2A_PEER_TOKENS=<present, redacted>
A2A_MAX_PINGPONG_TURNS=20
```

Each profile `.env` is ~25 KB — essentially the full upstream `.env.example` (24,792 B) with four A2A lines filled in plus provider credentials. **The Stark-authored delta is four lines.**

### Mutable / runtime / private (identified by path, contents not read)

`state.db` (1.7 MB) + `-wal`/`-shm`, `a2a_audit.jsonl` (33 KB), `a2a_conversations/`, `sessions/`, `memories/MEMORY.md` (775 B) + `.before-brain-pack`, `channel_directory.json`, `gateway_state.json`, `gateway.lock`, `gateway-starts.log`, `state/gateway.heartbeat`, `state/gateway.lifecycle.json`, `context_length_cache.yaml`, `cache/`, `logs/`, `sandboxes/`, `cron/`, `pairing/`, `pending_messages/`, `audio_cache/`, `image_cache/`, `.clean_shutdown`, `skills/.usage.json`, `skills/.curator_state`, `.skills_prompt_snapshot.json`.

Empty scaffolding dirs (created, never used): `home/`, `plans/`, `skins/`, `bin/`, `hooks/`, `platforms/`.

### Backup / experiment clutter present in the live profile

`SOUL_31AUG2026.md`, `SOUL.md.before-brain-pack`, `config.yaml.before-context-cwd`, `workspace/.hermes_31AUG2026.md`, `workspace/.hermes.md.before-p1a4-final`, `workspace/.hermes.md.context-test-passed`, `workspace/ARCHITECT_TEST_REFERENCE.md`, `_p1_archive/`.

I diffed `.hermes.md` against `.hermes.md.before-p1a4-final`: the **only** changes are the version bump 1.0→1.1, the date, one added version-history row, and renumbering §27→§28. The P1-A4 delta was metadata, not substance.

`_p1_archive/stark-architect-skill-experiment/` is a **rejected approach** — a `SKILL.md` plus a `references/` dir holding duplicate copies of the four core Factory docs. `.hermes.md:566` explicitly overrules it: *"Do not treat an optional skill or a skill `references/` directory as the authoritative source of Factory doctrine."* These four duplicates are stale-copy landmines.

`ARCHITECT_TEST_REFERENCE.md` and `.hermes.md.context-test-passed` are context-plumbing probes containing canary phrases. Test scaffolding, not doctrine — but `ARCHITECT_TEST_REFERENCE.md` sits in the live workspace root.

---

## D. Designer and DevOps — **shells, not workers**

Both profiles are structurally complete Hermes installs with **empty workspaces**.

| | Designer | DevOps |
|---|---|---|
| `SOUL.md` | 599 B, 15 lines — generic "Product and UI Designer", no Stark/Jarvis/Tony framing, no version header | 605 B, 16 lines — generic "DevOps Architect", same shape |
| `workspace/` | **empty** | **empty** |
| `.hermes.md` | **absent** | **absent** |
| `context/` | **absent** | **absent** |
| `terminal.cwd` | `.` | `.` |
| Model | `minimax-m3:cloud` | `glm-5.2:cloud` |
| A2A | `"Designer Agent"` : 9902 | `"Devops Agent"` : 9903 |
| Skills | identical upstream set | identical upstream set |
| Runtime state | `state.db` 586 KB, a2a audit 5.3 KB, 7 a2a contexts, last activity 2026-09-04 | `state.db` 389 KB, a2a audit 3.5 KB, 3 a2a contexts, last activity 2026-09-04 |

`DESIGNER_PLAYBOOK.md` (18,569 B) exists in the canonical docs and in the Architect's context dir — **but the Designer profile cannot see it.** Empty workspace, `cwd: .`, no context dir.

**Complete:** A2A wiring, model assignment, ADK registration, Workbench roster entry.
**Placeholder:** `SOUL.md` — two generic role blurbs, roughly 1/10th the Architect's depth and missing the entire Tony/Jarvis relationship model, grounding philosophy, and deliverable contract.
**Missing:** `.hermes.md` constitution, `context/` library, the `terminal.cwd` pointer that makes either load.
**Unverified:** whether either has ever produced useful role-specific output. They have A2A conversation history from Sep 4, but I did not read it and did not run them.

Note: `A2A_AGENT_NAME="Devops Agent"` — lowercase `o`, inconsistent with the Workbench label "DevOps Agent".

---

## E. QA Lead — **does not exist, in any layer**

Searched exhaustively:

| Layer | Result |
|---|---|
| Hermes profile | **None.** `~/.hermes/profiles/` = architect, designer, devops |
| Role source doc | **None.** No `QA_*.md` in `APP FACTORY DOCS/` (27 files, all named) |
| Architect context | **None.** No QA-named file among the 27 |
| ADK backend | **None.** No `qa_agent`/`qa_lead` string anywhere in `*.py`/`*.json`/`*.md`/`*.sh` |
| Workbench manifest | **None.** Not in `config/agents.manifest.json` |
| A2A port | **None** allocated (9900/01/02/03 used) |

The only QA references in the entire canonical doc set are **two headings** in one file: `SOFTWARE_FACTORY_PLAYBOOK.md:951` ("### QA Checklist") and `:954` ("## Pre-Release QA"). Zero hits for "quality assurance" or "QA Lead" across all 27 docs.

There *is* a QA-adjacent asset the handoff didn't mention: `TESTING_PLAYBOOK.md` (79,339 B — the second-largest doc in the library) plus `agent_docs/CURRENT_APP/BIM000/STAGE_A_QA_RUBRIC.md` in the frontend repo. Both are testing doctrine, not a QA *role* definition.

`.hermes.md:359` names QA in the role table — *"**QA** — independent verification and verdict"* — which is one line of aspiration, not a role document.

**Verdict: QA Lead is a named seat in the org chart with no role document, no profile, no worker, and no routing. It must be authored from scratch. There is nothing to port.**

---

## F. ADK / A2A backend

| Fact | Value |
|---|---|
| Path | `/home/moose/python/stark-ai-workbench-adk-backend-v1` |
| Branch | `main` |
| HEAD | `1eb7d88730447cc10d950817d24e8324429926cf` — "chore(p1): harden workforce shells and remove dead context cache" (2026-09-07) |
| Status | **dirty (1 file)**: `M architect_agent/.adk/session.db` — runtime session state, not source |
| Tracked files | 82 |

### Agent modules on disk

`architect_agent/`, `designer_agent/`, `devops_agent/`, `hermes_agent/`, `jarvis_agent/`, `product_agent_rico_1/`.

### RemoteA2aAgent mappings

All three worker agents are identical 18-line modules. `architect_agent/agent.py`:

```python
root_agent = RemoteA2aAgent(
    name="architect_agent",
    description="Stark Architect worker connected through Hermes A2A.",
    agent_card="http://127.0.0.1:9901/.well-known/agent-card.json",
    httpx_client=httpx.AsyncClient(
        timeout=httpx.Timeout(120.0),
        headers={"Authorization": f"Bearer {os.environ['HERMES_A2A_TOKEN']}"},
    ),
)
```

Designer → `:9902`, DevOps → `:9903`. Identical otherwise.

`jarvis_agent/agent.py` is a **different species** — a native ADK `Agent` on `gemini-3.7-flash` with `google_search`, instructions fetched live from GCS via `fetch_instructions("jarvis_agent")`, and receipt callbacks. It is not a Hermes worker.

### Auth / config

- Workers: `HERMES_A2A_TOKEN` from env (`.env`, gitignored). Correct pattern.
- `.env` names present: `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_REGION`, `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_STT_BUCKET`, `HERMES_A2A_TOKEN`. No values inspected.
- `credentials/cyberize-vertex-api.json` — a GCP service-account key on disk. **Correctly gitignored** (`.gitignore:211`) and confirmed untracked via `git ls-files`. Not read.
- `start_server.sh` → `adk api_server . --host=0.0.0.0 --port=8000 --session_service_uri="$SUPABASE_DB_URI"`

**Two defects found:**

1. **`hermes_agent/agent.py:13` carries a hardcoded `Authorization: Bearer` literal** instead of reading from env, unlike its three siblings. That literal is committed to git. It is not reproduced in this report. It is a test-grade token, but it is a credential in tracked source and should be rotated and moved to env.
2. **`start_server.sh:14` requires `$SUPABASE_DB_URI`, which is not defined in `.env`.** The error message on line 7 even names it. As written, the script starts the server with an empty `--session_service_uri`. Either the script is stale or `.env` is incomplete — I cannot tell which from disk alone, and I did not run it.

### Useful assets discovered here (not in the handoff)

- `agent_docs/SKILLS/stark-recon-skill-v1.1/` — a complete Stark-authored skill: `SKILL.md`, `CLAUDE.md`, `README.md`, `references/ANTI_PATTERNS.md`, `references/EVIDENCE_DISCIPLINE.md`, `templates/RECON_MISSION.md`, `templates/RECON_REPORT_TEMPLATE.md`, plus a worked example. **This is real reusable Cyberlorean IP sitting in the wrong repo.**
- `docs/ADK 2.7.1 ↔ Hermes A2A — Proven Local POC Setup.md` (+ PDF)
- `docs/HERMES_MULTI_PROFILE_A2A_ADK_RUNBOOK_v1.0 (1).md` (+ PDF) — the runbook for exactly what P2 wants to systematize
- `skills/SCAFFOLD_NEW_AGENT.md`
- `docs/NAMING_CONVENTIONS.md`, `docs/architecture.md`, `docs/decisions.md`, `docs/patterns.md`
- `docs/PYTHON_ADK_PLAYBOOKS/` — 10 playbooks

---

## G. Next.js Workbench — **discovered**

The handoff listed this as unknown. Found by bounded search (`find /home/moose -maxdepth 4 -name 'next.config.*'`, heavy dirs pruned).

| Fact | Value |
|---|---|
| Path | **`/home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1`** |
| Branch | `main` |
| HEAD | `466083f2b415d9faeb362eb5e48f6e259a42d840` — "chore(p1): bank inherited Workbench frontend baseline" (2026-09-07) |
| Status | **clean** |

### Roster — `config/agents.manifest.json` (12 lines, the whole file)

```json
{
  "bundles": [
    { "id": "v1",       "label": "ADK Bundle v1",      "urlEnv": "ADK_BUNDLE_URL_V1" },
    { "id": "v2-local", "label": "Harness v2 (local)", "urlEnv": "ADK_BUNDLE_URL_V2_LOCAL" }
  ],
  "agents": [
    { "name": "architect_agent", "bundle": "v1", "label": "Architect Agent" },
    { "name": "hermes_agent",    "bundle": "v1", "label": "Harmes Main Agent" },
    { "name": "designer_agent",  "bundle": "v1", "label": "Designer Agent" },
    { "name": "devops_agent",    "bundle": "v1", "label": "DevOps Agent" },
    { "name": "ghl_mcp_agent",   "bundle": "v1", "label": "GHL CRM Agent" }
  ]
}
```

### Selection → routing chain (clean, well-built)

1. `src/config/manifest.ts:14` imports the JSON; `:93` validates at module load — a malformed manifest fails the build loudly, listing every problem at once.
2. `:96-104` — `KNOWN_AGENTS`, `DEFAULT_AGENT` (manifest order is meaningful; first entry is default), `agentsForUi()`.
3. `src/components/chat/AgentSwitcher.tsx:11` renders the sidebar from `agentsForUi()`. Comment at `:9-10`: *"adding an agent is a JSON edit in `config/agents.manifest.json`, not a code change."*
4. `src/app/api/agent/run/route.ts:32` — `resolveBundleEnvVar(body.agent_name)` → env-var **name**; `:39` reads `process.env[urlEnv]` → base URL; `:47` `runAgentFlow()`. Unknown agent → 400; unconfigured bundle → 500.

The manifest deliberately carries **env-var names only**, never URLs (`manifest.ts:5-7`). This is the right pattern and the adding-a-worker seam is already a one-line JSON edit.

Env: `ADK_BUNDLE_URL_V1=http://127.0.0.1:8000`, `NEXT_PUBLIC_CHAT_MODE=live`.

### Roster drift — three-way mismatch

| Manifest entry | ADK module exists? | Hermes profile exists? |
|---|---|---|
| `architect_agent` | yes | yes |
| `hermes_agent` | yes | root install, no profile |
| `designer_agent` | yes | yes |
| `devops_agent` | yes | yes |
| `ghl_mcp_agent` | **NO** | **NO** |
| — | `jarvis_agent` (not in manifest) | — |
| — | `product_agent_rico_1` (not in manifest) | — |

**`ghl_mcp_agent` is selectable in the Workbench UI and will 502 on use** — the manifest resolves it to a valid bundle URL, but the ADK bundle has no such module. Also, the `v2-local` bundle is declared but referenced by zero agents, and `ADK_BUNDLE_URL_V2_LOCAL` is absent from `.env.local` (present only in `.env.example`) — dead config.

Label typo: `"Harmes Main Agent"`.

---

## H. Role source documents

**Canonical source:** `/home/moose/Documents/APP FACTORY DOCS/` — **27 files, all dated 2026-07-12 00:25**, directory mtime 2026-08-03. Uniform timestamps across all 27 indicate a single bulk materialization, not incremental authoring. **No version manifest, no CHANGELOG, no git repo** — provenance and version are undocumented.

| Role | Source document | Size | Referenced by that role's profile? |
|---|---|---|---|
| **Architect** | `ARCHITECT_PLAYBOOK.md` + `ARCHITECT_QUESTIONNAIRE.md` | 25,105 / 8,049 B | **Yes** — `.hermes.md:33-34`, mandatory startup reads |
| **Designer** | `DESIGNER_PLAYBOOK.md` | 18,569 B | **No** — empty workspace, no context dir, no reference |
| **DevOps** | **None** | — | n/a. No `DEVOPS_*.md` exists. `SOFTWARE_FACTORY_PLAYBOOK.md` is the closest fit but is not role-specific |
| **QA Lead** | **None** | — | n/a. Two headings in `SOFTWARE_FACTORY_PLAYBOOK.md`; `TESTING_PLAYBOOK.md` (79 KB) is testing doctrine, not a role |
| **Engineer** | `ENGINEER_PLAYBOOK.md` | 48,290 B | No Engineer profile exists |

### Competing versions — three copies of the four core docs

| Copy | Path | Status |
|---|---|---|
| Canonical | `~/Documents/APP FACTORY DOCS/` | **Authoritative** per `.hermes.md:559` |
| Runtime | `architect_agent/workspace/context/` | **Byte-identical today** (md5-verified). Independent copies — will drift silently |
| Rejected | `architect_agent/_p1_archive/stark-architect-skill-experiment/references/` | Explicitly overruled by `.hermes.md:566`. Same 4 files, copied 2026-08-30 |

A **fourth partial** copy exists: `stark-ai-workbench-nextjs-frontend-v1/agent_docs/APP_FACTORY/` holds 10 of the manuals — including `UI-UX-BUILDING-MANUAL.md` (hyphens) vs canonical `UI_UX_BUILDING_MANUAL.md` (underscores). I did not checksum these; **treat as an unverified fourth version.**

**Authority is clear for the Architect and undefined for everyone else.**

---

## Table 1 — Worker routing chain

| Worker | Workbench selection (label) | ADK agent module | A2A endpoint | Hermes profile | Configured model / provider |
|---|---|---|---|---|---|
| **Architect** | `architect_agent` — "Architect Agent" *(default: first in manifest)* | `architect_agent/agent.py` `RemoteA2aAgent` | `http://127.0.0.1:9901/.well-known/agent-card.json` | `architect_agent` (`A2A_PORT=9901`, `A2A_AGENT_NAME="Architect Agent"`) | `deepseek-v4-pro:cloud` / `ollama-launch` @ `127.0.0.1:11434/v1` |
| **Hermes main** | `hermes_agent` — "Harmes Main Agent" | `hermes_agent/agent.py` `RemoteA2aAgent` | `http://127.0.0.1:9900/.well-known/agent-card.json` | root `~/.hermes` (no profile dir) | `deepseek-v4-flash:0731-cloud` / `ollama-launch` |
| **Designer** | `designer_agent` — "Designer Agent" | `designer_agent/agent.py` `RemoteA2aAgent` | `http://127.0.0.1:9902/.well-known/agent-card.json` | `designer_agent` (`A2A_PORT=9902`) | `minimax-m3:cloud` / `ollama-launch` |
| **DevOps** | `devops_agent` — "DevOps Agent" | `devops_agent/agent.py` `RemoteA2aAgent` | `http://127.0.0.1:9903/.well-known/agent-card.json` | `devops_agent` (`A2A_PORT=9903`, name `"Devops Agent"`) | `glm-5.2:cloud` / `ollama-launch` |
| **GHL CRM** | `ghl_mcp_agent` — "GHL CRM Agent" | **MISSING** | — | **none** | — |
| **QA Lead** | **absent** | **absent** | **absent** | **absent** | **absent** |
| *Jarvis (non-worker)* | not in manifest | `jarvis_agent/agent.py` native ADK `Agent` | n/a — direct | n/a | `gemini-3.7-flash` / Vertex, instructions from GCS |

Auth on every A2A hop: `Authorization: Bearer $HERMES_A2A_TOKEN` (except `hermes_agent`, which hardcodes a literal — see F).

---

## Table 2 — Architect anatomy

| Path | Category | Reason |
|---|---|---|
| `profiles/architect_agent/SOUL.md` | **1 — CANDIDATE CYBERLOREAN SOURCE** | Stark-authored role identity, versioned (v1.0), zero Hermes coupling. The single highest-value artifact. |
| `profiles/architect_agent/workspace/.hermes.md` | **1 — CANDIDATE CYBERLOREAN SOURCE** | Stark-authored 28-section operating constitution, v1.1, with version history. Filename is Hermes-specific; content is portable. |
| `Documents/APP FACTORY DOCS/*.md` (27) | **1 — CANDIDATE CYBERLOREAN SOURCE** | Declared canonical Factory doctrine (`.hermes.md:559`). Tony-owned IP. Currently unversioned and outside git — the biggest banking opportunity. |
| `workspace/context/*.md` (27) | **4 — GENERATED/EPHEMERAL** | Deterministic materialization of the canonical source; md5-identical today. Derived artifact — bank the generator rule, not the copies. |
| `config.yaml` → `terminal.cwd` | **1 — CANDIDATE CYBERLOREAN SOURCE** (one line) | The load-bearing setting that makes `.hermes.md` resolve. Must be captured in any worker template. |
| `config.yaml` → `model.default`, `agent.*`, `toolsets` | **5 — UNCERTAIN** | Deliberate per-role tuning, but entangled with 140 lines of Hermes defaults and a live `api_key`. Needs a sanitized-shape ruling. |
| `config.yaml` → `model.api_key` | **3 — SECRET/PRIVATE** | Live provider credential. |
| `.env` lines 506-508 (`A2A_AGENT_NAME`, `A2A_PORT`) | **1 — CANDIDATE CYBERLOREAN SOURCE** | Worker identity + port allocation. Two non-secret lines; the rest of the file is vendor boilerplate. |
| `.env` (full 25 KB) | **3 — SECRET/PRIVATE** | Provider keys, `A2A_PEER_TOKENS`. Never bank. |
| `_p1_archive/stark-architect-skill-experiment/SKILL.md` | **5 — UNCERTAIN** | Stark-authored but an **explicitly rejected** approach (`.hermes.md:566`). Value is as a negative lesson. |
| `_p1_archive/.../references/*.md` (4) | **4 — GENERATED/EPHEMERAL** | Stale duplicates of canonical docs. Deletion candidates — active drift hazard. |
| `_p1_archive/PROMPT_ENGINEERING_MANUAL_v1.1.md` | **5 — UNCERTAIN** | Versioned Stark doc, archived, not referenced by any profile. Authority unknown. |
| `SOUL_31AUG2026.md`, `SOUL.md.before-brain-pack` | **4 — GENERATED/EPHEMERAL** | Manual backups superseded by the live `SOUL.md`. |
| `workspace/.hermes_31AUG2026.md`, `.hermes.md.before-p1a4-final` | **4 — GENERATED/EPHEMERAL** | Superseded drafts. Diff vs live = version metadata only. |
| `workspace/ARCHITECT_TEST_REFERENCE.md`, `.hermes.md.context-test-passed` | **4 — GENERATED/EPHEMERAL** | Context-plumbing canaries. Test scaffolding in a production workspace. |
| `skills/**` (all categories) | **2 — HERMES/RUNTIME STATE** | Verified identical to upstream `hermes-agent/skills`. **Vendor material — not Stark IP.** |
| `skills/.usage.json`, `.curator_state`, `.curator_backups/`, `.bundled_manifest`, `.skills_prompt_snapshot.json` | **2 — HERMES/RUNTIME STATE** | Skill-curator runtime bookkeeping. |
| `state.db`, `-wal`, `-shm` | **2 — HERMES/RUNTIME STATE** | Live agent DB (1.7 MB). Contains conversation history — treat as private. |
| `memories/MEMORY.md` (+ backup) | **3 — SECRET/PRIVATE** | Private learned facts. `.hermes.md:412` rules memory is *not* doctrine. Not read. |
| `sessions/`, `a2a_conversations/`, `a2a_audit.jsonl` | **3 — SECRET/PRIVATE** | Conversation transcripts and audit trail. |
| `channel_directory.json`, `gateway_state.json`, `state/gateway.*`, `*.lock`, `*.log`, `.clean_shutdown` | **2 — HERMES/RUNTIME STATE** | Gateway lifecycle and channel bookkeeping. |
| `cache/`, `logs/`, `sandboxes/`, `cron/`, `image_cache/`, `audio_cache/`, `pairing/`, `pending_messages/`, `context_length_cache.yaml` | **2 — HERMES/RUNTIME STATE** | Regenerable caches and transient dirs. |
| `home/`, `plans/`, `skins/`, `bin/`, `hooks/`, `platforms/` | **2 — HERMES/RUNTIME STATE** | Empty upstream scaffolding. |
| `hermes-agent/**` (clean @ `4c1f53b`) | **2 — HERMES/RUNTIME STATE** | Unmodified NousResearch vendor tree, incl. the A2A plugin. |
| `adk-backend/{architect,designer,devops}_agent/agent.py` | **1 — CANDIDATE CYBERLOREAN SOURCE** | 18-line Stark-authored A2A binding. Perfectly templatable — the clearest sanitized-template candidate in the system. |
| `adk-backend/agent_docs/SKILLS/stark-recon-skill-v1.1/` | **1 — CANDIDATE CYBERLOREAN SOURCE** | Complete, versioned Stark skill with templates and references. Real IP in the wrong repo. |
| `adk-backend/docs/HERMES_MULTI_PROFILE_A2A_ADK_RUNBOOK_v1.0.md`, `ADK 2.7.1 ↔ Hermes A2A POC Setup.md`, `skills/SCAFFOLD_NEW_AGENT.md` | **1 — CANDIDATE CYBERLOREAN SOURCE** | The written procedure for standing up a worker. Directly feeds the P2 factory. |
| `frontend/config/agents.manifest.json` | **1 — CANDIDATE CYBERLOREAN SOURCE** | The roster contract. Env-var-names-only design is sound and reusable. |
| `adk-backend/credentials/cyberize-vertex-api.json`, both repos' `.env*` | **3 — SECRET/PRIVATE** | GCP service-account key and env secrets. Gitignored; verified untracked; not read. |
| `adk-backend/hermes_agent/agent.py:13` | **3 — SECRET/PRIVATE** *(defect)* | Hardcoded bearer literal in tracked source. Rotate and move to env. |
| `adk-backend/*/.adk/session.db`, `logs/receipts/` | **2 — HERMES/RUNTIME STATE** | ADK session state; one is the sole dirty file in that repo. |

### Sanitized template candidates (conceptual only — nothing created)

Four templates are implied by the evidence, in dependency order: a **worker profile skeleton** (`SOUL.md` + `.hermes.md` + `context/` + the `terminal.cwd` pointer + the two non-secret A2A env lines); an **ADK binding template** (the 18-line `RemoteA2aAgent` with name/description/port substituted); a **roster entry** (one JSON object plus its port allocation); and a **context materialization rule** (canonical → runtime, with a drift check). None of these were created or copied.

---

## Conflicts with handoff

1. **Workforce repo, "empty or populated?" — RESOLVED: empty.** Disk shows one 88-byte `README.md` at a clean `452925e`, and nothing else. Any document describing workforce material in this repo is **proposing** it, not recording it. Documents that assert otherwise are wrong about today's disk.
2. **"27 context documents" — CONFIRMED, and stronger than claimed.** Exactly 27, and md5-identical to the canonical source. The handoff understated this: they are *copies*, not symlinks, so the identity is coincidental-today, not structural.
3. **Next.js Workbench "unknown" — RESOLVED.** `/home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1`, clean at `466083f`.
4. **QA profile "unknown" — RESOLVED: none exists,** in any of six layers checked.
5. **"QA source material outside APP FACTORY DOCS" — RESOLVED: none.** Only `TESTING_PLAYBOOK.md` and a frontend QA rubric, neither a role definition.
6. **"Parent multi-repo workspace" — RESOLVED: none.** No `additionalDirectories` in `~/.claude/settings.json` (2 keys: theme, notifications) or in any `~/.claude.json` project entry. The three repos are independent and unlinked.
7. **Handoff implies three comparable workers.** Disk shows **one** developed Architect and **two shells** with generic 600-byte SOULs and empty workspaces. This gap is the central finding of this recon.
8. **`ghl_mcp_agent` is in the shipped roster but has no backend.** Not mentioned in the handoff; it is a live user-facing 502.

---

## Summary

**Workforce repo:** Empty shell. `main` @ `452925e`, clean, one 88-byte `README.md`, remote `ahmedmusawir/stark-ai-workbench-cyberlorean-workforce-v1`. Zero workforce material. Greenfield.

**Architect:** The only complete worker. `SOUL.md` (6.4 KB, v1.0) + `workspace/.hermes.md` (17 KB, v1.1, 28 sections) + 27 context docs md5-identical to canonical. Loads because `config.yaml:121` sets `terminal.cwd` to the workspace. `deepseek-v4-pro:cloud` via local Ollama, A2A `:9901`. Cluttered with 8 backup/test files and a `_p1_archive/` holding a rejected skill experiment. **Context loading is a behavioral contract, not a harness guarantee.**

**Designer:** Shell. Generic 599-byte `SOUL.md`, **empty workspace**, no `.hermes.md`, no context, `cwd: .`. Fully wired for A2A (`:9902`, `minimax-m3:cloud`) and present in the roster. `DESIGNER_PLAYBOOK.md` exists canonically but is unreachable from this profile.

**DevOps:** Shell. Generic 605-byte `SOUL.md`, **empty workspace**, same gaps. A2A `:9903`, `glm-5.2:cloud`. **No DevOps role document exists anywhere.**

**QA:** Does not exist in any layer — no profile, no role doc, no ADK module, no roster entry, no port. Two headings in `SOFTWARE_FACTORY_PLAYBOOK.md:951,954` are the sum total. Must be authored from zero.

**Hermes/runtime:** v0.20.5 @ `4c1f53b`, **source tree byte-clean** against upstream, 911 commits behind. Three profiles. A2A is a stock plugin; all skills are stock. Stark's entire customization is `SOUL.md` + `.hermes.md` + `context/` + `terminal.cwd` + four `.env` lines per profile.

**ADK:** `main` @ `1eb7d88`, dirty only in `architect_agent/.adk/session.db`. Three identical 18-line `RemoteA2aAgent` bindings to `:9901/:9902/:9903` with `HERMES_A2A_TOKEN` bearer auth. Holds unbanked IP: `stark-recon-skill-v1.1`, the multi-profile A2A runbook, `SCAFFOLD_NEW_AGENT.md`. Two defects: hardcoded bearer at `hermes_agent/agent.py:13`, and `start_server.sh` requiring an undefined `$SUPABASE_DB_URI`.

**Frontend:** `/home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1`, `main` @ `466083f`, clean. `config/agents.manifest.json` is a validated single source of truth (5 agents, env-var names only); `manifest.ts` → `AgentSwitcher.tsx` → `api/agent/run/route.ts` → `process.env[urlEnv]` → `http://127.0.0.1:8000`, mode `live`. Adding a worker is a one-line JSON edit. Drift: `ghl_mcp_agent` has no backend; `v2-local` bundle is dead.

**Role source docs:** 27 files in `~/Documents/APP FACTORY DOCS/`, all timestamped 2026-07-12 00:25, no version manifest, not in git. Architect docs referenced and mandatory; Designer doc exists but unreferenced; DevOps and QA docs absent. Three-to-four copies of the core four exist across the machine.

**Conflicts with handoff:** Workforce repo is definitively empty (disk beats documents). Workbench and QA unknowns resolved. No parent workspace exists. The "three workers" framing overstates reality — one worker, two shells. `ghl_mcp_agent` roster/backend mismatch is undocumented.

**Risks/blockers:**

1. Canonical docs are unversioned, ungoverned, outside git — the one asset with no provenance is the one everything depends on.
2. Context loading depends on an instruction the model must choose to obey plus a single `terminal.cwd` value. Silent partial failure is the default failure mode.
3. Runtime context is a *copy*, not a link. First canonical edit creates undetected drift.
4. Hardcoded bearer literal in tracked source (`hermes_agent/agent.py:13`) — rotate.
5. `start_server.sh` references an undefined `$SUPABASE_DB_URI`.
6. Four competing copies of the core docs, one explicitly rejected, one with inconsistent filenames.
7. `ghl_mcp_agent` is user-selectable and will 502.
8. Hermes 911 commits behind; an upgrade could alter context-loading semantics.
9. IP is scattered across three unlinked repos with the designated home empty.

**Open questions (Architect ruling needed):**

1. Is the Cyberlorean unit the *role definition* (`SOUL.md` + `.hermes.md` + context manifest, runtime-agnostic), or the *full profile* including Hermes config shape?
2. Do the 27 canonical docs get banked into the workforce repo as versioned source, or does the repo hold only a pointer + materialization rule?
3. Does every worker get the full 27-doc library, or a role-scoped subset? (The Architect's four mandatory reads suggest per-role manifests.)
4. Are per-role model assignments (`deepseek-v4-pro` / `minimax-m3` / `glm-5.2`) deliberate IP or incidental?
5. QA Lead: author a new role document from `TESTING_PLAYBOOK.md`, or defer until Designer and DevOps are real workers?
6. Does `stark-recon-skill-v1.1` migrate to the workforce repo as shared capability?
7. Keep the canonical docs at `~/Documents/APP FACTORY DOCS/`, or make the workforce repo the new canon?

---

## Recommended first bounded experiment

**Bank the Architect as one portable Cyberlorean definition and prove it round-trips.**

Scope: create `workers/architect/` in the workforce repo holding exactly three things — a copy of `SOUL.md`, a copy of `.hermes.md` with the hardcoded workspace path at line 7 replaced by a placeholder, and a `context.manifest.json` listing the 27 filenames with their md5 checksums and the four marked `mandatory: true`. No `config.yaml`, no `.env`, no context file copies, no scripts, no other workers.

Observable success condition: a script reading `context.manifest.json` reports **27/27 filenames present and 27/27 checksums matching** against `~/Documents/APP FACTORY DOCS/`, and reports a clear failure if any file is edited, renamed, or removed. Verify the failure path by checksumming a temp copy with one byte changed — confirming the drift detector actually fires before trusting it.

Why this first: it converts the highest-value, best-understood artifact into versioned source; it forces the manifest-vs-copies decision (Q2/Q3) on one concrete case instead of in the abstract; it builds the drift detector that `.hermes.md:568` already demands but nothing implements; and it touches no runtime, no profile, no service — so it cannot break the working Architect.

**Not executed.** Awaiting ruling.
