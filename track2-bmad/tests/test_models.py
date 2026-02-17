"""Unit tests for data models module."""

from highlight_selector.models import GameEvent, UserPreference


def test_game_event_creation_with_all_fields():
    """Verify GameEvent instantiation with all fields provided."""
    event = GameEvent(
        id="event_001",
        type="dunk",
        timestamp="Q4 2:45",
        quarter=4,
        player="LeBron James",
        team="Lakers",
        description="Powerful dunk in transition",
        importance="critical",
        tags=["clutch", "game_winner", "fourth_quarter", "highlight_reel"],
    )

    assert event.id == "event_001"
    assert event.type == "dunk"
    assert event.timestamp == "Q4 2:45"
    assert event.quarter == 4
    assert event.player == "LeBron James"
    assert event.team == "Lakers"
    assert event.description == "Powerful dunk in transition"
    assert event.importance == "critical"
    assert event.tags == ["clutch", "game_winner", "fourth_quarter", "highlight_reel"]


def test_game_event_default_tags():
    """Verify tags defaults to empty list when not provided."""
    event = GameEvent(
        id="event_002",
        type="three_pointer",
        timestamp="Q3 5:12",
        quarter=3,
        player="Stephen Curry",
        team="Warriors",
        description="Three-pointer from downtown",
        importance="high",
    )

    assert event.tags == []
    assert isinstance(event.tags, list)


def test_game_event_field_access():
    """Verify all fields are accessible after creation."""
    event = GameEvent(
        id="event_003",
        type="block",
        timestamp="Q2 8:30",
        quarter=2,
        player="Anthony Davis",
        team="Lakers",
        description="Defensive block",
        importance="medium",
        tags=["highlight_reel"],
    )

    # Verify all fields are accessible
    fields = [
        "id",
        "type",
        "timestamp",
        "quarter",
        "player",
        "team",
        "description",
        "importance",
        "tags",
    ]
    for field_name in fields:
        assert hasattr(event, field_name), f"Field '{field_name}' not accessible"


def test_game_event_importance_values():
    """Verify all valid importance levels work correctly."""
    importance_levels = ["critical", "high", "medium", "low"]

    for i, importance in enumerate(importance_levels):
        event = GameEvent(
            id=f"event_{i}",
            type="test_play",
            timestamp="Q1 10:00",
            quarter=1,
            player="Test Player",
            team="Test Team",
            description="Test description",
            importance=importance,
        )
        assert event.importance == importance


def test_game_event_empty_tags_explicitly():
    """Verify empty tags list can be explicitly provided."""
    event = GameEvent(
        id="event_004",
        type="assist",
        timestamp="Q4 1:23",
        quarter=4,
        player="Chris Paul",
        team="Suns",
        description="Assist to teammate",
        importance="low",
        tags=[],
    )

    assert event.tags == []


def test_game_event_dataclass_features():
    """Verify dataclass auto-generated methods work correctly."""
    event1 = GameEvent(
        id="event_005",
        type="dunk",
        timestamp="Q4 0:15",
        quarter=4,
        player="Giannis Antetokounmpo",
        team="Bucks",
        description="Game-winning dunk",
        importance="critical",
        tags=["game_winner", "clutch"],
    )

    event2 = GameEvent(
        id="event_005",
        type="dunk",
        timestamp="Q4 0:15",
        quarter=4,
        player="Giannis Antetokounmpo",
        team="Bucks",
        description="Game-winning dunk",
        importance="critical",
        tags=["game_winner", "clutch"],
    )

    # Test __eq__ (dataclass generates this)
    assert event1 == event2

    # Test __repr__ (dataclass generates this)
    repr_str = repr(event1)
    assert "GameEvent" in repr_str
    assert "event_005" in repr_str


# UserPreference Tests


def test_user_preference_both_fields():
    """Verify UserPreference with both favorite_player and favorite_team."""
    pref = UserPreference(favorite_player="LeBron James", favorite_team="Lakers")

    assert pref.favorite_player == "LeBron James"
    assert pref.favorite_team == "Lakers"


def test_user_preference_player_only():
    """Verify UserPreference with only favorite_player specified."""
    pref = UserPreference(favorite_player="Stephen Curry", favorite_team=None)

    assert pref.favorite_player == "Stephen Curry"
    assert pref.favorite_team is None


def test_user_preference_team_only():
    """Verify UserPreference with only favorite_team specified."""
    pref = UserPreference(favorite_player=None, favorite_team="Celtics")

    assert pref.favorite_player is None
    assert pref.favorite_team == "Celtics"


