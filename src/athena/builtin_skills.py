"""Built-in skills that ship with Athena."""

from __future__ import annotations

import re
from collections import Counter

from athena.core import skill, Skill


@skill(name="summarize", description="Summarize text to key points", category="nlp")
def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Extract the most important sentences from text."""
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    selected = sentences[:max_sentences]
    return ". ".join(selected) + "." if selected else text


@skill(name="extract_keywords", description="Extract keywords from text", category="nlp")
def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """Extract the most frequent meaningful words from text."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "it", "its", "this", "that", "and", "but", "or", "not", "no",
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    filtered = [w for w in words if w not in stop_words]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]


@skill(name="analyze_sentiment", description="Analyze text sentiment", category="nlp")
def analyze_sentiment(text: str) -> dict[str, float | str]:
    """Perform simple rule-based sentiment analysis."""
    positive_words = {
        "good", "great", "excellent", "amazing", "wonderful", "fantastic",
        "love", "happy", "best", "awesome", "perfect", "beautiful",
    }
    negative_words = {
        "bad", "terrible", "awful", "horrible", "hate", "worst",
        "ugly", "poor", "disappointing", "sad", "angry", "broken",
    }
    words = set(re.findall(r"\b[a-z]+\b", text.lower()))
    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)
    total = pos_count + neg_count

    if total == 0:
        return {"sentiment": "neutral", "confidence": 0.5}

    score = pos_count / total
    label = "positive" if score > 0.5 else "negative" if score < 0.5 else "neutral"
    return {"sentiment": label, "confidence": round(score if score > 0.5 else 1 - score, 2)}


@skill(name="translate_placeholder", description="Placeholder for text translation", category="nlp")
def translate_text(text: str, target_language: str = "es") -> str:
    """Placeholder translation — returns text with language tag.

    In production, this would call a translation API.
    """
    return f"[{target_language}] {text}"


@skill(name="generate_outline", description="Generate a document outline", category="writing")
def generate_outline(topic: str, depth: int = 2) -> list[str]:
    """Generate a structured outline for a topic."""
    sections = [
        f"1. Introduction to {topic}",
        f"2. Background and Context",
        f"3. Key Concepts",
        f"4. Implementation Details",
        f"5. Best Practices",
        f"6. Conclusion",
    ]
    if depth >= 2:
        expanded: list[str] = []
        for section in sections:
            expanded.append(section)
            expanded.append(f"   - Overview")
            expanded.append(f"   - Details")
        return expanded
    return sections


def get_all_builtin_skills() -> list[Skill]:
    """Return all built-in skills."""
    return [
        summarize_text,
        extract_keywords,
        analyze_sentiment,
        translate_text,
        generate_outline,
    ]
