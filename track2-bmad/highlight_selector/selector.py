"""Highlight selection and scoring engine.

This module implements the core scoring logic for evaluating game events
and selecting the most important highlights based on importance, user
preferences, and context tags.
"""

from typing import Optional, Tuple, Union

from highlight_selector.models import (
    GameEvent,
    Highlight,
    ScoreBreakdown,
    UserPreference,
)


# Story 2.1: Base Importance Scoring


def calculate_base_score(event: GameEvent) -> int:
    """Calculate base score from event importance level.

    Maps event importance to numeric scores. Unknown or invalid importance
    levels default to "low" scoring.

    Args:
        event: GameEvent to score.

    Returns:
        Base score: 100 (critical), 75 (high), 50 (medium), or 25 (low/unknown).

    Example:
        >>> event = GameEvent(
        ...     id="evt1", type="touchdown", timestamp="Q4 2:45",
        ...     quarter=4, player="J.Allen", team="BUF",
        ...     description="Game-winning TD", importance="critical"
        ... )
        >>> calculate_base_score(event)
        100
    """
    importance_map = {
        "critical": 100,
        "high": 75,
        "medium": 50,
        "low": 25,
    }
    return importance_map.get(event.importance, 25)  # Default to low (25)


# Story 2.2: Player Preference Boost


def calculate_player_boost(
    event: GameEvent, preference: Optional[UserPreference]
) -> int:
    """Calculate score boost for events featuring user's favorite player.

    Adds +30 points if the event's player matches the user's favorite_player
    preference. Player name matching is case-sensitive and exact.

    Args:
        event: GameEvent to evaluate.
        preference: User's preferences, or None for objective scoring.

    Returns:
        30 if player matches favorite, otherwise 0.

    Example:
        >>> event = GameEvent(
        ...     id="evt1", type="touchdown", timestamp="Q4 2:45",
        ...     quarter=4, player="J.Allen", team="BUF",
        ...     description="TD pass", importance="critical"
        ... )
        >>> pref = UserPreference(favorite_player="J.Allen")
        >>> calculate_player_boost(event, pref)
        30
    """
    if preference is None or preference.favorite_player is None:
        return 0

    return 30 if event.player == preference.favorite_player else 0


# Story 2.3: Team Preference Boost


def calculate_team_boost(event: GameEvent, preference: Optional[UserPreference]) -> int:
    """Calculate score boost for events involving user's favorite team.

    Adds +15 points if the event's team matches the user's favorite_team
    preference. Team name matching is case-sensitive and exact.

    Args:
        event: GameEvent to evaluate.
        preference: User's preferences, or None for objective scoring.

    Returns:
        15 if team matches favorite, otherwise 0.

    Example:
        >>> event = GameEvent(
        ...     id="evt1", type="touchdown", timestamp="Q4 2:45",
        ...     quarter=4, player="J.Allen", team="BUF",
        ...     description="TD pass", importance="critical"
        ... )
        >>> pref = UserPreference(favorite_team="BUF")
        >>> calculate_team_boost(event, pref)
        15
    """
    if preference is None or preference.favorite_team is None:
        return 0

    return 15 if event.team == preference.favorite_team else 0


# Story 2.4: Context Tag Boosts


def calculate_context_boosts(event: GameEvent) -> dict[str, Union[int, float]]:
    """Calculate score boosts based on event context tags.

    Maps recognized context tags to their corresponding boost values.
    Unknown tags are ignored. Multiple tags accumulate.

    Recognized tags and their boosts:
    - clutch: +20 points
    - game_winner: +25 points
    - buzzer_beater: +15 points
    - highlight_reel: +15 points
    - fourth_quarter: +10 points

    Args:
        event: GameEvent to evaluate.

    Returns:
        Dictionary mapping tag names to boost values. Empty if no recognized tags.

    Example:
        >>> event = GameEvent(
        ...     id="evt1", type="touchdown", timestamp="Q4 2:45",
        ...     quarter=4, player="J.Allen", team="BUF",
        ...     description="Clutch TD", importance="critical",
        ...     tags=["clutch", "fourth_quarter"]
        ... )
        >>> boosts = calculate_context_boosts(event)
        >>> boosts
        {'clutch': 20, 'fourth_quarter': 10}
        >>> sum(boosts.values())
        30
    """
    tag_boost_map = {
        "clutch": 20,
        "game_winner": 25,
        "buzzer_beater": 15,
        "highlight_reel": 15,
        "fourth_quarter": 10,
    }

    boosts: dict[str, Union[int, float]] = {}
    for tag in event.tags:
        if tag in tag_boost_map:
            boosts[tag] = tag_boost_map[tag]

    return boosts


# Story 2.5: Total Score Calculation with Breakdown


