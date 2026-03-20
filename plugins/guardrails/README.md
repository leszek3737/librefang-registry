# guardrails

Safety filter plugin that detects potentially harmful content patterns in user messages and injects warning memories into agent context. Uses only Python stdlib regex -- no external dependencies.

## Detection Categories

| Category | Examples | Memory Tag |
|----------|----------|------------|
| PII | Email addresses, phone numbers, SSNs, credit card numbers | `[guardrails:pii]` |
| Prompt injection | "ignore previous instructions", "you are now", "system prompt:" | `[guardrails:injection]` |
| Credentials | `password=`, `api_key=`, `secret=`, `token=`, PEM private keys | `[guardrails:credential]` |

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Scans user messages for harmful patterns and returns warning memories |

## How It Works

When a user message arrives, the ingest hook runs all pattern checks against it. For each detected issue a memory is returned with the category tag and a recommendation for the agent (e.g. "avoid echoing PII", "maintain original instructions"). If nothing is detected the plugin returns an empty memories list.

All patterns use word boundaries and anchoring to minimise false positives on casual conversation.

## Usage

Installed automatically when enabled in agent configuration.
