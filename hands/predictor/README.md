# Predictor Hand

Autonomous future predictor -- collects signals, builds reasoning chains, makes calibrated predictions, and tracks accuracy.

## Configuration

| Field | Value |
|-------|-------|
| Category | `data` |
| Agent | `predictor-hand` |
| Routing | `predict`, `forecast`, `probability`, `likelihood`, `scenario analysis` |

## Integrations

None required.

## Settings

- **Prediction Domain** -- `tech`, `finance`, `geopolitics`, `climate`, `general`
- **Time Horizon** -- `1_week`, `1_month`, `3_months`, `1_year`
- **Data Sources** -- `news`, `social`, `financial`, `academic`, `all`
- **Report Frequency** -- `daily`, `weekly`, `biweekly`, `monthly`
- **Predictions Per Report** -- `3`, `5`, `10`, `20`
- **Track Accuracy** -- Score past predictions when they expire (default: on)
- **Confidence Threshold** -- `low` (20%+), `medium` (40%+), `high` (70%+)
- **Contrarian Mode** -- Seek counter-consensus predictions (default: off)

## Usage

```bash
librefang hand run predictor
```
