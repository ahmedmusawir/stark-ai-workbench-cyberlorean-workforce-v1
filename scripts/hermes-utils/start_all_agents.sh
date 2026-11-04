#!/usr/bin/env bash
# Open five visible gnome-terminal windows, one per Web Cyberlorean, each running its start script.
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
source "$SCRIPT_DIR/_web_agents_common.sh"

if [ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
    echo "No graphical session detected (DISPLAY/WAYLAND_DISPLAY unset), so terminal windows cannot be opened." >&2
    echo "Run each worker in its own terminal instead:" >&2
    for p in "${WEB_AGENT_PROFILES[@]}"; do echo "    $SCRIPT_DIR/start_${p}.sh" >&2; done
    exit 1
fi
if ! command -v gnome-terminal >/dev/null 2>&1; then
    echo "gnome-terminal not found. Run each worker in its own terminal instead:" >&2
    for p in "${WEB_AGENT_PROFILES[@]}"; do echo "    $SCRIPT_DIR/start_${p}.sh" >&2; done
    exit 1
fi

fail=0
for i in "${!WEB_AGENT_PROFILES[@]}"; do
    p="${WEB_AGENT_PROFILES[$i]}"; port="${WEB_AGENT_PORTS[$i]}"
    script="$SCRIPT_DIR/start_${p}.sh"
    # The window stays open after the worker exits (or fails to start) so errors remain visible.
    if gnome-terminal --window --title="$p :$port" --working-directory="$WORKDIR" -- \
        bash -c '"$1"; rc=$?; echo; echo "[$2 exited with status $rc] Press Enter to close this window."; read -r; exit $rc' \
        _ "$script" "$p"; then
        echo "Opened terminal: $p (port $port)"
    else
        echo "ERROR: could not open terminal for $p" >&2; fail=1
    fi
done
exit $fail