def test_user_preference_neither_specified():
    """Verify UserPreference with both fields as None."""
    pref = UserPreference(favorite_player=None, favorite_team=None)

    assert pref.favorite_player is None
    assert pref.favorite_team is None


def test_user_preference_default_none():
    """Verify UserPreference fields default to None when not provided."""
    pref = UserPreference()

    assert pref.favorite_player is None
    assert pref.favorite_team is None


def test_user_preference_optional_fields():
    """Verify Optional[str] type hints allow None values."""
    # This test verifies type system works correctly (mypy will validate)
    pref1 = UserPreference(favorite_player="Player", favorite_team="Team")
    pref2 = UserPreference(favorite_player="Player", favorite_team=None)
    pref3 = UserPreference(favorite_player=None, favorite_team="Team")
    pref4 = UserPreference(favorite_player=None, favorite_team=None)

    assert pref1.favorite_player is not None
    assert pref2.favorite_team is None
    assert pref3.favorite_player is None
    assert pref4.favorite_player is None and pref4.favorite_team is None


# Story 1.3: ScoreBreakdown Tests


def test_score_breakdown_creation_with_all_fields():
    """Verify ScoreBreakdown instantiation with all fields."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50,
        player_boost=10,
        team_boost=5,
        context_boosts={"clutch": 15, "highlight-reel": 10},
        total_score=90,
    )
    assert breakdown.base_score == 50
    assert breakdown.player_boost == 10
    assert breakdown.team_boost == 5
    assert breakdown.context_boosts == {"clutch": 15, "highlight-reel": 10}
    assert breakdown.total_score == 90


def test_score_breakdown_context_boosts_dict():
    """Verify context_boosts is a dictionary."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50,
        player_boost=0,
        team_boost=0,
        context_boosts={"clutch": 15},
        total_score=65,
    )
    assert isinstance(breakdown.context_boosts, dict)
    assert breakdown.context_boosts["clutch"] == 15


def test_score_breakdown_total_calculation():
    """Verify total_score equals sum of all components."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50,
        player_boost=10,
        team_boost=5,
        context_boosts={"clutch": 15, "highlight-reel": 10},
        total_score=90,
    )
    calculated_total = (
        breakdown.base_score
        + breakdown.player_boost
        + breakdown.team_boost
        + sum(breakdown.context_boosts.values())
    )
    assert breakdown.total_score == calculated_total


def test_score_breakdown_empty_context_boosts():
    """Verify ScoreBreakdown with empty context_boosts."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50,
        player_boost=10,
        team_boost=5,
        context_boosts={},
        total_score=65,
    )
    assert breakdown.context_boosts == {}
    assert breakdown.total_score == 65


def test_score_breakdown_numeric_types():
    """Verify ScoreBreakdown accepts both int and float."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50.5,
        player_boost=10,
        team_boost=5.5,
        context_boosts={"clutch": 15},
        total_score=81.0,
    )
    assert isinstance(breakdown.base_score, float)
    assert isinstance(breakdown.player_boost, int)
    assert isinstance(breakdown.team_boost, float)


def test_score_breakdown_dataclass_features():
    """Verify ScoreBreakdown dataclass equality."""
    from highlight_selector.models import ScoreBreakdown

    breakdown1 = ScoreBreakdown(
        base_score=50, player_boost=10, team_boost=5, context_boosts={}, total_score=65
    )
    breakdown2 = ScoreBreakdown(
        base_score=50, player_boost=10, team_boost=5, context_boosts={}, total_score=65
    )
    assert breakdown1 == breakdown2


# Story 1.4: Highlight Tests


def test_highlight_creation_with_event_reference():
    """Verify Highlight instantiation with GameEvent reference."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    assert highlight.event == event
    assert highlight.rank == 1
    assert highlight.score == 95.5
    assert highlight.explanation == "Critical touchdown in Q3."


def test_highlight_contains_full_game_event():
    """Verify Highlight contains full GameEvent object."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    assert highlight.event.id == "evt1"
    assert highlight.event.player == "J.Allen"
    assert highlight.event.team == "BUF"


def test_highlight_rank_in_range():
    """Verify rank is an integer in range 1-8."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=5, score=85.0, explanation="Mid-game touchdown."
    )
    assert isinstance(highlight.rank, int)
    assert 1 <= highlight.rank <= 8


def test_highlight_score_numeric():
    """Verify score is numeric (int or float)."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=1, score=95, explanation="Critical touchdown in Q3."
    )
    assert isinstance(highlight.score, (int, float))


def test_highlight_explanation_non_empty():
    """Verify explanation is a non-empty string."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    assert isinstance(highlight.explanation, str)
    assert len(highlight.explanation) > 0


