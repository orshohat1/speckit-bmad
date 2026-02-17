#!/usr/bin/env python3
"""
Demo script for AI Highlight Selector

Demonstrates:
1. Loading sample data
2. Objective (no preference) selection
3. Personalized selection with favorite player
4. Team preference selection
5. Combined player + team preference
6. Output formatting

Usage:
    python3 demo.py
"""

import json
from pathlib import Path
from highlight_selector.models import GameEvent, UserPreference
from highlight_selector.selector import select_highlights


def load_sample_data() -> list[GameEvent]:
    """Load sample data from shared folder."""
    sample_path = Path(__file__).parent.parent / "shared" / "sample_data.json"
    
    if not sample_path.exists():
        print(f"❌ Sample data not found at {sample_path}")
        print("Creating minimal sample data for demo...")
        return create_minimal_sample_data()
    
    with open(sample_path) as f:
        data = json.load(f)
        events = [GameEvent.from_dict(e) for e in data["events"]]
        print(f"✅ Loaded {len(events)} events from sample data\n")
        return events


def create_minimal_sample_data() -> list[GameEvent]:
    """Create minimal sample data if file doesn't exist."""
    return [
        GameEvent(
            id="evt-001",
            type="three_pointer",
            timestamp="Q4 02:34",
            quarter=4,
            player="LeBron James",
            team="Lakers",
            description="Deep three-pointer from the logo",
            importance="critical",
            tags=["clutch", "game_winner"]
        ),
        GameEvent(
            id="evt-002",
            type="dunk",
            timestamp="Q3 08:12",
            quarter=3,
            player="Stephen Curry",
            team="Warriors",
            description="Thunderous fast-break dunk",
            importance="high",
            tags=["highlight_reel"]
        ),
        GameEvent(
            id="evt-003",
            type="block",
            timestamp="Q4 01:23",
            quarter=4,
            player="Anthony Davis",
            team="Lakers",
            description="Game-saving block on potential game-tying shot",
            importance="critical",
            tags=["clutch", "defensive_play"]
        ),
        GameEvent(
            id="evt-004",
            type="three_pointer",
            timestamp="Q2 05:45",
            quarter=2,
            player="Stephen Curry",
            team="Warriors",
            description="Contested three-pointer",
            importance="medium",
            tags=["highlight_reel"]
        ),
        GameEvent(
            id="evt-005",
            type="assist",
            timestamp="Q1 09:30",
            quarter=1,
            player="LeBron James",
            team="Lakers",
            description="No-look assist to Davis for dunk",
            importance="medium",
            tags=["highlight_reel"]
        ),
        GameEvent(
            id="evt-006",
            type="steal",
            timestamp="Q4 03:15",
            quarter=4,
            player="Klay Thompson",
            team="Warriors",
            description="Crucial steal in final minutes",
            importance="high",
            tags=["clutch", "defensive_play"]
        ),
    ]


def print_separator(title: str = "") -> None:
    """Print a visual separator."""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def print_highlights(highlights, scenario: str) -> None:
    """Print highlights in a formatted way."""
    print_separator(f"Scenario: {scenario}")
    print(f"Selected {len(highlights)} highlights:\n")
    
    for h in highlights:
        print(f"#{h.rank} | Score: {h.score:.1f}")
        print(f"   {h.event.type.upper().replace('_', ' ')} - {h.event.description}")
        print(f"   Player: {h.event.player} | Team: {h.event.team} | {h.event.timestamp}")
        print(f"   Importance: {h.event.importance}")
        if h.event.tags:
            print(f"   Tags: {', '.join(h.event.tags)}")
        print(f"   💡 {h.explanation}")
        print()


