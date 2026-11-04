#!/usr/bin/env bash
# Run the web_qa_agent gateway in THIS terminal on port 9914. Ctrl+C stops it.
set -euo pipefail
source "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/_web_agents_common.sh"
start_web_agent web_qa_agent 9914
