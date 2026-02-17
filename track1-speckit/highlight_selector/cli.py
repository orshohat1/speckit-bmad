"""Command-line interface for AI Highlight Selector.

Reads JSON input from stdin, processes game events, and writes
JSON output to stdout. Supports personalized highlight selection.

Usage:
    cat sample_data.json | python -m highlight_selector.cli
    echo '{"events": [...]}' | python -m highlight_selector.cli
"""

from __future__ import annotations

import json
import sys
from typing import Any

from highlight_selector.models import GameEvent, Highlight, UserPreference
from highlight_selector.selector import select_highlights


def parse_input(raw: str) -> tuple[list[GameEvent], UserPreference]:
    """Parse JSON input string into events and preferences.

    Accepted input formats:
    1. Full format: {"events": [...], "user_preferences": {...}}
    2. Events only: {"events": [...]}
    3. With game wrapper: {"game": {...}, "events": [...], "user_preferences": {...}}

    Args:
        raw: JSON string from stdin.

    Returns:
        Tuple of (events list, user preference).

    Raises:
        ValueError: If JSON is invalid or missing required "events" field.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object with an 'events' key.")

    if "events" not in data:
        raise ValueError("Missing required 'events' key in input JSON.")

    events_data = data["events"]
    if not isinstance(events_data, list):
        raise ValueError("'events' must be a JSON array.")

    events = [GameEvent.from_dict(e) for e in events_data]

    # Parse preferences (optional)
    prefs_data = data.get("user_preferences") or data.get("preferences")
    if isinstance(prefs_data, dict):
        # If it contains named examples, pick the first one
        first_value = next(iter(prefs_data.values()), None)
        if isinstance(first_value, dict) and "favorite_player" in first_value:
            prefs = UserPreference.from_dict(first_value)
        else:
            prefs = UserPreference.from_dict(prefs_data)
    else:
        prefs = UserPreference()

    return events, prefs


def format_output(
    highlights: list[Highlight],
    total_events: int,
    prefs: UserPreference,
) -> dict[str, Any]:
    """Format highlights into JSON-serializable output.

    Args:
        highlights: Selected and ranked highlights.
        total_events: Total number of input events.
        prefs: User preferences used for this run.

    Returns:
        Dictionary ready for JSON serialization.
    """
    return {
        "highlights": [h.to_dict() for h in highlights],
        "metadata": {
            "total_events": total_events,
            "selected_count": len(highlights),
            "preferences": prefs.to_dict(),
        },
    }


def main() -> None:
    """Main CLI entry point. Reads from stdin, writes to stdout."""
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(
                json.dumps({"error": "No input provided. Pipe JSON to stdin."}),
                file=sys.stderr,
            )
            sys.exit(1)

        events, prefs = parse_input(raw_input)
        highlights = select_highlights(events, prefs)
        output = format_output(highlights, len(events), prefs)
        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            json.dumps({"error": f"Unexpected error: {e}"}),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
