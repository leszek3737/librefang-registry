#!/usr/bin/env python3
"""Keyword memory ingest hook.

Extracts keywords and named entities from user messages and returns
them as contextual memories so agents have topic awareness.

Receives via stdin:
    {"type": "ingest", "agent_id": "...", "message": "user message text"}

Prints to stdout:
    {"type": "ingest_result", "memories": [{"content": "..."}]}
"""
import json
import re
import sys

# Compact English stopword set (~50 common words)
STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "must",
    "it", "its", "i", "me", "my", "you", "your", "he", "she", "we",
    "they", "them", "their", "this", "that", "these", "those", "what",
    "which", "who", "how", "when", "where", "why", "if", "then", "so",
    "not", "no", "just", "also", "very", "too", "about", "up", "out",
    "all", "some", "any", "each", "every", "into", "over", "after",
})

# Minimum word length for plain keyword extraction
MIN_WORD_LEN = 3

# Maximum keywords to return
MAX_KEYWORDS = 10

# Pattern: email addresses
RE_EMAIL = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

# Pattern: URLs (http/https/ftp) — excludes trailing punctuation
RE_URL = re.compile(r"https?://[^\s,)>]+(?<=[a-zA-Z0-9/])|ftp://[^\s,)>]+(?<=[a-zA-Z0-9/])")

# Pattern: numbers with units (e.g. 500ms, 10GB, 3.5GHz, 200k)
RE_NUMBER_UNIT = re.compile(r"\b\d+(?:\.\d+)?(?:ms|s|min|hr|h|kb|mb|gb|tb|ghz|mhz|hz|k|m|px|em|rem|%)\b", re.IGNORECASE)

# Pattern: dates (YYYY-MM-DD, MM/DD/YYYY, DD.MM.YYYY)
RE_DATE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}/\d{1,2}/\d{2,4}\b"
    r"|\b\d{1,2}\.\d{1,2}\.\d{2,4}\b"
)

# Pattern: camelCase or PascalCase identifiers
RE_CAMEL = re.compile(r"\b[a-z]+(?:[A-Z][a-z0-9]+)+\b|\b(?:[A-Z][a-z0-9]+){2,}\b")

# Pattern: snake_case identifiers (at least one underscore)
RE_SNAKE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9]+)+\b")

# Pattern: dotted technical terms (e.g. api.endpoint, os.path)
RE_DOTTED = re.compile(r"\b[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z][a-zA-Z0-9]*)+\b")


def extract_patterns(text):
    """Extract structured patterns: emails, URLs, numbers+units, dates, tech terms."""
    found = []
    for pattern in (RE_EMAIL, RE_URL, RE_NUMBER_UNIT, RE_DATE, RE_CAMEL, RE_SNAKE, RE_DOTTED):
        found.extend(pattern.findall(text))
    return found


def extract_capitalized_phrases(text):
    """Detect consecutive capitalized words (likely proper nouns / named entities).

    Skips single capitalized words at sentence boundaries by requiring
    either multi-word phrases or mid-sentence capitalized words.
    """
    phrases = []
    # Find sequences of 2+ capitalized words
    for match in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", text):
        phrases.append(match.group(0))

    # Find single capitalized words that are NOT at sentence start
    # (preceded by a lowercase letter, comma, or mid-sentence punctuation)
    for match in re.finditer(r"(?<=[a-z,;]\s)([A-Z][a-zA-Z0-9]+)\b", text):
        word = match.group(1)
        if word.lower() not in STOPWORDS and len(word) >= MIN_WORD_LEN:
            phrases.append(word)

    return phrases


def extract_plain_keywords(text):
    """Split text into words and filter out stopwords and short tokens."""
    # Remove URLs and emails first so they don't pollute word splitting
    cleaned = RE_URL.sub(" ", text)
    cleaned = RE_EMAIL.sub(" ", cleaned)
    # Split on non-alphanumeric (keep hyphens inside words)
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9]|[a-zA-Z]", cleaned)
    keywords = []
    for w in words:
        lower = w.lower()
        if lower not in STOPWORDS and len(lower) >= MIN_WORD_LEN:
            keywords.append(lower)
    return keywords


def deduplicate_keywords(items):
    """Deduplicate while preserving insertion order. Case-insensitive for plain words."""
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def main():
    request = json.loads(sys.stdin.read())
    message = request.get("message", "")

    if not message.strip():
        print(json.dumps({"type": "ingest_result", "memories": []}))
        return

    # Collect keywords from all extraction methods (patterns first for priority)
    all_keywords = []
    all_keywords.extend(extract_patterns(message))
    all_keywords.extend(extract_capitalized_phrases(message))
    all_keywords.extend(extract_plain_keywords(message))

    # Deduplicate and cap at MAX_KEYWORDS
    keywords = deduplicate_keywords(all_keywords)[:MAX_KEYWORDS]

    if not keywords:
        print(json.dumps({"type": "ingest_result", "memories": []}))
        return

    topic_str = ", ".join(keywords)
    memories = [
        {"content": f"[keyword-memory] Key topics: {topic_str}"}
    ]

    print(json.dumps({"type": "ingest_result", "memories": memories}))


if __name__ == "__main__":
    main()
