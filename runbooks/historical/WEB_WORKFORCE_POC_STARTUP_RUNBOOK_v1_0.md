# WEB WORKFORCE POC — STARTUP RUNBOOK v1.0

> **Date:** 2026-10-26 (Asia/Dhaka) · **Runtime:** Hermes Agent v0.20.5 (2026.8.19), local commit 4c1f53be, install `/home/moose/.hermes/hermes-agent` · **User/home:** `moose` / `/home/moose`
> **Frontend note:** every frontend reference below is to the **inherited v1 checkout** `/home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1`. It is not the completed frontend-v2 integration, and its multi-session behavior is unverified.

## 1. Prerequisites

- Ollama listening on `127.0.0.1:11434` (model provider for every profile).
- Each profile's `.env` contains `OLLAMA_API_KEY`, `A2A_PORT`, `A2A_AGENT_NAME`, `A2A_PEER_TOKENS` (names only; never print values). Mode must be 600.
- Working directory for gateway commands: any directory. The gateway's own cwd is irrelevant; the agent's working directory comes from the profile `config.yaml` key `terminal.cwd`. Use `/home/moose` for consistency with the Architect.

## 2. Port and env precedence (verified on this pinned version)

| Profile | Port | Display name |
|---|---|---|
| architect_agent (original) | 9901 | Architect Agent |
| designer_agent (original, stopped) | 9902 | — |
| devops_agent (original, stopped) | 9903 | — |
| web_architect_agent | 9911 | Web Architect |
| web_designer_agent | 9912 | Web Designer |
| web_developer_agent | 9913 | Web Developer |
| web_qa_agent | 9914 | Web QA Lead |
| web_devops_agent | 9915 | Web DevOps |

`hermes_cli/env_loader.py` loads the selected profile's `.env` with `override=True`, then removes profile-managed keys that are in the shell but absent from the `.env`. So **the profile `.env` decides the port**; a shell `A2A_PORT` cannot override it. The commands below still pass the port explicitly in the environment so the command line is self-documenting, and both sources agree. The A2A plugin has no `--port` flag; `A2A_PORT` is the only supported knob.

## 3. Start the five Web workers (one terminal each, foreground)

```bash
# Terminal 1 — Web Architect, port 9911
cd /home/moose && A2A_PORT=9911 hermes -p web_architect_agent gateway run

# Terminal 2 — Web Designer, port 9912
cd /home/moose && A2A_PORT=9912 hermes -p web_designer_agent gateway run

# Terminal 3 — Web Developer, port 9913
cd /home/moose && A2A_PORT=9913 hermes -p web_developer_agent gateway run

# Terminal 4 — Web QA Lead, port 9914
cd /home/moose && A2A_PORT=9914 hermes -p web_qa_agent gateway run

# Terminal 5 — Web DevOps, port 9915
cd /home/moose && A2A_PORT=9915 hermes -p web_devops_agent gateway run
```

If a profile is already running (for example the background instances left by the build shot), `gateway run` refuses with a lock message; stop the old PID first (§6) or add `--replace`.

Original Architect (already running as pid 91664; start only if it is down):

```bash
cd /home/moose && A2A_PORT=9901 hermes -p architect_agent gateway run
```

## 4. Start the ADK backend and the frontend (as currently operated)

```bash
# ADK api_server on 127.0.0.1:8000 — exactly what is running today (no start_server.sh, no Supabase URI)
cd /home/moose/python/stark-ai-workbench-adk-backend-v1 && .venv/bin/adk api_server

# Frontend (inherited v1 checkout) on port 3000
cd /home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1 && npm run dev
```

The ADK reads `HERMES_A2A_TOKEN` from its repo-root `.env` at agent-load time. The Next.js app reads `ADK_BUNDLE_URL_V1=http://127.0.0.1:8000` from `.env.local`.

## 5. Checks

Port and card checks:

```bash
hermes profile list                                   # Gateway column must read "running" for the five web_* profiles
ss -ltnp | grep -E ':(9901|991[1-5])\b'               # one hermes listener per port, all 127.0.0.1
for p in 9911 9912 9913 9914 9915; do printf "$p: "; curl -s -m 3 http://127.0.0.1:$p/.well-known/agent-card.json | python3 -c 'import sys,json;print(json.load(sys.stdin)["name"])'; done
```

Expected card names, in order: Web Architect, Web Designer, Web Developer, Web QA Lead, Web DevOps.

Actual chat check (direct A2A, no ADK or Bob needed). Reads the token from the ADK `.env` without printing it:

```bash
TOK=$(grep -E '^HERMES_A2A_TOKEN=' /home/moose/python/stark-ai-workbench-adk-backend-v1/.env | cut -d= -f2- | tr -d '"'"'"'')
curl -s -m 120 http://127.0.0.1:9914/ -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"1","method":"message/send","params":{"message":{"role":"user","messageId":"m1","contextId":"ctx-check-1","parts":[{"kind":"text","text":"Hypothetical, no action: state your role name in one sentence."}]}}}' | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["result"]["status"]["state"])'
unset TOK
```

Expected: `TASK_STATE_COMPLETED`. The reply text is inside `result.status.message.parts` or `result.artifacts`.

Through the ADK (after Tony adds the agent folders, §7): `curl -s http://127.0.0.1:8000/list-apps` must list the five `web_*_agent` names. Through Bob: the sidebar must show the five labels and a message must return a reply within its 75 s cap.

## 6. Stop / restart specific owned processes

```bash
hermes profile list                                    # see which gateways run
cat /home/moose/.hermes/profiles/web_qa_agent/gateway.pid   # JSON with the exact PID of that profile's gateway
kill <pid>                                             # graceful stop of that one gateway only
```

Never use `pkill hermes` or `killall`: it would also stop the original Architect (pid 91664). To restart one worker, stop its PID, confirm its port is closed with `ss -ltnp | grep <port>`, then run its §3 command again. Build-shot background instances as of 2026-10-26 20:52: 1471989 (9911), 1471992 (9912), 1471995 (9913), 1471998 (9914), 1472001 (9915).

## 7. Session storage behavior (current, with uncertainty)

- **Hermes:** each profile keeps its own `state.db` (sessions + messages), `sessions/`, `a2a_conversations/` and `a2a_audit.jsonl` under `/home/moose/.hermes/profiles/<profile>/`. One A2A `contextId` maps to one Hermes session id; two contextIds to the same worker were verified to be separate conversations. Memory (`memories/`) starts empty for the five new workers.
- **ADK:** with the current `adk api_server` launch (no `--session_service_uri`), sessions persist in `<agent>/.adk/session.db` inside each agent folder. How ADK derives the A2A `contextId` from its session id was not inspected; isolation at the ADK layer is therefore **unverified** here.
- **Frontend v1:** whether it can create separate sessions per agent and how it maps them to ADK sessions was not tested in this shot. Do not treat this runbook as evidence of frontend isolation.

For Tony's integration step (not done): ADK folders `web_<role>_agent/{__init__.py,agent.py}` copied from `architect_agent/` with name, description and port changed (9911–9915), keeping `httpx.Timeout(120.0)` and `os.environ['HERMES_A2A_TOKEN']`; and five entries appended to `config/agents.manifest.json` with bundle `v1` and the labels in §2 (backup of the original is in `/home/moose/Downloads/WEB_WORKFORCE_POC_BACKUP_20261026_204503/`).

## 8. Known first-start side effect

On a profile's first gateway start Hermes downloads its `tirith` security helper into `<profile>/bin/` (SHA-256 verified only; cosign not installed). This happened for all five new profiles and is normal for this version.
