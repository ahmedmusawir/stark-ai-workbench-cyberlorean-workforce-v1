# Web Cyberlorean start/stop scripts

Simple Bash scripts for the five Web workers. No service framework, Docker or systemd.

| Profile              | Port |
|----------------------|------|
| web_architect_agent  | 9911 |
| web_designer_agent   | 9912 |
| web_developer_agent  | 9913 |
| web_qa_agent         | 9914 |
| web_devops_agent     | 9915 |

"All" means only these five. The original architect_agent, designer_agent and
devops_agent profiles are never touched.

## Start all / stop all

```bash
~/.hermes/scripts/start_all_agents.sh   # opens 5 titled gnome-terminal windows, one per worker
~/.hermes/scripts/stop_all_agents.sh    # stops only the 5 web workers, prints a per-worker summary
```

`start_all_agents.sh` needs a graphical session. If none is available it prints
the individual start commands instead of switching to background mode.
Each window stays open after the worker exits so startup errors remain visible.

## Individual start / stop

```bash
~/.hermes/scripts/start_web_architect_agent.sh   # runs in THIS terminal (foreground)
~/.hermes/scripts/stop_web_architect_agent.sh    # stops only this profile
```

Same pattern for `web_designer_agent`, `web_developer_agent`, `web_qa_agent`, `web_devops_agent`.

Under the hood a start script runs, from /home/moose:

```bash
A2A_PORT=9911 hermes -p web_architect_agent gateway run --replace
```

and a stop script runs `hermes -p <profile> gateway stop`.

## Behaviour notes

- **Start replaces** any existing running instance of that profile (`--replace`).
- **Ctrl+C** in a worker's terminal stops that worker.
- Before starting, the script checks that the profile's `.env` `A2A_PORT` matches the
  expected port (the profile `.env` overrides the shell value on this Hermes version).
  On a mismatch it reports the problem and exits without changing anything.
- Stopping an already-stopped worker is harmless (`No gateway running for this profile`).
- `stop_all_agents.sh` continues past a failed stop and exits nonzero only if a real stop failed.
- These scripts do **not** enable automatic startup after reboot. After a reboot,
  run `start_all_agents.sh` again.
- Check a worker is up: `curl -s http://127.0.0.1:9911/.well-known/agent-card.json`

## Verify the gateways after a restart

```bash
~/.hermes/scripts/verify_web_gateways_after_restart.sh            # all five
~/.hermes/scripts/verify_web_gateways_after_restart.sh developer  # one or more roles
```

Read-mostly health check for the shared A2A plugin changes (operator-console frame and
completed-reply persistence, 2026-11-01). For each worker it:

- checks whether the gateway process started after the last plugin edit (`PLUGIN_LOADED`);
- **skips any busy worker** (open connection on its port), so it never interrupts a task;
- sends ONE no-tool message ("READY <model>") through ADK (`127.0.0.1:8000`) in a **new**
  session under user `claudy-smoke`. It does not use the Workbench routes, which require a
  signed-in Supabase session;
- reads that worker's `agent.log` for the frame of the inbound message (`OPERATOR_FRAME`);
- reads the session back from ADK and counts stored completed replies (`COMPLETED_PERSISTED`).

Healthy row: `PLUGIN_LOADED yes`, `OPERATOR_FRAME operator-console`, `COMPLETED_PERSISTED 1 (want 1)`,
`READY <model>`. It never touches project files or existing sessions.

## Designer contest checks (2026-11-01)

```bash
~/.hermes/scripts/designer_contest_check.sh preflight 1   # before seat 1 (GLM) runs: must print RESULT: CLEAN
~/.hermes/scripts/designer_contest_check.sh audit 1       # after it finishes: flags any tool call that touched
                                                          # earlier design work, other entries or other profiles
```

Read-only. Seats 1–3 = GLM, Kimi K3, Astra (`designer_contest_{1_glm,3_kimi,4_astra}`; also accepts `glm|kimi|astra`). Terra and DeepSeek withdrawn 2026-11-01. Full procedure:
`~/Downloads/DESIGNER_CONTEST_2026-11-01.md`.

## Change an agent's model

```bash
~/.hermes/scripts/agent_model_change.sh                    # lists every profile, asks for a name or number
~/.hermes/scripts/agent_model_change.sh web_devops_agent   # skip the question
```

Runs `hermes -p <agent> model` (the interactive model picker). An unknown name exits without changing anything.
A model change applies on the agent's next turn; no gateway restart needed.
