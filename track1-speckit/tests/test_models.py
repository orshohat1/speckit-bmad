"""Tests for data models: dataclass creation, field validation, and JSON serialization."""

from __future__ import annotations

import pytest

from highlight_selector.models import (
    GameEvent,
    Highlight,
    ScoreBreakdown,
    UserPreference,
    IMPORTANCE_RANK,
)


class TestGameEvent:
    """Tests for the GameEvent dataclass."""

    def test_create_game_event(self) -> None:
        event = GameEvent(
            id="evt-001",
            type="dunk",
            timestamp="Q4 02:15",
            quarter=4,
            player="LeBron James",
            team="Lakers",
            description="A thunderous dunk.",
            importance="high",
            tags=["highlight_reel"],
        )
        assert event.id == "evt-001"
        assert event.type == "dunk"
        assert event.quarter == 4
        assert event.importance == "high"
        assert event.tags == ["highlight_reel"]

    def test_default_tags_empty_list(self) -> None:
        event = GameEvent(
            id="evt-002",
            type="block",
            timestamp="Q1 05:00",
            quarter=1,
            player="Davis",
            team="Lakers",
            description="Block",
            importance="medium",
        )
        assert event.tags == []

    def test_to_dict(self) -> None:
        event = GameEvent(
            id="evt-001",
            type="dunk",
            timestamp="Q4 02:15",
            quarter=4,
            player="LeBron",
            team="Lakers",
            description="Dunk",
            importance="high",
            tags=["clutch"],
        )
        d = event.to_dict()
        assert d["id"] == "evt-001"
        assert d["importance"] == "high"
        assert d["tags"] == ["clutch"]

    def test_from_dict(self) -> None:
        data = {
            "id": "evt-003",
            "type": "three_pointer",
            "timestamp": "Q2 08:00",
            "quarter": 2,
            "player": "Curry",
            "team": "Warriors",
            "description": "Three pointer",
            "importance": "critical",
            "tags": ["game_winner"],
        }
        event = GameEvent.from_dict(data)
        assert event.id == "evt-003"
        assert event.importance == "critical"
        assert event.tags == ["game_winner"]

    def test_from_dict_unknown_importance_defaults_to_low(self) -> None:
        """FR-012: Unknown importance defaults to 'low'."""
        data = {
            "id": "evt-004",
            "type": "foul",
            "timestamp": "Q1 01:00",
            "quarter": 1,
            "player": "Someone",
            "team": "TeamA",
            "description": "Foul",
            "importance": "ultra_rare",
            "tags": [],
        }
        event = GameEvent.from_dict(data)
        assert event.importance == "low"

    def test_from_dict_missing_importance_defaults_to_low(self) -> None:
        data = {
            "id": "evt-005",
            "type": "foul",
            "timestamp": "Q1 01:00",
            "quarter": 1,
            "player": "Someone",
            "team": "TeamA",
            "description": "Foul",
        }
        event = GameEvent.from_dict(data)
        assert event.importance == "low"

    def test_from_dict_missing_optional_fields(self) -> None:
        data = {
            "id": "evt-006",
            "type": "assist",
        }
        event = GameEvent.from_dict(data)
        assert event.timestamp == ""
        assert event.quarter == 1
        assert event.player == "Unknown"
        assert event.team == "Unknown"
        assert event.tags == []

    def test_round_trip_serialization(self) -> None:
        event = GameEvent(
            id="evt-010",
            type="steal",
            timestamp="Q3 09:00",
            quarter=3,
            player="Brown",
            team="Celtics",
            description="Steal and score",
            importance="medium",
            tags=["fast_break", "transition"],
        )
        d = event.to_dict()
        restored = GameEvent.from_dict(d)
        assert restored == event


class TestUserPreference:
    """Tests for the UserPreference dataclass."""

    def test_no_preferences(self) -> None:
        prefs = UserPreference()
        assert prefs.favorite_player is None
        assert prefs.favorite_team is None

    def test_player_preference(self) -> None:
        prefs = UserPreference(favorite_player="LeBron James")
        assert prefs.favorite_player == "LeBron James"
        assert prefs.favorite_team is None

    def test_team_preference(self) -> None:
        prefs = UserPreference(favorite_team="Celtics")
        assert prefs.favorite_team == "Celtics"

    def test_both_preferences(self) -> None:
        prefs = UserPreference(favorite_player="Davis", favorite_team="Lakers")
        assert prefs.favorite_player == "Davis"
        assert prefs.favorite_team == "Lakers"

    def test_to_dict(self) -> None:
        prefs = UserPreference(favorite_player="Curry")
        d = prefs.to_dict()
        assert d == {"favorite_player": "Curry", "favorite_team": None}

    def test_from_dict(self) -> None:
        data = {"favorite_player": "LeBron", "favorite_team": "Lakers"}
        prefs = UserPreference.from_dict(data)
        assert prefs.favorite_player == "LeBron"
        assert prefs.favorite_team == "Lakers"

    def test_from_dict_none_input(self) -> None:
        """FR-011: None input treated as no preference."""
        prefs = UserPreference.from_dict(None)
        assert prefs.favorite_player is None
        assert prefs.favorite_team is None

    def test_round_trip_serialization(self) -> None:
        prefs = UserPreference(favorite_player="Tatum", favorite_team="Celtics")
        d = prefs.to_dict()
        restored = UserPreference.from_dict(d)
        assert restored == prefs


