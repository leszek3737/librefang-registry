# Hands

Hand definitions for LibreFang. Hands are the user-facing "apps" -- higher-level application bundles that package an agent with tools, settings, dashboard metrics, and dependency requirements.

> "You have many hands helping you." -- Hands are how LibreFang users interact with specialized capabilities.

## Structure

```
hands/
├── browser/
│   ├── HAND.toml    # Hand definition
│   └── SKILL.md     # Documentation
├── trader/
│   ├── HAND.toml
│   └── SKILL.md
└── ...
```

## HAND.toml Format

```toml
id = "hand-id"                   # Must match directory name
name = "Hand Name"
description = "What this hand does"
category = "productivity"         # communication | content | data | development |
                                  # devops | finance | productivity | research | social
icon = "🔧"
tools = ["tool1", "tool2"]

[routing]
aliases = ["activate phrases"]
weak_aliases = ["keyword hints"]

[[requires]]                      # External dependencies
key = "python3"
requirement_type = "binary"
check_value = "python3"

[[settings]]                      # User-configurable options
key = "headless"
setting_type = "toggle"
default = "true"

[agent]                           # The agent powering this hand
name = "hand-agent"
module = "builtin:chat"
system_prompt = """..."""

[dashboard]                       # Dashboard metrics
[[dashboard.metrics]]
label = "Tasks Completed"
memory_key = "metric_key"
format = "number"
```

## Current Hands (14)

| Hand | Category | Description |
|------|----------|-------------|
| browser | productivity | Autonomous web browser |
| trader | data | Crypto/stock trading assistant |
| researcher | productivity | Deep research automation |
| analytics | data | Data analysis and dashboards |
| ... | | See each directory for details |

## Adding a New Hand

1. Create `hands/<name>/HAND.toml` (and optionally `SKILL.md`)
2. Ensure `id` matches the directory name
3. Run `python scripts/validate.py`
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.
