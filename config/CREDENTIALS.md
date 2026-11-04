# Credentials — names, locations and how to restore (no values here, ever)

| Where (live machine) | Name | Used by | How the operator restores it |
|---|---|---|---|
| `~/.hermes/profiles/<id>/.env` (mode 600) | `OLLAMA_API_KEY` | all five | Ollama Cloud key from the Ollama account; type it into the restored `.env` locally |
| same | `A2A_PEER_TOKENS` = `adk:<token>` | all five | One shared bearer token. It must equal ADK's `HERMES_A2A_TOKEN` (verified equal on all five at capture). Generate a new random one on restore and set both sides. |
| same | `ANTHROPIC_API_KEY` | Designer only | Anthropic subscription/OAuth token; re-enter locally |
| `~/.hermes/profiles/<id>/auth.json` | `openai-codex` OAuth (refresh token) | Architect, Designer, Developer, QA | `hermes -p <id> auth add openai-codex --type oauth --no-browser` (device code, per profile). Never copy `auth.json` between profiles or machines; refresh tokens rotate. |
| same | `anthropic` credential pool | Designer | re-add through `hermes -p web_designer_agent auth` |
| `stark-ai-workbench-adk-backend-v1/.env` | `HERMES_A2A_TOKEN` | ADK → Hermes | same value as the profiles' `adk` token |
| same | `GOOGLE_APPLICATION_CREDENTIALS` → `credentials/cyberize-vertex-api.json` | ADK (Vertex) | Service-account JSON from Google Cloud; git-ignored in the ADK repo |
| same | `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_CLOUD_REGION`, `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_STT_BUCKET` | ADK | settings; copy from the ADK repo's `.env_example` and fill locally |
| `stark-ai-workbench-nextjs-frontend-v1/.env.local` | `SUPABASE_SECRET_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` | Bob | from the Supabase / Stripe dashboards |
| same | `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_PRICE_*`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_CHAT_MODE`, `ADK_BUNDLE_URL_V1`, `ADK_WRAPPER_URL` | Bob | settings/publishable; `ADK_BUNDLE_URL_V1=http://127.0.0.1:8000` |
| `~/.config/gcloud/` | gcloud login | Web DevOps deployments | `gcloud auth login` by the operator (browser); Google Cloud SDK 591.0.0 via snap at capture |
| Ollama service | `ollama signin` | cloud models | operator signs in on the new machine |

Per-profile settings (ports, timeouts, peer names) keep their values in `profiles/<id>/env.template`; only secrets are blank.
