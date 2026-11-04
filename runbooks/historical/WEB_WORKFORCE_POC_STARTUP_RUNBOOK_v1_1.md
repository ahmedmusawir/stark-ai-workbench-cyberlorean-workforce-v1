# WEB WORKFORCE POC — STARTUP RUNBOOK v1.1

> **Date:** 2026-10-26 (Asia/Dhaka) · **Supersedes:** v1.0 · **Runtime:** Hermes Agent v0.20.5 (2026.8.19), local commit 4c1f53be, install `/home/moose/.hermes/hermes-agent` · **User/home:** `moose` / `/home/moose`
> **Legend:** **[TESTED]** = executed and observed in this session. **[UNTESTED]** = integration guidance not exercised here.
> **Frontend note:** any frontend reference is to the **inherited v1 checkout** `/home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1`. It is not the completed frontend-v2, and its multi-session behavior is unverified.

## 1. Fleet

| Profile | Port | Display name (agent card) | Model (via Ollama `ollama-launch`, `http://127.0.0.1:11434/v1`) |
|---|---|---|---|
| architect_agent (original) | 9901 | Architect Agent | deepseek-v4-pro:cloud |
| designer_agent (original, stopped) | 9902 | — | minimax-m3:cloud |
| devops_agent (original, stopped) | 9903 | — | glm-5.2:cloud |
| web_architect_agent | 9911 | Web Architect | deepseek-v4-pro:cloud |
| web_designer_agent | 9912 | Web Designer | minimax-m3.1-flash:cloud |
| web_developer_agent | 9913 | Web Developer | glm-5.3:cloud |
| web_qa_agent | 9914 | Web QA Lead | kimi-k2.7-code:cloud |
| web_devops_agent | 9915 | Web DevOps | glm-5.3-flash:cloud |

## 2. Prerequisites [TESTED]

- Ollama daemon listening on `127.0.0.1:11434`; the `:cloud` models are proxied by it and need the `OLLAMA_API_KEY` that each profile's `.env` already holds (mode 600, never print it).
- Each profile `.env` holds `A2A_PORT`, `A2A_AGENT_NAME`, `A2A_PEER_TOKENS` (the `adk` peer). Only `A2A_PEER_TOKENS` is set and no `A2A_HOST`, so the A2A server binds loopback only.
- Each profile `config.yaml` points `terminal.cwd` at its own `workspace/`, which holds `.hermes.md` (constitution with the role playbook, WBM playbook and README embedded) and `context/WEB_FACTORY_STARTER_v1_1/` (source copies). `context_file_max_chars: 150000` keeps the embedded documents untruncated.
- Working directory for gateway commands does not matter for the agent; use `/home/moose`.

## 3. Port and env precedence [TESTED, source-verified]

`hermes_cli/env_loader.py` loads the selected profile's `.env` with `override=True`, then deletes profile-managed keys that exist in the shell but not in the `.env`. **The profile `.env` wins over a shell `A2A_PORT`.** The commands below still state the port in the command line so each line documents itself; both sources agree for every worker. There is no `--port` flag on the A2A plugin.

## 4. Start the five Web workers (one terminal each, foreground) [TESTED command form; background variant was used in-session]

```bash
# Terminal 1 — Web Architect, port 9911, model deepseek-v4-pro:cloud
cd /home/moose && A2A_PORT=9911 hermes -p web_architect_agent gateway run

# Terminal 2 — Web Designer, port 9912, model minimax-m3.1-flash:cloud
cd /home/moose && A2A_PORT=9912 hermes -p web_designer_agent gateway run

# Terminal 3 — Web Developer, port 9913, model glm-5.3:cloud
cd /home/moose && A2A_PORT=9913 hermes -p web_developer_agent gateway run

# Terminal 4 — Web QA Lead, port 9914, model kimi-k2.7-code:cloud
cd /home/moose && A2A_PORT=9914 hermes -p web_qa_agent gateway run

# Terminal 5 — Web DevOps, port 9915, model glm-5.3-flash:cloud
cd /home/moose && A2A_PORT=9915 hermes -p web_devops_agent gateway run
```

If that profile's gateway is already running (for example the background instances left by this session), `gateway run` refuses with a lock message. Stop the live PID first (§7) or use `gateway run --replace`.

Original Architect (already running as pid 91664; only if down):
```bash
cd /home/moose && A2A_PORT=9901 hermes -p architect_agent gateway run
```

Background form actually used in this session (detached, survives the shell, not a reboot):
```bash
cd /home/moose && nohup hermes -p web_qa_agent gateway run > /tmp/web_qa_agent.gateway.out 2>&1 &
```

## 5. ADK backend and frontend launchers (as currently operated) [UNTESTED in this session; observed running]

