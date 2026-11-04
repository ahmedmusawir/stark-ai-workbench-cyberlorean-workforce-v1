#!/usr/bin/env bash
# Verify the shared A2A plugin changes on the RUNNING web gateways (Claudy, 2026-11-01).
# Path exercised: ADK api_server (127.0.0.1:8000) -> A2A bearer 'adk' -> Hermes gateway -> model.
# The Next.js routes are not used: they now require a signed-in Supabase session.
# Each check sends ONE harmless no-tool message in a NEW ADK session under user 'claudy-smoke'.
# Usage: ~/.hermes/scripts/verify_web_gateways_after_restart.sh [architect designer developer qa devops]
set -u
ADK=http://127.0.0.1:8000
PLUGIN=$HOME/.hermes/hermes-agent/plugins/platforms/a2a/security.py
declare -A PORT=([architect]=9911 [designer]=9912 [developer]=9913 [qa]=9914 [devops]=9915)
ROLES=("$@"); [ ${#ROLES[@]} -eq 0 ] && ROLES=(architect designer developer qa devops)
plugin_mtime=$(stat -c %Y "$PLUGIN")
printf '%-10s %-8s %-14s %-9s %-16s %-22s %s\n' ROLE PID PLUGIN_LOADED IDLE OPERATOR_FRAME COMPLETED_PERSISTED REPLY
for r in "${ROLES[@]}"; do
  agent="web_${r}_agent"; port=${PORT[$r]}; log=$HOME/.hermes/profiles/$agent/logs/agent.log
  pid=$(ss -ltnp 2>/dev/null | grep ":$port " | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)
  if [ -z "$pid" ]; then printf '%-10s %s\n' "$r" "NOT LISTENING on :$port"; continue; fi
  started=$(stat -c %Y /proc/$pid)
  loaded=$([ "$started" -gt "$plugin_mtime" ] && echo yes || echo "NO(restart)")
  conns=$(ss -tn state established "( dport = :$port )" | tail -n +2 | wc -l)
  if [ "$conns" -ne 0 ]; then printf '%-10s %-8s %-14s %s\n' "$r" "$pid" "$loaded" "BUSY - skipped"; continue; fi
  sid="session-verify-$(date +%s%N)"
  curl -sS -m 15 -o /dev/null -X POST -H 'content-type: application/json' -d '{}' "$ADK/apps/$agent/users/claudy-smoke/sessions/$sid"
  body=$(python3 -I -c 'import json,sys; print(json.dumps({"app_name":sys.argv[1],"user_id":"claudy-smoke","session_id":sys.argv[2],"new_message":{"role":"user","parts":[{"text":"Gateway verification (Claudy). Reply with exactly one line: READY <your model name>. Do not use any tools."}]}}))' "$agent" "$sid")
  reply=$(curl -sS -m 300 -H 'content-type: application/json' -d "$body" "$ADK/run" | python3 -I -c '
import json,sys
ev=json.load(sys.stdin); out=""
for e in reversed(ev if isinstance(ev,list) else []):
    for p in ((e.get("content") or {}).get("parts") or []):
        if p.get("text"): out=p["text"]; break
    if out: break
print(out.replace("\n"," ")[:40] or "(no text)")')
  frame=$(grep "inbound message" "$log" | tail -1 | grep -q "operator-console" && echo operator-console || echo "OLD(untrusted)")
  persisted=$(curl -sS -m 15 "$ADK/apps/$agent/users/claudy-smoke/sessions/$sid" | python3 -I -c '
import json,sys
s=json.load(sys.stdin); n=0
for e in s.get("events",[]):
    if e.get("author")=="user" or e.get("partial"): continue
    if any(p.get("text") for p in ((e.get("content") or {}).get("parts") or [])): n+=1
print(f"{n} (want 1)")')
  printf '%-10s %-8s %-14s %-9s %-16s %-22s %s\n' "$r" "$pid" "$loaded" yes "$frame" "$persisted" "$reply"
done
