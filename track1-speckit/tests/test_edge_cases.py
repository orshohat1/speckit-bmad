"""Tests for edge case handling (US-5)."""

from __future__ import annotations

import pytest

from highlight_selector.models import GameEvent, UserPreference
from highlight_selector.selector import select_highlights, score_event


def _make_event(
    event_id: str = "evt-001",
    importance: str = "medium",
    quarter: int = 2,
    player: str = "Player A",
    team: str = "Team A",
    tags: list[str] | None = None,
) -> GameEvent:
    return GameEvent(
        id=event_id,
        type="dunk",
        timestamp=f"Q{quarter} 05:00",
        quarter=quarter,
        player=player,
        team=team,
        description=f"Test event {event_id}",
        importance=importance,
        tags=tags if tags is not None else [],
    )


class TestEmptyEventList:
    """T027: FR-010 - Empty event list returns empty highlights."""

    def test_empty_list_returns_empty(self) -> None:
        highlights = select_highlights([])
        assert highlights == []

    def test_empty_list_with_preferences(self) -> None:
        prefs = UserPreference(favorite_player="LeBron")
        highlights = select_highlights([], prefs)
        assert highlights == []


class TestNullPreferences:
    """T028: FR-011 - Null preferences treated as no preference."""

    def test_null_preference_object(self) -> None:
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(8)]
        highlights = select_highlights(events, None)
        assert 5 <= len(highlights) <= 8

    def test_null_favorite_player(self) -> None:
        prefs = UserPreference(favorite_player=None, favorite_team="Lakers")
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(8)]
        highlights = select_highlights(events, prefs)
        assert 5 <= len(highlights) <= 8

    def test_null_favorite_team(self) -> None:
        prefs = UserPreference(favorite_player="LeBron", favorite_team=None)
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(8)]
        highlights = select_highlights(events, prefs)
        assert 5 <= len(highlights) <= 8


class TestUnknownImportance:
    """T029: FR-012 - Unknown importance defaults to 'low'."""

    def test_unknown_importance_scores_as_low(self) -> None:
        event = _make_event(importance="ultra_rare")
        # from_dict defaults, but if constructed directly, score_event handles it
        breakdown = score_event(event)
        assert breakdown.base_score == 25  # Same as "low"

    def test_missing_importance_field(self) -> None:
        data = {
            "id": "evt-missing-imp",
            "type": "dunk",
            "timestamp": "Q1 01:00",
            "quarter": 1,
            "player": "Someone",
            "team": "TeamA",
            "description": "A play",
        }
        event = GameEvent.from_dict(data)
        assert event.importance == "low"


class TestFewerThan5Events:
    """T030: When fewer than 5 events total, return all available."""

    def test_3_events_returns_all(self) -> None:
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(3)]
        highlights = select_highlights(events)
        assert len(highlights) == 3

    def test_1_event_returns_it(self) -> None:
        events = [_make_event()]
        highlights = select_highlights(events)
        assert len(highlights) == 1

    def test_4_events_returns_all(self) -> None:
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(4)]
        highlights = select_highlights(events)
        assert len(highlights) == 4

    def test_5_events_returns_5(self) -> None:
        events = [_make_event(event_id=f"evt-{i:03d}") for i in range(5)]
        highlights = select_highlights(events)
        assert len(highlights) == 5
