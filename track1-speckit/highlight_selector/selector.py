"""Core selection logic for AI Highlight Selector.

Provides functions to score game events, rank and filter them,
and orchestrate the full highlight selection pipeline.
"""

from __future__ import annotations

from highlight_selector.models import (
    GameEvent,
    Highlight,
    ScoreBreakdown,
    UserPreference,
    IMPORTANCE_RANK,
)

# --- Scoring constants ---

BASE_SCORES: dict[str, int] = {
    "critical": 100,
    "high": 75,
    "medium": 50,
    "low": 25,
}

CONTEXT_BOOST_MAP: dict[str, int] = {
    "clutch": 20,
    "highlight_reel": 15,
    "game_winner": 25,
    "buzzer_beater": 20,
}

FOURTH_QUARTER_BOOST: int = 10

PLAYER_BOOST: int = 30
TEAM_BOOST: int = 15

MIN_HIGHLIGHTS: int = 5
MAX_HIGHLIGHTS: int = 8


def score_event(
    event: GameEvent,
    prefs: UserPreference | None = None,
) -> ScoreBreakdown:
    """Score a single game event based on importance and preferences.

    Args:
        event: The game event to score.
        prefs: Optional user preferences for personalization boosts.

    Returns:
        A ScoreBreakdown with all scoring components.
    """
    # Base score from importance (FR-012: unknown defaults to "low")
    importance = event.importance if event.importance in BASE_SCORES else "low"
    base_score = BASE_SCORES[importance]

    # Player preference boost (+30 per plan)
    player_boost = 0
    if prefs and prefs.favorite_player and event.player == prefs.favorite_player:
        player_boost = PLAYER_BOOST

    # Team preference boost (+15 per plan)
    team_boost = 0
    if prefs and prefs.favorite_team and event.team == prefs.favorite_team:
        team_boost = TEAM_BOOST

    # Context boosts from tags
    context_boosts: dict[str, int] = {}
    for tag in event.tags:
        if tag in CONTEXT_BOOST_MAP:
            context_boosts[tag] = CONTEXT_BOOST_MAP[tag]

    # Fourth quarter bonus
    if event.quarter == 4:
        context_boosts["fourth_quarter"] = FOURTH_QUARTER_BOOST

    return ScoreBreakdown(
        base_score=base_score,
        player_boost=player_boost,
        team_boost=team_boost,
        context_boosts=context_boosts,
    )


def _importance_rank(importance: str) -> int:
    """Return numeric rank for an importance level (higher = more important)."""
    return IMPORTANCE_RANK.get(importance, 0)


def rank_and_filter(
    scored_events: list[tuple[GameEvent, ScoreBreakdown]],
    min_count: int = MIN_HIGHLIGHTS,
    max_count: int = MAX_HIGHLIGHTS,
) -> list[tuple[GameEvent, ScoreBreakdown]]:
    """Rank scored events and filter to 5-8 highlights.

    Selection rules (per spec):
    1. Force-include all critical events (FR-006).
    2. Sort remaining by score descending.
    3. Apply three-level tie-breaking: quarter desc, importance desc, id asc (FR-013).
    4. Select top events within min_count-max_count range (FR-005).

    Args:
        scored_events: List of (event, breakdown) tuples.
        min_count: Minimum desired highlights (default 5).
        max_count: Maximum desired highlights (default 8).

    Returns:
        Filtered and ranked list of (event, breakdown) tuples.
    """
    if not scored_events:
        return []

    # Deterministic sort key (FR-009, FR-013, SC-004)
    def sort_key(item: tuple[GameEvent, ScoreBreakdown]) -> tuple[int, int, int, str]:
        event, breakdown = item
        return (
            -breakdown.total_score,  # Descending score
            -event.quarter,  # Descending quarter
            -_importance_rank(event.importance),  # Descending importance
            event.id,  # Ascending ID (deterministic)
        )

    sorted_events = sorted(scored_events, key=sort_key)

    # Force-include critical events (FR-006)
    critical = [item for item in sorted_events if item[0].importance == "critical"]
    non_critical = [item for item in sorted_events if item[0].importance != "critical"]

    # If critical events exceed max_count, take the top-scored critical events
    if len(critical) > max_count:
        critical = critical[:max_count]

    # Build result: critical events first, then fill from non-critical
    result = list(critical)
    for item in non_critical:
        if len(result) >= max_count:
            break
        result.append(item)

    # Re-sort the final result by the same key for consistent output ordering
    result.sort(key=sort_key)

    return result


