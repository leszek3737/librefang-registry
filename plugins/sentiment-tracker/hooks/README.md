# sentiment-tracker hooks

Python hook scripts for the sentiment-tracker plugin. Each script reads a JSON request from stdin and writes a JSON response to stdout.

## Scripts

| Script | Hook | Description |
|--------|------|-------------|
| `ingest.py` | ingest | Receives `{"message": "..."}`, analyzes sentiment, returns emotional context as a memory fragment |

## Protocol

- **Input**: JSON object on stdin (fields vary by hook type)
- **Output**: JSON object on stdout (`ingest_result` with memories, empty for neutral sentiment)
