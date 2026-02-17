"""Unit tests for CLI module."""

import json
import tempfile
from pathlib import Path

import pytest

from highlight_selector.cli import (
    apply_only_filter,
    format_highlight_output,
    load_json_input,
    validate_and_parse_events,
    validate_preferences,
)
from highlight_selector.models import GameEvent, Highlight, UserPreference


@pytest.fixture
def sample_json_file():
    """Create a temporary JSON file with sample data."""
    data = {
        "events": [
            {
                "id": "evt1",
                "type": "touchdown",
                "timestamp": "10:23",
                "quarter": 4,
                "player": "J.Allen",
                "team": "BUF",
                "description": "15-yard TD pass",
                "importance": "critical",
                "tags": ["clutch"],
            },
            {
                "id": "evt2",
                "type": "interception",
                "timestamp": "08:15",
                "quarter": 3,
                "player": "T.White",
                "team": "BUF",
                "description": "Red zone INT",
                "importance": "high",
                "tags": [],
            },
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


# Story 5.2: JSON Input Loading Tests


def test_load_json_input_success(sample_json_file):
    """Verify successful JSON loading."""
    data = load_json_input(sample_json_file)
    assert "events" in data
    assert len(data["events"]) == 2


def test_load_json_input_file_not_found():
    """Verify FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        load_json_input("nonexistent_file.json")


def test_load_json_input_invalid_json():
    """Verify JSONDecodeError for invalid JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_json_input(temp_path)
    finally:
        Path(temp_path).unlink()


# Story 5.3: Validation Tests


def test_validate_and_parse_events_success():
    """Verify successful event parsing."""
    events_data = [
        {
            "id": "evt1",
            "type": "touchdown",
            "timestamp": "10:23",
            "quarter": 4,
            "player": "J.Allen",
            "team": "BUF",
            "description": "TD pass",
            "importance": "critical",
            "tags": [],
        }
    ]

    events = validate_and_parse_events(events_data)

    assert len(events) == 1
    assert isinstance(events[0], GameEvent)
    assert events[0].id == "evt1"


def test_validate_and_parse_events_empty_list():
    """Verify ValueError for empty event list."""
    with pytest.raises(ValueError, match="No events found"):
        validate_and_parse_events([])


def test_validate_and_parse_events_missing_field():
    """Verify ValueError for missing required field."""
    events_data = [
        {
            "id": "evt1",
            "type": "touchdown",
            # Missing required fields
        }
    ]

    with pytest.raises(ValueError, match="Invalid event data"):
        validate_and_parse_events(events_data)


def test_validate_preferences_both_fields():
    """Verify preference validation with both player and team."""
    events = [
        GameEvent(
            id="evt1",
            type="touchdown",
            timestamp="10:23",
            quarter=4,
            player="J.Allen",
            team="BUF",
            description="TD",
            importance="critical",
        )
    ]

    pref = validate_preferences("J.Allen", "BUF", events)

    assert pref is not None
    assert pref.favorite_player == "J.Allen"
    assert pref.favorite_team == "BUF"


def test_validate_preferences_none_when_empty():
    """Verify None returned when no preferences specified."""
    events = [
        GameEvent(
            id="evt1",
            type="touchdown",
            timestamp="10:23",
            quarter=4,
            player="J.Allen",
            team="BUF",
            description="TD",
            importance="critical",
        )
    ]

    pref = validate_preferences(None, None, events)

    assert pref is None


def test_validate_preferences_player_not_found():
    """Verify ValueError when player not in events."""
    events = [
        GameEvent(
            id="evt1",
            type="touchdown",
            timestamp="10:23",
            quarter=4,
            player="J.Allen",
            team="BUF",
            description="TD",
            importance="critical",
        )
    ]

    with pytest.raises(ValueError, match="Player 'T.Brady' not found"):
        validate_preferences("T.Brady", None, events)


def test_validate_preferences_team_not_found():
    """Verify ValueError when team not in events."""
    events = [
        GameEvent(
            id="evt1",
            type="touchdown",
            timestamp="10:23",
            quarter=4,
            player="J.Allen",
            team="BUF",
            description="TD",
            importance="critical",
        )
    ]

    with pytest.raises(ValueError, match="Team 'NE' not found"):
        validate_preferences(None, "NE", events)


# Story 5.4: Output Formatting Tests


def test_format_highlight_output():
    """Verify formatted output generation."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
        tags=["clutch"],
    )

    highlight = Highlight(
        event=event, rank=1, score=150, explanation="Critical game moment."
    )

    output = format_highlight_output([highlight])

    assert "Top 1 Highlights" in output
    assert "#1" in output
    assert "Score: 150.0" in output
    assert "J.Allen" in output
    assert "BUF" in output
    assert "Critical game moment." in output


def test_format_highlight_output_empty():
    """Verify output for empty highlight list."""
    output = format_highlight_output([])
    assert output == "No highlights selected."


def test_format_highlight_output_multiple():
    """Verify output for multiple highlights."""
    events = [
        GameEvent(
            id=f"evt{i}",
            type="play",
            timestamp="00:00",
            quarter=i,
            player="Player",
            team="TEAM",
            description=f"Event {i}",
            importance="high",
        )
        for i in range(1, 4)
    ]

    highlights = [
        Highlight(event=evt, rank=idx + 1, score=100 - idx * 10, explanation="Test")
        for idx, evt in enumerate(events)
    ]

    output = format_highlight_output(highlights)

    assert "Top 3 Highlights" in output
    assert "#1" in output
    assert "#2" in output
    assert "#3" in output


# Story 5.6: --only Flag Tests


def test_apply_only_filter_player_match():
    """Verify --only filter for favorite player."""
    pref = UserPreference(favorite_player="Star")

    events = [
        GameEvent(
            id="evt1",
            type="play",
            timestamp="00:00",
            quarter=1,
            player="Star",
            team="TEAM",
            description="Star play",
            importance="high",
        ),
        GameEvent(
            id="evt2",
            type="play",
            timestamp="00:00",
            quarter=1,
            player="Other",
            team="TEAM",
            description="Other play",
            importance="high",
        ),
    ]

    highlights = [
        Highlight(event=events[0], rank=1, score=100, explanation="Test"),
        Highlight(event=events[1], rank=2, score=90, explanation="Test"),
    ]

    filtered = apply_only_filter(highlights, pref)

    assert len(filtered) == 1
    assert filtered[0].event.player == "Star"


def test_apply_only_filter_team_match():
    """Verify --only filter for favorite team."""
    pref = UserPreference(favorite_team="STAR")

    events = [
        GameEvent(
            id="evt1",
            type="play",
            timestamp="00:00",
            quarter=1,
            player="P1",
            team="STAR",
            description="Play 1",
            importance="high",
        ),
        GameEvent(
            id="evt2",
            type="play",
            timestamp="00:00",
            quarter=1,
            player="P2",
            team="OTHER",
            description="Play 2",
            importance="high",
        ),
    ]

    highlights = [
        Highlight(event=events[0], rank=1, score=100, explanation="Test"),
        Highlight(event=events[1], rank=2, score=90, explanation="Test"),
    ]

    filtered = apply_only_filter(highlights, pref)

    assert len(filtered) == 1
    assert filtered[0].event.team == "STAR"


def test_apply_only_filter_no_preference():
    """Verify --only filter returns all when no preference."""
    highlights = [
        Highlight(
            event=GameEvent(
                id="evt1",
                type="play",
                timestamp="00:00",
                quarter=1,
                player="P1",
                team="T1",
                description="Play",
                importance="high",
            ),
            rank=1,
            score=100,
            explanation="Test",
        )
    ]

    filtered = apply_only_filter(highlights, None)

    assert len(filtered) == 1