def test_highlight_dataclass_features():
    """Verify Highlight dataclass equality."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight1 = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    highlight2 = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    assert highlight1 == highlight2


# Story 1.5: JSON Serialization Tests


def test_game_event_to_dict():
    """Verify GameEvent.to_dict() serialization."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
        tags=["offensive"],
    )
    result = event.to_dict()
    assert result["id"] == "evt1"
    assert result["player"] == "J.Allen"
    assert result["tags"] == ["offensive"]
    assert isinstance(result, dict)


def test_game_event_from_dict():
    """Verify GameEvent.from_dict() deserialization."""
    data = {
        "id": "evt1",
        "type": "touchdown",
        "timestamp": "10:23",
        "quarter": 3,
        "player": "J.Allen",
        "team": "BUF",
        "description": "15-yard TD pass",
        "importance": "critical",
        "tags": ["offensive"],
    }
    event = GameEvent.from_dict(data)
    assert event.id == "evt1"
    assert event.player == "J.Allen"
    assert event.tags == ["offensive"]
    assert isinstance(event, GameEvent)


def test_user_preference_to_dict_with_none():
    """Verify UserPreference.to_dict() preserves None values."""
    pref = UserPreference(favorite_player="J.Allen", favorite_team=None)
    result = pref.to_dict()
    assert result["favorite_player"] == "J.Allen"
    assert result["favorite_team"] is None


def test_user_preference_from_dict():
    """Verify UserPreference.from_dict() deserialization."""
    data = {"favorite_player": "J.Allen", "favorite_team": None}
    pref = UserPreference.from_dict(data)
    assert pref.favorite_player == "J.Allen"
    assert pref.favorite_team is None
    assert isinstance(pref, UserPreference)


def test_score_breakdown_to_dict():
    """Verify ScoreBreakdown.to_dict() serialization."""
    from highlight_selector.models import ScoreBreakdown

    breakdown = ScoreBreakdown(
        base_score=50,
        player_boost=10,
        team_boost=5,
        context_boosts={"clutch": 15},
        total_score=80,
    )
    result = breakdown.to_dict()
    assert result["base_score"] == 50
    assert result["context_boosts"]["clutch"] == 15
    assert isinstance(result, dict)


def test_score_breakdown_from_dict():
    """Verify ScoreBreakdown.from_dict() deserialization."""
    from highlight_selector.models import ScoreBreakdown

    data = {
        "base_score": 50,
        "player_boost": 10,
        "team_boost": 5,
        "context_boosts": {"clutch": 15},
        "total_score": 80,
    }
    breakdown = ScoreBreakdown.from_dict(data)
    assert breakdown.base_score == 50
    assert breakdown.context_boosts["clutch"] == 15
    assert isinstance(breakdown, ScoreBreakdown)


def test_highlight_to_dict_with_nested_event():
    """Verify Highlight.to_dict() converts nested GameEvent to dict."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
    )
    highlight = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    result = highlight.to_dict()
    assert isinstance(result["event"], dict)
    assert result["event"]["id"] == "evt1"
    assert result["rank"] == 1


def test_highlight_from_dict_with_nested_event():
    """Verify Highlight.from_dict() reconstructs nested GameEvent."""
    from highlight_selector.models import Highlight

    data = {
        "event": {
            "id": "evt1",
            "type": "touchdown",
            "timestamp": "10:23",
            "quarter": 3,
            "player": "J.Allen",
            "team": "BUF",
            "description": "15-yard TD pass",
            "importance": "critical",
            "tags": [],
        },
        "rank": 1,
        "score": 95.5,
        "explanation": "Critical touchdown in Q3.",
    }
    highlight = Highlight.from_dict(data)
    assert isinstance(highlight.event, GameEvent)
    assert highlight.event.id == "evt1"
    assert highlight.rank == 1


def test_round_trip_serialization_game_event():
    """Verify GameEvent serialization round-trip preserves data."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
        tags=["offensive"],
    )
    data = event.to_dict()
    reconstructed = GameEvent.from_dict(data)
    assert reconstructed == event


def test_round_trip_serialization_highlight():
    """Verify Highlight serialization round-trip preserves data."""
    from highlight_selector.models import Highlight

    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="15-yard TD pass",
        importance="critical",
        tags=["offensive"],
    )
    highlight = Highlight(
        event=event, rank=1, score=95.5, explanation="Critical touchdown in Q3."
    )
    data = highlight.to_dict()
    reconstructed = Highlight.from_dict(data)
    assert reconstructed == highlight
    assert reconstructed.event == event
