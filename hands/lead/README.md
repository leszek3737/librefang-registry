# Lead Hand

Autonomous lead generation -- discovers, enriches, and delivers qualified leads on a schedule.

## Configuration

| Field | Value |
|-------|-------|
| Category | `data` |
| Agent | `lead-hand` |
| Routing | `lead generation`, `prospect list`, `find customers`, `contact enrichment` |

## Integrations

None required.

## Settings

- **Target Industry** -- Industry vertical to focus on
- **Target Role** -- Decision-maker titles to target
- **Company Size** -- `any`, `startup`, `smb`, `enterprise`
- **Lead Source** -- `web_search`, `linkedin_public`, `crunchbase`, `custom`
- **Output Format** -- `csv`, `json`, `markdown_table`
- **Leads Per Report** -- `10`, `25`, `50`, `100`
- **Delivery Schedule** -- `daily_7am`, `daily_9am`, `weekdays_8am`, `weekly_monday`
- **Geographic Focus** -- Region to prioritize
- **Enrichment Depth** -- `basic`, `standard`, `deep`

## Usage

```bash
librefang hand run lead
```
