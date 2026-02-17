#!/usr/bin/env python3
"""Run highlight selector on sample data with custom preferences.

Usage:
    python run.py --player "LeBron James"
    python run.py --team "Lakers"
    python run.py --player "Jayson Tatum" --team "Celtics"
    python run.py --player "Derrick White" --only   # only show that player's highlights
    python run.py  # no preference
"""

import argparse
import json
from pathlib import Path

from highlight_selector import GameEvent, UserPreference, select_highlights


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Highlight Selector")
    parser.add_argument("--player", type=str, default=None, help="Favorite player name")
    parser.add_argument("--team", type=str, default=None, help="Favorite team name")
    parser.add_argument(
        "--data",
        type=str,
        default="../shared/sample_data.json",
        help="Path to game data JSON (default: shared/sample_data.json)",
    )
    parser.add_argument(
        "--only",
        action="store_true",
        default=False,
        help="Only show highlights for the specified --player/--team",
    )
    args = parser.parse_args()

    if args.only and not args.player and not args.team:
        print("Error: --only requires --player and/or --team")
        return

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: File not found: {data_path}")
        return

    with open(data_path) as f:
        raw = json.load(f)

    events = [GameEvent.from_dict(e) for e in raw["events"]]
    prefs = UserPreference(
        favorite_player=args.player,
        favorite_team=args.team,
    )

    # Validate preferred player/team exists in events
    all_players = {e.player for e in events}
    all_teams = {e.team for e in events}
    has_error = False

    if prefs.favorite_player and prefs.favorite_player not in all_players:
        print(f"\n⚠️  Player '{prefs.favorite_player}' not found in game data.")
        print(f"   Available players: {', '.join(sorted(all_players))}")
        has_error = True

    if prefs.favorite_team and prefs.favorite_team not in all_teams:
        print(f"\n⚠️  Team '{prefs.favorite_team}' not found in game data.")
        print(f"   Available teams: {', '.join(sorted(all_teams))}")
        has_error = True

    if has_error:
        print("\n   Please re-run with a valid --player or --team from the list above.")
        return

    highlights = select_highlights(events, prefs)

    # Filter to only the specified player/team if --only is set
    if args.only:
        highlights = [
            h for h in highlights
            if (args.player and h.event.player == args.player)
            or (args.team and h.event.team == args.team)
        ]
        # Re-number ranks
        for i, h in enumerate(highlights, 1):
            h.rank = i

    # Header
    game = raw.get("game", {})
    title = game.get("title", "Game Highlights")
    filter_label = " (filtered)" if args.only else ""
    print("=" * 80)
    print(f"  {title}")
    print(f"  Preferences:  Player={prefs.favorite_player or '—'}  |  Team={prefs.favorite_team or '—'}{filter_label}")
    print(f"  {len(events)} events → {len(highlights)} highlights")
    print("=" * 80)

    if not highlights:
        print("\n  No highlights found for the given filter.")
    else:
        for h in highlights:
            print(f"\n  #{h.rank}  [Score {h.score}]  {h.event.player} ({h.event.team}) — Q{h.event.quarter}")
            print(f"       {h.event.description}")
            print(f"       → {h.explanation}")

    print()


if __name__ == "__main__":
    main()
