"""Tests for explanation generation (US-4)."""

from __future__ import annotations

import re

import pytest

from highlight_selector.models import GameEvent, UserPreference, ScoreBreakdown
from highlight_selector.selector import (
    generate_explanation,
    score_event,
    select_highlights,
)


def _make_event(
    importance: str = "medium",
    tags: list[str] | None = None,
    quarter: int = 2,
    player: str = "LeBron James",
    team: str = "Lakers",
    event_type: str = "dunk",
) -> GameEvent:
    return GameEvent(
        id="evt-test",
        type=event_type,
        timestamp=f"Q{quarter} 05:00",
        quarter=quarter,
        player=player,
        team=team,
        description="Test event",
        importance=importance,
        tags=tags if tags is not None else [],
    )


def _make_events_for_highlights(count: int = 10) -> list[GameEvent]:
    importances = [
        "critical",
        "high",
        "high",
        "high",
        "medium",
        "medium",
        "medium",
        "low",
        "low",
        "low",
    ]
    events = []
    for i in range(min(count, len(importances))):
        events.append(
            GameEvent(
                id=f"evt-{i:03d}",
                type="dunk",
                timestamp=f"Q{(i % 4) + 1} {i:02d}:00",
                quarter=(i % 4) + 1,
                player=f"Player {chr(65 + i % 3)}",
                team="Team A" if i % 2 == 0 else "Team B",
                description=f"Event {i}",
                importance=importances[i],
                tags=["clutch"] if importances[i] == "critical" else [],
            )
        )
    return events


class TestExplanationPresence:
    """T038: SC-002 - 100% of highlights have non-empty explanation."""

    def test_all_highlights_have_explanation(self) -> None:
        events = _make_events_for_highlights()
        highlights = select_highlights(events)
        for h in highlights:
            assert h.explanation, f"Highlight {h.event.id} has empty explanation"
            assert len(h.explanation.strip()) > 0


class TestExplanationLength:
    """T039: SC-007 - Explanation is 1-2 sentences."""

    def _count_sentences(self, text: str) -> int:
        # Count sentences by splitting on sentence-ending punctuation
        sentences = re.split(r"[.!?]+", text.strip())
        # Filter out empty strings from trailing punctuation
        return len([s for s in sentences if s.strip()])

    def test_explanation_is_1_to_2_sentences(self) -> None:
        events = _make_events_for_highlights()
        highlights = select_highlights(events)
        for h in highlights:
            sentence_count = self._count_sentences(h.explanation)
            assert 1 <= sentence_count <= 2, (
                f"Expected 1-2 sentences for {h.event.id}, got {sentence_count}: "
                f"'{h.explanation}'"
            )

    def test_critical_explanation_with_context_is_2_sentences(self) -> None:
        event = _make_event(
            importance="critical",
            quarter=4,
            tags=["game_winner", "clutch"],
        )
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        sentences = self._count_sentences(explanation)
        assert sentences == 2


class TestScoringFactorReferences:
    """T040: Explanation references scoring factors (importance, context)."""

    def test_critical_references_importance(self) -> None:
        event = _make_event(importance="critical")
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        assert "critical" in explanation.lower()

    def test_high_references_importance(self) -> None:
        event = _make_event(importance="high")
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        assert "high-impact" in explanation.lower()

    def test_game_winner_references_context(self) -> None:
        event = _make_event(tags=["game_winner"])
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        assert "victory" in explanation.lower() or "sealed" in explanation.lower()

    def test_clutch_q4_references_context(self) -> None:
        event = _make_event(quarter=4, tags=["clutch"])
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        assert "clutch" in explanation.lower()
        assert (
            "fourth-quarter" in explanation.lower()
            or "fourth quarter" in explanation.lower()
        )

    def test_buzzer_beater_references_context(self) -> None:
        event = _make_event(tags=["buzzer_beater"])
        breakdown = score_event(event)
        explanation = generate_explanation(event, breakdown)
        assert "buzzer" in explanation.lower()

    def test_player_preference_references_player(self) -> None:
        """T049: Player preference mentioned in explanation."""
        event = _make_event(player="LeBron James")
        prefs = UserPreference(favorite_player="LeBron James")
        breakdown = score_event(event, prefs)
        explanation = generate_explanation(event, breakdown)
        assert "favorite player" in explanation.lower()
        assert "lebron james" in explanation.lower()

    def test_team_preference_references_team(self) -> None:
        """T057: Team preference mentioned in explanation."""
        event = _make_event(team="Lakers")
        prefs = UserPreference(favorite_team="Lakers")
        breakdown = score_event(event, prefs)
        explanation = generate_explanation(event, breakdown)
        assert "favorite team" in explanation.lower()
        assert "lakers" in explanation.lower()


class TestNonTechnicalLanguage:
    """T041: SC-007 - No technical jargon in explanations."""

    JARGON_WORDS = [
        "algorithm",
        "score_event",
        "breakdown",
        "base_score",
        "player_boost",
        "team_boost",
        "context_boost",
        "total_score",
        "dataclass",
        "function",
        "parameter",
        "tuple",
        "dict",
        "integer",
        "float",
        "boolean",
        "variable",
        "module",
        "import",
        "class",
        "method",
        "attribute",
        "instance",
    ]

    def test_no_jargon_in_explanations(self) -> None:
        events = _make_events_for_highlights()
        highlights = select_highlights(events)
        for h in highlights:
            explanation_lower = h.explanation.lower()
            for jargon in self.JARGON_WORDS:
                assert jargon not in explanation_lower, (
                    f"Jargon '{jargon}' found in explanation for {h.event.id}: "
                    f"'{h.explanation}'"
                )

    def test_no_jargon_with_preferences(self) -> None:
        events = _make_events_for_highlights()
        prefs = UserPreference(favorite_player="Player A", favorite_team="Team A")
        highlights = select_highlights(events, prefs)
        for h in highlights:
            explanation_lower = h.explanation.lower()
            for jargon in self.JARGON_WORDS:
                assert jargon not in explanation_lower
