# DevOps Hand

Autonomous DevOps engineer -- CI/CD management, infrastructure monitoring, deployment automation, and incident response.

## Configuration

| Field | Value |
|-------|-------|
| Category | `development` |
| Agent | `devops-hand` |
| Routing | `ci/cd`, `pipeline`, `github actions`, `infrastructure monitoring`, `deployment automation`, `incident response` |

## Integrations

None required.

## Settings

- **Infrastructure Type** -- `cloud`, `kubernetes`, `docker`, `bare_metal`, `serverless`
- **CI/CD Platform** -- `github_actions`, `gitlab_ci`, `jenkins`, `circleci`, `other`
- **Monitoring Focus** -- `uptime`, `performance`, `security`, `cost`, `balanced`
- **Auto Monitor** -- Automatically monitor infrastructure (default: off)
- **Health Check Interval** -- `1min`, `5min`, `15min`, `1hour`
- **Service URLs** -- Comma-separated URLs to monitor
- **Alert on Failure** -- Publish events on health check failures (default: on)
- **Rollback Strategy** -- `manual`, `auto_previous`, `blue_green`

## Usage

```bash
librefang hand run devops
```
