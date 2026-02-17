"""Tests for selection, ranking, and filtering logic."""

from __future__ import annotations

from typing import Any

import pytest

from highlight_selector.models import GameEvent, UserPreference, Highlight
from highlight_selector.selector import select_highlights


def _make_event(
    event_id: str = "evt-001",
    importance: str = "medium",
    quarter: int = 2,
    player: str = "Player A",
    team: str = "Team A",
    tags: list[str] | None = None,
    event_type: str = "dunk",
) -> GameEvent:
    return GameEvent(
        id=event_id,
        type=event_type,
        timestamp=f"Q{quarter} 05:00",
        quarter=quarter,
        player=player,
        team=team,
        description=f"Test event {event_id}",
        importance=importance,
        tags=tags if tags is not None else [],
    )


def _make_events_with_varying_importance(count: int = 15) -> list[GameEvent]:
    """Generate a diverse set of events for testing."""
    importances = [
        "critical",
        "high",
        "high",
        "high",
        "medium",
        "medium",
        "medium",
        "medium",
        "low",
        "low",
        "low",
        "low",
        "low",
        "low",
        "low",
    ]
    events = []
    for i in range(min(count, len(importances))):
        events.append(
            _make_event(
                event_id=f"evt-{i+1:03d}",
                importance=importances[i],
                quarter=(i % 4) + 1,
                player=f"Player {chr(65 + i % 5)}",
                team="Team A" if i % 2 == 0 else "Team B",
                tags=["clutch"] if importances[i] == "critical" else [],
            )
        )
    return events


class TestRankingOrder:
    """T025: Tests for ranking (score descending), critical inclusion, and count constraints."""

    def test_highlights_ranked_by_score_descending(self) -> None:
        events = _make_events_with_varying_importance()
        highlights = select_highlights(events)
        scores = [h.score for h in highlights]
        assert scores == sorted(scores, reverse=True)

    def test_returns_5_to_8_highlights(self) -> None:
        """FR-005: System returns 5-8 highlights."""
        events = _make_events_with_varying_importance(15)
        highlights = select_highlights(events)
        assert 5 <= len(highlights) <= 8

    def test_critical_events_always_included(self) -> None:
        """FR-006: All critical events must be in output."""
        events = _make_events_with_varying_importance()
        highlights = select_highlights(events)
        critical_in_highlights = [
            h for h in highlights if h.event.importance == "critical"
        ]
        critical_in_events = [e for e in events if e.importance == "critical"]
        assert len(critical_in_highlights) == len(critical_in_events)

    def test_rank_values_are_sequential(self) -> None:
        events = _make_events_with_varying_importance()
        highlights = select_highlights(events)
        ranks = [h.rank for h in highlights]
        assert ranks == list(range(1, len(highlights) + 1))


class TestTieBreaking:
    """T026: Tests for three-level tie-breaking."""

    def test_tie_break_by_quarter_descending(self) -> None:
        """Higher quarter wins when scores are equal."""
        evt_q2 = _make_event(event_id="evt-a", importance="medium", quarter=2)
        evt_q4 = _make_event(event_id="evt-b", importance="medium", quarter=4)
        # Add filler events to meet minimum
        fillers = [
            _make_event(event_id=f"evt-f{i}", importance="low", quarter=1)
            for i in range(6)
        ]
        highlights = select_highlights([evt_q2, evt_q4] + fillers)
        # Q4 event should rank higher than Q2 with same importance
        q4_highlight = next(h for h in highlights if h.event.id == "evt-b")
        q2_highlight = next(h for h in highlights if h.event.id == "evt-a")
        assert q4_highlight.rank < q2_highlight.rank

    def test_tie_break_by_importance_descending(self) -> None:
        """Higher importance wins when scores and quarters are equal."""
        # Same quarter, different importance level but same base through context
        evt_high = _make_event(event_id="evt-a", importance="high", quarter=3)
        evt_med_boost = _make_event(
            event_id="evt-b",
            importance="medium",
            quarter=3,
            tags=["game_winner"],  # +25 boost brings medium(50)+25=75 = high(75)
        )
        fillers = [
            _make_event(event_id=f"evt-f{i}", importance="low", quarter=1)
            for i in range(6)
        ]
        highlights = select_highlights([evt_high, evt_med_boost] + fillers)
        high_hl = next(h for h in highlights if h.event.id == "evt-a")
        med_hl = next(h for h in highlights if h.event.id == "evt-b")
        assert high_hl.rank < med_hl.rank

    def test_tie_break_by_event_id_ascending(self) -> None:
        """Alphabetical event ID as final deterministic fallback."""
        evt_a = _make_event(event_id="evt-aaa", importance="medium", quarter=2)
        evt_b = _make_event(event_id="evt-zzz", importance="medium", quarter=2)
        fillers = [
            _make_event(event_id=f"evt-f{i}", importance="low", quarter=1)
            for i in range(6)
        ]
        highlights = select_highlights([evt_b, evt_a] + fillers)
        hl_a = next(h for h in highlights if h.event.id == "evt-aaa")
        hl_b = next(h for h in highlights if h.event.id == "evt-zzz")
        assert hl_a.rank < hl_b.rank


class TestDeterminism:
    """T031: Verify identical inputs produce identical outputs (FR-009, SC-004)."""

    def test_identical_inputs_produce_identical_outputs(self) -> None:
        events = _make_events_with_varying_importance()
        prefs = UserPreference(favorite_player="Player A")

        result1 = select_highlights(events, prefs)
        result2 = select_highlights(events, prefs)

        assert len(result1) == len(result2)
        for h1, h2 in zip(result1, result2):
            assert h1.event.id == h2.event.id
            assert h1.rank == h2.rank
            assert h1.score == h2.score
            assert h1.explanation == h2.explanation

    def test_determinism_multiple_runs(self) -> None:
        events = _make_events_with_varying_importance()
        results = [select_highlights(events) for _ in range(10)]
        first = results[0]
        for result in results[1:]:
            ids_first = [h.event.id for h in first]
            ids_result = [h.event.id for h in result]
            assert ids_first == ids_result


