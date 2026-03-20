# API Tester Hand

Autonomous API testing agent -- endpoint discovery, request validation, load testing, and regression detection.

## Configuration

| Field | Value |
|-------|-------|
| Category | `development` |
| Agent | `apitester-hand` |
| Routing | `api test`, `endpoint test`, `load test`, `regression test`, `api discovery` |

## Integrations

None required.

## Settings

- **Base URL** -- Base URL of the API to test
- **Authentication Type** -- `none`, `bearer`, `api_key_header`, `basic`
- **Auth Token / API Key** -- Credentials for API authentication
- **Test Mode** -- `functional`, `regression`, `load`, `security`, `comprehensive`
- **OpenAPI Spec URL** -- URL to OpenAPI/Swagger spec for auto-discovery
- **Auto Schedule** -- Run tests on a schedule (default: off)
- **Test Frequency** -- `hourly`, `daily`, `weekly`
- **Strict Mode** -- Treat any non-2xx response as failure (default: off)

## Usage

```bash
librefang hand run apitester
```
