"""Tests for the scoring algorithm in selector.py."""

from __future__ import annotations

import pytest

from highlight_selector.models import GameEvent, UserPreference
from highlight_selector.selector import score_event


def _make_event(
    importance: str = "medium",
    tags: list[str] | None = None,
    quarter: int = 2,
    player: str = "Player A",
    team: str = "Team A",
    event_id: str = "evt-test",
    event_type: str = "dunk",
) -> GameEvent:
    return GameEvent(
        id=event_id,
        type=event_type,
        timestamp=f"Q{quarter} 05:00",
        quarter=quarter,
        player=player,
        team=team,
        description="Test event",
        importance=importance,
        tags=tags if tags is not None else [],
    )


class TestBaseScoring:
    """T023: Tests for base importance scoring."""

    def test_critical_base_score(self) -> None:
        event = _make_event(importance="critical")
        breakdown = score_event(event)
        assert breakdown.base_score == 100

    def test_high_base_score(self) -> None:
        event = _make_event(importance="high")
        breakdown = score_event(event)
        assert breakdown.base_score == 75

    def test_medium_base_score(self) -> None:
        event = _make_event(importance="medium")
        breakdown = score_event(event)
        assert breakdown.base_score == 50

    def test_low_base_score(self) -> None:
        event = _make_event(importance="low")
        breakdown = score_event(event)
        assert breakdown.base_score == 25


class TestContextBoosts:
    """T024: Tests for context boosts from tags and quarter."""

    def test_clutch_boost(self) -> None:
        event = _make_event(tags=["clutch"])
        breakdown = score_event(event)
        assert breakdown.context_boosts.get("clutch") == 20

    def test_highlight_reel_boost(self) -> None:
        event = _make_event(tags=["highlight_reel"])
        breakdown = score_event(event)
        assert breakdown.context_boosts.get("highlight_reel") == 15

    def test_game_winner_boost(self) -> None:
        event = _make_event(tags=["game_winner"])
        breakdown = score_event(event)
        assert breakdown.context_boosts.get("game_winner") == 25

    def test_buzzer_beater_boost(self) -> None:
        event = _make_event(tags=["buzzer_beater"])
        breakdown = score_event(event)
        assert breakdown.context_boosts.get("buzzer_beater") == 20

    def test_fourth_quarter_boost(self) -> None:
        event = _make_event(quarter=4)
        breakdown = score_event(event)
        assert breakdown.context_boosts.get("fourth_quarter") == 10

    def test_no_fourth_quarter_boost_for_other_quarters(self) -> None:
        event = _make_event(quarter=2)
        breakdown = score_event(event)
        assert "fourth_quarter" not in breakdown.context_boosts

    def test_combined_context_boosts(self) -> None:
        event = _make_event(
            importance="high", quarter=4, tags=["clutch", "game_winner"]
        )
        breakdown = score_event(event)
        # 75 base + 20 clutch + 25 game_winner + 10 fourth_quarter = 130
        assert breakdown.total_score == 130

    def test_no_boost_for_unknown_tags(self) -> None:
        event = _make_event(tags=["some_random_tag"])
        breakdown = score_event(event)
        assert len(breakdown.context_boosts) == 0


class TestPlayerBoost:
    """T045: Tests for player preference boost."""

    def test_player_boost_applied(self) -> None:
        event = _make_event(player="LeBron James")
        prefs = UserPreference(favorite_player="LeBron James")
        breakdown = score_event(event, prefs)
        assert breakdown.player_boost == 30

    def test_no_player_boost_different_player(self) -> None:
        event = _make_event(player="Other Player")
        prefs = UserPreference(favorite_player="LeBron James")
        breakdown = score_event(event, prefs)
        assert breakdown.player_boost == 0

    def test_no_player_boost_without_preference(self) -> None:
        event = _make_event(player="LeBron James")
        prefs = UserPreference()
        breakdown = score_event(event, prefs)
        assert breakdown.player_boost == 0


class TestTeamBoost:
    """T053: Tests for team preference boost."""

    def test_team_boost_applied(self) -> None:
        event = _make_event(team="Lakers")
        prefs = UserPreference(favorite_team="Lakers")
        breakdown = score_event(event, prefs)
        assert breakdown.team_boost == 15

    def test_no_team_boost_different_team(self) -> None:
        event = _make_event(team="Celtics")
        prefs = UserPreference(favorite_team="Lakers")
        breakdown = score_event(event, prefs)
        assert breakdown.team_boost == 0

    def test_no_team_boost_without_preference(self) -> None:
        event = _make_event(team="Lakers")
        prefs = UserPreference()
        breakdown = score_event(event, prefs)
        assert breakdown.team_boost == 0
