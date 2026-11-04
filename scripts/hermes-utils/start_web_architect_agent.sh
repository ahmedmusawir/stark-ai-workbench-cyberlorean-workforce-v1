#!/usr/bin/env bash
# Run the web_architect_agent gateway in THIS terminal on port 9911. Ctrl+C stops it.
set -euo pipefail
source "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/_web_agents_common.sh"
start_web_agent web_architect_agent 9911
