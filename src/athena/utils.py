"""Utility functions for Athena."""

from __future__ import annotations

from typing import Any


def fuzzy_match(query: str, text: str, threshold: float = 0.3) -> bool:
    """Check if query fuzzy-matches text using character overlap."""
    query_set = set(query.lower())
    text_set = set(text.lower())
    if not query_set:
        return False
    overlap = len(query_set & text_set) / len(query_set)
    return overlap >= threshold


def format_skill_info(info: dict[str, Any]) -> str:
    """Format skill info as a readable string."""
    lines = [
        f"Name: {info['name']}",
        f"Description: {info['description']}",
        f"Category: {info['category']}",
        f"Parameters: {info.get('parameters', {})}",
    ]
    return "\n".join(lines)


def validate_schema(data: dict[str, Any], schema: dict[str, type]) -> list[str]:
    """Validate data against a simple type schema. Returns list of errors."""
    errors: list[str] = []
    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"Missing key: {key}")
        elif not isinstance(data[key], expected_type):
            errors.append(f"Wrong type for {key}: expected {expected_type.__name__}")
    return errors