def generate_explanation(
    event: GameEvent,
    breakdown: ScoreBreakdown,
) -> str:
    """Generate a human-readable 1-2 sentence explanation for a highlight.

    Combines importance context, personalization context, and situational
    context into a fan-friendly explanation with no technical jargon.

    Args:
        event: The game event.
        breakdown: The score breakdown for explainability.

    Returns:
        A 1-2 sentence explanation string referencing scoring factors.
    """
    parts: list[str] = []

    # --- Sentence 1: Importance + event context ---
    event_type_display = event.type.replace("_", " ")

    if event.importance == "critical":
        parts.append(
            f"This critical {event_type_display} by {event.player} was a defining moment of the game."
        )
    elif event.importance == "high":
        parts.append(
            f"A high-impact {event_type_display} by {event.player} that made a significant difference."
        )
    elif event.importance == "medium":
        parts.append(
            f"A notable {event_type_display} by {event.player} that contributed to the game's story."
        )
    else:
        parts.append(
            f"This {event_type_display} by {event.player} added to the overall flow of the game."
        )

    # --- Sentence 2: Contextual and personalization details ---
    details: list[str] = []

    # Contextual tags
    if "game_winner" in event.tags:
        details.append("sealed the victory")
    if "clutch" in event.tags and event.quarter == 4:
        details.append("in a clutch fourth-quarter moment")
    elif "clutch" in event.tags:
        details.append("in a clutch moment")
    if "buzzer_beater" in event.tags:
        details.append("right at the buzzer")
    if "highlight_reel" in event.tags and "game_winner" not in event.tags:
        details.append("a highlight-reel play")

    # Player preference context
    if breakdown.player_boost > 0:
        details.append(f"featuring your favorite player, {event.player}")

    # Team preference context
    if breakdown.team_boost > 0:
        details.append(f"by your favorite team, the {event.team}")

    if details:
        detail_text = ", ".join(details)
        # Capitalize first letter and add period
        parts.append(detail_text[0].upper() + detail_text[1:] + ".")

    return " ".join(parts)


def select_highlights(
    events: list[GameEvent],
    prefs: UserPreference | None = None,
    min_count: int = MIN_HIGHLIGHTS,
    max_count: int = MAX_HIGHLIGHTS,
) -> list[Highlight]:
    """Select and rank highlights from a list of game events.

    Orchestrates the full pipeline: score → rank/filter → explain → build Highlights.

    Args:
        events: List of game events to process.
        prefs: Optional user preferences (FR-011: None = no preference).
        min_count: Minimum highlights to return (default 5).
        max_count: Maximum highlights to return (default 8).

    Returns:
        A list of Highlight objects, ranked by score descending.
        Returns empty list for empty input (FR-010).
    """
    # FR-010: Handle empty event list
    if not events:
        return []

    # FR-011: Handle null preferences
    if prefs is None:
        prefs = UserPreference()

    # Score all events
    scored_events = [(event, score_event(event, prefs)) for event in events]

    # Rank and filter
    filtered = rank_and_filter(scored_events, min_count, max_count)

    # Generate explanations and build Highlight objects
    highlights: list[Highlight] = []
    for rank, (event, breakdown) in enumerate(filtered, start=1):
        explanation = generate_explanation(event, breakdown)
        highlights.append(
            Highlight(
                event=event,
                rank=rank,
                score=breakdown.total_score,
                explanation=explanation,
            )
        )

    return highlights