class TestScoreBreakdown:
    """Tests for the ScoreBreakdown dataclass."""

    def test_auto_calculate_total(self) -> None:
        breakdown = ScoreBreakdown(
            base_score=75,
            player_boost=30,
            team_boost=0,
            context_boosts={"clutch": 20, "fourth_quarter": 10},
        )
        assert breakdown.total_score == 135

    def test_explicit_total(self) -> None:
        breakdown = ScoreBreakdown(
            base_score=50,
            player_boost=0,
            team_boost=15,
            context_boosts={},
            total_score=999,
        )
        assert breakdown.total_score == 999

    def test_to_dict(self) -> None:
        breakdown = ScoreBreakdown(
            base_score=100,
            player_boost=0,
            team_boost=0,
            context_boosts={"game_winner": 25},
        )
        d = breakdown.to_dict()
        assert d["base_score"] == 100
        assert d["total_score"] == 125
        assert d["context_boosts"] == {"game_winner": 25}

    def test_from_dict(self) -> None:
        data = {
            "base_score": 75,
            "player_boost": 30,
            "team_boost": 15,
            "context_boosts": {"clutch": 20},
            "total_score": 140,
        }
        breakdown = ScoreBreakdown.from_dict(data)
        assert breakdown.total_score == 140

    def test_round_trip_serialization(self) -> None:
        breakdown = ScoreBreakdown(
            base_score=50,
            player_boost=30,
            team_boost=15,
            context_boosts={"buzzer_beater": 20},
        )
        d = breakdown.to_dict()
        restored = ScoreBreakdown.from_dict(d)
        assert restored.total_score == breakdown.total_score
        assert restored.base_score == breakdown.base_score


class TestHighlight:
    """Tests for the Highlight dataclass."""

    def _make_event(self) -> GameEvent:
        return GameEvent(
            id="evt-001",
            type="dunk",
            timestamp="Q4 11:30",
            quarter=4,
            player="LeBron",
            team="Lakers",
            description="Game-winning dunk",
            importance="critical",
            tags=["game_winner"],
        )

    def test_create_highlight(self) -> None:
        event = self._make_event()
        hl = Highlight(event=event, rank=1, score=145, explanation="A critical play.")
        assert hl.rank == 1
        assert hl.score == 145
        assert hl.explanation == "A critical play."

    def test_to_dict(self) -> None:
        event = self._make_event()
        hl = Highlight(event=event, rank=1, score=145, explanation="Critical play.")
        d = hl.to_dict()
        assert d["rank"] == 1
        assert d["score"] == 145
        assert d["event"]["id"] == "evt-001"

    def test_from_dict(self) -> None:
        data = {
            "event": {
                "id": "evt-001",
                "type": "dunk",
                "timestamp": "Q4 11:30",
                "quarter": 4,
                "player": "LeBron",
                "team": "Lakers",
                "description": "Dunk",
                "importance": "critical",
                "tags": ["game_winner"],
            },
            "rank": 1,
            "score": 145,
            "explanation": "Great play.",
        }
        hl = Highlight.from_dict(data)
        assert hl.rank == 1
        assert hl.event.id == "evt-001"

    def test_round_trip_serialization(self) -> None:
        event = self._make_event()
        hl = Highlight(event=event, rank=2, score=120, explanation="High impact.")
        d = hl.to_dict()
        restored = Highlight.from_dict(d)
        assert restored.rank == hl.rank
        assert restored.event == hl.event


class TestImportanceRank:
    """Tests for the IMPORTANCE_RANK mapping."""

    def test_all_levels_present(self) -> None:
        assert set(IMPORTANCE_RANK.keys()) == {"critical", "high", "medium", "low"}

    def test_ordering(self) -> None:
        assert IMPORTANCE_RANK["critical"] > IMPORTANCE_RANK["high"]
        assert IMPORTANCE_RANK["high"] > IMPORTANCE_RANK["medium"]
        assert IMPORTANCE_RANK["medium"] > IMPORTANCE_RANK["low"]
