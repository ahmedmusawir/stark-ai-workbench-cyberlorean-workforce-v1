#!/usr/bin/env python3
"""Leak check for a safe export or a repo tree. Prints file + reason only, never a value.

1. Exact-value check: loads every secret VALUE from the live credential stores (profile .env and
   auth.json, ADK .env and service-account JSON, Bob .env.local, Hermes home .env) into memory
   and reports any file in TREE that contains one.
2. Pattern check: well-known token/key shapes and private-key blocks.
3. Inventory: e-mail addresses (reported for review, not a failure).
Exit 1 if (1) or (2) finds anything.
    python3 -I scan_for_secrets.py TREE
"""
import glob, json, os, re, sys

HOME = os.path.expanduser("~")
STORES_ENV = glob.glob(f"{HOME}/.hermes/profiles/web_*_agent/.env") + [
    f"{HOME}/.hermes/.env", f"{HOME}/python/stark-ai-workbench-adk-backend-v1/.env",
    f"{HOME}/nextjs/stark-ai-workbench-nextjs-frontend-v1/.env.local"]
STORES_JSON = glob.glob(f"{HOME}/.hermes/profiles/web_*_agent/auth.json") + [f"{HOME}/.hermes/auth.json"] + \
    glob.glob(f"{HOME}/python/stark-ai-workbench-adk-backend-v1/credentials/*.json")
# Values that are settings, not secrets (and too common to be useful as leak markers).
NOT_SECRET = re.compile(r"^(A2A_(AGENT_NAME|MAX_PINGPONG_TURNS|OPERATOR_PEERS|PORT|REPLY_TIMEOUT|TRUSTED_PEERS)|"
                        r"BROWSER\w*|\w+_DEBUG|TERMINAL_\w+|NEXT_PUBLIC_(SITE_URL|API_BASE_URL|CHAT_MODE)|"
                        r"GOOGLE_CLOUD_(LOCATION|REGION)|GOOGLE_GENAI_USE_VERTEXAI|GOOGLE_APPLICATION_CREDENTIALS|ADK_\w+_URL\w*|STRIPE_PRICE_\w+)$")
PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\b(sk-(ant|proj|live|test)?-?[A-Za-z0-9_\-]{20,})"), "sk- style API key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}"), "GitHub PAT"),
    (re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}"), "Google API key"),
    (re.compile(r"\bya29\.[0-9A-Za-z_\-]{20,}"), "Google OAuth token"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}"), "JWT"),
    (re.compile(r"\bxox[abpr]-[A-Za-z0-9\-]{20,}"), "Slack token"),
    (re.compile(r'"(refresh_token|access_token|id_token|private_key)"\s*:\s*"[^"]{8,}'), "credential JSON field"),
    (re.compile(r"(?i)\b[A-Z0-9_]*(API_KEY|TOKEN|SECRET|PASSWORD)S?=[^\s\"'#]{12,}"), "filled secret assignment"),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


def secret_values():
    vals = {}
    for p in STORES_ENV:
        if not os.path.exists(p):
            continue
        for line in open(p, errors="replace"):
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line.strip())
            if m and not NOT_SECRET.match(m.group(1)):
                v = m.group(2).strip().strip('"').strip("'")
                for part in re.split(r"[,\s]+", v):  # A2A_PEER_TOKENS is name:token,name:token
                    part = part.split(":", 1)[-1] if ":" in part and not part.startswith("http") else part
                    if len(part) >= 12:
                        vals[part] = f"{os.path.relpath(p, HOME)}:{m.group(1)}"
    def walk(o, src, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, src, f"{path}.{k}")
        elif isinstance(o, list):
            for v in o:
                walk(v, src, path)
        elif isinstance(o, str) and len(o) >= 16 and re.search(r"(token|key|secret|private|password)", path, re.I):
            vals[o] = f"{os.path.relpath(src, HOME)}:{path}"
    for p in STORES_JSON:
        try:
            walk(json.load(open(p)), p)
        except Exception:
            pass
    return vals


def main():
    tree = sys.argv[1]
    vals = secret_values()
    bad, emails = [], {}
    for root, dirs, files in os.walk(tree):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            p = os.path.join(root, f)
            if os.path.islink(p):
                continue
            data = open(p, "rb").read().decode("utf-8", "replace")
            rel = os.path.relpath(p, tree)
            for v, src in vals.items():
                if v in data:
                    bad.append(f"{rel}: contains the live value of {src}")
            for rx, why in PATTERNS:
                if rx.search(data):
                    bad.append(f"{rel}: {why}")
            for e in set(EMAIL.findall(data)):
                emails.setdefault(e, set()).add(rel)
    print(f"secret values loaded from live stores: {len(vals)}")
    print(f"files scanned under {tree}")
    for b in sorted(set(bad)):
        print("LEAK:", b)
    for e, fs in sorted(emails.items()):
        print(f"email: {e}  ({len(fs)} file(s): {', '.join(sorted(fs)[:3])})")
    print("RESULT:", "FAIL" if bad else "CLEAN")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
