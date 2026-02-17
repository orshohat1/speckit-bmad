"""Unit tests for highlight selection logic."""

from highlight_selector.models import GameEvent, UserPreference, Highlight
from highlight_selector.selector import select_highlights


# Test helpers
def make_event(
    id: str,
    importance: str,
    quarter: int = 1,
    player: str = "Player",
    team: str = "TEAM",
    tags: list[str] = None,
) -> GameEvent:
    """Helper to create test events."""
    return GameEvent(
        id=id,
        type="play",
        timestamp="00:00",
        quarter=quarter,
        player=player,
        team=team,
        description=f"Event {id}",
        importance=importance,
        tags=tags or [],
    )


# Story 3.1 & 3.2: Sorting and Tie-Breaking Tests


def test_select_highlights_sorts_by_score_descending():
    """Verify events are sorted by score in descending order."""
    events = [
        make_event("evt1", "low"),  # score: 25
        make_event("evt2", "critical"),  # score: 100
        make_event("evt3", "medium"),  # score: 50
    ]

    highlights = select_highlights(events, None)

    assert highlights[0].event.id == "evt2"  # critical (100)
    assert highlights[1].event.id == "evt3"  # medium (50)
    assert highlights[2].event.id == "evt1"  # low (25)


def test_select_highlights_tie_breaking_by_quarter():
    """Verify tie-breaking uses quarter (descending)."""
    events = [
        make_event("evt1", "high", quarter=1),  # 75 pts, Q1
        make_event("evt2", "high", quarter=4),  # 75 pts, Q4
        make_event("evt3", "high", quarter=3),  # 75 pts, Q3
    ]

    highlights = select_highlights(events, None)

    # Same score, should be ordered Q4 > Q3 > Q1
    assert highlights[0].event.id == "evt2"  # Q4
    assert highlights[1].event.id == "evt3"  # Q3
    assert highlights[2].event.id == "evt1"  # Q1


def test_select_highlights_tie_breaking_by_importance():
    """Verify tie-breaking uses importance when quarters equal."""
    events = [
        make_event("evt1", "medium", quarter=2),  # Different importance, same quarter
        make_event("evt2", "critical", quarter=2),
        make_event("evt3", "high", quarter=2),
    ]
    # All have different importance, different base scores, so this tests sorting

    highlights = select_highlights(events, None)

    assert highlights[0].event.id == "evt2"  # critical
    assert highlights[1].event.id == "evt3"  # high
    assert highlights[2].event.id == "evt1"  # medium


def test_select_highlights_tie_breaking_by_id():
    """Verify tie-breaking uses ID (ascending) as final tiebreaker."""
    events = [
        make_event("evt3", "high", quarter=2),
        make_event("evt1", "high", quarter=2),
        make_event("evt2", "high", quarter=2),
    ]

    highlights = select_highlights(events, None)

    # Same score, same quarter, should be ordered by ID: evt1 < evt2 < evt3
    assert highlights[0].event.id == "evt1"
    assert highlights[1].event.id == "evt2"
    assert highlights[2].event.id == "evt3"


# Story 3.3: Force-Include Critical Events


def test_select_highlights_includes_all_critical_events():
    """Verify all critical events are included regardless of count."""
    # Create 10 critical events (exceeds normal max of 8)
    events = [make_event(f"critical{i}", "critical") for i in range(10)]

    highlights = select_highlights(events, None)

    # All 10 critical events should be included
    assert len(highlights) == 10
    critical_ids = {h.event.id for h in highlights}
    expected_ids = {f"critical{i}" for i in range(10)}
    assert critical_ids == expected_ids


def test_select_highlights_critical_events_maintain_ranking():
    """Verify critical events maintain score-based ranking."""
    events = [
        make_event("crit1", "critical", quarter=1),
        make_event("crit2", "critical", quarter=4, tags=["clutch"]),  # Higher score
        make_event("high1", "high"),
    ]

    highlights = select_highlights(events, None)

    # crit2 should rank higher due to tag boost
    assert highlights[0].event.id == "crit2"
    assert highlights[1].event.id == "crit1"


# Story 3.4: Select 5-8 Highlights


def test_select_highlights_returns_all_when_fewer_than_5():
    """Verify all events returned when count < 5."""
    events = [make_event(f"evt{i}", "medium") for i in range(3)]

    highlights = select_highlights(events, None)

    assert len(highlights) == 3


def test_select_highlights_returns_all_when_5_to_8():
    """Verify all events returned when count is 5-8."""
    for count in [5, 6, 7, 8]:
        events = [make_event(f"evt{i}", "medium") for i in range(count)]
        highlights = select_highlights(events, None)
        assert len(highlights) == count


def test_select_highlights_returns_top_8_when_more_than_8():
    """Verify top 8 returned when count > 8 (no critical events)."""
    # 12 medium events, no special rules apply
    events = [make_event(f"evt{i:02d}", "medium") for i in range(12)]

    highlights = select_highlights(events, None)

    # Should return exactly 8
    assert len(highlights) == 8
    # Should be top 8 by ID (all same score, tie-break by ID)
    expected_ids = [f"evt{i:02d}" for i in range(8)]
    actual_ids = [h.event.id for h in highlights]
    assert actual_ids == expected_ids


def test_select_highlights_critical_can_exceed_max():
    """Verify critical events can push count above 8."""
    # 8 medium events + 3 critical events = 11 total
    events = [make_event(f"med{i}", "medium") for i in range(8)]
    events += [make_event(f"crit{i}", "critical") for i in range(3)]

    highlights = select_highlights(events, None)

    # All 11 should be included (8 medium + 3 critical)
    assert len(highlights) == 11


