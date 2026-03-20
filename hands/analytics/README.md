# Analytics Hand

Autonomous data analytics agent -- data collection, analysis, visualization, dashboards, and automated reporting.

## Configuration

| Field | Value |
|-------|-------|
| Category | `data` |
| Agent | `analytics-hand` |
| Routing | `data analysis`, `data visualization`, `dashboard`, `automated report`, `statistical analysis` |

## Integrations

- **Python 3** -- Required for data analysis with pandas, matplotlib, and seaborn.

## Settings

- **Data Source** -- Primary data source type (`csv`, `json`, `database`, `api`, `web`)
- **Analysis Type** -- Default analysis approach (`descriptive`, `diagnostic`, `predictive`, `prescriptive`)
- **Output Format** -- Report format (`report`, `dashboard`, `slides`, `executive`)
- **Visualization** -- Generate charts and visualizations (default: on)
- **Scheduled Reports** -- Auto-generate reports on a schedule (default: off)
- **Report Frequency** -- `daily`, `weekly`, `monthly`
- **Confidence Threshold** -- Minimum confidence for findings (`low`, `medium`, `high`)

## Usage

```bash
librefang hand run analytics
```