```bash
# ADK api_server on 127.0.0.1:8000 — matches the live process (no start_server.sh, no Supabase URI)
cd /home/moose/python/stark-ai-workbench-adk-backend-v1 && .venv/bin/adk api_server

# Frontend (inherited v1 checkout) on port 3000
cd /home/moose/nextjs/stark-ai-workbench-nextjs-frontend-v1 && npm run dev
```
ADK reads `HERMES_A2A_TOKEN` from its repo-root `.env` at agent-load time; Next.js reads `ADK_BUNDLE_URL_V1=http://127.0.0.1:8000` from `.env.local`. **Integration still to do by Tony (untested):** five ADK folders `web_<role>_agent/{__init__.py,agent.py}` copied from `architect_agent/` with name, description and port changed, keeping `httpx.Timeout(120.0)` and `os.environ['HERMES_A2A_TOKEN']`; five entries appended to `config/agents.manifest.json` with bundle `v1` and the display names above (original backed up at `/home/moose/Downloads/WEB_WORKFORCE_POC_BACKUP_20261026_204503/`).

## 6. Checks

Port and card [TESTED]:
```bash
hermes profile list                                   # Gateway "running" for the five web_* profiles; Model column shows the assigned model
ss -ltnp | grep -E ':(9901|991[1-5])\b'               # one hermes listener per port, all 127.0.0.1
for p in 9911 9912 9913 9914 9915; do printf "$p: "; curl -s -m 3 http://127.0.0.1:$p/.well-known/agent-card.json | python3 -c 'import sys,json;print(json.load(sys.stdin)["name"])'; done
```
Expected names: Web Architect, Web Designer, Web Developer, Web QA Lead, Web DevOps.

Prompt composition (offline, confirms embedded documents are present and untruncated) [TESTED]:
```bash
hermes -p web_developer_agent prompt-size --platform a2a | grep -E 'breakdown|context \('   # context block ≈ 44–50 KB; no TRUNCATED/BLOCKED lines
```

Actual chat through A2A, no ADK or Bob required [TESTED]. Token read from the ADK `.env` without printing:
```bash
TOK=$(grep -E '^HERMES_A2A_TOKEN=' /home/moose/python/stark-ai-workbench-adk-backend-v1/.env | cut -d= -f2- | tr -d '"'"'"'')
curl -s -m 120 http://127.0.0.1:9914/ -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"message/send","params":{"message":{"role":"user","messageId":"m1","contextId":"ctx-check-'$(date +%s)'","parts":[{"kind":"text","text":"Hypothetical, no action: state your role name in one sentence."}]}}}' \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["result"]["status"]["state"])'
unset TOK
```
Expected `TASK_STATE_COMPLETED`; observed 11–33 s per first turn in this session, within Bob's 75 s run cap.

Effective model at runtime [TESTED]: the latest session row in the profile's `state.db` records the model used:
```bash
python3 -c "import sqlite3;print(sqlite3.connect('file:/home/moose/.hermes/profiles/web_qa_agent/state.db?mode=ro',uri=True).execute('select id,model from sessions order by id desc limit 1').fetchone())"
```

Through ADK / Bob [UNTESTED]: `curl -s http://127.0.0.1:8000/list-apps` should list the five names once Tony adds the folders; Bob's sidebar should show the five labels.

## 7. Stop / restart specific owned processes [TESTED]

```bash
python3 -c "import json;print(json.load(open('/home/moose/.hermes/profiles/web_qa_agent/gateway.pid'))['pid'])"   # the live PID for that profile
kill <pid>                                   # graceful stop of that one gateway only
ss -ltn | grep ':9914 '                      # wait until empty, then start again per §4
```
Never use `pkill hermes` or `killall`: it would also stop the original Architect (pid 91664). Live PIDs as of 2026-10-26 21:31: 1497715 (9911), 1497875 (9912), 1498035 (9913), 1498197 (9914), 1498367 (9915). Always re-read `gateway.pid`; do not reuse these numbers blindly.

## 8. Session storage behavior

- **Hermes [TESTED]:** each profile has its own `state.db`, `sessions/`, `a2a_conversations/`, `a2a_audit.jsonl`. One A2A `contextId` = one Hermes session; two contextIds to the same worker were separate conversations; a different worker had no knowledge of the first worker's marker. Memory (`memories/`) started empty for the five new workers and is theirs alone.
- **ADK [observed, not tested for isolation]:** with the current `adk api_server` launch (no `--session_service_uri`) sessions persist in `<agent>/.adk/session.db` per agent folder. How ADK derives the A2A contextId from its session id was not inspected.
- **Frontend v1 [UNTESTED]:** per-agent session creation and mapping to ADK sessions were not tested. Do not read this runbook as evidence of frontend isolation.

## 9. How startup documents are loaded (changed in v1.1)

Hermes injects exactly two files into the system prompt: `SOUL.md` (identity = the role's full INSTRUCTIONS) and the `.hermes.md` found in `terminal.cwd`. Nothing auto-loads a `context/` folder, and the original Architect never read its `context/` files on a first turn either (0 `read_file` calls on `workspace/context/` in nine sessions). The Web workers' `.hermes.md` therefore **embeds** the role playbook, the WBM playbook and the pack README as Documents A–C with source paths. Tony does not need to say "read your playbooks". If a document is edited, edit the source copy under `workspace/context/…` **and** the embedded copy in `.hermes.md` (or regenerate `.hermes.md`), then restart that one worker.

## 10. First-start side effect [TESTED]

On a profile's first gateway start Hermes downloads its `tirith` security helper into `<profile>/bin/` (SHA-256 verified only). Normal for this version.
