#!/usr/bin/env python3
"""Capture a SAFE (no secrets, no sessions) export of the five Web Factory Hermes roles.

Read-only against live files. Writes only to a NEW output directory (refuses to reuse one).
Run with the Hermes venv python (needs PyYAML):
    ~/.hermes/hermes-agent/venv/bin/python -I capture_safe_export.py [--out DIR]
"""
import argparse, datetime, hashlib, json, os, re, shutil, stat, subprocess, sys

import yaml

HOME = os.path.expanduser("~")
HERMES = os.path.join(HOME, ".hermes")
HERMES_SRC = os.path.join(HERMES, "hermes-agent")
PROFILES = os.path.join(HERMES, "profiles")
ADK = os.path.join(HOME, "python/stark-ai-workbench-adk-backend-v1")
BOB = os.path.join(HOME, "nextjs/stark-ai-workbench-nextjs-frontend-v1")

ROLES = [  # role, profile id, ADK app name (ports are read live from each profile .env)
    ("Web Architect", "web_architect_agent"),
    ("Web Designer", "web_designer_agent"),
    ("Web Developer", "web_developer_agent"),
    ("Web QA Lead", "web_qa_agent"),
    ("Web DevOps", "web_devops_agent"),
]
STARTER = "workspace/context/WEB_FACTORY_STARTER_v1_1"

# .env names whose VALUES are non-secret settings and may be kept in templates.
ENV_KEEP = {
    "A2A_AGENT_NAME", "A2A_MAX_PINGPONG_TURNS", "A2A_OPERATOR_PEERS", "A2A_PORT",
    "A2A_REPLY_TIMEOUT", "A2A_TRUSTED_PEERS", "BROWSERBASE_ADVANCED_STEALTH",
    "BROWSERBASE_PROXIES", "BROWSER_INACTIVITY_TIMEOUT", "BROWSER_SESSION_TIMEOUT",
    "IMAGE_TOOLS_DEBUG", "MOA_TOOLS_DEBUG", "VISION_TOOLS_DEBUG", "WEB_TOOLS_DEBUG",
    "TERMINAL_LIFETIME_SECONDS", "TERMINAL_MODAL_IMAGE", "TERMINAL_TIMEOUT",
}
SECRET_KEY = re.compile(r"(api[_-]?key|token|secret|password|passwd|bearer|cookie|credential|private[_-]?key)", re.I)
TOKENISH = re.compile(r"^(sk-|ghp_|gho_|github_pat_|xox|AIza|ya29\.|eyJ|-----BEGIN)|^[A-Za-z0-9_\-]{40,}$")

manifest = []  # rows: relpath, size, mode, sha256, source, restore_target, kind


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo, *args):
    """Read-only git query."""
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True).stdout.strip()


def record(out, rel, source, target, kind):
    p = os.path.join(out, rel)
    st = os.stat(p)
    manifest.append((rel, st.st_size, oct(stat.S_IMODE(st.st_mode)), sha(p), source, target, kind))


def copy_file(out, src, rel, target, kind="copied"):
    dst = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)  # keeps mode + mtime
    record(out, rel, src, target, kind)


def copy_tree(out, src_dir, rel_dir, target_dir, skip=lambda n: False):
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not skip(d))
        for f in sorted(files):
            if skip(f) or f.endswith(".pyc"):
                continue
            s = os.path.join(root, f)
            if os.path.islink(s):
                raise SystemExit(f"symlink in curated tree, classify it first: {s}")
            r = os.path.relpath(s, src_dir)
            copy_file(out, s, os.path.join(rel_dir, r), os.path.join(target_dir, r))


def write(out, rel, text, target, kind, mode=0o644):
    dst = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as f:
        f.write(text)
    os.chmod(dst, mode)
    record(out, rel, "(generated)", target, kind)


