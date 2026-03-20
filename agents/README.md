# Agents

Autonomous agent definitions for LibreFang. Each agent is a directory containing an `agent.toml` manifest.

## Structure

```
agents/
├── hello-world/agent.toml
├── researcher/agent.toml
├── coder/agent.toml
└── ...
```

## agent.toml Format

```toml
name = "agent-name"              # Must match directory name
version = "0.1.0"
description = "What this agent does"
author = "author-name"
module = "builtin:chat"          # Runtime module

[model]
provider = "default"
model = "default"
max_tokens = 4096
temperature = 0.7
system_prompt = """Behavioral instructions for the agent."""

[metadata.routing]
aliases = ["exact match phrases"]
weak_aliases = ["keyword hints"]

[resources]
max_llm_tokens_per_hour = 100000

[capabilities]
tools = ["web_search", "file_read"]
network = ["*"]
memory_read = ["*"]
memory_write = ["self.*"]
agent_spawn = false
```

## Current Agents (33)

| Agent | Description |
|-------|-------------|
| assistant | Default conversational assistant |
| researcher | Deep research with web search |
| coder | Code generation and editing |
| hello-world | Friendly greeting agent for new users |
| ... | See each directory for details |

## Adding a New Agent

1. Create `agents/<name>/agent.toml`
2. Ensure `name` matches the directory name
3. Run `python scripts/validate.py`
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.
