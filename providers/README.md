# Providers

LLM provider and model metadata for LibreFang. Each provider file defines the provider's API configuration and all available models with pricing, context windows, and capability flags.

## Structure

```
providers/
├── anthropic.toml
├── openai.toml
├── groq.toml
└── ...           (46 providers, 220+ models)
```

## Provider TOML Format

```toml
[provider]
id = "provider-id"                # Unique identifier (lowercase, hyphenated)
display_name = "Provider Name"
api_key_env = "PROVIDER_API_KEY"  # Env var for API key
base_url = "https://api.example.com"
key_required = true

[[models]]
id = "model-id"                   # Exact API model ID
display_name = "Model Name"
tier = "smart"                    # frontier | smart | balanced | fast | local
context_window = 128000
max_output_tokens = 16384
input_cost_per_m = 2.50           # USD per million input tokens
output_cost_per_m = 10.0          # USD per million output tokens
supports_tools = true
supports_vision = false
supports_streaming = true
aliases = ["short-name"]
```

## Tier Definitions

| Tier | Description | Examples |
|------|-------------|----------|
| `frontier` | Most capable, cutting-edge | Claude Opus, GPT-4.1 |
| `smart` | Smart, cost-effective | Claude Sonnet, Gemini 2.5 Flash |
| `balanced` | Balanced speed/cost | GPT-4.1 Mini, Llama 3.3 70B |
| `fast` | Fastest, cheapest | GPT-4o Mini, Claude Haiku |
| `local` | Local models, zero cost | Ollama, vLLM, LM Studio |

## Validation

```bash
python scripts/validate.py
```

Checks: required fields, valid tiers, non-negative costs, no duplicate model IDs.

## Adding or Updating a Model

1. Edit or create the provider file in `providers/`
2. Use exact API model IDs and verify pricing from official sources
3. Run `python scripts/validate.py`
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide and pricing source links.
