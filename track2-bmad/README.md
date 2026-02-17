# AI Highlight Selector (Track 2 - BMAD Implementation)

An intelligent system for selecting and ranking game highlights based on importance, user preferences, and contextual factors.

## Features

- **Smart Scoring Engine**: Evaluates events based on importance levels, favorite players/teams, and context tags
- **Personalized Selection**: Boosts highlights featuring user's favorite player or team
- **Intelligent Selection Rules**:
  - Always includes critical importance events
  - Selects 5-8 top highlights (configurable)
  - Ensures 50% representation for favorite players when applicable
  - Deterministic tie-breaking for reproducible results
- **Human-Readable Explanations**: Auto-generates explanations for why each highlight was selected
- **Command-Line Interface**: Easy-to-use CLI with JSON input/output support

## Installation

### Option 1: Direct Installation

```bash
# Clone the repository
cd track2-bmad

# Install development dependencies (optional)
python3 -m pip install --user pytest pytest-cov mypy black
```

### Option 2: Using Virtual Environment (Recommended)

```bash
# Clone the repository
cd track2-bmad

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install development dependencies (optional)
pip install pytest pytest-cov mypy black

# When done, deactivate virtual environment
deactivate
```

**Note**: No runtime dependencies required! Uses Python standard library only. Dev dependencies are optional and only needed for testing and code quality checks.

## Quick Start

**If using virtual environment**, activate it first:
```bash
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### Basic Usage

```bash
# Objective selection (no preferences)
python3 -m highlight_selector.cli ../shared/sample_data.json

# Personalized for favorite player
python3 -m highlight_selector.cli ../shared/sample_data.json --player "LeBron James"

# Team preference
python3 -m highlight_selector.cli ../shared/sample_data.json --team "Lakers"

# Both player and team
python3 -m highlight_selector.cli ../shared/sample_data.json --player "LeBron James" --team "Lakers"

# Filter to only favorite player/team
python3 -m highlight_selector.cli ../shared/sample_data.json --player "LeBron James" --only

# JSON output
python3 -m highlight_selector.cli ../shared/sample_data.json --player "LeBron James" --json-output
```

### Running the Demo

See the system in action with various scenarios:

```bash
# Run interactive demo (no venv needed - uses standard library)
python3 demo.py

# Or if using venv:
source venv/bin/activate
python3 demo.py
```

### Input Format

JSON file with game events:

```json
{
  "events": [
    {
      "id": "evt-001",
      "type": "three_pointer",
      "timestamp": "Q4 02:34",
      "quarter": 4,
      "player": "LeBron James",
      "team": "Lakers",
      "description": "Deep three-pointer from the logo",
      "importance": "critical",
      "tags": ["clutch", "game_winner"]
    }
  ]
}
```

### Output Example

```
🏆 Top 5 Highlights 🏆
============================================================

#1 | Score: 190.0
   THREE_POINTER - Deep three-pointer from the logo
   Player: LeBron James | Team: Lakers | Q4 02:34
   Importance: critical
   Tags: clutch, game_winner
   💡 Critical game moment featuring your favorite player LeBron James as the game-winner.

...
```

## Architecture

### Core Modules

- **`models.py`**: Data models (GameEvent, UserPreference, ScoreBreakdown, Highlight)
- **`selector.py`**: Scoring engine and selection logic
- **`cli.py`**: Command-line interface

### Scoring Algorithm

1. **Base Score**: Importance level (critical=100, high=75, medium=50, low=25)
2. **Player Boost**: +30 points for favorite player
3. **Team Boost**: +15 points for favorite team
4. **Context Boosts**:
   - clutch: +20
   - game_winner: +25
   - buzzer_beater: +15
   - highlight_reel: +15
   - fourth_quarter: +10

### Selection Rules

1. **Force-Include Critical**: All "critical" importance events are always selected
2. **5-8 Range**: Selects between 5-8 highlights (critical events can exceed this)
3. **50% Favorite Player**: When ≥3 favorite player events exist, ensures ≥50% representation
4. **Deterministic Tie-Breaking**: Quarter (desc) → Importance (desc) → ID (asc)

## Development

**If using virtual environment**, ensure it's activated before running commands:
```bash
source venv/bin/activate  # macOS/Linux
```

### Running Tests

```bash
# All tests
python3 -m pytest tests/ -v

# With coverage
python3 -m pytest tests/ --cov=highlight_selector --cov-report=term-missing

# Specific test file
python3 -m pytest tests/test_selector.py -v
```

### Code Quality

```bash
# Type checking (mypy strict mode)
python3 -m mypy highlight_selector/ --strict

# Code formatting (black)
python3 -m black highlight_selector/ tests/

# Run all quality checks
python3 -m mypy highlight_selector/ --strict && python3 -m black highlight_selector/ tests/ --check
```

## Testing

- **Unit Tests**: 85+ tests covering all modules
- **Integration Tests**: End-to-end workflow testing
- **Coverage**: 85%+ code coverage (100% on core logic)
- **Quality Gates**: Mypy strict mode, Black formatting, comprehensive docstrings

## Requirements

- **Python**: 3.9+ (using standard library only)
- **Development**: pytest, pytest-cov, mypy, black (optional, for development)
- **Runtime**: No external dependencies!

## Project Structure

```
track2-bmad/
├── highlight_selector/
│   ├── __init__.py
│   ├── models.py           # Data models
│   ├── selector.py         # Scoring and selection
│   └── cli.py              # Command-line interface
├── tests/
│   ├── test_models.py      # Model tests (34 tests)
│   ├── test_selector.py    # Scoring tests (30 tests)
│   ├── test_selection.py   # Selection tests (21 tests)
│   ├── test_cli.py         # CLI tests (16 tests)
│   └── test_integration.py # E2E tests (6 tests)
└── README.md
```

## Technical Details

### Complexity

- **Scoring**: O(n×m) where n = events, m = average tags per event
- **Selection**: O(n log n) due to sorting
- **Overall**: O(n log n) per selection run

### Design Principles

- **Pure Functions**: All scoring/selection functions are pure (same input → same output)
- **Type Safety**: Full type hints with mypy strict mode
- **Testability**: TDD approach with comprehensive test coverage
- **Documentation**: Google-style docstrings for all public APIs
- **No Dependencies**: Standard library only for zero installation friction

## License

MIT License - See LICENSE file for details

## Authors

Developed using the BMAD Method (Branching Multi-Agent Development)

## Version

1.0.0 - February 2026
