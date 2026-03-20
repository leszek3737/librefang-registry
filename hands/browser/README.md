# Browser Hand

Autonomous web browser -- navigates sites, fills forms, clicks buttons, and completes multi-step web tasks with user approval for purchases.

## Configuration

| Field | Value |
|-------|-------|
| Category | `productivity` |
| Agent | `browser-hand` |
| Routing | `open website`, `navigate to`, `fill form`, `click button`, `web login`, `browser automation` |

## Integrations

- **Python 3** -- Required for Playwright browser automation library.
- **Chromium** (optional) -- A Chromium-based browser; Playwright can install its own if none found.

## Settings

- **Headless Mode** -- Run browser without a visible window (default: on)
- **Purchase Approval** -- Require confirmation before purchases (default: on)
- **Max Pages Per Task** -- Navigation limit per task (`10`, `20`, `50`)
- **Default Wait After Action** -- Page settle time (`auto`, `1s`, `3s`)
- **Screenshot After Actions** -- Auto-screenshot after every action (default: off)

## Usage

```bash
librefang hand run browser
```
