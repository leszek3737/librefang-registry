#!/usr/bin/env python3
"""Auto-summarizer ingest hook.

Returns the stored conversation summary as a memory fragment so agents
maintain awareness of prior conversation context.

Receives via stdin:
    {"type": "ingest", "agent_id": "...", "message": "user message text"}

Prints to stdout:
    {"type": "ingest_result", "memories": [{"content": "..."}]}
"""
import json
import os
import sys


def get_summary_path(agent_id):
    """Return the path to the summary file for the given agent."""
    home = os.path.expanduser("~")
    return os.path.join(
        home, ".librefang", "plugins", "auto-summarizer", f"{agent_id}.summary"
    )


def main():
    request = json.loads(sys.stdin.read())
    agent_id = request.get("agent_id", "unknown")

    memories = []
    summary_path = get_summary_path(agent_id)

    if os.path.isfile(summary_path):
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = f.read().strip()
            if summary:
                memories.append(
                    {"content": f"[summary] Conversation so far: {summary}"}
                )
        except (OSError, IOError):
            # If we cannot read the file, return no memories silently.
            pass

    print(json.dumps({"type": "ingest_result", "memories": memories}))


if __name__ == "__main__":
    main()
