#!/usr/bin/env python3
"""Sentiment tracker ingest hook.

Analyzes user message sentiment using keyword-based scoring and injects
emotional context so agents can respond with appropriate tone.

Receives via stdin:
    {"type": "ingest", "agent_id": "...", "message": "user message text"}

Prints to stdout:
    {"type": "ingest_result", "memories": [{"content": "..."}]}
"""
import json
import re
import sys

# Positive sentiment words with base score of +1
POSITIVE_WORDS = frozenset({
    "great", "love", "excellent", "happy", "thanks", "awesome", "perfect",
    "wonderful", "good", "nice", "amazing", "fantastic", "helpful", "pleased",
    "appreciate", "brilliant", "outstanding", "superb", "delightful", "glad",
    "impressive", "beautiful", "enjoy", "excited", "grateful", "incredible",
    "marvelous", "terrific", "thank", "cool",
})

# Negative sentiment words with base score of -1
NEGATIVE_WORDS = frozenset({
    "bad", "terrible", "hate", "angry", "frustrated", "disappointed", "broken",
    "wrong", "awful", "horrible", "annoying", "useless", "fail", "worst",
    "problem", "issue", "bug", "error", "crash", "slow", "stuck", "confused",
    "difficult", "painful", "ugly", "ridiculous", "poor", "sucks", "garbage",
    "missing",
})

# Intensifiers multiply the next sentiment word's score by this factor
INTENSIFIERS = frozenset({
    "very", "extremely", "really", "absolutely", "totally", "incredibly",
    "completely", "utterly", "highly", "so",
})
INTENSIFIER_MULTIPLIER = 1.5

# Negators flip the polarity of the next sentiment word
NEGATORS = frozenset({
    "not", "no", "never", "don't", "doesn't", "isn't", "can't", "won't",
    "didn't", "wasn't", "weren't", "couldn't", "shouldn't", "wouldn't",
    "hardly", "barely", "neither",
})

# Sentiment thresholds
POSITIVE_THRESHOLD = 0.3
NEGATIVE_THRESHOLD = -0.3


def tokenize(text):
    """Split text into lowercase tokens, preserving contractions."""
    return re.findall(r"[a-zA-Z][a-zA-Z']*", text.lower())


def compute_sentiment(tokens):
    """Compute sentiment score from -1.0 to 1.0.

    Walks through tokens tracking negator and intensifier state,
    then applies them to sentiment-bearing words.
    """
    if not tokens:
        return 0.0

    raw_score = 0.0
    negate_next = False
    intensify_next = False

    for token in tokens:
        if token in NEGATORS:
            negate_next = True
            continue

        if token in INTENSIFIERS:
            intensify_next = True
            continue

        score = 0.0
        if token in POSITIVE_WORDS:
            score = 1.0
        elif token in NEGATIVE_WORDS:
            score = -1.0

        if score != 0.0:
            if intensify_next:
                score *= INTENSIFIER_MULTIPLIER
                intensify_next = False

            if negate_next:
                score *= -1.0
                negate_next = False

            raw_score += score
        else:
            # Reset modifiers if the next word is not a sentiment word
            # (modifiers only apply to the immediately following sentiment word)
            negate_next = False
            intensify_next = False

    # Normalize to -1.0 .. 1.0 using tanh-like scaling
    # This keeps small scores proportional while bounding large ones
    word_count = len(tokens)
    if word_count == 0:
        return 0.0

    # Scale by number of tokens to normalize for message length
    normalized = raw_score / max(word_count ** 0.5, 1.0)

    # Clamp to [-1.0, 1.0]
    return max(-1.0, min(1.0, normalized))


def classify(score):
    """Classify sentiment score into a label."""
    if score > POSITIVE_THRESHOLD:
        return "positive"
    elif score < NEGATIVE_THRESHOLD:
        return "negative"
    else:
        return "neutral"


def main():
    request = json.loads(sys.stdin.read())
    message = request.get("message", "")

    if not message.strip():
        print(json.dumps({"type": "ingest_result", "memories": []}))
        return

    tokens = tokenize(message)
    score = compute_sentiment(tokens)
    label = classify(score)

    # Only inject memory for clearly non-neutral sentiment
    if label == "neutral":
        print(json.dumps({"type": "ingest_result", "memories": []}))
        return

    score_str = f"{score:.1f}"

    if label == "negative":
        content = f"[sentiment] User appears frustrated (score: {score_str}). Consider acknowledging the issue."
    else:
        content = f"[sentiment] User seems satisfied (score: {score_str}). Positive interaction."

    memories = [{"content": content}]
    print(json.dumps({"type": "ingest_result", "memories": memories}))


if __name__ == "__main__":
    main()
