"""End-to-end integration tests for the AI Highlight Selector."""

from __future__ import annotations

import json
import time
from typing import Any

import pytest

from highlight_selector.models import GameEvent, Highlight, UserPreference
from highlight_selector.selector import select_highlights
from highlight_selector.cli import parse_input, format_output


class TestEndToEndFlow:
    """T063: End-to-end test: JSON input → select_highlights() → JSON output."""

    def test_json_input_to_json_output(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        # Parse raw event dicts into GameEvent objects
        events = [GameEvent.from_dict(e) for e in sample_events]
        prefs = UserPreference(favorite_player="LeBron James")

        # Run selection
        highlights = select_highlights(events, prefs)

        # Format as output
        output = format_output(highlights, len(events), prefs)

        # Verify output structure
        assert "highlights" in output
        assert "metadata" in output
        assert output["metadata"]["total_events"] == 15
        assert 5 <= output["metadata"]["selected_count"] <= 8
        assert output["metadata"]["preferences"]["favorite_player"] == "LeBron James"

        # Verify highlights are serializable to JSON
        json_str = json.dumps(output)
        parsed_back = json.loads(json_str)
        assert len(parsed_back["highlights"]) == output["metadata"]["selected_count"]

    def test_each_highlight_has_all_fields(self, sample_game_events: list[Any]) -> None:
        highlights = select_highlights(sample_game_events)
        for h in highlights:
            assert h.event is not None
            assert h.rank > 0
            assert h.score > 0
            assert len(h.explanation) > 0


class TestAllUserStoriesTogether:
    """T064: Integration test for all 5 user stories working together."""

    def test_us1_basic_selection(self, sample_game_events: list[Any]) -> None:
        """US-1: Basic highlight selection returns 5-8 ranked highlights."""
        highlights = select_highlights(sample_game_events)
        assert 5 <= len(highlights) <= 8
        scores = [h.score for h in highlights]
        assert scores == sorted(scores, reverse=True)

    def test_us2_player_personalization(self, sample_game_events: list[Any]) -> None:
        """US-2: Player preference boosts player events."""
        prefs = UserPreference(favorite_player="LeBron James")
        highlights = select_highlights(sample_game_events, prefs)

        lebron_count = sum(1 for h in highlights if h.event.player == "LeBron James")
        # LeBron has 5 events in sample data, with boost should dominate
        assert lebron_count >= len(highlights) // 2

    def test_us3_team_personalization(self, sample_game_events: list[Any]) -> None:
        """US-3: Team preference boosts team events."""
        prefs = UserPreference(favorite_team="Celtics")
        highlights = select_highlights(sample_game_events, prefs)

        # Celtics events should have boost, but critical Lakers events still included
        assert len(highlights) >= 5

    def test_us4_explanations(self, sample_game_events: list[Any]) -> None:
        """US-4: Every highlight has an explanation."""
        highlights = select_highlights(sample_game_events)
        for h in highlights:
            assert h.explanation
            assert len(h.explanation) > 10

    def test_us5_edge_cases(self) -> None:
        """US-5: Edge cases handled gracefully."""
        # Empty list
        assert select_highlights([]) == []

        # None prefs
        event = GameEvent(
            id="e1",
            type="dunk",
            timestamp="Q1 01:00",
            quarter=1,
            player="P",
            team="T",
            description="D",
            importance="medium",
        )
        result = select_highlights([event], None)
        assert len(result) == 1

    def test_all_stories_combined(self, sample_game_events: list[Any]) -> None:
        """All user stories working simultaneously with both preferences."""
        prefs = UserPreference(favorite_player="LeBron James", favorite_team="Lakers")
        highlights = select_highlights(sample_game_events, prefs)

        # US-1: 5-8 highlights
        assert 5 <= len(highlights) <= 8

        # US-2/3: Boosts applied (LeBron/Lakers should be well represented)
        lebron_or_lakers = sum(
            1
            for h in highlights
            if h.event.player == "LeBron James" or h.event.team == "Lakers"
        )
        assert lebron_or_lakers >= len(highlights) // 2

        # US-4: All have explanations
        assert all(h.explanation for h in highlights)

        # US-5: Critical event included regardless
        critical_events = [h for h in highlights if h.event.importance == "critical"]
        assert len(critical_events) >= 1

        # FR-009: Deterministic
        highlights2 = select_highlights(sample_game_events, prefs)
        assert [h.event.id for h in highlights] == [h.event.id for h in highlights2]


class TestSampleDataIntegration:
    """T065: Integration tests using shared/sample_data.json as fixture."""

    def test_sample_data_no_preferences(
        self, sample_game_events: list[Any], no_preference: Any
    ) -> None:
        highlights = select_highlights(sample_game_events, no_preference)
        assert 5 <= len(highlights) <= 8

        # Critical event (evt-014, LeBron game-winning dunk) must be included
        critical = [h for h in highlights if h.event.id == "evt-014"]
        assert len(critical) == 1
        assert critical[0].rank == 1  # Should be #1 ranked

    def test_sample_data_lebron_preference(
        self, sample_game_events: list[Any], lebron_preference: Any
    ) -> None:
        highlights = select_highlights(sample_game_events, lebron_preference)
        lebron_count = sum(1 for h in highlights if h.event.player == "LeBron James")
        # LeBron has 5 events, with +30 boost should be well represented
        assert lebron_count >= 3

    def test_sample_data_celtics_preference(
        self, sample_game_events: list[Any], celtics_preference: Any
    ) -> None:
        highlights = select_highlights(sample_game_events, celtics_preference)
        # Celtics events get +15 boost
        assert len(highlights) >= 5

        # Critical Lakers event (game winner) should still be included
        critical = [h for h in highlights if h.event.id == "evt-014"]
        assert len(critical) == 1

    def test_sample_data_davis_lakers_preference(
        self, sample_game_events: list[Any], davis_lakers_preference: Any
    ) -> None:
        highlights = select_highlights(sample_game_events, davis_lakers_preference)
        assert 5 <= len(highlights) <= 8

    def test_cli_parse_full_sample_data(self, sample_data: dict[str, Any]) -> None:
        """Test CLI parsing of the full sample_data.json format."""
        raw = json.dumps(sample_data)
        events, prefs = parse_input(raw)
        assert len(events) == 15
        # First user_preference example is used
        assert prefs.favorite_player == "LeBron James"

    def test_cli_parse_events_only(self, sample_data: dict[str, Any]) -> None:
        """Test CLI parsing with just events key."""
        events_only = json.dumps({"events": sample_data["events"]})
        events, prefs = parse_input(events_only)
        assert len(events) == 15
        assert prefs.favorite_player is None
        assert prefs.favorite_team is None


class TestPerformance:
    """T067-T068: Performance benchmarks."""

    def test_performance_15_events(self, sample_game_events: list[Any]) -> None:
        """SC-001: Process 15 events in under 100ms."""
        start = time.perf_counter()
        for _ in range(100):
            select_highlights(sample_game_events)
        elapsed = (time.perf_counter() - start) / 100
        assert elapsed < 0.1, f"Average time {elapsed:.4f}s exceeds 100ms"

    def test_performance_1000_events(self) -> None:
        """SC-005: Process 1000 events in under 1 second."""
        events = []
        importances = ["critical", "high", "medium", "low"]
        for i in range(1000):
            events.append(
                GameEvent(
                    id=f"evt-{i:04d}",
                    type="dunk",
                    timestamp=f"Q{(i % 4) + 1} {i % 12:02d}:00",
                    quarter=(i % 4) + 1,
                    player=f"Player {i % 20}",
                    team=f"Team {i % 4}",
                    description=f"Event {i}",
                    importance=importances[i % 4],
                    tags=["clutch"] if i % 10 == 0 else [],
                )
            )
        start = time.perf_counter()
        highlights = select_highlights(events)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Time {elapsed:.4f}s exceeds 1 second"
        assert 5 <= len(highlights) <= 8
