# sentiment-tracker

Analyzes user message sentiment using keyword-based scoring and injects emotional context so agents can respond with appropriate tone. No external ML libraries required (stdlib only).

## Scoring Method

- **Positive words** (~30): great, love, excellent, awesome, helpful, appreciate, etc. (+1 each)
- **Negative words** (~30): bad, terrible, frustrated, broken, bug, error, crash, etc. (-1 each)
- **Intensifiers**: very, extremely, really, absolutely, totally (multiply next sentiment word by 1.5x)
- **Negators**: not, no, never, don't, doesn't, isn't, can't, won't (flip next word's polarity)

The raw score is normalized by message length and clamped to [-1.0, 1.0].

## Classification

| Score Range | Label | Action |
|-------------|-------|--------|
| > 0.3 | positive | Inject positive context memory |
| < -0.3 | negative | Inject frustration-aware memory |
| -0.3 to 0.3 | neutral | No memory injected (avoid context clutter) |

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Analyzes message sentiment and returns emotional context as a memory fragment |

## Example Output

Negative sentiment:
```json
{"type": "ingest_result", "memories": [{"content": "[sentiment] User appears frustrated (score: -0.6). Consider acknowledging the issue."}]}
```

Positive sentiment:
```json
{"type": "ingest_result", "memories": [{"content": "[sentiment] User seems satisfied (score: 0.7). Positive interaction."}]}
```

Neutral sentiment returns an empty memories list.

## Usage

Installed automatically when enabled in agent configuration. No external dependencies required (stdlib only).
