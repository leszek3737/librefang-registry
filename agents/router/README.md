# Router

Native deterministic router. Dispatches tasks to specialist agents without using an LLM.

## Configuration

| Field | Value |
|-------|-------|
| Module | `builtin:router` |
| Model | `default` |
| Provider | `default` |

This is a system-level agent. The `builtin:router` module performs deterministic routing and does not invoke an LLM.

## Skills

None configured.

## Usage

```bash
librefang agent run router
```
