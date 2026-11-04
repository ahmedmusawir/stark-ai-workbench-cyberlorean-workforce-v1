# Role map (captured 2026-11-04 17:32 Asia/Dhaka; machine-readable: `manifests/roles.json`)

| Role | Profile ID | A2A port | Provider / model at capture | ADK app (`stark-ai-workbench-adk-backend-v1/`) | Custom skill |
|---|---|---|---|---|---|
| Web Architect | `web_architect_agent` | 9911 | openai-codex / gpt-6-astra | `web_architect_agent/agent.py` | `web-factory/wbm-assembly` |
| Web Designer | `web_designer_agent` | 9912 | custom:ollama-launch / minimax-m3:cloud | `web_designer_agent/agent.py` | `software-development/html-prototype-render-qa` |
| Web Developer | `web_developer_agent` | 9913 | openai-codex / gpt-6.1-terra | `web_developer_agent/agent.py` | `software-development/wbm-engineering` |
| Web QA Lead | `web_qa_agent` | 9914 | openai-codex / gpt-6.1-sol | `web_qa_agent/agent.py` | `software-development/web-factory-qa-lead` |
| Web DevOps | `web_devops_agent` | 9915 | custom:ollama-launch / glm-5.3:cloud | `web_devops_agent/agent.py` | `software-development/cloud-deploy-prep` |

Models are the operator's current choice, not part of the role identity; change with
`scripts/hermes-utils/agent_model_change.sh`. Designer models must accept image input.

Common to all five:
- Profile dir `~/.hermes/profiles/<id>/`; agent working dir (`terminal.cwd`) `~/.hermes/profiles/<id>/workspace`.
- Instruction entry: `SOUL.md` + `workspace/.hermes.md` → `workspace/context/WEB_FACTORY_STARTER_v1_1/` (README, CONSTITUTION, own role folder).
- 82 upstream Hermes skills byte-identical to the pinned install (QA has 83: + optional `dogfood/adversarial-ux-test`). They are listed per profile in `roles.json` and come back from the Hermes install, not from this repo.
- Launcher: `A2A_PORT=<port> hermes -p <id> gateway run --replace` in a foreground terminal (`scripts/hermes-utils/start_<id>.sh`). No systemd/cron units exist for Hermes or ADK; `ollama.service` is the only system service involved.
- `agent.max_turns: 150`; `A2A_REPLY_TIMEOUT=3600`; `A2A_TRUSTED_PEERS=adk`; `A2A_OPERATOR_PEERS=adk`.
- The project context file `~/web-factory/projects/cyberize-poc/PROJECT_GUIDE.md` is referenced by the instructions but is project data, kept outside this repo.

Chain: Bob (Next.js, `:3000`, `ADK_BUNDLE_URL_V1`) → ADK `api_server` (`127.0.0.1:8000`, RemoteA2aAgent per role, bearer `HERMES_A2A_TOKEN`)
→ Hermes A2A gateway (`127.0.0.1:991x`, peer `adk` in `A2A_PEER_TOKENS`) → model provider (Ollama `127.0.0.1:11434` or OpenAI Codex OAuth).
