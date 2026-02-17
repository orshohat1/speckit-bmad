# AI Highlight Selector

A Python library that processes NBA game events and returns personalized, curated highlights based on event importance and user preferences (favorite player / team). Each highlight includes a human-readable explanation of why it was selected.

## Features

- **Smart Scoring** — Events scored by importance (`critical` 100 → `low` 25), context tags (`clutch` +20, `game_winner` +25, `buzzer_beater` +15, …), and user preferences
- **Personalization** — Favorite player boost (+30) and/or favorite team boost (+15)
- **Filtering** — Show all top highlights or filter to only your player/team with `--only`
- **Explainability** — Every highlight includes a fan-friendly 1-2 sentence explanation
- **Validation** — Warns you when a player/team isn't found and shows available options
- **Deterministic** — Identical inputs always produce identical outputs
- **Zero Dependencies** — Pure Python stdlib at runtime

---

## Quick Start

```bash
# 1. Create & activate virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. Install dev dependencies
pip install pytest pytest-cov black mypy

# 3. Run it — pick your favorite player
python run.py --player "LeBron James"
```

### Usage Examples

```bash
# Boost a player's highlights to the top
python run.py --player "Jayson Tatum"

# Boost a team's highlights
python run.py --team "Celtics"

# Show ONLY your player's highlights
python run.py --player "Derrick White" --only

# Show ONLY a team's highlights
python run.py --team "Lakers" --only

# Combine player + team preference
python run.py --player "Jayson Tatum" --team "Celtics"

# Use a different game data file
python run.py --player "LeBron James" --data path/to/game.json

# No preference (top highlights by score only)
python run.py
```

### Sample Output

```
python run.py --player "Derrick White" --only

================================================================================
  NBA Finals Game 7 — Lakers vs Celtics
  Preferences:  Player=Derrick White  |  Team=— (filtered)
  15 events → 1 highlights
================================================================================

  #1  [Score 145]  Derrick White (Celtics) — Q2
       Derrick White hits a buzzer-beating three at the end of the first half.
       → A high-impact three pointer by Derrick White that made a significant
         difference. In a clutch moment, right at the buzzer, featuring your
         favorite player, Derrick White.
```

If a player or team isn't in the data, you'll see:

```
⚠️  Player 'Giannis Antetokounmpo' not found in game data.
   Available players: Anthony Davis, Derrick White, Jaylen Brown, Jayson Tatum, LeBron James

   Please re-run with a valid --player or --team from the list above.
```

---

## Python API

```python
from highlight_selector import select_highlights, GameEvent, UserPreference

events = [
    GameEvent(
        id="evt-001", type="dunk", timestamp="Q4 01:30", quarter=4,
        player="LeBron James", team="Lakers",
        description="Game-winning dunk!", importance="critical",
        tags=["clutch", "game_winner"],
    ),
    # ... more events
]

prefs = UserPreference(favorite_player="LeBron James")
highlights = select_highlights(events, prefs)

for h in highlights:
    print(f"#{h.rank} [Score {h.score}] {h.event.description}")
    print(f"  Why: {h.explanation}")
```

### CLI (JSON stdin → stdout)

```bash
cat ../shared/sample_data.json | python -m highlight_selector.cli
```

---

## Game Data Format

Events are provided as JSON (see [sample_data.json](../shared/sample_data.json)):

```json
{
  "game": { "title": "NBA Finals Game 7 — Lakers vs Celtics" },
  "events": [
    {
      "id": "evt-001",
      "type": "three_pointer",
      "timestamp": "Q1 02:34",
      "quarter": 1,
      "player": "LeBron James",
      "team": "Lakers",
      "description": "Deep three-pointer from the logo",
      "importance": "high",
      "tags": ["clutch", "logo_shot"]
    }
  ]
}
```

| Field | Type | Values |
|-------|------|--------|
| `importance` | string | `critical`, `high`, `medium`, `low` |
| `tags` | string[] | `clutch`, `game_winner`, `buzzer_beater`, `highlight_reel`, `defensive`, etc. |

---

## Project Structure

```
track1-speckit/
├── run.py                       # CLI entry point (--player, --team, --only)
├── pyproject.toml               # Project metadata & tool config
│
├── highlight_selector/          # Core package
│   ├── __init__.py              # Public API (5 exports)
│   ├── models.py                # GameEvent, UserPreference, ScoreBreakdown, Highlight
│   ├── selector.py              # Scoring, ranking, selection, explanations
│   └── cli.py                   # JSON stdin → stdout interface
│
├── tests/                       # 99 tests, 88% coverage
│   ├── conftest.py              # Shared fixtures
│   ├── test_models.py           # Data model validation (27 tests)
│   ├── test_scoring.py          # Scoring algorithm (18 tests)
│   ├── test_selection.py        # Ranking & filtering (15 tests)
│   ├── test_explanations.py     # Explanation generation (12 tests)
│   ├── test_edge_cases.py       # Edge cases — US-5 (11 tests)
│   └── test_integration.py      # End-to-end + performance (16 tests)
│
└── 001-highlight-selector/      # Design documents
    ├── spec.md                  # Feature specification
    ├── plan.md                  # Implementation plan
    ├── tasks.md                 # Task breakdown (82/82 complete)
    ├── data-model.md            # Entity schemas
    ├── quickstart.md            # Usage guide
    ├── contracts/               # JSON I/O schemas
    └── checklists/              # Requirements checklist

shared/                          # Shared assets (repo root)
└── sample_data.json             # 15 NBA Finals events (default game data)
```

---

## Development

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=highlight_selector --cov-report=term-missing

# Type checking
mypy --strict highlight_selector/

# Code formatting
black highlight_selector/ tests/ run.py
```

## Requirements

- **Python**: 3.10+
- **Runtime**: None (stdlib only)
- **Dev**: pytest, pytest-cov, black, mypy