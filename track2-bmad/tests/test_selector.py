"""Unit tests for selector module scoring functions."""

from highlight_selector.models import GameEvent, UserPreference, ScoreBreakdown
from highlight_selector.selector import (
    calculate_base_score,
    calculate_player_boost,
    calculate_team_boost,
    calculate_context_boosts,
    calculate_score,
)


# Story 2.1: Base Importance Scoring Tests


def test_calculate_base_score_critical():
    """Verify critical importance returns 100 points."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="Critical TD",
        importance="critical",
    )
    assert calculate_base_score(event) == 100


def test_calculate_base_score_high():
    """Verify high importance returns 75 points."""
    event = GameEvent(
        id="evt2",
        type="interception",
        timestamp="08:15",
        quarter=2,
        player="S.Gilmore",
        team="BUF",
        description="Red zone INT",
        importance="high",
    )
    assert calculate_base_score(event) == 75


def test_calculate_base_score_medium():
    """Verify medium importance returns 50 points."""
    event = GameEvent(
        id="evt3",
        type="first_down",
        timestamp="12:00",
        quarter=1,
        player="D.Henry",
        team="TEN",
        description="First down run",
        importance="medium",
    )
    assert calculate_base_score(event) == 50


def test_calculate_base_score_low():
    """Verify low importance returns 25 points."""
    event = GameEvent(
        id="evt4",
        type="tackle",
        timestamp="05:30",
        quarter=4,
        player="T.Watt",
        team="PIT",
        description="Solo tackle",
        importance="low",
    )
    assert calculate_base_score(event) == 25


def test_calculate_base_score_unknown_defaults_to_low():
    """Verify unknown importance defaults to low (25 points)."""
    event = GameEvent(
        id="evt5",
        type="penalty",
        timestamp="03:45",
        quarter=2,
        player="Unknown",
        team="DAL",
        description="False start",
        importance="very_high",  # Unknown importance
    )
    assert calculate_base_score(event) == 25


def test_calculate_base_score_deterministic():
    """Verify same input always returns same output."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="Critical TD",
        importance="critical",
    )
    result1 = calculate_base_score(event)
    result2 = calculate_base_score(event)
    assert result1 == result2 == 100


# Story 2.2: Player Preference Boost Tests


def test_calculate_player_boost_match():
    """Verify +30 boost when player matches favorite."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_player="J.Allen")
    assert calculate_player_boost(event, pref) == 30


def test_calculate_player_boost_no_match():
    """Verify 0 boost when player does not match."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="T.Brady",
        team="TB",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_player="J.Allen")
    assert calculate_player_boost(event, pref) == 0


def test_calculate_player_boost_no_favorite_specified():
    """Verify 0 boost when no favorite player specified."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_player=None)
    assert calculate_player_boost(event, pref) == 0


def test_calculate_player_boost_case_sensitive():
    """Verify player name matching is case-sensitive."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_player="j.allen")  # lowercase
    assert calculate_player_boost(event, pref) == 0


def test_calculate_player_boost_handles_none_preference():
    """Verify function handles None preference without error."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    # Pass None as preference should not raise error
    assert calculate_player_boost(event, None) == 0


# Story 2.3: Team Preference Boost Tests


def test_calculate_team_boost_match():
    """Verify +15 boost when team matches favorite."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_team="BUF")
    assert calculate_team_boost(event, pref) == 15


def test_calculate_team_boost_no_match():
    """Verify 0 boost when team does not match."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="T.Brady",
        team="TB",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_team="NE")
    assert calculate_team_boost(event, pref) == 0


def test_calculate_team_boost_no_favorite_specified():
    """Verify 0 boost when no favorite team specified."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_team=None)
    assert calculate_team_boost(event, pref) == 0


def test_calculate_team_boost_case_sensitive():
    """Verify team name matching is case-sensitive."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    pref = UserPreference(favorite_team="buf")  # lowercase
    assert calculate_team_boost(event, pref) == 0


def test_calculate_team_boost_handles_none_preference():
    """Verify function handles None preference without error."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="critical",
    )
    assert calculate_team_boost(event, None) == 0


# Story 2.4: Context Tag Boosts Tests


