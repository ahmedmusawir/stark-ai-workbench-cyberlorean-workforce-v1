# Reporting the active runtime model and provider honestly

Scope: when an operator asks what model is serving the current session ("what is your brain
model", "check the brain model"), how to establish it from observed evidence and how to
report it without overclaiming.

## The question is asked repeatedly and changes mid-conversation

The operator may swap the active model between runs, and often does so *within* the same
chat. The expected answer therefore has three parts: the **current** model, whether it
**changed** from the previous answer, and whether a provider **response ID** was actually
exposed. "Current model X" alone under-reports.

## Where the evidence lives

`/home/moose/.hermes/profiles/<profile>/logs/agent.log` is authoritative for what actually
served the session. Each API call logs its identity:

```
2026-11-02 22:16:01,185 INFO [<session_id>] agent.conversation_loop: API call #5: model=minimax-m3:cloud provider=custom in=39199 out=250 total=39449 latency=4.0s cache=38538/39199 (98%)
```

- `model=` — the model slug sent to the provider, as the runtime resolved it.
- `provider=` — the provider id (`custom` for a named local/custom endpoint).
- The bracketed id is the **session id**; several can be interleaved, so filter by it when
  attributing a line to the current session.

Useful extractions:

```bash
# every distinct model seen in the log, with counts
grep -aoE 'model=[A-Za-z0-9._:/-]+' logs/agent.log | sort | uniq -c | sort -rn

# the most recent API-call line (current model)
grep -a 'API call #' logs/agent.log | tail -1

# model switches within one session, in order
grep -a 'API call #' logs/agent.log | sed -E 's/.*\[([^]]+)\].*model=([^ ]+) provider=([^ ]+).*/\1 \2 \3/' \
  | awk '{if ($1!=prev) {print; prev=$1}}'
```

`config.yaml` in the profile gives the *configured default*, which is not always the model
in flight:

```yaml
model:
  default: minimax-m3:cloud
  provider: custom:ollama-launch
providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
```

## Reporting shape

- **Current model + provider**, sourced from the latest `API call #` line, with the
  session id.
- **Change vs. the previous answer**, when the log shows a switch inside the same chat —
  give the short sequence (e.g. `deepseek-v4-pro:cloud` → `minimax-m3.1-flash:cloud` →
  `minimax-m3:cloud`) with times.
- **Configuration context** — `config.yaml` model block, so the operator can see the
  difference between "default" and "in flight".
- **Honest limit on response IDs.** A local OpenAI-compatible endpoint (Ollama's
  `/v1/chat/completions`) does not expose a provider response id. When none is surfaced,
  say so plainly: the model/provider label is observed from runtime logs, the response id
  is **not independently verified**. Do not invent one and do not imply the API echoed it.
- **Never** infer the serving model from a session-name, a channel label, a config default
  alone, or a previous session's notes.

## Why this matters beyond the question

Run records for independent explorations must distinguish the same three things:
observable runtime model/provider labels, independently verified provider response
identifiers, and effort/token/cost figures that were actually exposed. Where a figure is
not exposed, write "unavailable" rather than estimating it or making extra model calls to
manufacture it.
