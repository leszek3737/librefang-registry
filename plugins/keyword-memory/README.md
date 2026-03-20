# keyword-memory

Extracts keywords and named entities from user messages and returns them as contextual memories. Gives agents awareness of conversation topics without requiring external NLP libraries.

## Extraction Techniques

- **Plain keywords**: Splits words, filters English stopwords (~50 words), removes short tokens
- **Capitalized phrases**: Detects multi-word proper nouns and mid-sentence capitalized words
- **Emails and URLs**: Regex pattern matching
- **Numbers with units**: e.g. 500ms, 10GB, 3.5GHz
- **Dates**: YYYY-MM-DD, MM/DD/YYYY, DD.MM.YYYY formats
- **Technical terms**: camelCase, snake_case, dotted identifiers (e.g. `os.path`)

Results are deduplicated and capped at 10 keywords.

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Extracts keywords from the user message and returns them as a memory fragment |

## Example Output

```json
{"type": "ingest_result", "memories": [{"content": "[keyword-memory] Key topics: GPT-4, machine_learning, data pipeline, https://example.com"}]}
```

If no meaningful keywords are found, returns an empty memories list.

## Usage

Installed automatically when enabled in agent configuration. No external dependencies required (stdlib only).
