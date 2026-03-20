# LinkedIn Hand

Autonomous LinkedIn manager -- profile optimization, content creation, networking, and professional engagement.

## Configuration

| Field | Value |
|-------|-------|
| Category | `communication` |
| Agent | `linkedin-hand` |
| Routing | `linkedin`, `profile optimization`, `professional networking` |

## Integrations

- **LINKEDIN_ACCESS_TOKEN** -- OAuth 2.0 access token from the LinkedIn Developer Portal.

## Settings

- **Content Style** -- `thought_leader`, `educational`, `storyteller`, `data_driven`, `conversational`
- **Post Frequency** -- `1_weekly`, `3_weekly`, `5_weekly`, `1_daily`
- **Content Topics** -- Comma-separated topics to create content about
- **Auto Engage** -- Automatically like/comment on relevant posts (default: off)
- **Approval Mode** -- Queue posts for review before posting (default: on)
- **Hashtag Count** -- `0`, `3`, `5`
- **Target Audience** -- `peers`, `recruiters`, `clients`, `general`
- **Language** -- `en`, `zh`, `es`, `auto`

## Usage

```bash
librefang hand run linkedin
```
