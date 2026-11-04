#!/usr/bin/env bash
# Stop ONLY the web_qa_agent gateway (profile-scoped). Already stopped is harmless.
set -euo pipefail
source "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/_web_agents_common.sh"
stop_web_agent web_qa_agent