def calculate_score(
    event: GameEvent, preference: Optional[UserPreference]
) -> ScoreBreakdown:
    """Calculate final score and return complete breakdown.

    Orchestrates all scoring components (base, player, team, context) and
    returns a ScoreBreakdown showing how each component contributed to the
    total score.

    Complexity: O(n) where n = number of tags on the event.

    Args:
        event: GameEvent to score.
        preference: User's preferences, or None for objective scoring.

    Returns:
        ScoreBreakdown with all components and total score.

    Example:
        >>> event = GameEvent(
        ...     id="evt1", type="touchdown", timestamp="Q4 1:30",
        ...     quarter=4, player="J.Allen", team="BUF",
        ...     description="Game-winning TD", importance="critical",
        ...     tags=["clutch", "game_winner"]
        ... )
        >>> pref = UserPreference(favorite_player="J.Allen", favorite_team="BUF")
        >>> breakdown = calculate_score(event, pref)
        >>> breakdown.base_score
        100
        >>> breakdown.player_boost
        30
        >>> breakdown.team_boost
        15
        >>> breakdown.context_boosts
        {'clutch': 20, 'game_winner': 25}
        >>> breakdown.total_score
        190
    """
    base = calculate_base_score(event)
    player = calculate_player_boost(event, preference)
    team = calculate_team_boost(event, preference)
    context = calculate_context_boosts(event)

    total = base + player + team + sum(context.values())

    return ScoreBreakdown(
        base_score=base,
        player_boost=player,
        team_boost=team,
        context_boosts=context,
        total_score=total,
    )


# Story 3.1, 3.2: Sorting and Tie-Breaking


def _create_sort_key(
    event: GameEvent, score: Union[int, float]
) -> Tuple[Union[int, float], int, int, str]:
    """Create sort key for deterministic tie-breaking.

    Tie-breaking order:
    1. Score (descending)
    2. Quarter (descending: 4 > 3 > 2 > 1)
    3. Importance (descending: critical > high > medium > low)
    4. Event ID (ascending: lexicographic)

    Args:
        event: GameEvent to create key for.
        score: Calculated score for the event.

    Returns:
        Tuple for sorting: (negative_score, negative_quarter, negative_importance, id)
    """
    importance_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    importance_value = importance_rank.get(event.importance, 0)

    # Negative values for descending sort
    return (-score, -event.quarter, -importance_value, event.id)


# Story 3.3, 3.4, 3.5, 3.6: Main Selection Logic


def select_highlights(
    events: list[GameEvent],
    preference: Optional[UserPreference],
    min_count: int = 5,
    max_count: int = 8,
) -> list[Highlight]:
    """Select and rank highlights from a list of game events.

    Main entry point for highlight selection. Orchestrates all selection rules:
    - Scores all events using calculate_score()
    - Sorts by score with deterministic tie-breaking
    - Force-includes all critical importance events
    - Selects 5-8 highlights (or all if fewer than 5)
    - Applies 50% favorite player representation rule when applicable
    - Assigns rank numbers (1 through N)
    - Generates explanations for each selected highlight

    Selection Rules:
    1. All "critical" importance events are always included
    2. If fewer than min_count events total, return all
    3. If min_count to max_count events, return all
    4. If more than max_count events, return top max_count (unless critical rule applies)
    5. If favorite_player specified and ≥3 events with that player exist,
       ensure at least 50% of returned highlights feature that player

    Args:
        events: List of GameEvent objects to select from.
        preference: Optional user preferences for personalization.
        min_count: Minimum number of highlights to return (default: 5).
        max_count: Maximum number of highlights to return (default: 8).

    Returns:
        List of Highlight objects, ranked from 1 (best) to N, with scores
        and explanations included.

    Example:
        >>> events = [
        ...     GameEvent(id="evt1", type="touchdown", timestamp="Q4 1:30",
        ...               quarter=4, player="J.Allen", team="BUF",
        ...               description="Game-winning TD", importance="critical",
        ...               tags=["clutch", "game_winner"]),
        ...     GameEvent(id="evt2", type="interception", timestamp="Q3 5:00",
        ...               quarter=3, player="T.White", team="BUF",
        ...               description="Red zone INT", importance="high"),
        ... ]
        >>> pref = UserPreference(favorite_player="J.Allen", favorite_team="BUF")
        >>> highlights = select_highlights(events, pref)
        >>> len(highlights)
        2
        >>> highlights[0].rank
        1
        >>> highlights[0].event.id
        'evt1'
    """
    # Handle empty input
    if not events:
        return []

    # Step 1: Score all events
    scored_events: list[Tuple[GameEvent, ScoreBreakdown]] = []
    for event in events:
        breakdown = calculate_score(event, preference)
        scored_events.append((event, breakdown))

    # Step 2: Sort by score with deterministic tie-breaking
    scored_events.sort(key=lambda x: _create_sort_key(x[0], x[1].total_score))

    # Step 3: Force-include all critical events
    critical_events = [
        (evt, score) for evt, score in scored_events if evt.importance == "critical"
    ]
    non_critical_events = [
        (evt, score) for evt, score in scored_events if evt.importance != "critical"
    ]

    # Step 4: Apply 5-8 selection logic to NON-CRITICAL events only
    # Critical events are always included on top of this
    num_non_critical = len(non_critical_events)

    if num_non_critical <= min_count:
        # Include all non-critical
        selected_non_critical = non_critical_events
    elif num_non_critical <= max_count:
        # Include all non-critical (within range)
        selected_non_critical = non_critical_events
    else:
        # More than max: take top max_count non-critical events
        selected_non_critical = non_critical_events[:max_count]

    # Combine critical (always all) + selected non-critical
    selected = critical_events + selected_non_critical

    # Step 5: Apply 50% favorite player rule if applicable
    if preference and preference.favorite_player:
        selected = _apply_favorite_player_rule(selected, preference.favorite_player)

    # Step 6: Assign ranks and create Highlight objects
    highlights: list[Highlight] = []
    for rank, (event, breakdown) in enumerate(selected, start=1):
        explanation = _generate_explanation(event, breakdown, preference)
        highlight = Highlight(
            event=event,
            rank=rank,
            score=breakdown.total_score,
            explanation=explanation,
        )
        highlights.append(highlight)

    return highlights


