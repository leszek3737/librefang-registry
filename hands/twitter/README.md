# Twitter Hand

Autonomous Twitter/X manager -- content creation, scheduled posting, engagement, and performance tracking.

## Configuration

| Field | Value |
|-------|-------|
| Category | `communication` |
| Agent | `twitter-hand` |
| Routing | `twitter`, `tweet`, `x.com`, `scheduled tweet` |

## Integrations

- **TWITTER_BEARER_TOKEN** -- Bearer Token from the Twitter/X Developer Portal.

## Settings

- **Content Style** -- `professional`, `casual`, `witty`, `educational`, `provocative`, `inspirational`
- **Post Frequency** -- `1_daily`, `3_daily`, `5_daily`, `hourly`
- **Auto Reply** -- Reply to mentions automatically (default: off)
- **Auto Like** -- Like relevant tweets automatically (default: off)
- **Content Topics** -- Comma-separated topics
- **Brand Voice** -- Description of your unique voice
- **Thread Mode** -- Include multi-tweet threads (default: on)
- **Content Queue Size** -- `5`, `10`, `20`, `50`
- **Engagement Hours** -- `business_hours`, `waking_hours`, `all_day`
- **Approval Mode** -- Queue tweets for review (default: on)

## Usage

```bash
librefang hand run twitter
```
