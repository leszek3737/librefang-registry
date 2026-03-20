#!/usr/bin/env python3
"""Todo tracker after_turn hook.

Scans all conversation messages for task patterns and completion markers,
then persists the updated todo list to disk.

Receives via stdin:
    {"type": "after_turn", "agent_id": "...", "messages": [...]}

Prints to stdout:
    {"type": "ok"}
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

# Maximum number of pending todos to keep (oldest dropped first)
MAX_PENDING = 20

# Maximum characters to extract for a single task description
MAX_TASK_LEN = 100

# ── Task detection patterns ──────────────────────────────────────────

# Each pattern captures the task text in group 1
TASK_PATTERNS = [
    # "TODO: ..." or "todo: ..."
    re.compile(r"(?i)\btodo\s*:\s*(.+)"),
    # "remind me to ..."
    re.compile(r"(?i)\bremind\s+me\s+to\s+(.+)"),
    # "don't forget to ..."
    re.compile(r"(?i)\bdon'?t\s+forget\s+to\s+(.+)"),
    # "action item: ..."
    re.compile(r"(?i)\baction\s+item\s*:\s*(.+)"),
    # "need to ..."
    re.compile(r"(?i)\bneed\s+to\s+(.+)"),
    # "I should ..." or "we should ..."
    re.compile(r"(?i)\b(?:i|we)\s+should\s+(.+)"),
    # "- [ ] ..." markdown checkbox
    re.compile(r"-\s*\[\s*\]\s*(.+)"),
]

# ── Completion detection patterns ────────────────────────────────────

COMPLETION_PATTERNS = [
    # "done with ..."
    re.compile(r"(?i)\bdone\s+with\s+(.+)"),
    # "completed ..."
    re.compile(r"(?i)\bcompleted\s+(.+)"),
    # "finished ..."
    re.compile(r"(?i)\bfinished\s+(.+)"),
]

# Completion markers that apply to nearby text
COMPLETION_MARKERS = re.compile(r"(?:\u2705|\[x\])", re.IGNORECASE)

# Pattern to extract text near a completion marker
# Looks for marker followed by text, or text followed by marker
MARKER_CONTEXT = re.compile(
    r"(?:\u2705|\[x\])\s*(.+?)(?:\.|$)|(.+?)\s*(?:\u2705|\[x\])",
    re.IGNORECASE,
)


def get_storage_dir():
    """Return the plugin storage directory, creating it if needed."""
    home = os.path.expanduser("~")
    path = os.path.join(home, ".librefang", "plugins", "todo-tracker")
    os.makedirs(path, exist_ok=True)
    return path


def get_todos_path(agent_id):
    """Return the path to the todos file for the given agent."""
    return os.path.join(get_storage_dir(), f"{agent_id}.json")


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


def save_todos(agent_id, todos):
    """Persist the todo list to disk."""
    path = get_todos_path(agent_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"todos": todos}, f, indent=2, ensure_ascii=False)


def clean_task_text(text):
    """Clean and truncate extracted task text."""
    # Take up to end of first sentence or MAX_TASK_LEN
    text = text.strip()
    # Truncate at sentence boundary
    for delim in (".", "!", "\n"):
        idx = text.find(delim)
        if 0 < idx < MAX_TASK_LEN:
            text = text[:idx]
            break
    text = text.strip().rstrip(".,;:!?")
    if len(text) > MAX_TASK_LEN:
        text = text[:MAX_TASK_LEN].rstrip()
    return text


def normalize_for_comparison(text):
    """Normalize text for fuzzy deduplication: lowercase + strip non-alnum."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_duplicate(new_text, existing_todos):
    """Check if a task is a fuzzy duplicate of any existing todo."""
    normalized_new = normalize_for_comparison(new_text)
    if not normalized_new:
        return True  # empty tasks are always "duplicates"
    for todo in existing_todos:
        normalized_existing = normalize_for_comparison(todo.get("text", ""))
        if normalized_new == normalized_existing:
            return True
        # Check if one is a substring of the other (for near-duplicates)
        if len(normalized_new) >= 5 and len(normalized_existing) >= 5:
            if normalized_new in normalized_existing or normalized_existing in normalized_new:
                return True
    return False


def get_content(msg):
    """Extract text content from a message object."""
    if isinstance(msg, dict):
        return msg.get("content", "") or ""
    return str(msg)