def walk_yaml(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk_yaml(v, f"{p}.{k}" if p else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_yaml(v, f"{p}[{i}]")
    else:
        yield p, o


def config_template(path):
    text = open(path).read()
    for keypath, v in walk_yaml(yaml.safe_load(text)):
        leaf = keypath.split(".")[-1]
        if isinstance(v, str) and v and (SECRET_KEY.search(leaf) and not leaf.endswith("_tokens") or TOKENISH.search(v)):
            raise SystemExit(f"config value at {keypath} in {path} looks secret; refusing to template it")
    header = (
        "# SAFE TEMPLATE captured from the live profile config.yaml (no secrets found by the capture gate).\n"
        "# Credentials live in the profile .env / auth.json, never here. Paths are the capture machine's\n"
        f"# ({HOME}); remap them when restoring under a different HOME.\n"
    )
    return header + text


def env_template(path):
    names, lines = [], []
    for line in open(path):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line.rstrip("\n"))
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip().strip('"').strip("'")
        if k in ENV_KEEP and not TOKENISH.search(v) and not SECRET_KEY.search(k):
            lines.append(f"{k}={v}")
            names.append((k, "setting"))
        else:
            lines.append(f"{k}=")
            names.append((k, "SECRET - enter locally"))
    body = "# Profile .env template: settings keep their captured values; secrets are blank.\n" \
           "# Restore as <profile>/.env with mode 600. Never commit the filled-in file.\n" + "\n".join(lines) + "\n"
    return body, names


def main():
    ap = argparse.ArgumentParser()
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    ap.add_argument("--out", default=os.path.join(HOME, "web-factory/preservation", f"workforce-safe-export-{ts}"))
    out = ap.parse_args().out
    if os.path.exists(out):
        raise SystemExit(f"{out} already exists; exports are additive, choose a new --out")
    os.makedirs(out)

    roles, env_names = [], {}
    starter_seen = set()
    for role, pid in ROLES:
        pdir = os.path.join(PROFILES, pid)
        tgt = f"~/.hermes/profiles/{pid}"
        rel = f"profiles/{pid}"
        for f in ("SOUL.md", "profile.yaml", "workspace/.hermes.md"):
            copy_file(out, os.path.join(pdir, f), f"{rel}/{f}", f"{tgt}/{f}")
        if os.path.isdir(os.path.join(pdir, "scripts")):
            copy_tree(out, os.path.join(pdir, "scripts"), f"{rel}/scripts", f"{tgt}/scripts")
        write(out, f"{rel}/config.template.yaml", config_template(os.path.join(pdir, "config.yaml")),
              f"{tgt}/config.yaml", "sanitized-template", 0o600)
        body, names = env_template(os.path.join(pdir, ".env"))
        write(out, f"{rel}/env.template", body, f"{tgt}/.env (mode 600)", "sanitized-template", 0o600)
        env_names[pid] = names

        # Custom skills = anything not byte-identical to an upstream bundled/optional skill.
        upstream = {}
        for base in ("skills", "optional-skills"):
            for r, d, fs in os.walk(os.path.join(HERMES_SRC, base)):
                if "SKILL.md" in fs:
                    upstream.setdefault(os.path.basename(r), []).append(r)
        sdir = os.path.join(pdir, "skills")
        upstream_skills, custom = [], []
        for r, d, fs in os.walk(sdir):
            d[:] = [x for x in d if not x.startswith(".")]
            if "SKILL.md" not in fs:
                continue
            srel = os.path.relpath(r, sdir)
            tree = lambda p: {os.path.relpath(os.path.join(a, f), p): sha(os.path.join(a, f))
                              for a, _, ff in os.walk(p) for f in ff
                              if not f.startswith(".usage") and not f.endswith(".pyc") and "__pycache__" not in a}
            mine = tree(r)
            match = next((c for c in upstream.get(os.path.basename(r), []) if tree(c) == mine), None)
            if match:
                upstream_skills.append({"skill": srel, "upstream": os.path.relpath(match, HERMES_SRC)})
            else:
                custom.append(srel)
                copy_tree(out, r, f"{rel}/skills/{srel}", f"{tgt}/skills/{srel}")

        # Starter pack: one shared copy; the mapping says which parts each profile receives.
        ctx = os.path.join(pdir, STARTER)
        parts = []
        for r, d, fs in os.walk(ctx):
            for f in fs:
                s = os.path.join(r, f)
                srel = os.path.relpath(s, ctx)
                parts.append(srel)
                dst_rel = f"shared/WEB_FACTORY_STARTER_v1_1/{srel}"
                if srel in starter_seen:
                    if sha(s) != sha(os.path.join(out, dst_rel)):
                        raise SystemExit(f"starter file differs between profiles: {srel}")
                    continue
                starter_seen.add(srel)
                copy_file(out, s, dst_rel, f"~/.hermes/profiles/<profile>/{STARTER}/{srel}")

        cfg = yaml.safe_load(open(os.path.join(pdir, "config.yaml")))
        port = next((l.split("=", 1)[1].strip() for l in open(os.path.join(pdir, ".env")) if l.startswith("A2A_PORT=")), None)
        roles.append({
            "role": role, "profile_id": pid, "profile_dir": tgt, "port": port,
            "model": (cfg.get("model") or {}).get("default"), "provider": (cfg.get("model") or {}).get("provider"),
            "workspace": (cfg.get("terminal") or {}).get("cwd"),
            "instruction_entry": [f"{tgt}/SOUL.md", f"{tgt}/workspace/.hermes.md"],
            "starter_parts": sorted(parts), "custom_skills": custom,
            "upstream_skills": sorted(upstream_skills, key=lambda x: x["skill"]),
            "launcher": f"A2A_PORT={port} hermes -p {pid} gateway run --replace  (via ~/.hermes/scripts/start_{pid}.sh)",
            "adk_app": f"{ADK}/{pid}/agent.py",
            "adk_agent_sha256": sha(os.path.join(ADK, pid, "agent.py")),
        })

    # Shared Hermes utility scripts (modes preserved).
    copy_tree(out, os.path.join(HERMES, "scripts"), "scripts/hermes-utils", "~/.hermes/scripts")
    copy_file(out, os.path.join(HOME, ".local/bin/hermes"), "scripts/bin/hermes", "~/.local/bin/hermes",
              "copied (installer-generated wrapper)")

    # Local Hermes modification as a bounded patch against its upstream base commit.
    base = git(HERMES_SRC, "rev-parse", "HEAD")
    write(out, "hermes-patches/a2a-operator-console-and-lastchunk.patch",
          subprocess.run(["git", "-C", HERMES_SRC, "diff", "HEAD"], capture_output=True, text=True).stdout,
          f"apply in {HERMES_SRC} at {base}", "patch")
    patched = git(HERMES_SRC, "diff", "--name-only", "HEAD").split()

    # Bob (frontend) web-agent wiring snapshot: reference only; the frontend repo is authoritative once committed.
    mf = json.load(open(os.path.join(BOB, "config/agents.manifest.json")))
    def find_web(o):
        if isinstance(o, dict):
            if str(o.get("name", "")).startswith("web_"):
                yield o
            for v in o.values():
                yield from find_web(v)
        elif isinstance(o, list):
            for v in o:
                yield from find_web(v)
    write(out, "bridge/bob/agents.manifest.web-entries.snapshot.json",
          json.dumps(list(find_web(mf)), indent=2) + "\n", f"{BOB}/config/agents.manifest.json (reference)", "snapshot")

    # Historical runbooks that built this fleet.
    for f in ("WEB_WORKFORCE_POC_STARTUP_RUNBOOK_v1_1.md", "WEB_WORKFORCE_POC_STARTUP_RUNBOOK_v1_0.md"):
        src = os.path.join(HOME, "Downloads/ARCHIVE_OLD", f)
        if os.path.exists(src):
            copy_file(out, src, f"runbooks/historical/{f}", "(reference only)")

    def env_names_of(path):
        return sorted({l.split("=", 1)[0] for l in open(path) if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", l)}) if os.path.exists(path) else []

    versions = {
        "captured_at_local": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "host": " ".join(os.uname()[i] for i in (0, 2, 4)), "user": os.environ.get("USER"), "home": HOME,
        "hermes": {
            "version": subprocess.run(["hermes", "--version"], capture_output=True, text=True).stdout.splitlines()[0],
            "install_dir": HERMES_SRC, "install_method": "git", "remote": git(HERMES_SRC, "remote", "get-url", "origin"),
            "base_commit": base, "local_patch_files": patched,
            "python": subprocess.run([os.path.join(HERMES_SRC, "venv/bin/python"), "--version"], capture_output=True, text=True).stdout.strip(),
            "tirith": subprocess.run([os.path.join(PROFILES, "web_devops_agent/bin/tirith"), "--version"], capture_output=True, text=True).stdout.strip(),
        },
        "adk_backend": {"path": ADK, "remote": git(ADK, "remote", "get-url", "origin"), "commit": git(ADK, "rev-parse", "HEAD"),
                        "dirty": git(ADK, "status", "--short").splitlines(), "env_names": env_names_of(os.path.join(ADK, ".env"))},
        "bob_frontend": {"path": BOB, "remote": git(BOB, "remote", "get-url", "origin"), "commit": git(BOB, "rev-parse", "HEAD"),
                         "dirty_count": len(git(BOB, "status", "--short").splitlines()),
                         "env_names": env_names_of(os.path.join(BOB, ".env.local"))},
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "ollama": subprocess.run(["ollama", "--version"], capture_output=True, text=True).stdout.strip().splitlines()[-1],
    }
    write(out, "manifests/versions.json", json.dumps(versions, indent=2) + "\n", "(record)", "record")
    write(out, "manifests/roles.json", json.dumps(roles, indent=2) + "\n", "(record)", "record")
    write(out, "manifests/env-variable-names.json", json.dumps(env_names, indent=2) + "\n", "(record)", "record")

    # Checksums last, over everything above.
    rows = sorted(manifest)
    write(out, "manifests/manifest.tsv",
          "relpath\tsize\tmode\tsha256\tsource\trestore_target\tkind\n" + "".join("\t".join(map(str, r)) + "\n" for r in rows),
          "(record)", "record")
    with open(os.path.join(out, "SHA256SUMS"), "w") as f:
        for r in sorted(manifest):
            f.write(f"{r[3]}  {r[0]}\n")
    print(f"export: {out}\nfiles: {len(manifest)}")


if __name__ == "__main__":
    main()
