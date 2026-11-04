#!/usr/bin/env bash
# Run the web_designer_agent gateway in THIS terminal on port 9912. Ctrl+C stops it.
set -euo pipefail
source "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/_web_agents_common.sh"
start_web_agent web_designer_agent 9912