def test_calculate_context_boosts_clutch():
    """Verify clutch tag adds +20 points."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="Game-tying TD",
        importance="critical",
        tags=["clutch"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"clutch": 20}


def test_calculate_context_boosts_game_winner():
    """Verify game_winner tag adds +25 points."""
    event = GameEvent(
        id="evt2",
        type="field_goal",
        timestamp="00:01",
        quarter=4,
        player="T.Bass",
        team="BUF",
        description="Game-winning FG",
        importance="critical",
        tags=["game_winner"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"game_winner": 25}


def test_calculate_context_boosts_buzzer_beater():
    """Verify buzzer_beater tag adds +15 points."""
    event = GameEvent(
        id="evt3",
        type="field_goal",
        timestamp="00:00",
        quarter=2,
        player="T.Bass",
        team="BUF",
        description="Half-ending FG",
        importance="high",
        tags=["buzzer_beater"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"buzzer_beater": 15}


def test_calculate_context_boosts_highlight_reel():
    """Verify highlight_reel tag adds +15 points."""
    event = GameEvent(
        id="evt4",
        type="catch",
        timestamp="08:30",
        quarter=3,
        player="D.Adams",
        team="GB",
        description="One-handed catch",
        importance="high",
        tags=["highlight_reel"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"highlight_reel": 15}


def test_calculate_context_boosts_fourth_quarter():
    """Verify fourth_quarter tag adds +10 points."""
    event = GameEvent(
        id="evt5",
        type="interception",
        timestamp="03:15",
        quarter=4,
        player="T.White",
        team="BUF",
        description="Late INT",
        importance="high",
        tags=["fourth_quarter"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"fourth_quarter": 10}


def test_calculate_context_boosts_multiple_tags():
    """Verify multiple tags accumulate correctly."""
    event = GameEvent(
        id="evt6",
        type="touchdown",
        timestamp="01:30",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="Clutch fourth quarter TD",
        importance="critical",
        tags=["clutch", "fourth_quarter"],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {"clutch": 20, "fourth_quarter": 10}
    assert sum(boosts.values()) == 30


def test_calculate_context_boosts_unknown_tags_ignored():
    """Verify unknown tags are ignored."""
    event = GameEvent(
        id="evt7",
        type="sack",
        timestamp="07:00",
        quarter=2,
        player="M.Garrett",
        team="CLE",
        description="QB sack",
        importance="medium",
        tags=["defensive", "unknown_tag"],  # Unknown tags
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {}


def test_calculate_context_boosts_no_tags():
    """Verify empty dict when event has no tags."""
    event = GameEvent(
        id="evt8",
        type="run",
        timestamp="11:00",
        quarter=1,
        player="D.Henry",
        team="TEN",
        description="5-yard run",
        importance="low",
        tags=[],
    )
    boosts = calculate_context_boosts(event)
    assert boosts == {}


# Story 2.5: Total Score Calculation with Breakdown Tests


def test_calculate_score_all_components():
    """Verify complete score calculation with all components."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="01:30",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="Clutch TD",
        importance="critical",
        tags=["clutch", "fourth_quarter"],
    )
    pref = UserPreference(favorite_player="J.Allen", favorite_team="BUF")

    breakdown = calculate_score(event, pref)

    assert breakdown.base_score == 100  # critical
    assert breakdown.player_boost == 30  # favorite player
    assert breakdown.team_boost == 15  # favorite team
    assert breakdown.context_boosts == {"clutch": 20, "fourth_quarter": 10}
    assert breakdown.total_score == 175  # 100 + 30 + 15 + 20 + 10


def test_calculate_score_no_preferences():
    """Verify score calculation with None preference."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="01:30",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="high",
        tags=["highlight_reel"],
    )

    breakdown = calculate_score(event, None)

    assert breakdown.base_score == 75  # high
    assert breakdown.player_boost == 0  # no preference
    assert breakdown.team_boost == 0  # no preference
    assert breakdown.context_boosts == {"highlight_reel": 15}
    assert breakdown.total_score == 90  # 75 + 0 + 0 + 15


def test_calculate_score_partial_preference():
    """Verify score calculation with only player preference."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="01:30",
        quarter=4,
        player="J.Allen",
        team="BUF",
        description="TD pass",
        importance="medium",
    )
    pref = UserPreference(favorite_player="J.Allen", favorite_team=None)

    breakdown = calculate_score(event, pref)

    assert breakdown.base_score == 50  # medium
    assert breakdown.player_boost == 30  # favorite player
    assert breakdown.team_boost == 0  # no favorite team
    assert breakdown.context_boosts == {}  # no tags
    assert breakdown.total_score == 80  # 50 + 30 + 0 + 0


def test_calculate_score_no_boosts():
    """Verify score calculation with only base score."""
    event = GameEvent(
        id="evt1",
        type="tackle",
        timestamp="09:00",
        quarter=2,
        player="D.Jones",
        team="NYG",
        description="Routine tackle",
        importance="low",
    )
    pref = UserPreference(favorite_player="J.Allen", favorite_team="BUF")

    breakdown = calculate_score(event, pref)

    assert breakdown.base_score == 25  # low
    assert breakdown.player_boost == 0  # no match
    assert breakdown.team_boost == 0  # no match
    assert breakdown.context_boosts == {}  # no tags
    assert breakdown.total_score == 25  # 25 + 0 + 0 + 0


def test_calculate_score_returns_score_breakdown():
    """Verify function returns ScoreBreakdown instance."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="10:23",
        quarter=3,
        player="J.Allen",
        team="BUF",
        description="TD",
        importance="critical",
    )
    pref = UserPreference(favorite_player="J.Allen")

    breakdown = calculate_score(event, pref)

    assert isinstance(breakdown, ScoreBreakdown)


def test_calculate_score_total_matches_sum():
    """Verify total_score equals sum of all components."""
    event = GameEvent(
        id="evt1",
        type="touchdown",
        timestamp="01:30",
        quarter=4,
        player="T.Kelce",
        team="KC",
        description="Game winner",
        importance="critical",
        tags=["clutch", "game_winner", "highlight_reel"],
    )
    pref = UserPreference(favorite_player="T.Kelce", favorite_team="KC")

    breakdown = calculate_score(event, pref)

    expected_total = (
        breakdown.base_score
        + breakdown.player_boost
        + breakdown.team_boost
        + sum(breakdown.context_boosts.values())
    )
    assert breakdown.total_score == expected_total