def main() -> None:
    """Run all demo scenarios."""
    print("\n🎬 AI Highlight Selector Demo 🎬")
    print("=" * 70)
    
    # Load data
    events = load_sample_data()
    
    # Get unique players and teams
    players = sorted(set(e.player for e in events))
    teams = sorted(set(e.team for e in events))
    
    print(f"Sample contains:")
    print(f"  - Players: {', '.join(players)}")
    print(f"  - Teams: {', '.join(teams)}")
    print(f"  - Quarters: Q1-Q{max(e.quarter for e in events)}")
    print()
    
    # Scenario 1: Objective selection (no preferences)
    print("\n" + "█" * 70)
    print("  SCENARIO 1: Objective Selection (No Preferences)")
    print("█" * 70)
    highlights = select_highlights(events, None, min_count=5, max_count=8)
    print_highlights(highlights, "Objective - No user preferences")
    print("📊 All events scored purely on importance and context")
    
    # Scenario 2: Favorite player
    if len(players) > 0:
        favorite_player = players[0]  # Pick first player alphabetically
        print("\n" + "█" * 70)
        print(f"  SCENARIO 2: Favorite Player ({favorite_player})")
        print("█" * 70)
        pref = UserPreference(favorite_player=favorite_player)
        highlights = select_highlights(events, pref, min_count=5, max_count=8)
        print_highlights(highlights, f"Favorite Player: {favorite_player}")
        print(f"📊 Events featuring {favorite_player} receive +30 score boost")
        
        # Count how many highlights feature the favorite player
        fav_count = sum(1 for h in highlights if h.event.player == favorite_player)
        print(f"   {fav_count}/{len(highlights)} highlights feature {favorite_player}")
    
    # Scenario 3: Favorite team
    if len(teams) > 0:
        favorite_team = teams[0]  # Pick first team alphabetically
        print("\n" + "█" * 70)
        print(f"  SCENARIO 3: Favorite Team ({favorite_team})")
        print("█" * 70)
        pref = UserPreference(favorite_team=favorite_team)
        highlights = select_highlights(events, pref, min_count=5, max_count=8)
        print_highlights(highlights, f"Favorite Team: {favorite_team}")
        print(f"📊 Events from {favorite_team} receive +15 score boost")
        
        # Count how many highlights are from the favorite team
        team_count = sum(1 for h in highlights if h.event.team == favorite_team)
        print(f"   {team_count}/{len(highlights)} highlights are from {favorite_team}")
    
    # Scenario 4: Both player and team
    if len(players) > 0 and len(teams) > 0:
        favorite_player = players[0]
        favorite_team = teams[0]
        print("\n" + "█" * 70)
        print(f"  SCENARIO 4: Combined ({favorite_player} + {favorite_team})")
        print("█" * 70)
        pref = UserPreference(
            favorite_player=favorite_player,
            favorite_team=favorite_team
        )
        highlights = select_highlights(events, pref, min_count=5, max_count=8)
        print_highlights(
            highlights,
            f"Favorite Player: {favorite_player}, Favorite Team: {favorite_team}"
        )
        print(f"📊 Events get up to +45 boost (player +30, team +15)")
        
        # Count highlights matching preferences
        player_count = sum(1 for h in highlights if h.event.player == favorite_player)
        team_count = sum(1 for h in highlights if h.event.team == favorite_team)
        both_count = sum(
            1 for h in highlights 
            if h.event.player == favorite_player and h.event.team == favorite_team
        )
        print(f"   {player_count}/{len(highlights)} feature {favorite_player}")
        print(f"   {team_count}/{len(highlights)} are from {favorite_team}")
        print(f"   {both_count}/{len(highlights)} match both preferences")
    
    # Scenario 5: Selection rules demo
    print("\n" + "█" * 70)
    print("  SCENARIO 5: Selection Rules Demonstration")
    print("█" * 70)
    
    critical_events = [e for e in events if e.importance == "critical"]
    print(f"\n🔴 Critical Events: {len(critical_events)} found")
    print("   Rule: ALL critical events are ALWAYS included")
    for e in critical_events:
        print(f"   - {e.description} ({e.player})")
    
    if len(players) > 0:
        favorite_player = players[0]
        player_events = [e for e in events if e.player == favorite_player]
        print(f"\n⭐ {favorite_player} Events: {len(player_events)} found")
        if len(player_events) >= 3:
            print(f"   Rule: ≥50% of highlights must feature {favorite_player}")
            pref = UserPreference(favorite_player=favorite_player)
            highlights = select_highlights(events, pref, min_count=5, max_count=8)
            player_highlights = [h for h in highlights if h.event.player == favorite_player]
            percentage = (len(player_highlights) / len(highlights)) * 100
            print(f"   Result: {len(player_highlights)}/{len(highlights)} = {percentage:.0f}%")
    
    print("\n📏 Range Rule: Selects 5-8 highlights (unless more critical events exist)")
    highlights = select_highlights(events, None, min_count=5, max_count=8)
    print(f"   Result: {len(highlights)} highlights selected")
    
    # Final summary
    print_separator("Demo Complete!")
    print("Key Features Demonstrated:")
    print("  ✅ Objective selection based on importance")
    print("  ✅ Personalized scoring with favorite player/team")
    print("  ✅ Intelligent selection rules (critical events, 50% rule)")
    print("  ✅ Human-readable explanations")
    print("  ✅ Deterministic, reproducible results")
    print("\nTry it yourself:")
    print("  python3 -m highlight_selector.cli ../shared/sample_data.json")
    print("  python3 -m highlight_selector.cli ../shared/sample_data.json --player 'LeBron James'")
    print("  python3 -m highlight_selector.cli ../shared/sample_data.json --team 'Lakers'")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
