"""End-to-end integration tests using real sample data."""

import json
from pathlib import Path

from highlight_selector.models import GameEvent, UserPreference
from highlight_selector.selector import select_highlights


def test_end_to_end_with_sample_data():
    """Test complete workflow with sample data from shared folder."""
    # Load sample data
    sample_path = Path(__file__).parent.parent.parent / "shared" / "sample_data.json"

    if not sample_path.exists():
        # Create minimal sample if file doesn't exist
        events_data = [
            {
                "id": f"evt-{i:03d}",
                "type": "play",
                "timestamp": f"Q{i//3+1} 00:00",
                "quarter": i // 3 + 1,
                "player": f"Player{i % 3 + 1}",
                "team": "TEAM" if i % 2 == 0 else "OPPONENT",
                "description": f"Event {i}",
                "importance": ["critical", "high", "medium", "low"][i % 4],
                "tags": ["clutch"] if i % 5 == 0 else [],
            }
            for i in range(12)
        ]
    else:
        with open(sample_path) as f:
            data = json.load(f)
            events_data = data.get("events", [])

    # Parse events
    events = [GameEvent.from_dict(evt) for evt in events_data]

    # Test objective selection
    highlights = select_highlights(events, None)
    # Selection can exceed max_count when critical events are present
    critical_events = [e for e in events if e.importance == "critical"]
    expected_min = min(5, len(events))
    assert len(highlights) >= expected_min
    # All critical events should be included
    critical_ids = {e.id for e in critical_events}
    highlight_ids = {h.event.id for h in highlights}
    assert critical_ids.issubset(highlight_ids)
    assert all(h.rank == idx + 1 for idx, h in enumerate(highlights))
    assert all(h.explanation for h in highlights)

    # Test with preferences
    if events:
        first_player = events[0].player
        first_team = events[0].team
        pref = UserPreference(favorite_player=first_player, favorite_team=first_team)

        highlights_personalized = select_highlights(events, pref)
        # Selection can exceed max_count when critical events are present
        expected_min = min(5, len(events))
        assert len(highlights_personalized) >= expected_min
        # All critical events should be included
        assert critical_ids.issubset({h.event.id for h in highlights_personalized})

        # Verify scores reflect personalization
        player_events = [
            h for h in highlights_personalized if h.event.player == first_player
        ]
        if player_events:
            # Player boost should be reflected in scores
            assert any(h.score > 75 for h in player_events)


def test_end_to_end_critical_event_handling():
    """Test that critical events are always included."""
    events = [
        GameEvent(
            id=f"crit{i}",
            type="play",
            timestamp="00:00",
            quarter=4,
            player="Player",
            team="TEAM",
            description="Critical play",
            importance="critical",
        )
        for i in range(10)
    ]

    # Add some non-critical
    events.extend(
        [
            GameEvent(
                id=f"norm{i}",
                type="play",
                timestamp="00:00",
                quarter=1,
                player="Player",
                team="TEAM",
                description="Normal play",
                importance="medium",
            )
            for i in range(5)
        ]
    )

    highlights = select_highlights(events, None)

    # All 10 critical should be included (exceeds normal max of 8)
    critical_count = sum(1 for h in highlights if h.event.importance == "critical")
    assert critical_count == 10


def test_end_to_end_50_percent_rule():
    """Test 50% favorite player rule in realistic scenario."""
    pref = UserPreference(favorite_player="StarPlayer")

    # Create 6 star player events and 6 other player events
    events = []
    for i in range(6):
        events.append(
            GameEvent(
                id=f"star{i}",
                type="play",
                timestamp="00:00",
                quarter=i // 2 + 1,
                player="StarPlayer",
                team="TEAM",
                description="Star play",
                importance="high",
            )
        )
    for i in range(6):
        events.append(
            GameEvent(
                id=f"other{i}",
                type="play",
                timestamp="00:00",
                quarter=i // 2 + 1,
                player="OtherPlayer",
                team="TEAM",
                description="Other play",
                importance="high",
            )
        )

    highlights = select_highlights(events, pref)

    # Should select 8 total highlights
    assert len(highlights) == 8

    # At least 50% should be StarPlayer
    star_count = sum(1 for h in highlights if h.event.player == "StarPlayer")
    assert star_count >= 4


def test_end_to_end_deterministic():
    """Test that repeated runs produce identical results."""
    events = [
        GameEvent(
            id=f"evt{i}",
            type="play",
            timestamp=f"Q{i//3+1} 00:00",
            quarter=i // 3 + 1,
            player=f"Player{i % 3}",
            team="TEAM",
            description=f"Event {i}",
            importance=["critical", "high", "medium"][i % 3],
            tags=["clutch"] if i % 4 == 0 else [],
        )
        for i in range(15)
    ]

    pref = UserPreference(favorite_player="Player0", favorite_team="TEAM")

    # Run multiple times
    results = [select_highlights(events, pref) for _ in range(3)]

    # All results should be identical
    for i in range(1, len(results)):
        assert len(results[0]) == len(results[i])
        for j in range(len(results[0])):
            assert results[0][j].event.id == results[i][j].event.id
            assert results[0][j].rank == results[i][j].rank
            assert results[0][j].score == results[i][j].score


def test_end_to_end_json_serialization_round_trip():
    """Test that highlights can be serialized and deserialized."""
    events = [
        GameEvent(
            id="evt1",
            type="touchdown",
            timestamp="Q4 02:00",
            quarter=4,
            player="J.Allen",
            team="BUF",
            description="Game-winning TD",
            importance="critical",
            tags=["clutch", "game_winner"],
        )
    ]

    pref = UserPreference(favorite_player="J.Allen", favorite_team="BUF")
    highlights = select_highlights(events, pref)

    # Serialize to dict
    highlights_dict = [h.to_dict() for h in highlights]

    # Verify structure
    assert len(highlights_dict) == 1
    assert "event" in highlights_dict[0]
    assert "rank" in highlights_dict[0]
    assert "score" in highlights_dict[0]
    assert "explanation" in highlights_dict[0]

    # Can be JSON serialized
    json_str = json.dumps(highlights_dict)
    assert len(json_str) > 0

    # Can be deserialized
    deserialized = json.loads(json_str)
    assert len(deserialized) == 1
    assert deserialized[0]["rank"] == 1
