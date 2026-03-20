# Reddit Hand

Autonomous Reddit manager -- monitors subreddits, posts content, replies to threads, and tracks karma and engagement.

## Configuration

| Field | Value |
|-------|-------|
| Category | `communication` |
| Agent | `reddit-hand` |
| Routing | `reddit`, `subreddit`, `reddit post`, `reddit monitor` |

## Integrations

- **REDDIT_CLIENT_ID** -- OAuth2 client ID from a Reddit app.
- **REDDIT_CLIENT_SECRET** -- OAuth2 client secret from a Reddit app.
- **REDDIT_USERNAME** -- Reddit account username.
- **REDDIT_PASSWORD** -- Reddit account password.

## Settings

- **Subreddits** -- Comma-separated list of subreddits to monitor
- **Monitor Mode** -- `hot_only`, `new_only`, `hot_and_new`, `rising`
- **Auto Reply** -- Automatically reply to relevant posts (default: off)
- **Post Frequency** -- `never`, `1_daily`, `3_daily`, `weekly`
- **Content Style** -- `helpful`, `casual`, `expert`, `witty`
- **Approval Mode** -- Queue posts for review (default: on)
- **Max Reply Depth** -- `1`, `3`, `5`, `unlimited`

## Usage

```bash
librefang hand run reddit
```
