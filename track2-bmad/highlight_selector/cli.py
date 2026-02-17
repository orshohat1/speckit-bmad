"""Command-line interface for the AI Highlight Selector.

This module provides the CLI for running highlight selection from the command line,
including argument parsing, JSON input loading, and formatted output.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

from highlight_selector.models import GameEvent, Highlight, UserPreference
from highlight_selector.selector import select_highlights


def load_json_input(file_path: str) -> dict[str, Any]:
    """Load and parse JSON input file.

    Args:
        file_path: Path to JSON file containing game events and preferences.

    Returns:
        Parsed JSON data as dictionary.

    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If file contains invalid JSON.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    return data


def validate_and_parse_events(events_data: list[dict[str, Any]]) -> list[GameEvent]:
    """Validate and parse event data into GameEvent objects.

    Args:
        events_data: List of event dictionaries from JSON.

    Returns:
        List of validated GameEvent objects.

    Raises:
        ValueError: If events data is invalid or missing required fields.
    """
    if not events_data:
        raise ValueError("No events found in input data")

    events: list[GameEvent] = []
    for idx, event_dict in enumerate(events_data):
        try:
            event = GameEvent.from_dict(event_dict)
            events.append(event)
        except (KeyError, TypeError) as e:
            raise ValueError(
                f"Invalid event data at index {idx}: {e}. "
                f"Expected fields: id, type, timestamp, quarter, player, team, "
                f"description, importance, tags"
            )

    return events


def validate_preferences(
    player: Optional[str], team: Optional[str], events: list[GameEvent]
) -> Optional[UserPreference]:
    """Validate user preferences against available events.

    Args:
        player: Favorite player name (or None).
        team: Favorite team name (or None).
        events: List of available game events.

    Returns:
        UserPreference object, or None if no preferences specified.

    Raises:
        ValueError: If specified player/team not found in events.
    """
    if not player and not team:
        return None

    # Validate player exists in events
    if player:
        available_players = {evt.player for evt in events}
        if player not in available_players:
            raise ValueError(
                f"Player '{player}' not found in events. "
                f"Available players: {', '.join(sorted(available_players))}"
            )

    # Validate team exists in events
    if team:
        available_teams = {evt.team for evt in events}
        if team not in available_teams:
            raise ValueError(
                f"Team '{team}' not found in events. "
                f"Available teams: {', '.join(sorted(available_teams))}"
            )

    return UserPreference(favorite_player=player, favorite_team=team)


def format_highlight_output(
    highlights: list[Highlight], only_filter: bool = False
) -> str:
    """Format highlights as human-readable output.

    Args:
        highlights: List of Highlight objects to format.
        only_filter: If True, only show highlights matching preferences.

    Returns:
        Formatted string output.
    """
    if not highlights:
        return "No highlights selected."

    lines: list[str] = []
    lines.append(f"🏆 Top {len(highlights)} Highlights 🏆")
    lines.append("=" * 60)
    lines.append("")

    for highlight in highlights:
        event = highlight.event
        lines.append(f"#{highlight.rank} | Score: {highlight.score:.1f}")
        lines.append(f"   {event.type.upper()} - {event.description}")
        lines.append(
            f"   Player: {event.player} | Team: {event.team} | Q{event.quarter} {event.timestamp}"
        )
        lines.append(f"   Importance: {event.importance}")
        if event.tags:
            lines.append(f"   Tags: {', '.join(event.tags)}")
        lines.append(f"   💡 {highlight.explanation}")
        lines.append("")

    return "\n".join(lines)


def apply_only_filter(
    highlights: list[Highlight], preference: Optional[UserPreference]
) -> list[Highlight]:
    """Filter highlights to only include favorite player/team.

    Args:
        highlights: List of all highlights.
        preference: User preferences for filtering.

    Returns:
        Filtered list of highlights.
    """
    if not preference:
        return highlights

    filtered: list[Highlight] = []
    for h in highlights:
        matches = False
        if preference.favorite_player and h.event.player == preference.favorite_player:
            matches = True
        if preference.favorite_team and h.event.team == preference.favorite_team:
            matches = True

        if matches:
            filtered.append(h)

    return filtered


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="AI Highlight Selector - Select and rank game highlights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Objective selection (no preferences)
  python -m highlight_selector.cli input.json

  # Personalized for favorite player
  python -m highlight_selector.cli input.json --player "LeBron James"

  # Team preference
  python -m highlight_selector.cli input.json --team "Lakers"

  # Both player and team
  python -m highlight_selector.cli input.json --player "LeBron James" --team "Lakers"

  # Only show favorite player's highlights
  python -m highlight_selector.cli input.json --player "LeBron James" --only
""",
    )

    parser.add_argument(
        "input_file",
        help="Path to JSON file containing game events",
    )

    parser.add_argument(
        "--player",
        type=str,
        default=None,
        help="Favorite player name for personalized selection",
    )

    parser.add_argument(
        "--team",
        type=str,
        default=None,
        help="Favorite team name for personalized selection",
    )

    parser.add_argument(
        "--only",
        action="store_true",
        help="Only show highlights featuring favorite player/team",
    )

    parser.add_argument(
        "--min-count",
        type=int,
        default=5,
        help="Minimum number of highlights to return (default: 5)",
    )

    parser.add_argument(
        "--max-count",
        type=int,
        default=8,
        help="Maximum number of highlights to return (default: 8)",
    )

    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results in JSON format instead of human-readable",
    )

    return parser.parse_args()


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        args = parse_args()

        # Load input data
        data = load_json_input(args.input_file)

        # Parse events
        events_data = data.get("events", [])
        events = validate_and_parse_events(events_data)

        # Validate and create preferences
        preference = validate_preferences(args.player, args.team, events)

        # Run selection
        highlights = select_highlights(
            events, preference, min_count=args.min_count, max_count=args.max_count
        )

        # Apply --only filter if requested
        if args.only:
            if not preference:
                print(
                    "Warning: --only flag requires --player or --team to be specified",
                    file=sys.stderr,
                )
            else:
                highlights = apply_only_filter(highlights, preference)

        # Output results
        if args.json_output:
            # JSON output
            output_data = {
                "highlights": [h.to_dict() for h in highlights],
                "count": len(highlights),
            }
            print(json.dumps(output_data, indent=2))
        else:
            # Human-readable output
            output = format_highlight_output(highlights)
            print(output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
