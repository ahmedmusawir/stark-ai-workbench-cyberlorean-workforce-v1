#!/usr/bin/env bash
# Shared helper for the Web Cyberlorean start/stop scripts. Sourced, not run.
#
# Roster ("all" means ONLY these five):
#   web_architect_agent  9911
#   web_designer_agent   9912
#   web_developer_agent  9913
#   web_qa_agent         9914
#   web_devops_agent     9915

WEB_AGENT_PROFILES=(web_architect_agent web_designer_agent web_developer_agent web_qa_agent web_devops_agent)
WEB_AGENT_PORTS=(9911 9912 9913 9914 9915)

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
WORKDIR="/home/moose"

# Resolve the installed Hermes executable.
resolve_hermes() {
    local c
    for c in "$(command -v hermes 2>/dev/null || true)" \
             "$HOME/.local/bin/hermes" \
             "$HERMES_HOME/hermes-agent/hermes"; do
        if [ -n "$c" ] && [ -x "$c" ]; then
            printf '%s\n' "$c"
            return 0
        fi
    done
    echo "ERROR: hermes executable not found (looked in PATH, ~/.local/bin, ~/.hermes/hermes-agent)." >&2
    return 1
}

# On this Hermes version the profile .env A2A_PORT overrides the shell A2A_PORT.
# Verify the configured port matches the expected one. Prints only A2A_PORT, never other values.
check_profile_port() {
    local profile="$1" expected="$2"
    local envfile="$HERMES_HOME/profiles/$profile/.env"
    if [ ! -d "$HERMES_HOME/profiles/$profile" ]; then
        echo "ERROR: profile '$profile' not found under $HERMES_HOME/profiles" >&2
        return 1
    fi
    [ -f "$envfile" ] || return 0   # no .env: shell A2A_PORT applies
    local configured
    configured="$(grep -E '^[[:space:]]*(export[[:space:]]+)?A2A_PORT=' "$envfile" | tail -n1 \
                  | sed -E 's/^[[:space:]]*(export[[:space:]]+)?A2A_PORT=//; s/^"//; s/"$//; s/^'"'"'//; s/'"'"'$//; s/[[:space:]]*$//')"
    [ -n "$configured" ] || return 0  # not set in .env: shell A2A_PORT applies
    if [ "$configured" != "$expected" ]; then
        echo "ERROR: $profile has A2A_PORT=$configured configured in its profile .env, expected $expected." >&2
        echo "       Not starting and not changing any configuration. Fix the .env or the script first." >&2
        return 1
    fi
}

# Replace this process with the gateway in the foreground (preserves exit status and Ctrl+C).
start_web_agent() {
    local profile="$1" port="$2" hermes
    hermes="$(resolve_hermes)" || exit 1
    check_profile_port "$profile" "$port" || exit 1
    cd "$WORKDIR" || { echo "ERROR: cannot cd to $WORKDIR" >&2; exit 1; }
    echo ">>> Starting $profile on port $port (replaces any existing instance; Ctrl+C stops it)"
    exec env A2A_PORT="$port" "$hermes" -p "$profile" gateway run --replace
}

# Stop only the named profile. Already stopped is harmless (Hermes reports it and exits 0).
stop_web_agent() {
    local profile="$1" hermes
    hermes="$(resolve_hermes)" || return 1
    cd "$WORKDIR" || { echo "ERROR: cannot cd to $WORKDIR" >&2; return 1; }
    echo ">>> Stopping $profile"
    "$hermes" -p "$profile" gateway stop
}
