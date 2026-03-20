# Skills

Reusable skill definitions for LibreFang agents. Skills are either prompt templates or code scripts that agents can invoke to perform specific tasks.

## Structure

```
skills/
├── custom-skill-prompt/
│   └── skill.toml           # Prompt-only skill
└── custom-skill-python/
    ├── skill.toml            # Skill manifest
    └── main.py               # Python implementation
```

## Skill Types

### Prompt-Only

No code needed -- pure prompt engineering:

```toml
[skill]
name = "meeting-agenda"
version = "0.1.0"
description = "Generate a structured meeting agenda"
tags = ["meeting", "productivity"]

[runtime]
type = "promptonly"

[input]
topic = { type = "string", description = "The meeting topic", required = true }
duration_minutes = { type = "string", description = "Duration in minutes", required = true }

[prompt]
template = """
Create a meeting agenda for:
Topic: {{topic}}
Duration: {{duration_minutes}} minutes
"""
```

### Python

Custom logic with a Python entry point:

```toml
[skill]
name = "my-skill"
version = "0.1.0"
description = "Skill with custom logic"

[runtime]
type = "python"
entry = "main.py"

[input]
data = { type = "string", description = "Input data", required = true }
```

### Other Runtimes

Also supported: `node`, `shell`.

## Testing Skills Locally

```bash
librefang skill test ./skills/custom-skill-prompt \
  --input '{"topic": "Q1 planning", "duration_minutes": "30"}'
```

## Adding a New Skill

1. Create `skills/<name>/skill.toml`
2. Add implementation files if not `promptonly`
3. Run `python scripts/validate.py`
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.
