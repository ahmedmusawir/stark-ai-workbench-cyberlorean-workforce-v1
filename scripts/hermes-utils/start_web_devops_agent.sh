#!/usr/bin/env bash
# Run the web_devops_agent gateway in THIS terminal on port 9915. Ctrl+C stops it.
set -euo pipefail
source "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/_web_agents_common.sh"
start_web_agent web_devops_agent 9915
