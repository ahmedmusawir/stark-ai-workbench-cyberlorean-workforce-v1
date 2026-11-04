#!/usr/bin/env bash
# Stop ONLY the five Web Cyberloreans, one profile at a time. Continues on failure; nonzero exit if any stop failed.
set -uo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
source "$SCRIPT_DIR/_web_agents_common.sh"

declare -a results=()
fail=0
for p in "${WEB_AGENT_PROFILES[@]}"; do
    if out="$("$SCRIPT_DIR/stop_${p}.sh" 2>&1)"; then
        results+=("$(printf '  %-22s OK   %s' "$p" "$(printf '%s\n' "$out" | tail -n1)")")
    else
        fail=1
        results+=("$(printf '  %-22s FAIL %s' "$p" "$(printf '%s\n' "$out" | tail -n1)")")
    fi
done
echo "Stop summary:"
printf '%s\n' "${results[@]}"
exit $fail
