# todo-tracker

Detects action items and tasks mentioned in conversations, persists them, and recalls them as context. Helps agents keep track of what needs to be done without the user having to repeat themselves.

## How it works

### Task detection

After each conversation turn, the plugin scans **all** messages (both user and assistant) for task patterns:

- `TODO: ...` or `todo: ...`
- `remind me to ...`
- `don't forget to ...`
- `action item: ...`
- `need to ...`
- `I should ...` or `we should ...`
- `- [ ] ...` (markdown checkbox)

### Completion detection

The plugin also detects when tasks are marked as done:

- `done with ...`
- `completed ...`
- `finished ...`
- Completion markers near task text (checkmark emoji, `[x]`)

### Deduplication

New tasks are deduplicated against existing ones using normalized lowercase comparison and substring matching, so "Fix the login bug" and "fix the login bug" are treated as the same item.

### Limits

Only the latest 20 pending items are kept (FIFO). Completed items are retained for reference.

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Returns pending todo items as a memory fragment |
| after_turn | `hooks/after_turn.py` | Scans messages for tasks and completions, updates the todo list |

## Storage

Todos are stored at `~/.librefang/plugins/todo-tracker/{agent_id}.json` in the format:

```json
{
  "todos": [
    {"text": "Fix the login bug", "status": "pending", "added": "2026-03-21T12:00:00+00:00"},
    {"text": "Update README", "status": "done", "added": "2026-03-21T12:00:00+00:00", "completed": "2026-03-21T13:00:00+00:00"}
  ]
}
```

## Usage

Installed automatically when enabled in agent configuration.
