#!/usr/bin/env python3
"""Auto-summarizer after_turn hook.

Generates a compact extractive summary of the conversation after each turn.
Keeps agents aware of conversation context even in long exchanges.

Receives via stdin:
    {"type": "after_turn", "agent_id": "...", "messages": [...]}

Prints to stdout:
    {"type": "ok"}
"""
import json
import os
import sys

# Only summarize when conversation exceeds this many messages
MIN_MESSAGES_FOR_SUMMARY = 6

# Maximum length of the generated summary
MAX_SUMMARY_CHARS = 500

# Keywords that signal decisions or conclusions
DECISION_KEYWORDS = (
    "let's", "i'll", "we should", "decided", "agreed",
    "the plan is", "we'll", "going to", "conclusion",
    "in summary", "to summarize", "final answer",
)


def get_storage_dir():
    """Return the plugin storage directory, creating it if needed."""
    home = os.path.expanduser("~")
    path = os.path.join(home, ".librefang", "plugins", "auto-summarizer")
    os.makedirs(path, exist_ok=True)
    return path


def get_content(msg):
    """Extract text content from a message object."""
    if isinstance(msg, dict):
        return msg.get("content", "") or ""
    return str(msg)


def get_role(msg):
    """Extract the role from a message object."""
    if isinstance(msg, dict):
        return msg.get("role", "unknown")
    return "unknown"


def contains_question(text):
    """Check if text contains a question."""
    return "?" in text


def contains_decision(text):
    """Check if text contains decision/conclusion language."""
    lower = text.lower()
    return any(kw in lower for kw in DECISION_KEYWORDS)


def truncate(text, max_len):
    """Truncate text to max_len, adding ellipsis if needed."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def build_summary(messages):
    """Build an extractive summary from the conversation messages.

    Strategy:
    - First user message (topic opener)
    - Messages containing questions
    - Messages containing decisions/conclusions
    - Last 2 exchanges (most recent context)

    Deduplicates and truncates to MAX_SUMMARY_CHARS.
    """
    if len(messages) <= MIN_MESSAGES_FOR_SUMMARY:
        return ""

    selected = []
    seen_indices = set()

    # 1. First user message (topic opener)
    for i, msg in enumerate(messages):
        if get_role(msg) == "user":
            content = get_content(msg).strip()
            if content:
                selected.append(f"Topic: {truncate(content, 120)}")
                seen_indices.add(i)
            break

    # 2. Messages containing questions
    for i, msg in enumerate(messages):
        if i in seen_indices:
            continue
        content = get_content(msg).strip()
        if content and contains_question(content):
            role = get_role(msg)
            prefix = "Q" if role == "user" else "Agent-Q"
            selected.append(f"{prefix}: {truncate(content, 100)}")
            seen_indices.add(i)

    # 3. Messages containing decisions/conclusions
    for i, msg in enumerate(messages):
        if i in seen_indices:
            continue
        content = get_content(msg).strip()
        if content and contains_decision(content):
            selected.append(f"Decision: {truncate(content, 100)}")
            seen_indices.add(i)

    # 4. Last 2 exchanges (up to 4 messages: user+assistant pairs)
    tail_start = max(0, len(messages) - 4)
    for i in range(tail_start, len(messages)):
        if i in seen_indices:
            continue
        content = get_content(messages[i]).strip()
        if content:
            role = get_role(messages[i])
            label = "User" if role == "user" else "Agent"
            selected.append(f"Recent({label}): {truncate(content, 100)}")
            seen_indices.add(i)

    if not selected:
        return ""

    summary = " | ".join(selected)
    return truncate(summary, MAX_SUMMARY_CHARS)


def main():
    request = json.loads(sys.stdin.read())
    agent_id = request.get("agent_id", "unknown")
    messages = request.get("messages", [])

    summary = build_summary(messages)

    if summary:
        storage_dir = get_storage_dir()
        summary_path = os.path.join(storage_dir, f"{agent_id}.summary")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

    print(json.dumps({"type": "ok"}), flush=True)


if __name__ == "__main__":
    main()
