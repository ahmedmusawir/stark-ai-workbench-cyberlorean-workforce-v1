#!/usr/bin/env bash
# Change a Hermes profile's model: asks which agent, then runs `hermes -p <agent> model`.
#   ~/.hermes/scripts/agent_model_change.sh                 # pick from a list
#   ~/.hermes/scripts/agent_model_change.sh web_devops_agent  # skip the question
set -euo pipefail

PROFILES_DIR="$HOME/.hermes/profiles"
mapfile -t profiles < <(find "$PROFILES_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)

agent="${1:-}"
if [ -z "$agent" ]; then
  echo "Agents:"
  for i in "${!profiles[@]}"; do printf '  %2d) %s\n' "$((i + 1))" "${profiles[$i]}"; done
  read -rp "Agent name or number: " agent
fi

# A number picks from the list
if [[ "$agent" =~ ^[0-9]+$ ]] && [ "$agent" -ge 1 ] && [ "$agent" -le "${#profiles[@]}" ]; then
  agent="${profiles[$((agent - 1))]}"
fi

if [ -z "$agent" ] || [ ! -d "$PROFILES_DIR/$agent" ]; then
  echo "No such agent: '${agent}'. Nothing changed." >&2
  exit 1
fi

echo "Running: hermes -p $agent model"
exec hermes -p "$agent" model