def _apply_favorite_player_rule(
    scored_events: list[Tuple[GameEvent, ScoreBreakdown]],
    favorite_player: str,
) -> list[Tuple[GameEvent, ScoreBreakdown]]:
    """Apply 50% favorite player representation rule.

    If at least 3 events featuring the favorite player exist in the input,
    ensure at least 50% of the selection features that player.

    Args:
        scored_events: List of (event, breakdown) tuples, already sorted.
        favorite_player: Name of favorite player.

    Returns:
        Modified list ensuring 50% representation if rule applies.
    """
    # Count how many favorite player events are available
    fav_events = [
        (evt, score) for evt, score in scored_events if evt.player == favorite_player
    ]

    # Rule only applies if ≥3 favorite player events exist
    if len(fav_events) < 3:
        return scored_events

    # Calculate required count (50% of selection)
    selection_size = len(scored_events)
    required_fav_count = (selection_size + 1) // 2  # Round up

    # Count how many favorite player events are already in selection
    current_fav_count = sum(
        1 for evt, _ in scored_events if evt.player == favorite_player
    )

    # If already meeting requirement, return as-is
    if current_fav_count >= required_fav_count:
        return scored_events

    # Need to add more favorite player events
    # Split selection into favorite and non-favorite
    fav_in_selection = [
        (evt, score) for evt, score in scored_events if evt.player == favorite_player
    ]
    non_fav_in_selection = [
        (evt, score) for evt, score in scored_events if evt.player != favorite_player
    ]

    # Get additional favorite player events not yet selected
    # (They must exist since we have ≥3 total and need more)
    all_fav_events = [
        (evt, score) for evt, score in scored_events if evt.player == favorite_player
    ]

    # Calculate how many more we need
    needed = required_fav_count - current_fav_count

    # Take top favorite player events to meet the requirement
    # This maintains score-based ranking
    selected_fav = all_fav_events[:required_fav_count]

    # Take remaining slots from non-favorite events
    remaining_slots = selection_size - len(selected_fav)
    selected_non_fav = non_fav_in_selection[:remaining_slots]

    # Merge and re-sort by original scoring
    combined = selected_fav + selected_non_fav
    combined.sort(key=lambda x: _create_sort_key(x[0], x[1].total_score))

    return combined


def _generate_explanation(
    event: GameEvent, breakdown: ScoreBreakdown, preference: Optional[UserPreference]
) -> str:
    """Generate a brief explanation for why an event was selected.

    Creates a 1-2 sentence human-readable explanation based on importance,
    personalization boosts, and context tags.

    Args:
        event: The GameEvent being explained.
        breakdown: ScoreBreakdown showing scoring components.
        preference: Optional user preferences.

    Returns:
        String explanation (1-2 sentences).
    """
    # Start with importance-based phrase
    importance_phrases = {
        "critical": "Critical game moment",
        "high": "High-impact play",
        "medium": "Notable play",
        "low": "Contributing play",
    }
    parts = [importance_phrases.get(event.importance, "Notable play")]

    # Add personalization context
    if breakdown.player_boost > 0:
        parts.append(f"featuring your favorite player {event.player}")
    elif breakdown.team_boost > 0:
        parts.append(f"by your favorite team {event.team}")

    # Add context tags
    if breakdown.context_boosts:
        tag_phrases = {
            "clutch": "in a clutch situation",
            "game_winner": "as the game-winner",
            "buzzer_beater": "at the buzzer",
            "highlight_reel": "with highlight-reel quality",
            "fourth_quarter": "in the critical fourth quarter",
        }
        for tag in breakdown.context_boosts:
            if tag in tag_phrases:
                parts.append(tag_phrases[tag])
                break  # Only add one context phrase

    # Combine into sentence
    if len(parts) == 1:
        return f"{parts[0]}."
    else:
        return f"{parts[0]} {' '.join(parts[1:])}."
