# Collector Hand

Autonomous intelligence collector -- monitors any target continuously with change detection and knowledge graphs.

## Configuration

| Field | Value |
|-------|-------|
| Category | `data` |
| Agent | `collector-hand` |
| Routing | `monitor changes`, `track updates`, `collect intelligence`, `osint`, `change detection` |

## Integrations

None required.

## Settings

- **Target Subject** -- What to monitor (company, person, technology, market, topic)
- **Collection Depth** -- `surface`, `deep`, `exhaustive`
- **Update Frequency** -- `hourly`, `every_6h`, `daily`, `weekly`
- **Focus Area** -- `market`, `business`, `competitor`, `person`, `technology`, `general`
- **Alert on Changes** -- Publish events on significant changes (default: on)
- **Report Format** -- `markdown`, `json`, `html`
- **Max Sources Per Cycle** -- `10`, `30`, `50`, `100`
- **Track Sentiment** -- Analyze sentiment trends over time (default: off)

## Usage

```bash
librefang hand run collector
```
