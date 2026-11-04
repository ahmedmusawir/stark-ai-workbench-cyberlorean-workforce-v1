#!/usr/bin/env bash
# Designer contest isolation checks (Claudy, 2026-11-01). Seat 1 = GLM 5.3 Flash (Terra withdrawn 2026-11-01). Read-only: never sends a message,
# never edits a profile.
#   designer_contest_check.sh preflight <1|2|3|glm|kimi|astra>   before a run: clean memory, no learned
#                                                   skills, no sessions, correct model/port/pointer
#   designer_contest_check.sh audit <1|2|3|glm|kimi|astra>       after a run: every path the contestant's tool
#                                                   calls touched outside its inputs/own entry
set -u
MODE=${1:-}; N=${2:-}
# Lineup (revised 2026-11-01): 1 = GLM 5.3 Flash, 2 = Kimi K3, 3 = Astra 6. Seats may also be given by name.
# Withdrawn, kept for the record: designer_contest_1_terra, designer_contest_2_deepseek (no image input).
declare -A NAME=([1]=designer_contest_1_glm [2]=designer_contest_3_kimi [3]=designer_contest_4_astra [glm]=designer_contest_1_glm [kimi]=designer_contest_3_kimi [astra]=designer_contest_4_astra)
declare -A ENTRY=([1]=1-glm [2]=3-kimi [3]=4-astra [glm]=1-glm [kimi]=3-kimi [astra]=4-astra)
[ -z "$MODE" ] || [ -z "${NAME[$N]:-}" ] && { echo "usage: $0 preflight|audit 1|2|3  (or glm|kimi|astra)"; exit 2; }
P=$HOME/.hermes/profiles/${NAME[$N]}; C=$HOME/web-factory/contests/designer-2026-11-01
python3 -I - "$MODE" "$P" "$C" "${ENTRY[$N]}" <<'PY'
import sys, os, re, json, sqlite3, yaml
mode, P, C, entry = sys.argv[1:]
ok = True
def row(label, good, detail=""):
    global ok; ok &= good
    print(f"{'PASS' if good else 'FAIL'}  {label}" + (f"  — {detail}" if detail else ""))
db = os.path.join(P, "state.db")
def con(): return sqlite3.connect(f"file:{db}?mode=ro", uri=True)
if mode == "preflight":
    mem = [f for f in os.listdir(os.path.join(P, "memories")) if f.endswith(".md") and os.path.getsize(os.path.join(P, "memories", f)) > 0]
    row("memory empty", not mem, ", ".join(mem))
    man = {l.split(":")[0] for l in open(os.path.join(P, "skills", ".bundled_manifest")) if ":" in l}
    found = set()
    for root, dirs, files in os.walk(os.path.join(P, "skills")):
        if "SKILL.md" in files: found.add(os.path.basename(root))
    # Approved contest skill: Anthropic frontend-design @ anthropics/skills ca45fc496a3436251f191354091d557da31c15b5
    approved = {"frontend-design": {"SKILL.md": "d91970639e9f5c37682ac7ab60094d35f1c7c1f38d731bd56396563aee10c1d3",
                                    "LICENSE.txt": "0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594"}}
    extra = sorted(found - man - set(approved))
    row("no learned skills (only bundled + approved)", not extra, ", ".join(extra))
    import hashlib
    for name, want in approved.items():
        d = os.path.join(P, "skills", "creative", name)
        have = {f: hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest() for f in (os.listdir(d) if os.path.isdir(d) else [])}
        row(f"{name} pinned files exact (SKILL.md + LICENSE.txt)", have == want, "" if have == want else f"found {sorted(have)}")
    n = con().execute("select count(*) from sessions").fetchone()[0] if os.path.exists(db) else 0
    row("no prior sessions", n == 0, f"{n} sessions")
    cfg = yaml.safe_load(open(os.path.join(P, "config.yaml")))
    print(f"INFO  model {cfg['model'].get('default')} via {cfg['model'].get('provider')} · cwd {cfg['terminal'].get('cwd')}")
    row("terminal cwd is own workspace", cfg["terminal"].get("cwd") == os.path.join(P, "workspace"))
    env = dict(l.strip().split("=", 1) for l in open(os.path.join(P, ".env")) if re.match(r"^A2A_(PORT|AGENT_NAME|TRUSTED_PEERS|OPERATOR_PEERS|REPLY_TIMEOUT)=", l))
    row("A2A port 9916 / operator peer adk", env.get("A2A_PORT") == "9916" and env.get("A2A_OPERATOR_PEERS") == "adk", str(env))
    hm = open(os.path.join(P, "workspace", ".hermes.md")).read()
    row("workspace pointer names own entry", f"{C}/entries/{entry}/" in hm and "web_designer_agent/workspace" not in hm)
    if cfg["model"].get("provider") == "openai-codex":
        row("Codex login present for this profile", os.path.exists(os.path.join(P, "auth.json")), "run: hermes -p %s auth add openai-codex --type oauth --no-browser" % os.path.basename(P))
    out = os.listdir(os.path.join(C, "entries", entry))
    row("entry folder empty", not out, f"{len(out)} items")
else:
    if not os.path.exists(db): print("no sessions yet"); sys.exit(0)
    allowed = (os.path.join(C, "inputs"), os.path.join(C, "entries", entry), P, "/tmp", "/usr", "/bin", "/proc", "/dev")
    pat = re.compile(r"(/home/moose/[^\s'\"`;|&)<>,\]]+|~/[^\s'\"`;|&)<>,\]]+)")
    hits = {}
    for sid, tc in con().execute("select session_id, tool_calls from messages where tool_calls is not null and tool_calls != ''"):
        for m in pat.findall(tc.replace("\\/", "/")):
            p = m.replace("~/", "/home/moose/", 1).rstrip(".\\")
            if not p.startswith(allowed): hits.setdefault(p, set()).add(sid)
    sessions = con().execute("select id, model, message_count, tool_call_count from sessions").fetchall()
    for s in sessions: print(f"INFO  session {s[0]} model={s[1]} messages={s[2]} tool_calls={s[3]}")
    bad = {p: s for p, s in hits.items() if "/web-factory/" in p or "/.hermes/profiles/" in p or "/Downloads" in p}
    row("no tool call touched earlier design work, other entries or other profiles", not bad)
    for p in sorted(bad): print(f"      {p}")
    other = sorted(set(hits) - set(bad))
    if other: print("INFO  other paths outside inputs/entry (review):"); [print("      " + p) for p in other[:40]]
print("RESULT:", "CLEAN" if ok else "ATTENTION")
PY
