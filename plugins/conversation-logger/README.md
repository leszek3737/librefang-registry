# conversation-logger

Logs all conversations to JSONL files for auditing, analytics, and debugging. Each agent gets its own log file at `~/.librefang/logs/conversations/{agent_id}.jsonl`.

## Log Format

Each line is a JSON object:

```json
{
  "timestamp": "2026-03-21T12:34:56Z",
  "agent_id": "agent-abc123",
  "turn_number": 5,
  "message_count": 10,
  "last_user_message": "truncated to 200 chars...",
  "last_assistant_message": "truncated to 200 chars..."
}
```

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| after_turn | `hooks/after_turn.py` | Appends a log entry after each conversation turn |

## How It Works

After each conversation turn the hook extracts summary information from the messages array and appends a single JSON line to the agent's log file. User and assistant messages are truncated to 200 characters to keep log files manageable.

Errors from the filesystem (permissions, disk full, etc.) are caught silently so the agent conversation is never interrupted by a logging failure.

## Usage

Installed automatically when enabled in agent configuration. Log files are created on first write -- no manual setup required.
