# echo-memory hooks

Python hook scripts for the echo-memory demo plugin. Each script reads a JSON request from stdin and writes a JSON response to stdout.

## Scripts

| Script | Hook | Description |
|--------|------|-------------|
| `ingest.py` | ingest | Receives `{"message": "..."}`, returns it wrapped as a memory fragment |
| `after_turn.py` | after_turn | Receives the conversation messages array, responds with `{"type": "ok"}` |

## Protocol

- **Input**: JSON object on stdin (fields vary by hook type)
- **Output**: JSON object on stdout (`ingest_result` with memories, or `ok`)