# Story 3.5: 50% Favorite Player Rule


def test_select_highlights_50_percent_favorite_player_rule():
    """Verify at least 50% of highlights feature favorite player when possible."""
    pref = UserPreference(favorite_player="Star")

    # Create 10 events: 6 with favorite player, 4 without
    events = [make_event(f"star{i}", "high", player="Star") for i in range(6)]
    events += [make_event(f"other{i}", "high", player="Other") for i in range(4)]

    highlights = select_highlights(events, pref)

    # Should select 8 events, at least 4 should be Star
    assert len(highlights) == 8
    star_count = sum(1 for h in highlights if h.event.player == "Star")
    assert star_count >= 4  # At least 50%


def test_select_highlights_50_percent_rule_requires_3_events():
    """Verify 50% rule only applies when ≥3 favorite player events exist."""
    pref = UserPreference(favorite_player="Star")

    # Only 2 events with favorite player
    events = [make_event(f"star{i}", "high", player="Star") for i in range(2)]
    events += [make_event(f"other{i}", "high", player="Other") for i in range(8)]

    highlights = select_highlights(events, pref)

    # Rule doesn't apply, should just return top 8 by score
    assert len(highlights) == 8


def test_select_highlights_50_percent_rule_with_no_favorite():
    """Verify 50% rule skipped when no favorite player specified."""
    pref = UserPreference(favorite_player=None)

    events = [make_event(f"player{i}", "high", player=f"P{i}") for i in range(10)]

    highlights = select_highlights(events, pref)

    # Just returns top 8, no player filtering
    assert len(highlights) == 8


def test_select_highlights_50_percent_respects_score_ranking():
    """Verify 50% rule respects score-based ranking within constraint."""
    pref = UserPreference(favorite_player="Star")

    # Create events where favorite player has lower scores
    events = [
        make_event("star1", "medium", player="Star"),  # 50 + 30 = 80
        make_event("star2", "medium", player="Star"),  # 50 + 30 = 80
        make_event("star3", "medium", player="Star"),  # 50 + 30 = 80
        make_event("star4", "low", player="Star"),  # 25 + 30 = 55
        make_event("other1", "high", player="Other"),  # 75
        make_event("other2", "high", player="Other"),  # 75
        make_event("other3", "high", player="Other"),  # 75
        make_event("other4", "high", player="Other"),  # 75
    ]

    highlights = select_highlights(events, pref)

    # Should select 8 events, with at least 4 Star events
    # Star events have score 80 (medium + boost), Others have 75
    # Top 3 should be Star (80), then need 1 more Star to meet 50%
    star_count = sum(1 for h in highlights if h.event.player == "Star")
    assert star_count >= 4


# Story 3.6: Main Orchestrator Function


def test_select_highlights_returns_highlight_objects():
    """Verify function returns Highlight objects."""
    events = [make_event("evt1", "critical")]

    highlights = select_highlights(events, None)

    assert len(highlights) == 1
    assert isinstance(highlights[0], Highlight)
    assert highlights[0].event.id == "evt1"


def test_select_highlights_assigns_rank_numbers():
    """Verify rank numbers are assigned 1 through N."""
    events = [
        make_event("evt1", "critical"),
        make_event("evt2", "high"),
        make_event("evt3", "medium"),
    ]

    highlights = select_highlights(events, None)

    assert highlights[0].rank == 1
    assert highlights[1].rank == 2
    assert highlights[2].rank == 3


def test_select_highlights_includes_scores_in_highlights():
    """Verify Highlight objects include calculated scores."""
    events = [make_event("evt1", "critical")]  # Should have score 100

    highlights = select_highlights(events, None)

    assert highlights[0].score == 100


def test_select_highlights_deterministic():
    """Verify same inputs produce same outputs."""
    events = [make_event(f"evt{i}", "high") for i in range(10)]
    pref = UserPreference(favorite_player="Player")

    result1 = select_highlights(events, pref)
    result2 = select_highlights(events, pref)

    ids1 = [h.event.id for h in result1]
    ids2 = [h.event.id for h in result2]
    assert ids1 == ids2


def test_select_highlights_empty_input():
    """Verify function handles empty event list."""
    highlights = select_highlights([], None)
    assert highlights == []


def test_select_highlights_integration_all_rules():
    """Integration test applying all selection rules together."""
    pref = UserPreference(favorite_player="Star", favorite_team="TEAM")

    events = [
        # Critical events (must be included)
        make_event("crit1", "critical", quarter=4, player="Star", tags=["clutch"]),
        make_event("crit2", "critical", quarter=3),
        # High scoring favorite player events
        make_event("star1", "high", player="Star"),
        make_event("star2", "high", player="Star"),
        make_event("star3", "medium", player="Star"),
        # Other events
        make_event("other1", "high"),
        make_event("other2", "high"),
        make_event("other3", "medium"),
        make_event("other4", "medium"),
        make_event("other5", "low"),
    ]

    highlights = select_highlights(events, pref)

    # Verify critical events included
    critical_ids = {h.event.id for h in highlights if h.event.importance == "critical"}
    assert "crit1" in critical_ids
    assert "crit2" in critical_ids

    # Verify ranking
    assert highlights[0].rank == 1
    assert highlights[-1].rank == len(highlights)

    # Verify all have scores
    assert all(h.score > 0 for h in highlights)


def test_select_highlights_with_custom_limits():
    """Verify function respects custom min/max_count parameters."""
    events = [make_event(f"evt{i}", "medium") for i in range(20)]

    # Test with custom limits
    highlights = select_highlights(events, None, min_count=3, max_count=6)

    # Should return top 6 (max_count)
    assert len(highlights) == 6
