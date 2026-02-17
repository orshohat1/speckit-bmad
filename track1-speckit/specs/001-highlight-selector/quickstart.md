# Quickstart Guide: AI Highlight Selector

**Feature**: `001-highlight-selector`  
**Python**: 3.10+

## Installation

```bash
# Clone the repository
git clone https://github.com/orshohat1/speckit-bmad.git
cd speckit-bmad

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dev dependencies
pip install pytest pytest-cov black mypy
```

## Python API Usage

```python
from highlight_selector import select_highlights, GameEvent, UserPreference

# Create events
events = [
    GameEvent(
        id="evt-001", type="dunk", timestamp="Q4 11:30", quarter=4,
        player="LeBron James", team="Lakers",
        description="Game-winning dunk!",
        importance="critical", tags=["game_winner", "clutch"],
    ),
    GameEvent(
        id="evt-002", type="three_pointer", timestamp="Q3 09:00", quarter=3,
        player="Jayson Tatum", team="Celtics",
        description="Step-back three to cut the lead.",
        importance="high", tags=["clutch", "step_back"],
    ),
    # ... more events
]

# Basic selection (no preferences)
highlights = select_highlights(events)

# With player preference
prefs = UserPreference(favorite_player="LeBron James")
highlights = select_highlights(events, prefs)

# With team preference
prefs = UserPreference(favorite_team="Lakers")
highlights = select_highlights(events, prefs)

# With both preferences
prefs = UserPreference(favorite_player="LeBron James", favorite_team="Lakers")
highlights = select_highlights(events, prefs)

# Access results
for h in highlights:
    print(f"#{h.rank} [{h.score}] {h.event.description}")
    print(f"  Why: {h.explanation}")
```

## CLI Usage

The CLI reads JSON from stdin and writes highlights to stdout:

```bash
# Using sample data
cat shared/sample_data.json | python -m highlight_selector.cli

# With custom input
echo '{
  "events": [
    {"id": "e1", "type": "dunk", "timestamp": "Q4 02:00", "quarter": 4,
     "player": "LeBron", "team": "Lakers", "description": "Big dunk",
     "importance": "critical", "tags": ["game_winner"]}
  ],
  "user_preferences": {
    "favorite_player": "LeBron",
    "favorite_team": null
  }
}' | python -m highlight_selector.cli
```

### Output Format

```json
{
  "highlights": [
    {
      "event": { "id": "evt-014", "type": "dunk", ... },
      "rank": 1,
      "score": 175,
      "explanation": "This critical dunk by LeBron James was a defining moment of the game. Sealed the victory, in a clutch fourth-quarter moment."
    }
  ],
  "metadata": {
    "total_events": 15,
    "selected_count": 7,
    "preferences": { "favorite_player": "LeBron James", "favorite_team": null }
  }
}
```

## Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=highlight_selector --cov-report=term-missing

# Run specific test modules
python -m pytest tests/test_scoring.py -v      # Scoring algorithm
python -m pytest tests/test_selection.py -v     # Selection logic
python -m pytest tests/test_explanations.py -v  # Explanation generation
python -m pytest tests/test_edge_cases.py -v    # Edge case handling
python -m pytest tests/test_integration.py -v   # End-to-end integration
```

## Code Quality

```bash
# Format code
python -m black highlight_selector/ tests/

# Type check
python -m mypy highlight_selector/ --strict
```

## Key Behaviors

- **Returns 5-8 highlights** from any number of input events
- **Critical events always included** regardless of preferences
- **Deterministic**: Same input always produces same output
- **Player boost**: +30 points for events featuring favorite player
- **Team boost**: +15 points for events from favorite team
- **Tie-breaking**: Quarter (desc) → Importance (desc) → Event ID (asc)
- **Edge cases**: Handles empty lists, null prefs, unknown importance gracefully
