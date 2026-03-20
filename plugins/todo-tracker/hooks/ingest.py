#!/usr/bin/env python3
"""Todo tracker ingest hook.

Returns pending todo items as a memory fragment so agents stay aware
of outstanding action items during conversations.

Receives via stdin:
    {"type": "ingest", "agent_id": "...", "message": "user message text"}

Prints to stdout:
    {"type": "ingest_result", "memories": [{"content": "..."}]}
"""
import json
import os
import sys


def get_todos_path(agent_id):
    """Return the path to the todos file for the given agent."""
    home = os.path.expanduser("~")
    return os.path.join(
        home, ".librefang", "plugins", "todo-tracker", f"{agent_id}.json"
    )


def load_todos(agent_id):
    """Load existing todos from disk. Returns a list of todo dicts."""
    path = get_todos_path(agent_id)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("todos", [])
    except (OSError, IOError, json.JSONDecodeError):
        return []


def main():
    request = json.loads(sys.stdin.read())
    agent_id = request.get("agent_id", "unknown")

    memories = []
    todos = load_todos(agent_id)

    # Filter to pending items only
    pending = [t for t in todos if t.get("status") == "pending"]

    if pending:
        items = []
        for i, todo in enumerate(pending, 1):
            items.append(f"{i}) {todo.get('text', '?')}")
        items_str = " ".join(items)
        memories.append(
            {"content": f"[todo] Pending items: {items_str}"}
        )

    print(json.dumps({"type": "ingest_result", "memories": memories}))


if __name__ == "__main__":
    main()
