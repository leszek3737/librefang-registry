#!/usr/bin/env python3
"""Conversation logger after_turn hook.

Appends a JSON line to a per-agent log file after each conversation turn.
Log files are stored under ~/.librefang/logs/conversations/{agent_id}.jsonl.

Receives via stdin:
    {"type": "after_turn", "agent_id": "...", "messages": [...]}

Prints to stdout:
    {"type": "ok"}
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _log_dir() -> Path:
    """Return the conversations log directory, creating it if needed."""
    home = Path.home()
    log_path = home / ".librefang" / "logs" / "conversations"
    log_path.mkdir(parents=True, exist_ok=True)
    return log_path


def _last_message_by_role(messages: list, role: str) -> str:
    """Find the last message with the given role and return its content truncated to 200 chars."""
    for msg in reversed(messages):
        if msg.get("role") == role:
            content = msg.get("content", "")
            if len(content) > 200:
                return content[:200] + "..."
            return content
    return ""


def main():
    request = json.loads(sys.stdin.read())
    agent_id = request.get("agent_id", "unknown")
    messages = request.get("messages", [])

    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent_id": agent_id,
        "turn_number": max(
            sum(1 for m in messages if m.get("role") == "assistant"), 1
        ),
        "message_count": len(messages),
        "last_user_message": _last_message_by_role(messages, "user"),
        "last_assistant_message": _last_message_by_role(messages, "assistant"),
    }

    try:
        log_file = _log_dir() / f"{agent_id}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        # Filesystem issues should not crash the agent. The hook still
        # responds with "ok" so the conversation continues normally.
        pass

    print(json.dumps({"type": "ok"}))


if __name__ == "__main__":
    main()