def extract_tasks_from_text(text):
    """Extract task descriptions from a block of text."""
    tasks = []
    for pattern in TASK_PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(1)
            cleaned = clean_task_text(raw)
            if cleaned and len(cleaned) >= 3:
                tasks.append(cleaned)
    return tasks


def extract_completions_from_text(text):
    """Extract completed task descriptions from a block of text."""
    completions = []

    # Explicit completion phrases
    for pattern in COMPLETION_PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(1)
            cleaned = clean_task_text(raw)
            if cleaned and len(cleaned) >= 3:
                completions.append(cleaned)

    # Completion markers (checkmark emoji, [x])
    for match in MARKER_CONTEXT.finditer(text):
        raw = match.group(1) or match.group(2) or ""
        cleaned = clean_task_text(raw)
        if cleaned and len(cleaned) >= 3:
            completions.append(cleaned)

    return completions


def stem_word(word):
    """Minimal suffix stripping to normalize verb forms (ing, ed, s, etc.).

    This is intentionally simple -- just enough to match "fixing" to "fix",
    "updated" to "updat(e)", etc. without pulling in nltk.
    """
    if len(word) <= 4:
        return word
    if word.endswith("ing") and len(word) > 5:
        # running -> runn -> run (but we keep the stem for comparison)
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 4:
        return word[:-1]
    return word


def word_overlap_score(text_a, text_b):
    """Compute a word-overlap similarity score between two texts.

    Returns a float between 0.0 and 1.0 indicating what fraction of
    the shorter text's stemmed words appear in the longer text.
    """
    words_a = set(stem_word(w) for w in re.findall(r"[a-z]+", text_a.lower()) if len(w) >= 3)
    words_b = set(stem_word(w) for w in re.findall(r"[a-z]+", text_b.lower()) if len(w) >= 3)
    if not words_a or not words_b:
        return 0.0
    smaller = words_a if len(words_a) <= len(words_b) else words_b
    larger = words_b if len(words_a) <= len(words_b) else words_a
    overlap = smaller & larger
    return len(overlap) / len(smaller)


# Minimum word-overlap score to consider a completion matching a todo
COMPLETION_MATCH_THRESHOLD = 0.6


def mark_completed(todos, completions):
    """Mark todos as done if they match any completion descriptions."""
    if not completions:
        return todos

    now = datetime.now(timezone.utc).isoformat()
    completion_norms = [normalize_for_comparison(c) for c in completions]

    for todo in todos:
        if todo.get("status") == "done":
            continue
        todo_text = todo.get("text", "")
        todo_norm = normalize_for_comparison(todo_text)
        for i, comp_norm in enumerate(completion_norms):
            if not comp_norm or not todo_norm:
                continue
            # Exact substring match (normalized)
            if comp_norm in todo_norm or todo_norm in comp_norm:
                todo["status"] = "done"
                todo["completed"] = now
                break
            # Fuzzy word-overlap match (handles verb form differences)
            if word_overlap_score(completions[i], todo_text) >= COMPLETION_MATCH_THRESHOLD:
                todo["status"] = "done"
                todo["completed"] = now
                break

    return todos


def enforce_pending_limit(todos):
    """Keep only the latest MAX_PENDING pending items. Done items are kept."""
    pending = [t for t in todos if t.get("status") == "pending"]
    done = [t for t in todos if t.get("status") != "pending"]

    if len(pending) > MAX_PENDING:
        # Keep the most recent MAX_PENDING pending items (by position / added time)
        pending = pending[-MAX_PENDING:]

    return pending + done


def main():
    request = json.loads(sys.stdin.read())
    agent_id = request.get("agent_id", "unknown")
    messages = request.get("messages", [])

    todos = load_todos(agent_id)
    now = datetime.now(timezone.utc).isoformat()

    all_new_tasks = []
    all_completions = []

    # Scan ALL messages for task and completion patterns
    for msg in messages:
        content = get_content(msg)
        if not content.strip():
            continue

        all_new_tasks.extend(extract_tasks_from_text(content))
        all_completions.extend(extract_completions_from_text(content))

    # Add new tasks (deduplicated against existing)
    for task_text in all_new_tasks:
        if not is_duplicate(task_text, todos):
            todos.append({
                "text": task_text,
                "status": "pending",
                "added": now,
            })

    # Mark completed tasks
    todos = mark_completed(todos, all_completions)

    # Enforce pending limit
    todos = enforce_pending_limit(todos)

    # Persist
    save_todos(agent_id, todos)

    print(json.dumps({"type": "ok"}), flush=True)


if __name__ == "__main__":
    main()
