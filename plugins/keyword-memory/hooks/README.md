# keyword-memory hooks

Python hook scripts for the keyword-memory plugin. Each script reads a JSON request from stdin and writes a JSON response to stdout.

## Scripts

| Script | Hook | Description |
|--------|------|-------------|
| `ingest.py` | ingest | Receives `{"message": "..."}`, extracts keywords and named entities, returns them as memory fragments |

## Protocol

- **Input**: JSON object on stdin (fields vary by hook type)
- **Output**: JSON object on stdout (`ingest_result` with memories)