class TestPlayerSelection:
    """T046-T048: Tests for player-based personalization in selection."""

    def test_50_percent_player_involvement(self) -> None:
        """FR-014: At least 50% of highlights feature favorite player when enough events exist."""
        # Create 15 events: 8 involve LeBron
        events = []
        for i in range(8):
            events.append(
                _make_event(
                    event_id=f"evt-lb-{i:02d}",
                    player="LeBron James",
                    team="Lakers",
                    importance="high" if i < 4 else "medium",
                    quarter=(i % 4) + 1,
                )
            )
        for i in range(7):
            events.append(
                _make_event(
                    event_id=f"evt-ot-{i:02d}",
                    player="Other Player",
                    team="Celtics",
                    importance="high" if i < 2 else "medium",
                    quarter=(i % 4) + 1,
                )
            )

        prefs = UserPreference(favorite_player="LeBron James")
        highlights = select_highlights(events, prefs)

        lebron_count = sum(1 for h in highlights if h.event.player == "LeBron James")
        assert (
            lebron_count >= len(highlights) / 2
        ), f"Expected at least 50% LeBron highlights, got {lebron_count}/{len(highlights)}"

    def test_critical_non_player_events_still_included(self) -> None:
        """Game narrative maintained: critical opponent plays still included."""
        events = [
            _make_event(
                event_id="evt-crit",
                player="Opponent Star",
                team="Celtics",
                importance="critical",
                quarter=4,
                tags=["game_winner"],
            ),
        ]
        # Add LeBron events
        for i in range(10):
            events.append(
                _make_event(
                    event_id=f"evt-lb-{i:02d}",
                    player="LeBron James",
                    team="Lakers",
                    importance="high" if i < 5 else "medium",
                    quarter=(i % 4) + 1,
                )
            )

        prefs = UserPreference(favorite_player="LeBron James")
        highlights = select_highlights(events, prefs)

        critical_ids = [h.event.id for h in highlights if h.event.id == "evt-crit"]
        assert len(critical_ids) == 1, "Critical non-player event must be included"

    def test_no_favorite_player_events_fallback(self) -> None:
        """When no events match favorite player, fall back to basic selection."""
        events = _make_events_with_varying_importance()
        prefs = UserPreference(favorite_player="Nonexistent Player")
        highlights = select_highlights(events, prefs)
        assert 5 <= len(highlights) <= 8


class TestTeamSelection:
    """T054-T056: Tests for team-based personalization in selection."""

    def test_team_weighting(self) -> None:
        """Highlights should be weighted toward favorite team."""
        events = []
        for i in range(8):
            events.append(
                _make_event(
                    event_id=f"evt-la-{i:02d}",
                    team="Lakers",
                    importance="medium",
                    quarter=(i % 4) + 1,
                )
            )
        for i in range(7):
            events.append(
                _make_event(
                    event_id=f"evt-ce-{i:02d}",
                    team="Celtics",
                    importance="medium",
                    quarter=(i % 4) + 1,
                )
            )

        prefs = UserPreference(favorite_team="Lakers")
        highlights = select_highlights(events, prefs)
        lakers_count = sum(1 for h in highlights if h.event.team == "Lakers")
        celtics_count = sum(1 for h in highlights if h.event.team == "Celtics")
        assert lakers_count > celtics_count

    def test_opponent_critical_play_included(self) -> None:
        """FR-015: Critical opponent plays included for game narrative."""
        events = [
            _make_event(
                event_id="evt-opp-crit",
                team="Celtics",
                importance="critical",
                quarter=4,
            ),
        ]
        for i in range(10):
            events.append(
                _make_event(
                    event_id=f"evt-la-{i:02d}",
                    team="Lakers",
                    importance="high" if i < 5 else "medium",
                    quarter=(i % 4) + 1,
                )
            )

        prefs = UserPreference(favorite_team="Lakers")
        highlights = select_highlights(events, prefs)
        opp_in = any(h.event.id == "evt-opp-crit" for h in highlights)
        assert opp_in, "Critical opponent play must be included"

    def test_both_player_and_team_preferences(self) -> None:
        """T056: When both player and team preferences set, player takes precedence."""
        events = []
        # Player event on other team
        events.append(
            _make_event(
                event_id="evt-player-other-team",
                player="LeBron James",
                team="Celtics",
                importance="medium",
                quarter=3,
            )
        )
        # Team event with other player
        events.append(
            _make_event(
                event_id="evt-team-other-player",
                player="Davis",
                team="Lakers",
                importance="medium",
                quarter=3,
            )
        )
        # Filler events
        for i in range(6):
            events.append(
                _make_event(
                    event_id=f"evt-fill-{i:02d}",
                    player="Other",
                    team="Other",
                    importance="low",
                    quarter=1,
                )
            )

        prefs = UserPreference(favorite_player="LeBron James", favorite_team="Lakers")
        highlights = select_highlights(events, prefs)

        player_event = next(
            (h for h in highlights if h.event.id == "evt-player-other-team"), None
        )
        team_event = next(
            (h for h in highlights if h.event.id == "evt-team-other-player"), None
        )

        # Player boost (+30) > team boost (+15), so player event should rank higher
        assert player_event is not None
        assert team_event is not None
        assert player_event.score > team_event.score
