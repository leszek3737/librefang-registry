# echo-memory

Simple demo plugin that echoes back the user message as a "recalled memory". Useful for verifying the plugin system works end-to-end.

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Echoes the user message back as a recalled memory fragment |
| after_turn | `hooks/after_turn.py` | Acknowledges each conversation turn (no-op demo) |

## Usage

Installed automatically when enabled in agent configuration.
