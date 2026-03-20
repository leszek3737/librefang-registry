# Strategist Hand

Autonomous strategy analyst -- market research, competitive analysis, business planning, and strategic recommendations.

## Configuration

| Field | Value |
|-------|-------|
| Category | `productivity` |
| Agent | `strategist-hand` |
| Routing | `strategic analysis`, `competitive analysis`, `business plan`, `market research` |

## Integrations

None required.

## Settings

- **Focus Area** -- `general`, `market_entry`, `competitive`, `product`, `growth`
- **Analysis Depth** -- `quick`, `thorough`, `comprehensive`
- **Industry** -- Primary industry to focus on
- **Key Competitors** -- Comma-separated list of competitors to track
- **Auto Monitor** -- Track competitor moves automatically (default: off)
- **Report Format** -- `executive`, `detailed`, `slide_deck`, `memo`
- **Confidence Threshold** -- `low`, `medium`, `high`
- **Preferred Frameworks** -- e.g. `SWOT`, `Porter`, `PESTEL`

## Usage

```bash
librefang hand run strategist
```
