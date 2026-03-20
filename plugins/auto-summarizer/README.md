# auto-summarizer

Maintains a running conversation summary to help agents handle long conversations without losing context. Uses extractive summarization (no ML or external dependencies) to identify the most important parts of a conversation.

## How it works

After each conversation turn, the plugin scans all messages and extracts:

- **Topic opener** -- the first user message that started the conversation
- **Questions** -- any messages containing questions (detected via `?`)
- **Decisions** -- messages with conclusion/decision language ("let's", "decided", "the plan is", etc.)
- **Recent context** -- the last 2 exchanges to preserve immediate context

These are combined into a compact summary (max 500 characters) and persisted to disk. On the next ingest, the summary is returned as a memory fragment so the agent retains awareness of the full conversation.

Summarization only activates when the conversation exceeds 6 messages -- shorter conversations are passed through as-is.

## Hooks

| Hook | Script | Description |
|------|--------|-------------|
| ingest | `hooks/ingest.py` | Returns the stored conversation summary as a memory fragment |
| after_turn | `hooks/after_turn.py` | Builds and persists an extractive summary of the conversation |

## Storage

Summaries are stored at `~/.librefang/plugins/auto-summarizer/{agent_id}.summary`.

## Usage

Installed automatically when enabled in agent configuration.
